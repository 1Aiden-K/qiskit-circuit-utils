# `operation`

Utilities for multi-qubit operations.

## `reverse`

```python
reverse(circuit: QuantumCircuit, qubits: Sequence[QubitSpecifier]) -> None
```

Reverse the order of the specified qubits using SWAP gates.

### Parameters

- `circuit` — Circuit to modify.
- `qubits` — Qubits whose states to reverse.

### Raises

- `ValueError` — If duplicate qubits are specified.
