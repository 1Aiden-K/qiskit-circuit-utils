"""Tests for qiskit_circuit_utils._validation."""

import pytest
from qiskit import QuantumCircuit

from qiskit_circuit_utils._validation import (
    require_clbits,
    require_distinct,
    require_distinct_clbits,
    require_distinct_qubits,
    require_length,
    require_min_length,
    require_min_qubits,
    require_non_empty,
    require_qubits,
    require_same_length,
)

# ---------------------------------------------------------------------------
# require_length
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "count"),
    [
        ([], 0),
        ([1], 1),
        ([1, 2], 2),
        ([1, 2, 3], 3),
    ],
)
def test_require_length_accepts_correct_length(
    values,
    count,
):
    require_length(
        values,
        count,
    )


@pytest.mark.parametrize(
    ("values", "count"),
    [
        ([], 1),
        ([1], 0),
        ([1], 2),
        ([1, 2, 3], 2),
    ],
)
def test_require_length_rejects_wrong_length(
    values,
    count,
):
    with pytest.raises(ValueError):
        require_length(
            values,
            count,
        )


def test_require_length_uses_name_in_error():
    with pytest.raises(
        ValueError,
        match="Expected exactly 2 qubits",
    ):
        require_length(
            [0],
            2,
            name="qubits",
        )


# ---------------------------------------------------------------------------
# require_min_length
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "minimum"),
    [
        ([1], 1),
        ([1, 2], 1),
        ([1, 2], 2),
        ([1, 2, 3], 2),
    ],
)
def test_require_min_length_accepts_valid_length(
    values,
    minimum,
):
    require_min_length(
        values,
        minimum,
    )


@pytest.mark.parametrize(
    ("values", "minimum"),
    [
        ([], 1),
        ([1], 2),
        ([1, 2], 3),
    ],
)
def test_require_min_length_rejects_too_few(
    values,
    minimum,
):
    with pytest.raises(ValueError):
        require_min_length(
            values,
            minimum,
        )


def test_require_min_length_uses_name_in_error():
    with pytest.raises(
        ValueError,
        match="Expected at least 3 qubits",
    ):
        require_min_length(
            [0, 1],
            3,
            name="qubits",
        )


# ---------------------------------------------------------------------------
# require_same_length
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sequences",
    [
        ([], []),
        ([1], ["a"]),
        ([1, 2], ["a", "b"]),
        ([1, 2], ["a", "b"], [True, False]),
    ],
)
def test_require_same_length_accepts_equal_lengths(
    sequences,
):
    require_same_length(*sequences)


@pytest.mark.parametrize(
    "sequences",
    [
        ([1], []),
        ([1, 2], ["a"]),
        ([1], ["a"], [True, False]),
    ],
)
def test_require_same_length_rejects_different_lengths(
    sequences,
):
    with pytest.raises(ValueError):
        require_same_length(*sequences)


def test_require_same_length_accepts_single_sequence():
    require_same_length([1, 2])


def test_require_same_length_accepts_no_sequences():
    require_same_length()


def test_require_same_length_uses_names_in_error():
    with pytest.raises(
        ValueError,
        match="qubits=2, classical bits=1",
    ):
        require_same_length(
            [0, 1],
            [0],
            names=(
                "qubits",
                "classical bits",
            ),
        )


def test_require_same_length_rejects_wrong_number_of_names():
    with pytest.raises(ValueError):
        require_same_length(
            [0, 1],
            [0],
            names=("qubits",),
        )


# ---------------------------------------------------------------------------
# require_non_empty
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "values",
    [
        [1],
        [1, 2],
        ["a"],
    ],
)
def test_require_non_empty_accepts_non_empty(
    values,
):
    require_non_empty(values)


def test_require_non_empty_rejects_empty():
    with pytest.raises(ValueError):
        require_non_empty([])


def test_require_non_empty_uses_name_in_error():
    with pytest.raises(
        ValueError,
        match="Expected at least one qubit",
    ):
        require_non_empty(
            [],
            name="qubit",
        )


