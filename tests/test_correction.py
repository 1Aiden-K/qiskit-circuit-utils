"""Tests for qiskit_circuit_utils.correction."""

import pytest
from qiskit import QuantumCircuit
from qiskit.circuit import Clbit, Qubit
from qiskit.circuit.controlflow import IfElseOp

from qiskit_circuit_utils import correction


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def assert_conditional_gate(
    circuit: QuantumCircuit,
    index: int,
    gate: str,
    target: Qubit,
    control_bit: Clbit,
) -> None:
    """Assert that an instruction is a conditional single-qubit gate."""
    instruction = circuit.data[index]
    operation = instruction.operation

    assert isinstance(operation, IfElseOp)
    assert operation.condition == (control_bit, 1)

    true_body = operation.blocks[0]

    assert len(true_body.data) == 1

    gate_instruction = true_body.data[0]

    assert gate_instruction.operation.name == gate
    assert gate_instruction.qubits == (
        true_body.qubits[
            circuit.find_bit(target).index
        ],
    )


# ---------------------------------------------------------------------------
# X correction
# ---------------------------------------------------------------------------


def test_x_if():
    circuit = QuantumCircuit(1, 1)

    correction.x_if(
        circuit,
        circuit.qubits[0],
        circuit.clbits[0],
    )

    assert len(circuit.data) == 1

    operation = circuit.data[0].operation

    assert isinstance(operation, IfElseOp)
    assert operation.condition == (
        circuit.clbits[0],
        1,
    )

    body = operation.blocks[0]

    assert len(body.data) == 1
    assert body.data[0].operation.name == "x"


def test_x_if_accepts_integer_specifiers():
    circuit = QuantumCircuit(1, 1)

    correction.x_if(
        circuit,
        0,
        0,
    )

    operation = circuit.data[0].operation

    assert isinstance(operation, IfElseOp)
    assert operation.condition == (
        circuit.clbits[0],
        1,
    )

    assert operation.blocks[0].data[0].operation.name == "x"


# ---------------------------------------------------------------------------
# Z correction
# ---------------------------------------------------------------------------


def test_z_if():
    circuit = QuantumCircuit(1, 1)

    correction.z_if(
        circuit,
        circuit.qubits[0],
        circuit.clbits[0],
    )

    assert len(circuit.data) == 1

    operation = circuit.data[0].operation

    assert isinstance(operation, IfElseOp)
    assert operation.condition == (
        circuit.clbits[0],
        1,
    )

    body = operation.blocks[0]

    assert len(body.data) == 1
    assert body.data[0].operation.name == "z"


def test_z_if_accepts_integer_specifiers():
    circuit = QuantumCircuit(1, 1)

    correction.z_if(
        circuit,
        0,
        0,
    )

    operation = circuit.data[0].operation

    assert isinstance(operation, IfElseOp)
    assert operation.condition == (
        circuit.clbits[0],
        1,
    )

    assert operation.blocks[0].data[0].operation.name == "z"


# ---------------------------------------------------------------------------
# Pauli correction
# ---------------------------------------------------------------------------


def test_pauli():
    circuit = QuantumCircuit(1, 2)

    target = circuit.qubits[0]
    x_bit = circuit.clbits[0]
    z_bit = circuit.clbits[1]

    correction.pauli(
        circuit,
        target,
        x_bit=x_bit,
        z_bit=z_bit,
    )

    assert len(circuit.data) == 2

    x_operation = circuit.data[0].operation
    z_operation = circuit.data[1].operation

    assert isinstance(x_operation, IfElseOp)
    assert isinstance(z_operation, IfElseOp)

    assert x_operation.condition == (
        x_bit,
        1,
    )
    assert z_operation.condition == (
        z_bit,
        1,
    )

    assert (
        x_operation.blocks[0]
        .data[0]
        .operation.name
        == "x"
    )

    assert (
        z_operation.blocks[0]
        .data[0]
        .operation.name
        == "z"
    )


def test_pauli_accepts_integer_specifiers():
    circuit = QuantumCircuit(1, 2)

    correction.pauli(
        circuit,
        0,
        x_bit=0,
        z_bit=1,
    )

    x_operation = circuit.data[0].operation
    z_operation = circuit.data[1].operation

    assert x_operation.condition == (
        circuit.clbits[0],
        1,
    )

    assert z_operation.condition == (
        circuit.clbits[1],
        1,
    )


