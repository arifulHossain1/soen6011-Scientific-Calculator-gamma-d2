"""Accessible Tkinter graphical user interface for Gamma Guard."""

import tkinter as tk
from tkinter import ttk

from gamma_core import GammaGuardError, evaluate_input
from version import __version__


class GammaGuardApp:
    """Tkinter GUI for the F4 Gamma-function calculator."""

    def __init__(self, root):
        self.root = root
        self.root.title(
            f"Scientific Calculator - F4 Gamma Function v{__version__}"
        )
        self.root.geometry("980x640")
        self.root.minsize(820, 540)

        self.input_value = tk.StringVar()
        self.status_value = tk.StringVar(
            value="Ready. Enter a real number, then choose Calculate."
        )

        self._configure_styles()
        self._build_layout()
        self._bind_keyboard_shortcuts()

    def _configure_styles(self):
        """Configure readable widget spacing without color-only cues."""
        style = ttk.Style(self.root)
        style.configure("Accessible.TButton", padding=(12, 8))
        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 11, "bold"),
        )

    def _build_layout(self):
        """Build the single-window calculator interface."""
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        title = ttk.Label(
            main,
            text=f"Scientific Calculator - F4 Gamma Function v{__version__}",
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            main,
            text=(
                "From-scratch Lanczos implementation with reflection, "
                "helpful errors, and validation-ready output."
            ),
            wraplength=760,
        )
        subtitle.pack(anchor="w", pady=(2, 8))

        help_label = ttk.Label(
            main,
            text=(
                "Keyboard: Enter or Alt+C = Calculate; "
                "Esc or Alt+L = Clear. "
                "Examples: 0.5, -0.5, 0, abc, 5."
            ),
            wraplength=760,
        )
        help_label.pack(anchor="w", pady=(0, 14))

        input_frame = ttk.LabelFrame(main, text="Input", padding=12)
        input_frame.pack(fill="x")

        input_label = ttk.Label(
            input_frame,
            text="Enter one real value x:",
        )
        input_label.grid(row=0, column=0, sticky="w")

        self.entry = ttk.Entry(
            input_frame,
            textvariable=self.input_value,
            width=28,
            takefocus=True,
        )
        self.entry.grid(row=0, column=1, padx=10, sticky="we")
        self.entry.bind("<Return>", self.calculate)
        input_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=2, padx=(10, 0))

        calculate_button = ttk.Button(
            button_frame,
            text="Calculate",
            command=self.calculate,
            style="Accessible.TButton",
            takefocus=True,
        )
        calculate_button.pack(side="left")

        clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear,
            style="Accessible.TButton",
            takefocus=True,
        )
        clear_button.pack(side="left", padx=(6, 0))

        result_frame = ttk.LabelFrame(
            main,
            text="Calculation history",
            padding=12,
        )
        result_frame.pack(fill="both", expand=True, pady=14)
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)

        self.output = tk.Text(
            result_frame,
            height=12,
            wrap="word",
            font=("Consolas", 11),
            padx=8,
            pady=8,
            takefocus=True,
        )
        self.output.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.output.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=scrollbar.set)

        self.output.insert(
            "end",
            (
                "Calculation history will appear here. "
                "Errors and warnings are also explained in text.\n\n"
            ),
        )
        self.output.configure(state="disabled")

        status_frame = ttk.Frame(main)
        status_frame.pack(fill="x")

        ttk.Label(
            status_frame,
            text="Status:",
            style="Status.TLabel",
        ).pack(side="left")

        ttk.Label(
            status_frame,
            textvariable=self.status_value,
            wraplength=700,
        ).pack(side="left", padx=(6, 0))

        self.entry.focus_set()

    def _bind_keyboard_shortcuts(self):
        """Provide keyboard alternatives for the main actions."""
        self.root.bind("<Escape>", self.clear)
        self.root.bind("<Alt-c>", self.calculate)
        self.root.bind("<Alt-C>", self.calculate)
        self.root.bind("<Alt-l>", self.clear)
        self.root.bind("<Alt-L>", self.clear)

    def write_output(self, message):
        """Append a message to the calculation-history area."""
        self.output.configure(state="normal")
        self.output.insert("end", message + "\n\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def calculate(self, _event=None):
        """Handle Calculate actions from the button or keyboard."""
        text = self.input_value.get()

        try:
            message = evaluate_input(text)
            self.write_output("Input x: " + text + "\n" + message)
            self.status_value.set(
                "Calculation completed. Ready for another input."
            )
            self.entry.focus_set()
            self.entry.selection_range(0, "end")
        except GammaGuardError as error:
            self.write_output("Input error: " + str(error))
            self.status_value.set(
                "Input needs correction. Review the message in history."
            )
            self.entry.focus_set()
            self.entry.selection_range(0, "end")

    def clear(self, _event=None):
        """Clear input and history, then return focus to the input field."""
        self.input_value.set("")
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert(
            "end",
            "Calculation history is clear. Ready for a new input.\n\n",
        )
        self.output.configure(state="disabled")
        self.status_value.set("Cleared. Ready for a new input.")
        self.entry.focus_set()


def run_gui():
    """Create the root window and start the Tkinter event loop."""
    root = tk.Tk()
    GammaGuardApp(root)
    root.mainloop()