# ---------------------------------------------------------------------------
# require_distinct
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "values",
    [
        [],
        [1],
        [1, 2],
        [1, 2, 3],
        ["a", "b", "c"],
    ],
)
def test_require_distinct_accepts_unique_values(
    values,
):
    require_distinct(values)


@pytest.mark.parametrize(
    "values",
    [
        [1, 1],
        [1, 2, 1],
        ["a", "b", "a"],
    ],
)
def test_require_distinct_rejects_duplicates(
    values,
):
    with pytest.raises(ValueError):
        require_distinct(values)


def test_require_distinct_uses_name_in_error():
    with pytest.raises(
        ValueError,
        match="Expected distinct qubits",
    ):
        require_distinct(
            [0, 0],
            name="qubits",
        )


# ---------------------------------------------------------------------------
# require_qubits
# ---------------------------------------------------------------------------


def test_require_qubits_accepts_correct_count():
    circuit = QuantumCircuit(2)

    require_qubits(
        circuit.qubits,
        2,
    )


def test_require_qubits_rejects_wrong_count():
    circuit = QuantumCircuit(3)

    with pytest.raises(
        ValueError,
        match="Expected exactly 2 qubits",
    ):
        require_qubits(
            circuit.qubits,
            2,
        )


def test_require_qubits_accepts_integer_specifiers():
    require_qubits(
        [0, 1],
        2,
    )


# ---------------------------------------------------------------------------
# require_min_qubits
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "num_qubits",
    [
        2,
        3,
        4,
    ],
)
def test_require_min_qubits_accepts_valid_count(
    num_qubits,
):
    circuit = QuantumCircuit(num_qubits)

    require_min_qubits(
        circuit.qubits,
        2,
    )


def test_require_min_qubits_rejects_too_few():
    circuit = QuantumCircuit(1)

    with pytest.raises(
        ValueError,
        match="Expected at least 2 qubits",
    ):
        require_min_qubits(
            circuit.qubits,
            2,
        )


# ---------------------------------------------------------------------------
# require_distinct_qubits
# ---------------------------------------------------------------------------


def test_require_distinct_qubits():
    circuit = QuantumCircuit(2)

    require_distinct_qubits(
        circuit.qubits,
    )


def test_require_distinct_qubits_rejects_duplicate_objects():
    circuit = QuantumCircuit(1)

    qubit = circuit.qubits[0]

    with pytest.raises(
        ValueError,
        match="Expected distinct qubits",
    ):
        require_distinct_qubits(
            [qubit, qubit],
        )


def test_require_distinct_qubits_rejects_duplicate_indices():
    with pytest.raises(
        ValueError,
        match="Expected distinct qubits",
    ):
        require_distinct_qubits(
            [0, 0],
        )


# ---------------------------------------------------------------------------
# require_clbits
# ---------------------------------------------------------------------------


def test_require_clbits_accepts_correct_count():
    circuit = QuantumCircuit(1, 2)

    require_clbits(
        circuit.clbits,
        2,
    )


def test_require_clbits_rejects_wrong_count():
    circuit = QuantumCircuit(1, 3)

    with pytest.raises(
        ValueError,
        match="Expected exactly 2 classical bits",
    ):
        require_clbits(
            circuit.clbits,
            2,
        )


def test_require_clbits_accepts_integer_specifiers():
    require_clbits(
        [0, 1],
        2,
    )


# ---------------------------------------------------------------------------
# require_distinct_clbits
# ---------------------------------------------------------------------------


def test_require_distinct_clbits():
    circuit = QuantumCircuit(1, 2)

    require_distinct_clbits(
        circuit.clbits,
    )


def test_require_distinct_clbits_rejects_duplicate_objects():
    circuit = QuantumCircuit(1, 1)

    clbit = circuit.clbits[0]

    with pytest.raises(
        ValueError,
        match="Expected distinct classical bits",
    ):
        require_distinct_clbits(
            [clbit, clbit],
        )


def test_require_distinct_clbits_rejects_duplicate_indices():
    with pytest.raises(
        ValueError,
        match="Expected distinct classical bits",
    ):
        require_distinct_clbits(
            [0, 0],
        )
