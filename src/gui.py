"""Tkinter graphical user interface for Gamma Guard."""

import tkinter as tk
from tkinter import ttk

from gamma_core import GammaGuardError, evaluate_input


class GammaGuardApp:
    """Tkinter GUI for the F4 Gamma-function calculator."""

    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator - F4 Gamma Function")
        self.root.geometry("980x620")
        self.root.minsize(820, 520)

        self.input_value = tk.StringVar()
        self.status_value = tk.StringVar(value="Ready")
        self._build_layout()

    def _build_layout(self):
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        title = ttk.Label(
            main,
            text="Scientific Calculator - F4 Gamma Function",
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            main,
            text=(
                "From-scratch Lanczos implementation with reflection, "
                "helpful errors, and validation-ready output."
            ),
            wraplength=700,
        )
        subtitle.pack(anchor="w", pady=(2, 16))

        input_frame = ttk.LabelFrame(main, text="Input", padding=12)
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="Enter real value x:").grid(
            row=0, column=0, sticky="w"
        )
        entry = ttk.Entry(input_frame, textvariable=self.input_value, width=28)
        entry.grid(row=0, column=1, padx=10, sticky="we")
        entry.bind("<Return>", self.calculate)
        input_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=2, padx=(10, 0))
        ttk.Button(
            button_frame, text="Calculate", command=self.calculate
        ).pack(side="left")
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(
            side="left", padx=6
        )

        result_frame = ttk.LabelFrame(
            main, text="Calculation history", padding=12
        )
        result_frame.pack(fill="both", expand=True, pady=14)

        self.output = tk.Text(
            result_frame, height=12, wrap="word", font=("Consolas", 10)
        )
        self.output.pack(fill="both", expand=True)
        self.output.insert(
            "end",
            "Examples to try: 0.5, -0.5, 0, abc, 5, "
            "-1.0000000000001\n\n",
        )
        self.output.configure(state="disabled")

        ttk.Label(main, textvariable=self.status_value).pack(anchor="w")
        entry.focus_set()

    def write_output(self, message):
        """Append a message to the calculation-history area."""
        self.output.configure(state="normal")
        self.output.insert("end", message + "\n\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def calculate(self, event=None):
        """Handle the Calculate button and Return key."""
        text = self.input_value.get()
        try:
            message = evaluate_input(text)
            self.write_output("Input x: " + text + "\n" + message)
            self.status_value.set("Calculation completed")
        except GammaGuardError as error:
            self.write_output("Input error: " + str(error))
            self.status_value.set("Input needs correction")

    def clear(self):
        """Clear the input field and calculation history."""
        self.input_value.set("")
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")
        self.status_value.set("Cleared")


def run_gui():
    """Create the root window and start the Tkinter event loop."""
    root = tk.Tk()
    GammaGuardApp(root)
    root.mainloop()
