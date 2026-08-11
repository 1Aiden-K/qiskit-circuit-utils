"""Tests for quantum operations."""

import pytest
from qiskit import QuantumCircuit

from qiskit_circuit_utils import operation

def instruction_names(circuit):
    return [
        instruction.operation.name
        for instruction in circuit.data
    ]


# ---------------------------------------------------------------------------
# Reverse
# ---------------------------------------------------------------------------


def test_reverse_even_qubits():
    circuit = QuantumCircuit(4)

    operation.reverse(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit) == [
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


def test_reverse_odd_qubits():
    circuit = QuantumCircuit(5)

    operation.reverse(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit) == [
        "swap",
        "swap",
    ]

    assert circuit.data[0].qubits == (
        circuit.qubits[0],
        circuit.qubits[4],
    )

    assert circuit.data[1].qubits == (
        circuit.qubits[1],
        circuit.qubits[3],
    )


def test_reverse_two_qubits():
    circuit = QuantumCircuit(2)

    operation.reverse(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit) == ["swap"]

    assert circuit.data[0].qubits == (
        circuit.qubits[0],
        circuit.qubits[1],
    )


def test_reverse_one_qubit():
    circuit = QuantumCircuit(1)

    operation.reverse(
        circuit,
        circuit.qubits,
    )

    assert instruction_names(circuit) == []


def test_reverse_empty_qubits():
    circuit = QuantumCircuit(2)

    operation.reverse(
        circuit,
        [],
    )

    assert instruction_names(circuit) == []


def test_reverse_requires_distinct_qubits():
    circuit = QuantumCircuit(3)

    with pytest.raises(ValueError):
        operation.reverse(
            circuit,
            [
                circuit.qubits[0],
                circuit.qubits[1],
                circuit.qubits[0],
            ],
        )