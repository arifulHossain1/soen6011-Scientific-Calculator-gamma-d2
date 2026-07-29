# D2 Updated Requirements for Gamma Guard

Problem 7 updates the D1 requirements based on the D2 Problem 5 implementation. Repository, README, and commit-message evidence are treated as Problem 6 project constraints, not function requirements.

## Input and Domain

| ID | Status | Updated Requirement | Verification |
|---|---|---|---|
| GG-UI-01 | Modified | The software shall present a Tkinter input field for one real Gamma-function argument x. | GUI inspection |
| GG-IN-01 | Modified | When the entered text represents one finite real number, the software shall parse it using the project-defined parser. | Input test |
| GG-IN-02 | Modified | When the entered text is not one finite real number, the GUI shall display a corrective input message. | Invalid-input test |
| GG-DM-01 | Unchanged | When x is 0 or a negative integer, the software shall display a Gamma-domain pole message. | Boundary test |
| GG-DM-02 | Modified | When x is within 1e-12 of a nonpositive integer but is not exactly a pole, the GUI shall display a near-pole warning. | Sensitivity test |
| GG-FN-01 | Modified | When x is finite, not a pole, and the result is finite in double precision, the software shall compute Gamma(x) from scratch using the selected algorithm. | Reference test |
| GG-RG-01 | Modified | When the Gamma value exceeds the supported range, the GUI shall display a range message. | Range test |
| GG-RG-02 | Modified | When a nonzero Gamma value cannot be represented distinctly from zero, the GUI shall display an underflow message. | Underflow test |

## Output and Quality

| ID | Status | Updated Requirement | Verification |
|---|---|---|---|
| GG-OU-01 | Modified | After a successful calculation, the GUI shall display x and Gamma(x) with at least ten significant digits in the history area. | Output test |
| GG-OU-02 | Modified | After a successful calculation, the GUI shall display the algorithm path used. | Output test |
| GG-SE-01 | Modified | After each result or error, the GUI shall permit another calculation without restarting the application. | Session test |
| GG-PR-01 | Unchanged | For the validation set {0.1, 0.5, 1, 1.5, 2.5, 5, -0.5, -1.5}, relative error shall be no greater than 1e-10. | Validation script |
| GG-US-01 | Modified | For invalid input, domain rejection, range, or underflow, the GUI shall display a plain-language message with cause and corrective direction. | Usability test |

## D2 Additions

| ID | Status | Updated Requirement | Verification |
|---|---|---|---|
| GG-GUI-01 | New | The software shall provide a Tkinter GUI with an input field, Calculate control, Clear control, status label, and output/history area. | GUI inspection |
| GG-SC-01 | New | The production code shall implement sine, exponential, logarithm, positive-base power, and absolute-value support as project-defined subordinate functions. | Code inspection |
| GG-SC-02 | New | The production Gamma calculation shall not call Python's math-library Gamma, sine, exponential, logarithm, square-root, or power functions. | Code inspection |
| GG-BI-01 | New | The production numerical calculation shall avoid range() and len() by using while loops and manual counters where needed. | Code inspection |
| GG-EX-01 | New | Expected input, domain, range, and underflow cases shall be represented by user-facing exception classes. | Exception test |
| GG-DEP-01 | New | The application shall run from a terminal command without depending on a specific IDE. | Terminal test |
