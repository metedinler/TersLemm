import tkinter as tk

class C64BorderEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("C64 Halı Motifi & Border Editörü (7 Byte x 24 Satır)")
        
        self.rows = 24
        self.bytes_per_row = 7
        self.cols = self.bytes_per_row * 8  # 56 piksel
        self.pixels = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.setup_ui()

    def setup_ui(self):
        # Sol Panel: Grid (Görsel Alan)
        self.canvas = tk.Canvas(self.root, width=self.cols*12, height=self.rows*12, bg="black")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Sağ Panel: Kontroller ve Data
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        
        tk.Label(self.right_frame, text="HEX DATA (C64 Format)", font=("Courier", 10, "bold")).pack()
        
        self.data_text = tk.Text(self.right_frame, width=40, height=25, font=("Courier", 9))
        self.data_text.pack(pady=5)
        
        self.btn_draw = tk.Button(self.right_frame, text="DATADAN GÖRSELE ÇİZ", command=self.draw_from_data, bg="lightblue")
        self.btn_draw.pack(fill=tk.X, pady=2)
        
        self.btn_clear = tk.Button(self.right_frame, text="TEMİZLE", command=self.clear_all)
        self.btn_clear.pack(fill=tk.X)

        self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                color = "#00FF00" if self.pixels[r][c] else "#222222" # Retro yeşil veya koyu gri
                x1, y1 = c * 12, r * 12
                x2, y2 = x1 + 10, y1 + 10
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333333")

    def on_canvas_click(self, event):
        c, r = event.x // 12, event.y // 12
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.pixels[r][c] = 1 - self.pixels[r][c]
            self.redraw_canvas()
            self.update_data_from_pixels()

    def update_data_from_pixels(self):
        self.data_text.delete("1.0", tk.END)
        for r in range(self.rows):
            row_hex = []
            for b in range(self.bytes_per_row):
                byte_val = 0
                for bit in range(8):
                    if self.pixels[r][b * 8 + bit]:
                        byte_val |= (1 << (7 - bit))
                row_hex.append(f"${byte_val:02X}")
            self.data_text.insert(tk.END, f"DATA {', '.join(row_hex)}\n")

    def draw_from_data(self):
        raw_data = self.data_text.get("1.0", tk.END).strip().split('\n')
        self.clear_all(refresh_text=False)
        
        for r, line in enumerate(raw_data):
            if r >= self.rows: break
            # HEX değerlerini ayıkla ($, 0x veya sadece hex)
            clean_line = line.replace("DATA", "").replace("$", "").replace(" ", "").split(",")
            for b, hex_val in enumerate(clean_line):
                if b >= self.bytes_per_row: break
                try:
                    val = int(hex_val, 16)
                    for bit in range(8):
                        if val & (1 << (7 - bit)):
                            self.pixels[r][b * 8 + bit] = 1
                except ValueError: continue
        self.redraw_canvas()

    def clear_all(self, refresh_text=True):
        self.pixels = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if refresh_text: self.data_text.delete("1.0", tk.END)
        self.redraw_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = C64BorderEditor(root)
    root.mainloop()