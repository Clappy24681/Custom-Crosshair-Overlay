import tkinter as tk
from tkinter import colorchooser

class CrosshairOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Custom Crosshair Overlay")

        # Initial crosshair settings
        self.cl_crosshairdot = tk.BooleanVar(value=True)
        self.cl_crosshairsize = tk.DoubleVar(value=5)
        self.cl_crosshairthickness = tk.DoubleVar(value=1)
        self.cl_crosshairgap = tk.DoubleVar(value=0)
        self.cl_crosshaircolor_r = tk.IntVar(value=255)
        self.cl_crosshaircolor_g = tk.IntVar(value=0)
        self.cl_crosshaircolor_b = tk.IntVar(value=0)
        self.cl_crosshair_t = tk.BooleanVar(value=False)
        self.cl_crosshair_dynamic_splitdist = tk.DoubleVar(value=0)
        self.cl_crosshair_dynamic_splitalpha_innermod = tk.DoubleVar(value=1)
        self.cl_crosshair_dynamic_splitalpha_outermod = tk.DoubleVar(value=1)
        self.cl_crosshair_dynamic_maxdist_splitratio = tk.DoubleVar(value=0)
        self.overlay_visible = False

        # GUI for customization
        self.create_customization_gui()

        # Fullscreen crosshair overlay
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes('-fullscreen', True)
        self.overlay.attributes('-topmost', True)
        self.overlay.attributes('-transparentcolor', 'black')
        self.overlay.configure(bg='black')
        self.overlay.withdraw()  # Start with overlay hidden

        self.canvas = tk.Canvas(self.overlay, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.update_crosshair()

        self.overlay.bind("<Escape>", self.exit_overlay)

    def create_customization_gui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Checkbutton(control_frame, text="Center Dot", variable=self.cl_crosshairdot).grid(row=0, column=0, sticky='w')

        tk.Label(control_frame, text="Length:").grid(row=1, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshairsize, from_=0.1, to=10, resolution=0.1, orient=tk.HORIZONTAL).grid(row=1, column=1, sticky='ew')

        tk.Label(control_frame, text="Thickness:").grid(row=2, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshairthickness, from_=0.1, to=6, resolution=0.1, orient=tk.HORIZONTAL).grid(row=2, column=1, sticky='ew')

        tk.Label(control_frame, text="Gap:").grid(row=3, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshairgap, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL).grid(row=3, column=1, sticky='ew')

        tk.Label(control_frame, text="Red:").grid(row=4, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshaircolor_r, from_=0, to=255, orient=tk.HORIZONTAL).grid(row=4, column=1, sticky='ew')

        tk.Label(control_frame, text="Green:").grid(row=5, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshaircolor_g, from_=0, to=255, orient=tk.HORIZONTAL).grid(row=5, column=1, sticky='ew')

        tk.Label(control_frame, text="Blue:").grid(row=6, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshaircolor_b, from_=0, to=255, orient=tk.HORIZONTAL).grid(row=6, column=1, sticky='ew')

        tk.Checkbutton(control_frame, text="T Style", variable=self.cl_crosshair_t).grid(row=7, column=0, sticky='w')

        tk.Label(control_frame, text="Split Distance:").grid(row=8, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshair_dynamic_splitdist, from_=0, to=16, resolution=0.1, orient=tk.HORIZONTAL).grid(row=8, column=1, sticky='ew')

        tk.Label(control_frame, text="Inner Split Alpha:").grid(row=9, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshair_dynamic_splitalpha_innermod, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL).grid(row=9, column=1, sticky='ew')

        tk.Label(control_frame, text="Outer Split Alpha:").grid(row=10, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshair_dynamic_splitalpha_outermod, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL).grid(row=10, column=1, sticky='ew')

        tk.Label(control_frame, text="Split Size Ratio:").grid(row=11, column=0, sticky='w')
        tk.Scale(control_frame, variable=self.cl_crosshair_dynamic_maxdist_splitratio, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL).grid(row=11, column=1, sticky='ew')

        color_button = tk.Button(control_frame, text="Choose Color", command=self.choose_color)
        color_button.grid(row=12, column=0, columnspan=2, pady=5)

        tk.Button(control_frame, text="Apply", command=self.apply_settings).grid(row=13, column=0, columnspan=2, pady=10)

        self.toggle_button = tk.Button(control_frame, text="Show Overlay", command=self.toggle_overlay)
        self.toggle_button.grid(row=14, column=0, columnspan=2, pady=10)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.cl_crosshaircolor_r.set(int(color_code[1:3], 16))
            self.cl_crosshaircolor_g.set(int(color_code[3:5], 16))
            self.cl_crosshaircolor_b.set(int(color_code[5:7], 16))

    def apply_settings(self):
        self.update_crosshair()

    def toggle_overlay(self):
        if self.overlay_visible:
            self.overlay.withdraw()
            self.toggle_button.config(text="Show Overlay")
        else:
            self.overlay.deiconify()
            self.toggle_button.config(text="Hide Overlay")
        self.overlay_visible = not self.overlay_visible

    def update_crosshair(self):
        self.canvas.delete("crosshair")
        screen_width = self.overlay.winfo_screenwidth()
        screen_height = self.overlay.winfo_screenheight()
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Convert the color values to a hex string
        color = f'#{self.cl_crosshaircolor_r.get():02x}{self.cl_crosshaircolor_g.get():02x}{self.cl_crosshaircolor_b.get():02x}'

        self.canvas.create_line(center_x - self.cl_crosshairgap.get() - self.cl_crosshairsize.get(), center_y,
                                center_x - self.cl_crosshairgap.get(), center_y,
                                fill=color, width=self.cl_crosshairthickness.get(), tags="crosshair")
        self.canvas.create_line(center_x + self.cl_crosshairgap.get(), center_y,
                                center_x + self.cl_crosshairgap.get() + self.cl_crosshairsize.get(), center_y,
                                fill=color, width=self.cl_crosshairthickness.get(), tags="crosshair")

        if not self.cl_crosshair_t.get():
            self.canvas.create_line(center_x, center_y - self.cl_crosshairgap.get() - self.cl_crosshairsize.get(),
                                    center_x, center_y - self.cl_crosshairgap.get(),
                                    fill=color, width=self.cl_crosshairthickness.get(), tags="crosshair")
            self.canvas.create_line(center_x, center_y + self.cl_crosshairgap.get(),
                                    center_x, center_y + self.cl_crosshairgap.get() + self.cl_crosshairsize.get(),
                                    fill=color, width=self.cl_crosshairthickness.get(), tags="crosshair")

        if self.cl_crosshairdot.get():
            dot_size = self.cl_crosshairthickness.get()
            self.canvas.create_oval(center_x - dot_size / 2, center_y - dot_size / 2,
                                    center_x + dot_size / 2, center_y + dot_size / 2,
                                    fill=color, outline=color, tags="crosshair")

        self.overlay.after(50, self.update_crosshair)

    def exit_overlay(self, event=None):
        self.overlay.withdraw()
        self.toggle_button.config(text="Show Overlay")
        self.overlay_visible = False

if __name__ == "__main__":
    app = CrosshairOverlay()
    app.root.mainloop()
