"""Minimal desktop UI for converting .xlsb files to .xlsx."""
import math
import subprocess
import sys
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tkinter import filedialog

from converter import convert

BG = "#ffffff"
FG = "#1f2328"
MUTED = "#6e7781"
ACCENT = "#217346"
ACCENT_DARK = "#185c37"
ERROR = "#cf222e"
FONT = "Segoe UI"
FRAME_MS = 16


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.output = None

        root.title("XLSB to XLSX")
        root.configure(bg=BG, padx=40, pady=32)
        root.resizable(False, False)

        tk.Label(root, text="XLSB → XLSX", font=(FONT, 16, "bold"), bg=BG, fg=FG).pack()
        self.status = tk.Label(root, font=(FONT, 10), bg=BG, wraplength=280)
        self.status.pack(pady=(4, 16))

        self.stage = tk.Frame(root, bg=BG, width=280, height=56)
        self.stage.pack_propagate(False)
        self.stage.pack()

        self.button = tk.Button(
            self.stage, text="Choose file…", command=self.choose, font=(FONT, 11),
            bg=ACCENT, fg=BG, activebackground=ACCENT_DARK, activeforeground=BG,
            relief="flat", bd=0, padx=24, pady=8, cursor="hand2",
        )
        self.spinner = tk.Canvas(self.stage, width=44, height=44, bg=BG, highlightthickness=0)
        self.arc = self.spinner.create_arc(4, 4, 40, 40, style="arc", outline=ACCENT, width=4)

        self.reveal = tk.Label(root, text="Show in folder", font=(FONT, 10, "underline"),
                               bg=BG, fg=ACCENT, cursor="hand2")
        self.reveal.bind("<Button-1>", lambda _: reveal(self.output))

        self.set_status("Convert Excel binary workbooks", MUTED)
        self.show(self.button)

    def choose(self) -> None:
        source = filedialog.askopenfilename(
            title="Select a workbook", filetypes=[("Excel Binary Workbook", "*.xlsb")])
        if not source:
            return
        source = Path(source)
        target = filedialog.asksaveasfilename(
            title="Save as", initialdir=source.parent, initialfile=f"{source.stem}.xlsx",
            defaultextension=".xlsx", filetypes=[("Excel Workbook", "*.xlsx")])
        if not target:
            return

        self.output = Path(target)
        self.reveal.pack_forget()
        self.set_status(f"Converting {source.name}…", MUTED)
        self.show(self.spinner)
        self.animate(self.executor.submit(convert, source, self.output), angle=0)

    def animate(self, job, angle: int) -> None:
        if job.done():
            self.finish(job)
            return
        extent = 110 + 80 * math.sin(math.radians(angle * 2))
        self.spinner.itemconfigure(self.arc, start=-angle, extent=extent)
        self.root.after(FRAME_MS, self.animate, job, (angle + 8) % 360)

    def finish(self, job) -> None:
        self.button.configure(text="Convert another…")
        self.show(self.button)
        error = job.exception()
        if error:
            self.set_status(f"Conversion failed: {error}", ERROR)
        else:
            self.set_status(f"Saved {self.output.name}", ACCENT)
            self.reveal.pack(pady=(12, 0))

    def show(self, widget: tk.Widget) -> None:
        for child in self.stage.winfo_children():
            child.place_forget()
        widget.place(relx=0.5, rely=0.5, anchor="center")

    def set_status(self, text: str, color: str) -> None:
        self.status.configure(text=text, fg=color)


def reveal(path: Path) -> None:
    if sys.platform == "win32":
        subprocess.Popen(f'explorer /select,"{path}"')
    else:
        subprocess.Popen(["open", "-R", str(path)])


def main() -> None:
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    App(root)
    root.eval("tk::PlaceWindow . center")
    root.mainloop()


if __name__ == "__main__":
    main()
