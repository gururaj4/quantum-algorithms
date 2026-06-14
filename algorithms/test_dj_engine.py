import pytest
from deutsch_jozsa import DeutschJoszaEngine

def test_initial_conditions():
    #verify all initial conditions
    test_engine = DeutschJoszaEngine(3)
    assert test_engine.num_qubits == 3
    assert test_engine.input_qubits == 2
    assert test_engine.target_qubit == 2
    assert test_engine.qc == None
    assert test_engine.oracle == None

def test_error_thrown():
    #verify error raised
    with pytest.raises(TypeError):
        test_2 = DeutschJoszaEngine(1)

def test_algorithm_execution_loop():
    test3 = DeutschJoszaEngine(4)
    simulated_circuit = test3.construct_circuit()
    counts = test3.run_simulator()
    all_zeroes = "0"*test3.input_qubits
    if test3.oracle.name in ["always 0","always 1"]:
        assert all_zeroes in counts
    else:
        assert all_zeroes not in counts
