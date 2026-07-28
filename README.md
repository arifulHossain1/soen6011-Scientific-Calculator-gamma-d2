# Scientific Calculator — F4 Gamma Function

SOEN 6011 Deliverable 2 project implementing the real-valued Gamma function, \(\Gamma(x)\), from scratch in Python with a Tkinter graphical user interface.

## Course Information

- **Course:** SOEN 6011 — Software Engineering Processes
- **Deliverable:** D2
- **Assigned function:** F4 — Gamma Function
- **Student:** Md. Ariful Hossain
- **Repository:** https://github.com/arifulHossain1/soen6011-Scientific-Calculator-gamma-d2

## Features

- Lanczos approximation with Euler's reflection formula
- Tkinter GUI with input, Calculate, Clear, and calculation history
- Manual parsing of decimal and scientific-notation inputs
- Helpful messages for invalid input, poles, near-pole values, overflow, and underflow
- Separate validation against Python's `math.gamma()`

## From-Scratch Boundary

The production implementation does not use Python's `math` module for Gamma, sine, exponential, logarithm, square root, or power calculations. These numerical operations are implemented inside the project. Tkinter is used only for the graphical interface.

`math.gamma()` appears only in `validate_gamma.py` as an independent validation reference.

## Project Structure

```text
.
├── README.md
├── .gitignore
├── validation_output.txt
└── src/
    ├── gamma_core.py
    ├── gui.py
    ├── main.py
    └── validate_gamma.py
```

- `main.py` — starts the application
- `gui.py` — Tkinter interface and event handling
- `gamma_core.py` — parsing, numerical helpers, exceptions, and Gamma calculation
- `validate_gamma.py` — independent numerical validation

## Run the Application

From the repository root:

```bash
python src/main.py
```

On Windows, this may also be used:

```bash
py src/main.py
```

## Run Validation

```bash
python src/validate_gamma.py
```

The validation accepts a result when the relative error is no greater than `1.0e-10`.

## Requirements

- Python 3
- Tkinter
- No third-party packages

## Author

**Md. Ariful Hossain**  
SOEN 6011 — Software Engineering Processes