# ---------------------------------------------------------------------------
# X corrections over multiple targets
# ---------------------------------------------------------------------------


def test_x_all():
    circuit = QuantumCircuit(3, 3)

    correction.x_if_all(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    assert len(circuit.data) == 3

    for index in range(3):
        operation = circuit.data[index].operation

        assert isinstance(operation, IfElseOp)

        assert operation.condition == (
            circuit.clbits[index],
            1,
        )

        assert (
            operation.blocks[0]
            .data[0]
            .operation.name
            == "x"
        )


def test_x_all_rejects_mismatched_lengths():
    circuit = QuantumCircuit(3, 2)

    with pytest.raises(ValueError):
        correction.x_if_all(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


# ---------------------------------------------------------------------------
# Z corrections over multiple targets
# ---------------------------------------------------------------------------


def test_z_all():
    circuit = QuantumCircuit(3, 3)

    correction.z_if_all(
        circuit,
        circuit.qubits,
        circuit.clbits,
    )

    assert len(circuit.data) == 3

    for index in range(3):
        operation = circuit.data[index].operation

        assert isinstance(operation, IfElseOp)

        assert operation.condition == (
            circuit.clbits[index],
            1,
        )

        assert (
            operation.blocks[0]
            .data[0]
            .operation.name
            == "z"
        )


def test_z_all_rejects_mismatched_lengths():
    circuit = QuantumCircuit(3, 2)

    with pytest.raises(ValueError):
        correction.z_if_all(
            circuit,
            circuit.qubits,
            circuit.clbits,
        )


# ---------------------------------------------------------------------------
# Pauli corrections over multiple targets
# ---------------------------------------------------------------------------


def test_pauli_all():
    circuit = QuantumCircuit(2, 4)

    targets = circuit.qubits

    x_bits = [
        circuit.clbits[0],
        circuit.clbits[1],
    ]

    z_bits = [
        circuit.clbits[2],
        circuit.clbits[3],
    ]

    correction.pauli_all(
        circuit,
        targets,
        x_bits,
        z_bits,
    )

    # Two conditional operations per target:
    # X correction followed by Z correction.
    assert len(circuit.data) == 4

    for index in range(2):
        x_operation = circuit.data[2 * index].operation
        z_operation = circuit.data[2 * index + 1].operation

        assert isinstance(x_operation, IfElseOp)
        assert isinstance(z_operation, IfElseOp)

        assert x_operation.condition == (
            x_bits[index],
            1,
        )

        assert z_operation.condition == (
            z_bits[index],
            1,
        )

        assert (
            x_operation.blocks[0]
            .data[0]
            .operation.name
            == "x"
        )

        assert (
            z_operation.blocks[0]
            .data[0]
            .operation.name
            == "z"
        )


@pytest.mark.parametrize(
    ("target_count", "x_count", "z_count"),
    [
        (2, 1, 2),
        (2, 2, 1),
        (1, 2, 2),
    ],
)
def test_pauli_all_rejects_mismatched_lengths(
    target_count,
    x_count,
    z_count,
):
    circuit = QuantumCircuit(2, 2)

    targets = circuit.qubits[:target_count]
    x_bits = circuit.clbits[:x_count]
    z_bits = circuit.clbits[:z_count]

    with pytest.raises(ValueError):
        correction.pauli_all(
            circuit,
            targets,
            x_bits,
            z_bits,
        )


# ---------------------------------------------------------------------------
# Empty collections
# ---------------------------------------------------------------------------


def test_x_all_accepts_empty_sequences():
    circuit = QuantumCircuit(1, 1)

    correction.x_if_all(
        circuit,
        [],
        [],
    )

    assert len(circuit.data) == 0


def test_z_all_accepts_empty_sequences():
    circuit = QuantumCircuit(1, 1)

    correction.z_if_all(
        circuit,
        [],
        [],
    )

    assert len(circuit.data) == 0


def test_pauli_all_accepts_empty_sequences():
    circuit = QuantumCircuit(1, 1)

    correction.pauli_all(
        circuit,
        [],
        [],
        [],
    )

    assert len(circuit.data) == 0