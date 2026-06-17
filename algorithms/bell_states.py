import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*urllib3 v2 only supports OpenSSL.*")
from qiskit import QuantumCircuit
import random
class BellStateFactory():
    def __init__(self,qc: QuantumCircuit,state: str):
        if state not in ["phi_plus","phi_minus","psi_plus","psi_minus"]:
            raise ValueError("Invalid type entered,enter the greek letter, followed by an underscore and then the specific phase, in all lowercase")
        if qc.num_qubits != 2 :
            raise ValueError("Building bell states requires a circuit with exactly 2 qubits")
        self.qc = qc
        self.state = state
    def Generate(self):
        if self.state == "phi_plus":
            self.qc.h(0)
            self.qc.cx(0,1)
            return self.qc
        elif self.state == "phi_minus":
            self.qc.x(0)
            self.qc.h(0)
            self.qc.cx(0,1)
            return self.qc
        elif self.state == "psi_plus":
            self.qc.h(0)
            self.qc.cx(0,1)
            self.qc.x(1)
            return self.qc
        elif self.state == "psi_minus":
            self.qc.x(0)
            self.qc.h(0)
            self.qc.cx(0,1)
            self.qc.x(1)
            return self.qc
