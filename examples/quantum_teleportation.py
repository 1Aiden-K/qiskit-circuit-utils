"""Demonstrate quantum teleportation."""

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from qiskit_circuit_utils import correction, measurement, preparation

if __name__ == "__main__":
        # Teleport q[0] to q[2].
    qr = QuantumRegister(3, "q")
    cr = ClassicalRegister(2, "c")

    source=qr[0]
    ancillary=qr[1]
    target=qr[2]
    phase_bit=cr[0]
    parity_bit=cr[1]

    circuit = QuantumCircuit(qr, cr)

    # Prepare the state to teleport.
    circuit.x(qr[0])

    circuit.barrier()

    # Prepare an entangled Bell pair.
    preparation.bell_state(circuit, [ancillary, target])

    # Measure the source and ancillary qubits in the Bell basis.
    measurement.bell_basis(
        circuit,
        [source, ancillary],
        [phase_bit, parity_bit],
    )

    # Correct the target using the measurement results.
    correction.pauli(
        circuit,
        target,
        x_bit=parity_bit,
        z_bit=phase_bit,
    )

    print(circuit.draw(output="text"))