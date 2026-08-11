"""Shared type definitions for qiskit_circuit_utils."""

from typing import Literal, TypeAlias

from qiskit.circuit import Clbit, Qubit

# Qubit and classical-bit specifiers

QubitSpecifier: TypeAlias = int | Qubit
"""A qubit specified by either its circuit index or Qiskit Qubit object."""

ClbitSpecifier: TypeAlias = int | Clbit
"""A classical bit specified by either its circuit index or Clbit object."""

# Qubit groupings

QubitPair: TypeAlias = tuple[
    QubitSpecifier,
    QubitSpecifier,
]
"""An ordered pair of qubits."""

QubitTriple: TypeAlias = tuple[
    QubitSpecifier,
    QubitSpecifier,
    QubitSpecifier,
]
"""An ordered group of three qubits."""

# Measurement mappings

MeasurementPair: TypeAlias = tuple[
    QubitSpecifier,
    ClbitSpecifier,
]
"""A mapping from a qubit to a classical measurement bit."""

# State specifications

BellState: TypeAlias = Literal[
    "phi+",
    "phi-",
    "psi+",
    "psi-",
]
"""One of the four Bell states."""

PauliBasis: TypeAlias = Literal[
    "X",
    "Y",
    "Z",
    "x",
    "y",
    "z",
]
"""A Pauli measurement basis."""

Eigenvalue: TypeAlias = Literal[
    -1,
    1,
]
"""An eigenvalue of a Pauli operator."""

BinaryValue: TypeAlias = Literal[0, 1]
"""More explicit 1 or 0"""
