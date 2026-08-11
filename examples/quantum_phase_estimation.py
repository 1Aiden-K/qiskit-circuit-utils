"""Demonstrate quantum phase estimation."""

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_circuit_utils import transform

if __name__ == "__main__":
    """Create a two-qubit phase estimation circuit for the Z gate."""
    eigenstate = QuantumRegister(1, "b")
    phase = QuantumRegister(2, "q")
    classical = ClassicalRegister(2, "c")
    circuit = QuantumCircuit(eigenstate, phase, classical)

    # Prepare the |1> eigenstate of Z.
    circuit.x(eigenstate[0])

    # Prepare the phase register in |++>.
    circuit.h(phase)

    circuit.barrier()

    # Apply controlled powers of Z.
    circuit.cz(phase[0], eigenstate[0])

    circuit.barrier()

    # Apply the inverse quantum Fourier transform.
    transform.inverse_qft(circuit, phase)

    circuit.barrier()

    # Measure the phase register.
    circuit.measure(phase, classical)

    print(circuit.draw(output="text"))