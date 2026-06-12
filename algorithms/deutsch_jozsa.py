import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*urllib3 v2 only supports OpenSSL.*")
from qiskit import QuantumCircuit
import random
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.primitives import StatevectorSampler

#designing the oracle
num_qubits = 3
num_inputs = 2
target_qubit = 2
always_0 = QuantumCircuit(num_qubits)
always_0_gate = always_0.to_gate()
always_0_gate.name = "always 0"

always_1 = QuantumCircuit(num_qubits)
always_1.x(target_qubit)
always_1_gate = always_1.to_gate()
always_1_gate.name = "always 1"

identity = QuantumCircuit(num_qubits)
for i in range(num_inputs):
    identity.cx(i,target_qubit)
identity_gate = identity.to_gate()
identity_gate.name = "identity"

complement = QuantumCircuit(num_qubits)
for i in range(num_inputs):
    complement.x(i)
    complement.cx(i,target_qubit)
    complement.x(i)
complement_gate = complement.to_gate()
complement_gate.name = "complement"

oracle = random.choice([always_0_gate,always_1_gate,identity_gate,complement_gate])
print(oracle.name)

#building the simulation circuit
qc = QuantumCircuit(num_qubits,num_inputs)
for i in range(num_inputs):
    qc.h(i)
qc.x(target_qubit)
qc.h(target_qubit)
qc.barrier()
qc.append(oracle,range(num_qubits))
qc.barrier()
for i in range(num_inputs):
    qc.h(i)
for i in range(num_inputs):
    qc.measure(i,i)
qc.draw(output='text')

#running the simulation circuit
backend = AerSimulator()
pm = generate_preset_pass_manager(optimization_level=1,backend=backend)
isa = pm.run(qc)
sampler = StatevectorSampler()
job = sampler.run([isa],shots=1000)
result = job.result()
counts = result[0].data.c.get_counts()
print(counts)
