import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class C64ProEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("C64 Motif & Border Pro Editor")
        
        # Varsayılan Değerler
        self.rows = 24
        self.bytes_per_row = 7
        self.pixel_size = 15
        self.pixels = []
        
        self.init_pixels()
        self.setup_ui()
        self.setup_menu()

    def init_pixels(self):
        self.cols = self.bytes_per_row * 8
        self.pixels = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        # Dosya Menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Dosya Aç (.txt)", command=self.load_file)
        file_menu.add_command(label="Kaydet (.txt)", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        
        # Ayarlar Menüsü
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Boyutları Ayarla", command=self.change_dimensions)
        menubar.add_cascade(label="Ayarlar", menu=settings_menu)
        
        self.root.config(menu=menubar)

    def setup_ui(self):
        # Ana Konteyner
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sol: Canvas (Kaydırma çubuğu ile birlikte)
        canvas_frame = tk.Frame(self.main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#1a1a1a", borderwidth=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_click) # Sürükleyerek çizim

        # Sağ: Veri Paneli
        right_panel = tk.Frame(self.main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        tk.Label(right_panel, text="HEX DATA", font=("Arial", 10, "bold")).pack()
        self.data_text = tk.Text(right_panel, width=35, font=("Courier New", 10))
        self.data_text.pack(fill=tk.Y, expand=True)
        
        btn_update = tk.Button(right_panel, text="DATADAN ÇİZ", command=self.draw_from_data, bg="#4CAF50", fg="white")
        btn_update.pack(fill=tk.X, pady=5)

        self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        # Canvas boyutunu güncelle
        self.canvas.config(width=self.cols * self.pixel_size, height=self.rows * self.pixel_size)
        
        for r in range(self.rows):
            for c in range(self.cols):
                color = "#00FF41" if self.pixels[r][c] else "#333333"
                x1, y1 = c * self.pixel_size, r * self.pixel_size
                x2, y2 = x1 + (self.pixel_size-1), y1 + (self.pixel_size-1)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222222")

    def on_canvas_click(self, event):
        c, r = int(event.x // self.pixel_size), int(event.y // self.pixel_size)
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.pixels[r][c] = 1 # Çizim modu (tıklananı yakar)
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

    def draw_from_data(self, content=None):
        if content is None:
            content = self.data_text.get("1.0", tk.END)
        
        lines = content.strip().split('\n')
        for r, line in enumerate(lines):
            if r >= self.rows: break
            # Temizleme: DATA, $, boşlukları at
            parts = line.replace("DATA", "").replace("$", "").replace(" ", "").split(",")
            for b, hex_val in enumerate(parts):
                if b >= self.bytes_per_row: break
                try:
                    val = int(hex_val, 16)
                    for bit in range(8):
                        self.pixels[r][b * 8 + bit] = 1 if (val & (1 << (7 - bit))) else 0
                except ValueError: continue
        self.redraw_canvas()

    def change_dimensions(self):
        new_r = simpledialog.askinteger("Ayarlar", "Satır Sayısı:", initialvalue=self.rows)
        new_b = simpledialog.askinteger("Ayarlar", "Satır Başına Byte (8 piksel = 1 byte):", initialvalue=self.bytes_per_row)
        if new_r and new_b:
            self.rows = new_r
            self.bytes_per_row = new_b
            self.init_pixels()
            self.redraw_canvas()
            self.data_text.delete("1.0", tk.END)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.data_text.get("1.0", tk.END))
            messagebox.showinfo("Başarılı", "Dosya kaydedildi.")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as f:
                content = f.read()
                self.data_text.delete("1.0", tk.END)
                self.data_text.insert(tk.END, content)
                self.draw_from_data(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = C64ProEditor(root)
    root.mainloop()