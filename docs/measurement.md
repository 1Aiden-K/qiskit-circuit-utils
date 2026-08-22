# `measurement`

Utilities for adding non-basic measurements to quantum circuits.

## `z`

```python
z(circuit: QuantumCircuit, qubit: QubitSpecifier, clbit: ClbitSpecifier) -> None
```

Measure a qubit in the Z basis.

## `z_all`

```python
z_all(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], clbits: Sequence[ClbitSpecifier]) -> None
```

Measure each qubit in the Z basis.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to measure.
- `clbits` — Classical bits receiving the measurement results.

### Raises

- `ValueError` — If the number of qubits and classical bits differ.

## `x`

```python
x(circuit: QuantumCircuit, qubit: QubitSpecifier, clbit: ClbitSpecifier) -> None
```

Measure a qubit in the X basis.

## `x_all`

```python
x_all(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], clbits: Sequence[ClbitSpecifier]) -> None
```

Measure each qubit in the X basis.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to measure.
- `clbits` — Classical bits receiving the measurement results.

### Raises

- `ValueError` — If the number of qubits and classical bits differ.

## `y`

```python
y(circuit: QuantumCircuit, qubit: QubitSpecifier, clbit: ClbitSpecifier) -> None
```

Measure a qubit in the Y basis.

## `y_all`

```python
y_all(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], clbits: Sequence[ClbitSpecifier]) -> None
```

Measure each qubit in the Y basis.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits to measure.
- `clbits` — Classical bits receiving the measurement results.

### Raises

- `ValueError` — If the number of qubits and classical bits differ.

## `pauli`

```python
pauli(circuit: QuantumCircuit, qubit: QubitSpecifier, clbit: ClbitSpecifier, basis: PauliBasis = 'Z') -> None
```

Measure a qubit in a Pauli basis.

### Parameters

- `circuit` — Circuit to modify.
- `qubit` — Qubit to measure.
- `clbit` — Classical bit receiving the result.
- `basis` — Measurement basis: "X", "Y", or "Z".

### Raises

- `ValueError` — If the basis is unsupported.

## `bell_basis`

```python
bell_basis(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier], clbits: Sequence[ClbitSpecifier]) -> None
```

Measure two qubits in the Bell basis.

Performs the inverse of Bell-state preparation followed by measurement in the computational basis.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Two distinct qubits to measure.
- `clbits` — Two distinct classical bits receiving the results.

### Raises

- `ValueError` — If exactly two qubits and classical bits are not provided.
- `ValueError` — If duplicate qubits or classical bits are specified.

## `z_pairs`

```python
z_pairs(circuit: QuantumCircuit, pairs: Iterable[MeasurementPair]) -> None
```

Measure each (qubit, classical-bit) pair in the Z basis.

## `x_pairs`

```python
x_pairs(circuit: QuantumCircuit, pairs: Iterable[MeasurementPair]) -> None
```

Measure each (qubit, classical-bit) pair in the X basis.

## `y_pairs`

```python
y_pairs(circuit: QuantumCircuit, pairs: Iterable[MeasurementPair]) -> None
```

Measure each (qubit, classical-bit) pair in the Y basis.
