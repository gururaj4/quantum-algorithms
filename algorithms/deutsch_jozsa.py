import warnings
warnings.filterwarnings(action="ignore", category=DeprecationWarning)

from qiskit import QuantumCircuit
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

qc = QuantumCircuit(2,1)
qc.h(0)
qc.x(1)
qc.h(1)
qc.barrier()
qc.append(identity_gate,[0,1])
qc.barrier()
qc.h(0)
qc.measure(0,0)
qc.draw(output='text')
