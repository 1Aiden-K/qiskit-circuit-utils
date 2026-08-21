# qiskit-circuit-utils

`qiskit-circuit-utils` is a collection of reusable circuit-building utilities for [Qiskit](https://www.ibm.com/quantum/qiskit), providing concise implementations of common quantum states, measurements, transformations, operations, and protocols.

The library is designed to complement Qiskit's `QuantumCircuit` API rather than replace it. Functions operate directly on a supplied circuit, making them easy to combine with standard Qiskit operations while keeping higher-level circuit construction readable.

## Installation

Install from PyPI:

```bash
pip install qiskit-circuit-utils
```

Requirements:

* Python 3.11 or later
* Qiskit 2.0 or later
* NumPy 2.0 or later

## Quick Start

Modules are intended to be imported by functionality:

```python
from qiskit import QuantumCircuit
from qiskit_circuit_utils import preparation as prep

circuit = QuantumCircuit(3)

prep.ghz_state(circuit, [0, 1, 2])

print(circuit)
```

This modifies `circuit` in place by preparing its three qubits in a GHZ state.

Utilities can be combined freely with standard Qiskit operations:

```python
from qiskit import QuantumCircuit
from qiskit_circuit_utils import measurement, preparation

circuit = QuantumCircuit(2, 2)

preparation.bell_state(circuit, [0, 1])
measurement.x(circuit, 0, 0)
measurement.z(circuit, 1, 1)
```

## Features

The public API is organized into modules according to functionality.

### `preparation`

State-preparation utilities, including:

* Bell states
* GHZ and W states
* Computational basis states
* `|+>` and `|->` states
* Uniform superpositions
* Arbitrary statevectors
* Product states
* Random pure states
* Pauli X, Y, and Z eigenstates
* Single-qubit states specified by Bloch-sphere angles

```python
from qiskit import QuantumCircuit
from qiskit_circuit_utils import preparation as prep

circuit = QuantumCircuit(2)

prep.bell_state(circuit, [0, 1], state="psi+")
```

### `measurement`

Measurement utilities for:

* X, Y, and Z bases
* Pauli-basis selection
* Bell-basis measurement
* Multi-qubit measurement
* Explicit qubit/classical-bit measurement pairs

```python
from qiskit import QuantumCircuit
from qiskit_circuit_utils import measurement

circuit = QuantumCircuit(2, 2)

measurement.x(circuit, 0, 0)
measurement.y(circuit, 1, 1)
```

### `correction`

Classically controlled correction operations, including:

* Conditional X corrections
* Conditional Z corrections
* Pauli X/Z corrections
* Corresponding multi-qubit operations

These utilities are useful when constructing protocols involving measurement-dependent corrections.

### `entanglement`

Higher-level entanglement and communication protocols, including:

* Entanglement swapping
* Quantum teleportation
* GHZ-style entanglement distribution and extension
* Qubit connection and disconnection
* State transfer
* Superdense coding

```python
from qiskit import QuantumCircuit
from qiskit_circuit_utils import entanglement

circuit = QuantumCircuit(3, 2)

entanglement.teleport(
    circuit,
    [0, 1, 2],
    [0, 1],
)
```

### `operation`

General circuit operations not specific to state preparation, measurement, or protocols.

Currently includes multi-qubit order reversal using SWAP gates:

```python
from qiskit import QuantumCircuit
from qiskit_circuit_utils import operation

circuit = QuantumCircuit(4)

operation.reverse(circuit, [0, 1, 2, 3])
```

### `transform`

Quantum circuit transformations, including:

* Quantum Fourier transform (QFT)
* Inverse quantum Fourier transform

Both transformations optionally include the final qubit-order reversal.

```python
from qiskit import QuantumCircuit
from qiskit_circuit_utils import transform

circuit = QuantumCircuit(4)

transform.qft(circuit, [0, 1, 2, 3])
transform.inverse_qft(circuit, [0, 1, 2, 3])
```

## Library Conventions

### Circuits are modified in place

Public functions accept a `QuantumCircuit` as their first argument, modify that circuit directly, and return `None`.

```python
prep.bell_state(circuit, [0, 1])
```

The library does not provide an alternative circuit class or wrapper around `QuantumCircuit`.

### Qubits and classical bits

Utilities support Qiskit bit objects and integer bit specifiers where applicable, allowing calls such as:

```python
prep.ghz_state(circuit, [0, 1, 2])
```

as well as calls using qubits obtained directly from a circuit or register.

### Module-oriented imports

The recommended import style is:

```python
from qiskit_circuit_utils import preparation as prep

prep.bell_state(circuit, [0, 1])
prep.ghz_state(circuit, [0, 1, 2])
```

rather than importing individual functions directly:

```python
from qiskit_circuit_utils.preparation import bell_state
```

Module-oriented imports preserve the context of utility names and reduce the possibility of naming conflicts as multiple parts of the library are used together.

## Examples

Runnable examples are available in the [`examples/`](examples/) directory:

* [`deutsch_algorithm.py`](examples/deutsch_algorithm.py) — Deutsch's algorithm
* [`quantum_phase_estimation.py`](examples/quantum_phase_estimation.py) — quantum phase estimation
* [`quantum_teleportation.py`](examples/quantum_teleportation.py) — quantum teleportation

The examples demonstrate how the library's utilities can be combined with Qiskit to construct complete quantum circuits.

## Project History

This library grew from a collection of utility functions originally written while working through Hiu Yung Wong's *Introduction to Quantum Computing*.

It has since been developed into a general-purpose package for reusable Qiskit circuit construction.

## License

This project is distributed under the MIT license.
