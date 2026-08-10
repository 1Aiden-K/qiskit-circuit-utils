Created this library based on a set of utility functions I created for personal use while going through Hiu Yung Wong's Introduction to Quantum Computing.

### Library Conventions:
- Follows Qiskit conventions
- Doesn't directly implement QuantumCircuit class, i.e. requires some QuantumCiruit object to be passed through each function
- Intended to be imported as "from qiskit_circuit_utils import preparation as prep" instead of from qiskit_circuit_utils.preparation import bell_state"
  - Otherwise readability could be obstructed
  - Also this is dangerous as function naming conflicts may arise