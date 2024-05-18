import tkinter as tk
import pyautogui

class CrosshairOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'black')
        self.root.configure(bg='black')
        
        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.crosshair_color = "red"
        self.crosshair_size = 20

        self.update_crosshair()

        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.mainloop()

    def update_crosshair(self):
        self.canvas.delete("crosshair")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        self.canvas.create_line(center_x - self.crosshair_size, center_y, 
                                center_x + self.crosshair_size, center_y, 
                                fill=self.crosshair_color, width=2, tags="crosshair")
        self.canvas.create_line(center_x, center_y - self.crosshair_size, 
                                center_x, center_y + self.crosshair_size, 
                                fill=self.crosshair_color, width=2, tags="crosshair")
        
        self.root.after(50, self.update_crosshair)

if __name__ == "__main__":
    CrosshairOverlay()