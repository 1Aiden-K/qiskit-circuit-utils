"""Tests for quantum transforms."""

from math import pi

import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.circuit.library import QFTGate

from qiskit_circuit_utils import transform


def instruction_names(circuit):
    return [
        instruction.operation.name
        for instruction in circuit.data
    ]


# ---------------------------------------------------------------------------
# QFT
# ---------------------------------------------------------------------------


def test_qft_one_qubit():
    circuit = QuantumCircuit(1)

    transform.qft(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit) == ["h"]


def test_qft_instructions_without_swaps():
    circuit = QuantumCircuit(3)

    transform.qft(
        circuit,
        circuit.qubits,
        swaps=False,
    )

    assert instruction_names(circuit) == [
        "h",
        "cp",
        "cp",
        "h",
        "cp",
        "h",
    ]


def test_qft_controlled_phases():
    circuit = QuantumCircuit(3)

    transform.qft(
        circuit,
        circuit.qubits,
        swaps=False,
    )

    first = circuit.data[1]
    second = circuit.data[2]
    third = circuit.data[4]

    assert first.operation.params == [pi / 2]
    assert first.qubits == (
        circuit.qubits[1],
        circuit.qubits[2],
    )

    assert second.operation.params == [pi / 4]
    assert second.qubits == (
        circuit.qubits[0],
        circuit.qubits[2],
    )

    assert third.operation.params == [pi / 2]
    assert third.qubits == (
        circuit.qubits[0],
        circuit.qubits[1],
    )


def test_qft_includes_swaps_by_default():
    circuit = QuantumCircuit(4)

    transform.qft(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit)[-2:] == [
        "swap",
        "swap",
    ]

    assert circuit.data[-2].qubits == (
        circuit.qubits[0],
        circuit.qubits[3],
    )

    assert circuit.data[-1].qubits == (
        circuit.qubits[1],
        circuit.qubits[2],
    )


def test_qft_swaps_odd_qubits():
    circuit = QuantumCircuit(3)

    transform.qft(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit)[-1] == "swap"

    assert circuit.data[-1].qubits == (
        circuit.qubits[0],
        circuit.qubits[2],
    )


def test_qft_can_omit_swaps():
    circuit = QuantumCircuit(4)

    transform.qft(
        circuit,
        circuit.qubits,
        swaps=False,
    )

    assert "swap" not in instruction_names(circuit)


def test_qft_requires_qubits():
    circuit = QuantumCircuit(1)

    with pytest.raises(ValueError):
        transform.qft(
            circuit,
            [],
        )


def test_qft_requires_distinct_qubits():
    circuit = QuantumCircuit(2)

    with pytest.raises(ValueError):
        transform.qft(
            circuit,
            [
                circuit.qubits[0],
                circuit.qubits[0],
            ],
        )


# ---------------------------------------------------------------------------
# Inverse QFT
# ---------------------------------------------------------------------------


def test_inverse_qft_one_qubit():
    circuit = QuantumCircuit(1)

    transform.inverse_qft(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit) == ["h"]


def test_inverse_qft_instructions_without_swaps():
    circuit = QuantumCircuit(3)

    transform.inverse_qft(
        circuit,
        circuit.qubits,
        swaps=False,
    )

    assert instruction_names(circuit) == [
        "h",
        "cp",
        "h",
        "cp",
        "cp",
        "h",
    ]


def test_inverse_qft_controlled_phases():
    circuit = QuantumCircuit(3)

    transform.inverse_qft(
        circuit,
        circuit.qubits,
        swaps=False,
    )

    first = circuit.data[1]
    second = circuit.data[3]
    third = circuit.data[4]

    assert first.operation.params == [-pi / 2]
    assert first.qubits == (
        circuit.qubits[0],
        circuit.qubits[1],
    )

    assert second.operation.params == [-pi / 4]
    assert second.qubits == (
        circuit.qubits[0],
        circuit.qubits[2],
    )

    assert third.operation.params == [-pi / 2]
    assert third.qubits == (
        circuit.qubits[1],
        circuit.qubits[2],
    )


def test_inverse_qft_includes_swaps_by_default():
    circuit = QuantumCircuit(4)

    transform.inverse_qft(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit)[:2] == [
        "swap",
        "swap",
    ]

    assert circuit.data[0].qubits == (
        circuit.qubits[0],
        circuit.qubits[3],
    )

    assert circuit.data[1].qubits == (
        circuit.qubits[1],
        circuit.qubits[2],
    )


def test_inverse_qft_swaps_odd_qubits():
    circuit = QuantumCircuit(3)

    transform.inverse_qft(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit)[0] == "swap"

    assert circuit.data[0].qubits == (
        circuit.qubits[0],
        circuit.qubits[2],
    )


def test_inverse_qft_can_omit_swaps():
    circuit = QuantumCircuit(4)

    transform.inverse_qft(
        circuit,
        circuit.qubits,
        swaps=False,
    )

    assert "swap" not in instruction_names(circuit)


def test_inverse_qft_requires_qubits():
    circuit = QuantumCircuit(1)

    with pytest.raises(ValueError):
        transform.inverse_qft(
            circuit,
            [],
        )


def test_inverse_qft_requires_distinct_qubits():
    circuit = QuantumCircuit(2)

    with pytest.raises(ValueError):
        transform.inverse_qft(
            circuit,
            [
                circuit.qubits[0],
                circuit.qubits[0],
            ],
        )


# ---------------------------------------------------------------------------
# QFT correctness
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("num_qubits", range(1, 6))
@pytest.mark.parametrize("swaps", [False, True])
def test_inverse_qft_inverts_qft(
    num_qubits,
    swaps,
):
    circuit = QuantumCircuit(num_qubits)

    transform.qft(
        circuit,
        circuit.qubits,
        swaps=swaps,
    )

    transform.inverse_qft(
        circuit,
        circuit.qubits,
        swaps=swaps,
    )

    assert Operator(circuit).equiv(
        Operator(
            QuantumCircuit(num_qubits),
        )
    )


@pytest.mark.parametrize("num_qubits", range(1, 6))
def test_qft_matches_qiskit(num_qubits):
    circuit = QuantumCircuit(num_qubits)

    transform.qft(
        circuit,
        circuit.qubits,
    )

    expected = QuantumCircuit(num_qubits)
    expected.append(
        QFTGate(num_qubits),
        expected.qubits,
    )

    assert Operator(circuit).equiv(
        Operator(expected)
    )