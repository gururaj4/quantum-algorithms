from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
class MultiQubitOracleFactory():
    def __init__(self, num_inputs: int):
        if num_inputs < 1:
            raise ValueError("Number of input qubits has to be greater than or equal to 1")
        self.num_inputs = num_inputs
        self.target_qubit = num_inputs
        self.num_qubits = num_inputs + 1

    def create_constant_oracle(self, val: int) -> Gate:
        if val not in [0, 1]:
            raise ValueError("Value of the function has to be either always 0 or always 1")
        qc = QuantumCircuit(self.num_qubits) 
        if val == 0:
            zero_gate = qc.to_gate()
            zero_gate.name = "always 0 gate"
            return zero_gate
        if val == 1:
            qc.x(self.target_qubit)
            one_gate = qc.to_gate()
            one_gate.name = "always 1 gate"
            return one_gate

    def create_balanced_oracle(self, hidden_state: str, Type: str) -> Gate:
        if Type not in ["identity", "complement"]:
            raise ValueError("Balanced Oracle must have a type of either 'identity' or 'complement' entered in all lowercase")
        state = ""
        for bit in hidden_state[::-1]:
            if bit not in ["0", "1"]:
                raise ValueError("Bitstring must contain all qubits having values 0 and 1 only")
            state += bit
        qc = QuantumCircuit(self.num_qubits)
        if Type == "identity":
            bit_tracker = []
            for idx, bit in enumerate(state):
                if bit == "0":
                    qc.x(idx)
                    bit_tracker.append(idx)
            qc.mcx(list(range(self.num_inputs)), self.target_qubit)
            for idx, bit in enumerate(state):
                if idx in bit_tracker:
                    qc.x(idx)
            identity_gate = qc.to_gate()
            identity_gate.name = "identity gate"
            return identity_gate
        if Type == "complement":
            bit_tracker = []
            for idx, bit in enumerate(state):
                if bit == "1":
                    qc.x(idx)
                    bit_tracker.append(idx)
            qc.mcx(list(range(self.num_inputs)), self.target_qubit)
            for idx, bit in enumerate(state):
                if idx in bit_tracker:
                    qc.x(idx)
            complement_gate = qc.to_gate()
            complement_gate.name = "complement gate"
            return complement_gate
