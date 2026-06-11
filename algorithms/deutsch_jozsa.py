import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*urllib3 v2 only supports OpenSSL.*")
from qiskit.primitives import StatevectorSampler
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
import random
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
backend = AerSimulator()
print(f"backend initialised successfully: {backend}")

#gates
identity = QuantumCircuit(2)
identity.cx(0,1)
identity_gate = identity.to_gate()
identity_gate.name = "identity"
complement = QuantumCircuit(2)
complement.x(0)
complement.cx(0,1)
complement.x(0)
complement_gate = complement.to_gate()
complement_gate.name = "complement"
always_1 = QuantumCircuit(2)
always_1.x(1)
always_1_gate = always_1.to_gate()
always_1_gate.name = "always_1"
always_0 = QuantumCircuit(2)
always_0_gate = always_0.to_gate()
always_0_gate.name = "always_0"
#wrapping in the oracle
oracle_gate = random.choice([identity_gate,complement_gate,always_1_gate,always_0_gate])
print(f"{oracle_gate.name}")
#building the circuit
oracle_test = QuantumCircuit(2,1)
oracle_test.h(0)
oracle_test.x(1)
oracle_test.h(1)
oracle_test.barrier()
oracle_test.append(oracle_gate,[0,1])
oracle_test.barrier()
oracle_test.h(0)
oracle_test.measure(0,0)
oracle_test.draw(output='text')
#running the circuit
pm = generate_preset_pass_manager(optimization_level=1, backend= backend)
isa_circuit = pm.run(oracle_test)
sampler = StatevectorSampler()
job = sampler.run([isa_circuit],shots=1)
result=job.result()
data_packet = result[0]
data_packet.data.c.get_counts()
