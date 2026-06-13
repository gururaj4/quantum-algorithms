import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*urllib3 v2 only supports OpenSSL.*")
from qiskit import QuantumCircuit
import random
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler

class DeutschJoszaEngine:
    def __init__(self, num_qubits:int):
        if num_qubits < 2:
            raise TypeError("invalid input type, needs to be a natural number greater than 1")
        self.num_qubits = num_qubits
        self.input_qubits = num_qubits-1
        self.target_qubit = self.input_qubits
        self.qc = None
        self.oracle = None
        
    def _build_initialisation(self):
        self.qc = QuantumCircuit(self.num_qubits, self.input_qubits)
        for i in range(self.input_qubits):
            self.qc.h(i)
        self.qc.x(self.target_qubit)
        self.qc.h(self.target_qubit)
        self.qc.barrier()
        
    def _build_measurement(self):
        for i in range(self.input_qubits):
            self.qc.h(i)
            self.qc.measure(i,i)
            
    def _oracle_initialisation(self):
        always_0 = QuantumCircuit(self.num_qubits)
        always_0_gate = always_0.to_gate()
        always_0_gate.name = "always 0"

        always_1 = QuantumCircuit(self.num_qubits)
        always_1.x(self.target_qubit)
        always_1_gate = always_1.to_gate()
        always_1_gate.name = "always 1"

        identity = QuantumCircuit(self.num_qubits)
        for i in range(self.input_qubits):
            identity.cx(i,self.target_qubit)
        identity_gate = identity.to_gate()
        identity_gate.name = "identity"

        complement = QuantumCircuit(self.num_qubits)
        for i in range(self.input_qubits):
            complement.x(i)
            complement.cx(i,self.target_qubit)
            complement.x(i)
        complement_gate = complement.to_gate()
        complement_gate.name = "complement"

        self.oracle = random.choice([always_0_gate,always_1_gate,identity_gate,complement_gate])
        
    def construct_circuit(self)->QuantumCircuit:
        self._build_initialisation()
        self._oracle_initialisation()
        self.qc.append(self.oracle,range(self.num_qubits))
        self.qc.barrier()
        self._build_measurement()
        return self.qc

    def run_simulator(self)-> dict:
        backend=AerSimulator()
        pm=generate_preset_pass_manager(optimization_level=1,backend=backend)
        isa_circuit = pm.run(self.qc)
        sampler = StatevectorSampler()
        job = sampler.run([isa_circuit],shots=1)
        result=job.result()
        counts = result[0].data.c.get_counts()
        return counts

    def verify(self):
        print(self.oracle.name)
