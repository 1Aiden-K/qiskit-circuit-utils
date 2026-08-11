"""Demonstrate Deutsch's algorithm."""

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate

from qiskit_circuit_utils import measurement as measure


def deutsch_oracle(f0: int, f1: int) -> Gate:
    """Create a Deutsch oracle with the specified outputs."""
    if f0 not in (0, 1) or f1 not in (0, 1):
        raise ValueError("f0 and f1 must be either 0 or 1.")

    oracle = QuantumCircuit(2, name="Uf")

    if f0 == 1 and f1 == 1:
        oracle.x(1)

    elif f0 != f1:
        if f0 == 1:
            oracle.x(1)

        oracle.cx(0, 1)

    return oracle.to_gate()


if __name__ == "__main__":
    qr = QuantumRegister(2, "q")
    cr = ClassicalRegister(1, "c")
    circuit = QuantumCircuit(qr, cr)

    # Choose the unknown function.
    oracle = deutsch_oracle(0, 1)

    # Prepare |0>|1>.
    circuit.x(1)

    # Prepare |+>|->.
    circuit.h(qr)

    circuit.barrier()

    # Query f once.
    circuit.append(oracle, qr)

    circuit.barrier()

    # Measure the input qubit in the X basis.
    measure.x(circuit, qr[0], cr[0])

    print(circuit.draw(output="text"))