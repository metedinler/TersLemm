import json
import math
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def hex_to_rgb(value):
    value = value.lstrip("#")
    if len(value) != 6:
        return 0, 0, 0
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def build_xterm_256_palette():
    base16 = [
        "#000000", "#800000", "#008000", "#808000", "#000080", "#800080", "#008080", "#c0c0c0",
        "#808080", "#ff0000", "#00ff00", "#ffff00", "#0000ff", "#ff00ff", "#00ffff", "#ffffff",
    ]
    out = list(base16)
    steps = [0, 95, 135, 175, 215, 255]
    for r in steps:
        for g in steps:
            for b in steps:
                out.append(f"#{r:02x}{g:02x}{b:02x}")
    for gray in range(8, 238 + 1, 10):
        out.append(f"#{gray:02x}{gray:02x}{gray:02x}")
    return out[:256]


def parse_hex_bytes(text):
    return [int(x, 16) for x in re.findall(r"(?:\$|0x)?([0-9A-Fa-f]{2})", text)]


def bytes_to_data_lines(label, data, line_len=16):
    lines = []
    for i in range(0, len(data), line_len):
        chunk = data[i:i + line_len]
        lines.append(f"{label} " + ", ".join(f"${b:02X}" for b in chunk))
    return "\n".join(lines)


def pack_5bit(values):
    out = []
    acc = 0
    bits = 0
    for v in values:
        acc = (acc << 5) | (v & 0x1F)
        bits += 5
        while bits >= 8:
            bits -= 8
            out.append((acc >> bits) & 0xFF)
            acc &= (1 << bits) - 1
    if bits:
        out.append((acc << (8 - bits)) & 0xFF)
    return out


def unpack_5bit(data, count):
    out = []
    acc = 0
    bits = 0
    idx = 0
    while len(out) < count:
        if bits < 5:
            if idx >= len(data):
                out.append(0)
                continue
            acc = (acc << 8) | data[idx]
            bits += 8
            idx += 1
        bits -= 5
        out.append((acc >> bits) & 0x1F)
        acc &= (1 << bits) - 1
    return out


class C64MasterEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("C64 Motif Designer & Asset Module")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_json_path = os.path.join(self.base_dir, "halidesen_varliklar.json")
        self.game_assets_source_path = os.path.join(self.base_dir, "..", "harita_yoneticisi.py")

        self.palette256 = build_xterm_256_palette()
        self.project = self.default_project_data()
        self.load_project_json()

        self.rows = int(self.project["grid"]["rows"])
        self.cols = int(self.project["grid"]["cols"])
        self.pixel_size = int(self.project["sizes"]["pixel_size"])
        self.current_color_slot = 1

        self.selected_asset_index = None
        self.filtered_asset_indices = []
        self.pixels = []
        self.brush_size = 1
        self.shape_start = None
        self.selection_start = None
        self.selection_bounds = None
        self.clipboard_pixels = None
        self.paste_dragging = False
        self.paste_drag_moved = False
        self.paste_preview_origin = None
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo = 60
        self.stroke_in_progress = False
        self.init_pixels()

        self.setup_ui()
        self.setup_menu()
        self.sync_game_assets_to_project(save=True)
        self.refresh_asset_list()
        self.redraw_canvas()
        self.update_data_text()
        self.update_size_preview()

    def default_project_data(self):
        return {
            "version": 1,
            "grid": {"rows": 24, "cols": 56},
            "sizes": {
                "pixel_size": 16,
                "emoji_size": 18,
                "small_char_size": 12,
                "tool_icon_size": 20,
            },
            "palette32_indices": list(range(32)),
            "assets": [],
        }

    def default_asset(self, name="isimsiz", width=16, height=16):
        return {
            "name": name,
            "category": "genel",
            "purpose": "",
            "usage": "",
            "mapped_game_asset": "",
            "width": int(width),
            "height": int(height),
            "bitmap_hex": "",
            "color5_hex": "",
            "source": "halidesennakismod",
        }

    def category_display_color(self, category):
        c = (category or "genel").lower()
        if c == "oyun_aleti":
            return "#204a37"
        if c in {"emoji", "duygu", "isaret"}:
            return "#4a3f20"
        if c in {"hud", "metin", "font"}:
            return "#20354a"
        return "#2f2f2f"

    def ensure_project_schema(self):
        defaults = self.default_project_data()
        for key, val in defaults.items():
            if key not in self.project:
                self.project[key] = val
        for key, val in defaults["grid"].items():
            self.project["grid"].setdefault(key, val)
        for key, val in defaults["sizes"].items():
            self.project["sizes"].setdefault(key, val)
        if len(self.project.get("palette32_indices", [])) != 32:
            self.project["palette32_indices"] = list(range(32))
        self.project["palette32_indices"] = [clamp(int(x), 0, 255) for x in self.project["palette32_indices"]][:32]
        if not isinstance(self.project.get("assets"), list):
            self.project["assets"] = []
        normalized = []
        for item in self.project["assets"]:
            base = self.default_asset()
            if isinstance(item, dict):
                base.update(item)
            normalized.append(base)
        self.project["assets"] = normalized

    def discover_game_asset_names(self):
        out = []
        if not os.path.exists(self.game_assets_source_path):
            return out
        try:
            with open(self.game_assets_source_path, "r", encoding="utf-8") as f:
                content = f.read()
            names = re.findall(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\(OyuncuAleti\)", content)
            seen = set()
            for n in names:
                if n not in seen:
                    seen.add(n)
                    out.append(n)
        except Exception:
            return []
        return out

    def sync_game_assets_to_project(self, save=True):
        game_names = self.discover_game_asset_names()
        if not game_names:
            return 0
        existing_map = {}
        for i, asset in enumerate(self.project["assets"]):
            key = (asset.get("mapped_game_asset") or "").strip()
            if key:
                existing_map[key] = i

        added = 0
        for n in game_names:
            if n in existing_map:
                asset = self.project["assets"][existing_map[n]]
                asset["category"] = asset.get("category") or "oyun_aleti"
                continue
            asset = self.default_asset(name=n, width=16, height=16)
            asset["category"] = "oyun_aleti"
            asset["mapped_game_asset"] = n
            asset["purpose"] = f"{n} gorseli"
            asset["usage"] = "oyun ici arac"
            self.project["assets"].append(asset)
            added += 1

        if save and added:
            self.save_project_json()
        return added

    def load_project_json(self):
        if not os.path.exists(self.project_json_path):
            return
        try:
            with open(self.project_json_path, "r", encoding="utf-8") as f:
                self.project = json.load(f)
            self.ensure_project_schema()
        except Exception as exc:
            messagebox.showwarning("Uyarı", f"JSON okunamadı, varsayılan kullanılacak.\n{exc}")
            self.project = self.default_project_data()

    def save_project_json(self):
        self.project["grid"]["rows"] = int(self.rows)
        self.project["grid"]["cols"] = int(self.cols)
        self.project["sizes"]["pixel_size"] = int(self.pixel_size)
        try:
            with open(self.project_json_path, "w", encoding="utf-8") as f:
                json.dump(self.project, f, indent=2, ensure_ascii=False)
        except Exception as exc:
            messagebox.showerror("Hata", f"JSON kaydedilemedi:\n{exc}")

    @property
    def bytes_per_row(self):
        return (self.cols + 7) // 8

    def init_pixels(self):
        self.pixels = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def set_grid_size(self, rows, cols, keep_content=True):
        rows = clamp(int(rows), 1, 128)
        cols = clamp(int(cols), 1, 256)
        old = self.pixels
        old_r = len(old)
        old_c = len(old[0]) if old else 0

        self.rows = rows
        self.cols = cols
        self.pixels = [[None for _ in range(cols)] for _ in range(rows)]
        if keep_content:
            for r in range(min(rows, old_r)):
                for c in range(min(cols, old_c)):
                    self.pixels[r][c] = old[r][c]

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        left_panel = tk.Frame(self.main_frame, bg="#253341", width=260)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)

        tk.Label(left_panel, text="GÖRÜNTÜ PARÇALARI", fg="white", bg="#253341", font=("Arial", 10, "bold")).pack(pady=(6, 2))

        filter_row = tk.Frame(left_panel, bg="#253341")
        filter_row.pack(fill=tk.X, padx=6, pady=(0, 4))
        self.asset_search_var = tk.StringVar()
        self.asset_search_var.trace_add("write", lambda *_: self.refresh_asset_list())
        tk.Entry(filter_row, textvariable=self.asset_search_var, width=16).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.asset_category_filter_var = tk.StringVar(value="Tümü")
        self.asset_category_menu = tk.OptionMenu(filter_row, self.asset_category_filter_var, "Tümü", command=lambda *_: self.refresh_asset_list())
        self.asset_category_menu.config(width=10)
        self.asset_category_menu.pack(side=tk.LEFT)

        self.asset_listbox = tk.Listbox(left_panel, height=15)
        self.asset_listbox.pack(fill=tk.X, padx=6)
        self.asset_listbox.bind("<<ListboxSelect>>", self.on_asset_selected)

        thumb_box = tk.Frame(left_panel, bg="#253341")
        thumb_box.pack(fill=tk.X, padx=6, pady=(4, 4))
        tk.Label(thumb_box, text="Seçili Varlık Önizleme", fg="#dfe6e9", bg="#253341").pack(anchor="w")
        self.thumb_canvas = tk.Canvas(thumb_box, width=180, height=120, bg="#101820", highlightthickness=1, highlightbackground="#4f5b66")
        self.thumb_canvas.pack(fill=tk.X)

        asset_btns = tk.Frame(left_panel, bg="#253341")
        asset_btns.pack(fill=tk.X, padx=6, pady=4)
        tk.Button(asset_btns, text="Yeni", command=self.new_asset).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(asset_btns, text="Sil", command=self.delete_asset).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(asset_btns, text="Yükle", command=self.load_selected_asset_to_grid).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        sync_btns = tk.Frame(left_panel, bg="#253341")
        sync_btns.pack(fill=tk.X, padx=6, pady=(0, 4))
        tk.Button(sync_btns, text="Oyun Varlıklarını Senkronla", command=self.on_sync_game_assets, bg="#2d6a4f", fg="white").pack(fill=tk.X)

        tk.Label(left_panel, text="Ad", fg="white", bg="#253341").pack(anchor="w", padx=6)
        self.asset_name_var = tk.StringVar()
        tk.Entry(left_panel, textvariable=self.asset_name_var).pack(fill=tk.X, padx=6)

        tk.Label(left_panel, text="Amaç", fg="white", bg="#253341").pack(anchor="w", padx=6)
        self.asset_purpose_var = tk.StringVar()
        tk.Entry(left_panel, textvariable=self.asset_purpose_var).pack(fill=tk.X, padx=6)

        tk.Label(left_panel, text="Kategori", fg="white", bg="#253341").pack(anchor="w", padx=6)
        self.asset_category_var = tk.StringVar()
        tk.Entry(left_panel, textvariable=self.asset_category_var).pack(fill=tk.X, padx=6)

        tk.Label(left_panel, text="Kullanım Yeri", fg="white", bg="#253341").pack(anchor="w", padx=6)
        self.asset_usage_var = tk.StringVar()
        tk.Entry(left_panel, textvariable=self.asset_usage_var).pack(fill=tk.X, padx=6)

        tk.Label(left_panel, text="Oyun Eşleşmesi", fg="white", bg="#253341").pack(anchor="w", padx=6)
        self.asset_mapped_var = tk.StringVar()
        tk.Entry(left_panel, textvariable=self.asset_mapped_var).pack(fill=tk.X, padx=6)

        tk.Button(left_panel, text="Grid -> Seçili Parça", command=self.save_grid_to_selected_asset, bg="#16a085", fg="white").pack(fill=tk.X, padx=6, pady=6)

        self.asset_info_label = tk.Label(left_panel, text="Seçili parça yok", fg="#d0d0d0", bg="#253341", justify="left")
        self.asset_info_label.pack(fill=tk.X, padx=6, pady=(2, 6))

        center_panel = tk.Frame(self.main_frame, bg="#2c3e50")
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        tool_row = tk.Frame(center_panel, bg="#2c3e50")
        tool_row.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))
        self.active_tool_var = tk.StringVar(value="kalem")
        tools = [
            ("Kalem", "kalem"),
            ("Silgi", "silgi"),
            ("Seçim", "secim"),
            ("Yapıştır", "yapistir"),
            ("Çizgi", "cizgi"),
            ("Dikdörtgen", "dikdortgen"),
            ("Çember", "cember"),
            ("Üçgen", "ucgen"),
            ("Doldur", "doldur"),
        ]
        for txt, val in tools:
            tk.Radiobutton(
                tool_row,
                text=txt,
                variable=self.active_tool_var,
                value=val,
                indicatoron=0,
                padx=8,
                pady=2,
                fg="#ecf0f1",
                bg="#3b4d5f",
                selectcolor="#16a085",
                activebackground="#16a085",
                activeforeground="white",
            ).pack(side=tk.LEFT, padx=2)

        tk.Label(tool_row, text="Kalınlık(px)", fg="#ecf0f1", bg="#2c3e50").pack(side=tk.LEFT, padx=(8, 2))
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        tk.Spinbox(tool_row, from_=1, to=32, width=4, textvariable=self.brush_size_var, command=self.on_brush_size_changed).pack(side=tk.LEFT)
        self.brush_size_var.trace_add("write", lambda *_: self.on_brush_size_changed())

        action_row = tk.Frame(center_panel, bg="#2c3e50")
        action_row.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))
        tk.Button(action_row, text="Seç", command=self.start_select_mode, bg="#f4d03f", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="Kopyala", command=self.copy_selection, bg="#5dade2", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="Yapıştır", command=self.start_paste_mode, bg="#82e0aa", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="Kes", command=self.cut_selection, bg="#f5b041", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="Geri Al", command=self.undo_action, bg="#aed6f1", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="İleri Al", command=self.redo_action, bg="#d6eaf8", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="90° Çevir", command=self.rotate_selection_90, bg="#d7bde2", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="15° Sol", command=lambda: self.rotate_selection_small(-15), bg="#d7bde2", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="15° Sağ", command=lambda: self.rotate_selection_small(15), bg="#d7bde2", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="Ayna Yatay", command=self.mirror_selection_horizontal, bg="#f9e79f", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(action_row, text="Ayna Dikey", command=self.mirror_selection_vertical, bg="#f9e79f", fg="black").pack(side=tk.LEFT, padx=2)

        color_row = tk.Frame(center_panel, bg="#2c3e50")
        color_row.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))
        tk.Button(color_row, text="32 Gri", command=self.convert_to_grayscale32, bg="#bdc3c7", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(color_row, text="32 Renge İndir", command=self.quantize_to_current_palette32, bg="#a3e4d7", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(color_row, text="Invert", command=self.invert_active_colors, bg="#95a5a6", fg="black").pack(side=tk.LEFT, padx=2)
        self.transform_color_var = tk.StringVar(value="Gri Skala")
        self.transform_color_menu = tk.OptionMenu(color_row, self.transform_color_var, "Gri Skala")
        self.transform_color_menu.config(width=18)
        self.transform_color_menu.pack(side=tk.LEFT, padx=(8, 2))
        tk.Button(color_row, text="Ton Rampası 32", command=self.convert_to_selected_tone, bg="#58d68d", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(color_row, text="Paleti Normal 32", command=self.reset_palette_default, bg="#f8c471", fg="black").pack(side=tk.LEFT, padx=2)

        self.editor_status_var = tk.StringVar(value="Araç: Kalem")
        tk.Label(center_panel, textvariable=self.editor_status_var, fg="#d5dbdb", bg="#2c3e50", anchor="w").pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(center_panel, bg="black", bd=0, highlightthickness=1)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_left_down)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_up)
        self.canvas.bind("<Button-3>", self.on_paint_erase)
        self.canvas.bind("<B3-Motion>", self.on_paint_erase)

        right_panel = tk.Frame(self.main_frame, bg="#34495e", width=420)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=6, pady=6)

        tk.Label(right_panel, text="GRID VE BOYUT AYARLARI", fg="white", bg="#34495e", font=("Arial", 10, "bold")).pack(pady=(6, 2))
        self.row_var = tk.IntVar(value=self.rows)
        self.col_var = tk.IntVar(value=self.cols)
        self.pixel_size_var = tk.IntVar(value=self.pixel_size)
        self.emoji_size_var = tk.IntVar(value=int(self.project["sizes"]["emoji_size"]))
        self.small_char_size_var = tk.IntVar(value=int(self.project["sizes"]["small_char_size"]))
        self.tool_icon_size_var = tk.IntVar(value=int(self.project["sizes"]["tool_icon_size"]))

        self._entry_row(right_panel, "Satır", self.row_var)
        self._entry_row(right_panel, "Sütun", self.col_var)
        self._entry_row(right_panel, "Piksel Boyutu", self.pixel_size_var)
        self._entry_row(right_panel, "Emoji Boyutu", self.emoji_size_var)
        self._entry_row(right_panel, "Küçük Karakter Boyutu", self.small_char_size_var)
        self._entry_row(right_panel, "Alet İkon Boyutu", self.tool_icon_size_var)
        tk.Button(right_panel, text="Ayarları Uygula", command=self.apply_size_settings, bg="#2980b9", fg="white").pack(fill=tk.X, padx=8, pady=6)

        tk.Label(right_panel, text="32 RENK PALET (256'DAN)", fg="white", bg="#34495e", font=("Arial", 10, "bold")).pack(pady=(4, 2))
        self.palette_info_var = tk.StringVar(value="Seçili Slot: 1")
        tk.Label(right_panel, textvariable=self.palette_info_var, fg="#e8e8e8", bg="#34495e").pack(anchor="w", padx=8)
        self.palette_frame = tk.Frame(right_panel, bg="#34495e")
        self.palette_frame.pack(fill=tk.X, padx=8)
        self.refresh_palette_buttons()
        self.refresh_transform_color_menu()

        tk.Button(right_panel, text="Palette Slot Düzenle", command=self.edit_palette_slot, bg="#8e44ad", fg="white").pack(fill=tk.X, padx=8, pady=4)

        preview_frame = tk.Frame(right_panel, bg="#34495e")
        preview_frame.pack(fill=tk.X, padx=8, pady=(4, 8))
        tk.Label(preview_frame, text="Boyut Önizleme:", fg="#e8e8e8", bg="#34495e").pack(anchor="w")
        self.preview_emoji = tk.Label(preview_frame, text="🙂 🛠 📦", fg="#f6f6f6", bg="#34495e")
        self.preview_emoji.pack(anchor="w")
        self.preview_small = tk.Label(preview_frame, text="abc0123 küçük karakter", fg="#f6f6f6", bg="#34495e")
        self.preview_small.pack(anchor="w")
        self.preview_tool = tk.Label(preview_frame, text="[ALET_IKON]", fg="#f6f6f6", bg="#34495e")
        self.preview_tool.pack(anchor="w")

        tk.Label(right_panel, text="C64 BENZERİ DATA", fg="white", bg="#34495e", font=("Arial", 10, "bold")).pack(pady=(4, 2))
        self.data_text = tk.Text(right_panel, width=48, height=16, font=("Courier", 9), bg="#ecf0f1")
        self.data_text.pack(padx=8, pady=4)

        tk.Button(right_panel, text="DATADAN GÖRSELE", command=self.draw_from_data, bg="#27ae60", fg="white").pack(fill=tk.X, padx=8, pady=2)
        tk.Button(right_panel, text="KAĞIDA GEÇİRME REHBERİ", command=self.open_narrator, bg="#e67e22", fg="white").pack(fill=tk.X, padx=8, pady=(2, 8))

    def _entry_row(self, parent, label, var):
        row = tk.Frame(parent, bg="#34495e")
        row.pack(fill=tk.X, padx=8, pady=1)
        tk.Label(row, text=label, width=20, anchor="w", fg="#e8e8e8", bg="#34495e").pack(side=tk.LEFT)
        tk.Entry(row, textvariable=var, width=8).pack(side=tk.LEFT)

    def setup_menu(self):
        m = tk.Menu(self.root)
        f = tk.Menu(m, tearoff=0)
        f.add_command(label="Data/JSON Aç", command=self.load_data_file)
        f.add_command(label="Data/JSON Kaydet", command=self.save_data_file)
        f.add_command(label="Seçili Varlık Aç (JSON/TXT)", command=self.load_single_asset_file)
        f.add_command(label="Seçili Varlık Kaydet (JSON/TXT)", command=self.save_single_asset_file)
        f.add_separator()
        f.add_command(label="JSON Projeyi Kaydet", command=self.save_project_json)
        m.add_cascade(label="Dosya", menu=f)
        self.root.config(menu=m)

    def refresh_category_filter_menu(self):
        categories = sorted({(a.get("category") or "genel") for a in self.project["assets"]})
        categories = ["Tümü"] + categories
        menu = self.asset_category_menu["menu"]
        menu.delete(0, "end")
        for c in categories:
            menu.add_command(label=c, command=lambda v=c: self._set_category_filter(v))
        if self.asset_category_filter_var.get() not in categories:
            self.asset_category_filter_var.set("Tümü")

    def _set_category_filter(self, value):
        self.asset_category_filter_var.set(value)
        self.refresh_asset_list()

    def _asset_matches_filter(self, asset):
        q = self.asset_search_var.get().strip().lower()
        cat = self.asset_category_filter_var.get().strip()
        if cat and cat != "Tümü":
            if (asset.get("category") or "genel") != cat:
                return False
        if not q:
            return True
        haystack = " ".join([
            str(asset.get("name", "")),
            str(asset.get("category", "")),
            str(asset.get("purpose", "")),
            str(asset.get("usage", "")),
            str(asset.get("mapped_game_asset", "")),
        ]).lower()
        return q in haystack

    def get_palette32(self):
        idxs = self.project.get("palette32_indices", list(range(32)))
        return [self.palette256[i] for i in idxs]

    def refresh_palette_buttons(self):
        for child in self.palette_frame.winfo_children():
            child.destroy()
        colors = self.get_palette32()
        for i, col in enumerate(colors):
            btn = tk.Button(
                self.palette_frame,
                bg=col,
                width=2,
                relief=tk.SUNKEN if i == self.current_color_slot else tk.RAISED,
                command=lambda slot=i: self.select_palette_slot(slot),
            )
            btn.grid(row=i // 8, column=i % 8, padx=1, pady=1)
        if hasattr(self, "transform_color_menu"):
            self.refresh_transform_color_menu()

    def refresh_transform_color_menu(self):
        if not hasattr(self, "transform_color_menu"):
            return
        labels = ["Gri Skala"]
        for i, col in enumerate(self.get_default_palette32()):
            labels.append(f"Slot {i}: {col}")
        menu = self.transform_color_menu["menu"]
        menu.delete(0, "end")
        for label in labels:
            menu.add_command(label=label, command=lambda v=label: self.transform_color_var.set(v))
        if self.transform_color_var.get() not in labels:
            self.transform_color_var.set("Gri Skala")

    def get_default_palette32(self):
        return [self.palette256[i] for i in range(32)]

    def select_palette_slot(self, slot):
        self.current_color_slot = int(slot)
        self.palette_info_var.set(f"Seçili Slot: {slot} / Renk: {self.get_palette32()[slot]}")
        self.refresh_palette_buttons()

    def edit_palette_slot(self):
        slot = simpledialog.askinteger("Slot", "Düzenlenecek slot (0-31):", minvalue=0, maxvalue=31)
        if slot is None:
            return
        idx = simpledialog.askinteger("256 Renk İndeksi", "Yeni indeks (0-255):", minvalue=0, maxvalue=255)
        if idx is None:
            return
        self.project["palette32_indices"][slot] = idx
        self.select_palette_slot(slot)
        self.redraw_canvas()
        self.save_project_json()

    def apply_size_settings(self):
        new_rows = clamp(int(self.row_var.get()), 1, 128)
        new_cols = clamp(int(self.col_var.get()), 1, 256)
        self.pixel_size = clamp(int(self.pixel_size_var.get()), 4, 64)

        self.project["sizes"]["emoji_size"] = clamp(int(self.emoji_size_var.get()), 6, 72)
        self.project["sizes"]["small_char_size"] = clamp(int(self.small_char_size_var.get()), 6, 72)
        self.project["sizes"]["tool_icon_size"] = clamp(int(self.tool_icon_size_var.get()), 6, 72)

        self.set_grid_size(new_rows, new_cols, keep_content=True)
        self.redraw_canvas()
        self.update_data_text()
        self.update_size_preview()
        self.save_project_json()

    def update_size_preview(self):
        emoji_size = int(self.project["sizes"]["emoji_size"])
        small_size = int(self.project["sizes"]["small_char_size"])
        tool_size = int(self.project["sizes"]["tool_icon_size"])
        self.preview_emoji.config(font=("Segoe UI Emoji", emoji_size))
        self.preview_small.config(font=("Consolas", small_size))
        self.preview_tool.config(font=("Consolas", tool_size, "bold"))

    def on_brush_size_changed(self):
        try:
            self.brush_size = clamp(int(self.brush_size_var.get()), 1, 32)
        except Exception:
            self.brush_size = 1

    def set_status(self, text):
        self.editor_status_var.set(text)

    def event_to_cell(self, event):
        c = int(event.x // self.pixel_size)
        r = int(event.y // self.pixel_size)
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return r, c
        return None

    def on_left_down(self, event):
        rc = self.event_to_cell(event)
        if rc is None:
            return
        r, c = rc
        tool = self.active_tool_var.get()
        if tool == "kalem":
            if not self.stroke_in_progress:
                self.push_undo_state("kalem")
            self.stroke_in_progress = True
            self.paint_cell_with_brush(r, c, self.current_color_slot)
            self.update_data_text()
            self.set_status(f"Araç: Kalem | Kalınlık: {self.brush_size}px")
        elif tool == "silgi":
            if not self.stroke_in_progress:
                self.push_undo_state("silgi")
            self.stroke_in_progress = True
            self.paint_cell_with_brush(r, c, None)
            self.update_data_text()
            self.set_status(f"Araç: Silgi | Kalınlık: {self.brush_size}px")
        elif tool == "secim":
            self.selection_start = (r, c)
            self.draw_selection_preview(r, c)
            self.set_status("Seçim sürükleniyor")
        elif tool == "yapistir":
            self.push_undo_state("yapistir")
            self.paste_dragging = True
            self.paste_drag_moved = False
            self.paste_preview_origin = (r, c)
            self.draw_paste_preview(r, c, center=False)
            self.set_status("Yapıştırma: tek tık sol-üst, sürükle merkez")
        elif tool == "doldur":
            self.push_undo_state("doldur")
            self.flood_fill(r, c, self.current_color_slot)
        else:
            self.shape_start = (r, c)
            self.draw_shape_preview(r, c)

    def on_left_drag(self, event):
        rc = self.event_to_cell(event)
        if rc is None:
            return
        r, c = rc
        tool = self.active_tool_var.get()
        if tool == "kalem":
            self.paint_cell_with_brush(r, c, self.current_color_slot)
            self.update_data_text()
        elif tool == "silgi":
            self.paint_cell_with_brush(r, c, None)
            self.update_data_text()
        elif tool == "secim" and self.selection_start is not None:
            self.draw_selection_preview(r, c)
        elif tool == "yapistir" and self.paste_dragging:
            self.paste_drag_moved = True
            self.paste_preview_origin = (r, c)
            self.draw_paste_preview(r, c, center=True)
        elif tool in {"cizgi", "dikdortgen", "cember", "ucgen"} and self.shape_start is not None:
            self.draw_shape_preview(r, c)

    def on_left_up(self, event):
        rc = self.event_to_cell(event)
        tool = self.active_tool_var.get()
        if tool in {"kalem", "silgi"}:
            self.stroke_in_progress = False
        if rc is None:
            self.canvas.delete("shape_preview")
            self.shape_start = None
            self.canvas.delete("paste_preview")
            self.paste_dragging = False
            self.paste_drag_moved = False
            return
        r1, c1 = rc
        if tool == "secim" and self.selection_start is not None:
            r0, c0 = self.selection_start
            self.selection_bounds = self.normalize_bounds(r0, c0, r1, c1)
            self.selection_start = None
            self.canvas.delete("selection_preview")
            self.redraw_canvas()
            self.set_status(self.selection_summary())
        elif tool == "yapistir" and self.paste_dragging:
            self.canvas.delete("paste_preview")
            self.paste_dragging = False
            if self.paste_drag_moved:
                self.paste_clipboard_at(r1, c1, center=True)
            else:
                self.paste_clipboard_at(r1, c1, center=False)
            self.paste_drag_moved = False
        elif tool in {"cizgi", "dikdortgen", "cember", "ucgen"} and self.shape_start is not None:
            self.push_undo_state("sekil")
            r0, c0 = self.shape_start
            if tool == "cizgi":
                self.draw_line(r0, c0, r1, c1, self.current_color_slot, self.brush_size)
            elif tool == "dikdortgen":
                self.draw_rectangle(r0, c0, r1, c1, self.current_color_slot, self.brush_size)
            elif tool == "cember":
                self.draw_ellipse(r0, c0, r1, c1, self.current_color_slot, self.brush_size)
            elif tool == "ucgen":
                self.draw_triangle(r0, c0, r1, c1, self.current_color_slot, self.brush_size)
            self.canvas.delete("shape_preview")
            self.shape_start = None
            self.redraw_canvas()
            self.update_data_text()

    def on_paint_draw(self, event):
        rc = self.event_to_cell(event)
        if rc is None:
            return
        r, c = rc
        self.paint_cell_with_brush(r, c, self.current_color_slot)
        self.update_data_text()

    def on_paint_erase(self, event):
        rc = self.event_to_cell(event)
        if rc is None:
            return
        r, c = rc
        self.paint_cell_with_brush(r, c, None)
        self.update_data_text()

    def normalize_bounds(self, r0, c0, r1, c1):
        top = min(r0, r1)
        left = min(c0, c1)
        bottom = max(r0, r1)
        right = max(c0, c1)
        return top, left, bottom, right

    def selection_summary(self):
        if self.selection_bounds is None:
            return "Seçim yok"
        top, left, bottom, right = self.selection_bounds
        return f"Seçim: {right - left + 1}x{bottom - top + 1} px"

    def draw_selection_preview(self, r1, c1):
        if self.selection_start is None:
            return
        r0, c0 = self.selection_start
        top, left, bottom, right = self.normalize_bounds(r0, c0, r1, c1)
        x0 = left * self.pixel_size
        y0 = top * self.pixel_size
        x1 = (right + 1) * self.pixel_size
        y1 = (bottom + 1) * self.pixel_size
        self.canvas.delete("selection_preview")
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#f1c40f", width=2, dash=(5, 3), tags="selection_preview")

    def draw_selection_overlay(self):
        self.canvas.delete("selection_overlay")
        if self.selection_bounds is None:
            return
        top, left, bottom, right = self.selection_bounds
        x0 = left * self.pixel_size
        y0 = top * self.pixel_size
        x1 = (right + 1) * self.pixel_size
        y1 = (bottom + 1) * self.pixel_size
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#f1c40f", width=2, dash=(5, 3), tags="selection_overlay")

    def get_selection_matrix(self):
        if self.selection_bounds is None:
            return None
        top, left, bottom, right = self.selection_bounds
        return [row[left:right + 1] for row in self.pixels[top:bottom + 1]]

    def get_full_matrix(self):
        return [row[:] for row in self.pixels]

    def write_matrix(self, top, left, matrix):
        for r_offset, row in enumerate(matrix):
            for c_offset, value in enumerate(row):
                rr = top + r_offset
                cc = left + c_offset
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    self.pixels[rr][cc] = value

    def clear_selection_area(self):
        if self.selection_bounds is None:
            return
        top, left, bottom, right = self.selection_bounds
        for rr in range(top, bottom + 1):
            for cc in range(left, right + 1):
                self.pixels[rr][cc] = None

    def copy_selection(self):
        matrix = self.get_selection_matrix()
        if matrix is None:
            messagebox.showinfo("Bilgi", "Önce seçim aracıyla bir alan seçin.")
            return
        self.clipboard_pixels = [row[:] for row in matrix]
        self.set_status(f"Kopyalandı: {len(matrix[0])}x{len(matrix)} px")

    def cut_selection(self):
        matrix = self.get_selection_matrix()
        if matrix is None:
            messagebox.showinfo("Bilgi", "Önce seçim aracıyla bir alan seçin.")
            return
        self.push_undo_state("kes")
        self.clipboard_pixels = [row[:] for row in matrix]
        self.clear_selection_area()
        self.redraw_canvas()
        self.update_data_text()
        self.set_status(f"Kesildi: {len(matrix[0])}x{len(matrix)} px")

    def start_paste_mode(self):
        if not self.clipboard_pixels:
            messagebox.showinfo("Bilgi", "Önce bir alan kopyalayın veya kesin.")
            return
        self.active_tool_var.set("yapistir")
        self.set_status("Yapıştırma modu: hedef piksele tıklayın")

    def start_select_mode(self):
        self.active_tool_var.set("secim")
        self.set_status("Seçim modu aktif")

    def paste_clipboard_at(self, top, left, center=False):
        if not self.clipboard_pixels:
            return
        height = len(self.clipboard_pixels)
        width = len(self.clipboard_pixels[0]) if height else 0
        if center:
            top = top - (height // 2)
            left = left - (width // 2)
        self.write_matrix(top, left, self.clipboard_pixels)
        if width and height:
            self.selection_bounds = self.normalize_bounds(top, left, min(self.rows - 1, top + height - 1), min(self.cols - 1, left + width - 1))
        self.redraw_canvas()
        self.update_data_text()
        anchor = "merkez" if center else "sol-üst"
        self.set_status(f"Yapıştırıldı: {width}x{height} px ({anchor})")

    def draw_paste_preview(self, r, c, center=False):
        self.canvas.delete("paste_preview")
        if not self.clipboard_pixels:
            return
        height = len(self.clipboard_pixels)
        width = len(self.clipboard_pixels[0]) if height else 0
        if width == 0 or height == 0:
            return
        top = r - (height // 2) if center else r
        left = c - (width // 2) if center else c
        x0 = left * self.pixel_size
        y0 = top * self.pixel_size
        x1 = (left + width) * self.pixel_size
        y1 = (top + height) * self.pixel_size
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#2ecc71", width=2, dash=(4, 2), tags="paste_preview")

    def transform_selection(self, transform):
        self.push_undo_state("transform")
        if self.selection_bounds is None:
            matrix = self.get_full_matrix()
            top, left = 0, 0
        else:
            matrix = self.get_selection_matrix()
            top, left, _bottom, _right = self.selection_bounds
        new_matrix = transform(matrix)
        if self.selection_bounds is None:
            self.init_pixels()
        else:
            self.clear_selection_area()
        self.write_matrix(top, left, new_matrix)
        new_height = len(new_matrix)
        new_width = len(new_matrix[0]) if new_height else 0
        self.selection_bounds = self.normalize_bounds(
            top,
            left,
            min(self.rows - 1, top + new_height - 1),
            min(self.cols - 1, left + new_width - 1),
        )
        self.redraw_canvas()
        self.update_data_text()

    def rotate_selection_90(self):
        self.transform_selection(lambda matrix: [list(row) for row in zip(*matrix[::-1])])
        self.set_status("Seçim 90° çevrildi")

    def rotate_matrix(self, matrix, angle_deg):
        height = len(matrix)
        width = len(matrix[0]) if height else 0
        if width == 0 or height == 0:
            return matrix
        angle = math.radians(angle_deg)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        cx = (width - 1) / 2.0
        cy = (height - 1) / 2.0
        corners = [(-cx, -cy), (width - 1 - cx, -cy), (-cx, height - 1 - cy), (width - 1 - cx, height - 1 - cy)]
        rotated = []
        for x, y in corners:
            rx = x * cos_a - y * sin_a
            ry = x * sin_a + y * cos_a
            rotated.append((rx, ry))
        min_x = math.floor(min(x for x, _ in rotated))
        max_x = math.ceil(max(x for x, _ in rotated))
        min_y = math.floor(min(y for _, y in rotated))
        max_y = math.ceil(max(y for _, y in rotated))
        new_width = max_x - min_x + 1
        new_height = max_y - min_y + 1
        out = [[None for _ in range(new_width)] for _ in range(new_height)]
        ncx = (new_width - 1) / 2.0
        ncy = (new_height - 1) / 2.0
        for nr in range(new_height):
            for nc in range(new_width):
                dx = nc - ncx
                dy = nr - ncy
                src_x = dx * cos_a + dy * sin_a + cx
                src_y = -dx * sin_a + dy * cos_a + cy
                sc = int(round(src_x))
                sr = int(round(src_y))
                if 0 <= sr < height and 0 <= sc < width:
                    out[nr][nc] = matrix[sr][sc]
        return out

    def rotate_selection_small(self, angle_deg):
        self.transform_selection(lambda matrix: self.rotate_matrix(matrix, angle_deg))
        direction = "sağa" if angle_deg > 0 else "sola"
        self.set_status(f"{abs(angle_deg)}° {direction} çevrildi")

    def mirror_selection_horizontal(self):
        self.transform_selection(lambda matrix: [list(reversed(row)) for row in matrix])
        self.set_status("Seçim yatay aynalandı")

    def mirror_selection_vertical(self):
        self.transform_selection(lambda matrix: list(reversed([row[:] for row in matrix])))
        self.set_status("Seçim dikey aynalandı")

    def get_active_cells(self):
        if self.selection_bounds is None:
            cells = []
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.pixels[r][c] is not None:
                        cells.append((r, c))
            return cells
        top, left, bottom, right = self.selection_bounds
        cells = []
        for r in range(top, bottom + 1):
            for c in range(left, right + 1):
                if self.pixels[r][c] is not None:
                    cells.append((r, c))
        return cells

    def nearest_palette256_index(self, rgb):
        best_idx = 0
        best_dist = None
        tr, tg, tb = rgb
        for i, color in enumerate(self.palette256):
            r, g, b = hex_to_rgb(color)
            dist = (r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_idx = i
        return best_idx

    def build_tonal_palette_indices(self, target_rgb=None):
        indices = []
        if target_rgb is None:
            for i in range(32):
                v = int(round((255 * i) / 31))
                indices.append(self.nearest_palette256_index((v, v, v)))
            return indices
        tr, tg, tb = target_rgb
        for i in range(32):
            scale = i / 31.0
            rgb = (int(round(tr * scale)), int(round(tg * scale)), int(round(tb * scale)))
            indices.append(self.nearest_palette256_index(rgb))
        return indices

    def get_slot_luminance(self, slot, palette_colors=None):
        colors = palette_colors or self.get_palette32()
        r, g, b = hex_to_rgb(colors[slot])
        return int(round(0.299 * r + 0.587 * g + 0.114 * b))

    def remap_active_pixels_by_luminance(self, source_palette=None):
        cells = self.get_active_cells()
        if not cells:
            return 0
        for r, c in cells:
            lum = self.get_slot_luminance(self.pixels[r][c], source_palette)
            self.pixels[r][c] = clamp(int(round((lum / 255.0) * 31)), 0, 31)
        return len(cells)

    def convert_to_grayscale32(self):
        self.push_undo_state("gri")
        old_palette = self.get_palette32()
        self.project["palette32_indices"] = self.build_tonal_palette_indices()
        changed = self.remap_active_pixels_by_luminance(old_palette)
        self.refresh_palette_buttons()
        self.redraw_canvas()
        self.update_data_text()
        self.save_project_json()
        self.set_status(f"32 gri skala uygulandı ({changed} piksel)")

    def get_selected_transform_rgb(self):
        value = self.transform_color_var.get().strip()
        if value == "Gri Skala":
            return None
        match = re.search(r"Slot\s+(\d+)", value)
        if not match:
            return None
        slot = clamp(int(match.group(1)), 0, 31)
        return hex_to_rgb(self.get_default_palette32()[slot])

    def convert_to_selected_tone(self):
        target_rgb = self.get_selected_transform_rgb()
        if target_rgb is None:
            self.convert_to_grayscale32()
            return
        self.push_undo_state("ton")
        old_palette = self.get_palette32()
        self.project["palette32_indices"] = self.build_tonal_palette_indices(target_rgb)
        changed = self.remap_active_pixels_by_luminance(old_palette)
        self.refresh_palette_buttons()
        self.redraw_canvas()
        self.update_data_text()
        self.save_project_json()
        self.set_status(f"Seçili renge göre 32 ton rampası uygulandı ({changed} piksel)")

    def nearest_palette32_slot(self, rgb):
        best_slot = 0
        best_dist = None
        colors = self.get_palette32()
        tr, tg, tb = rgb
        for slot, color in enumerate(colors):
            r, g, b = hex_to_rgb(color)
            dist = (r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_slot = slot
        return best_slot

    def snapshot_state(self):
        return {
            "pixels": [row[:] for row in self.pixels],
            "palette32_indices": list(self.project.get("palette32_indices", list(range(32)))),
            "selection_bounds": None if self.selection_bounds is None else tuple(self.selection_bounds),
        }

    def restore_state(self, state):
        self.pixels = [row[:] for row in state.get("pixels", self.pixels)]
        self.project["palette32_indices"] = list(state.get("palette32_indices", self.project.get("palette32_indices", list(range(32)))))
        sel = state.get("selection_bounds")
        self.selection_bounds = None if sel is None else tuple(sel)
        self.refresh_palette_buttons()
        self.redraw_canvas()
        self.update_data_text()

    def push_undo_state(self, _reason=""):
        self.undo_stack.append(self.snapshot_state())
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo_action(self):
        if not self.undo_stack:
            self.set_status("Geri al: kayıt yok")
            return
        self.redo_stack.append(self.snapshot_state())
        self.restore_state(self.undo_stack.pop())
        self.save_project_json()
        self.set_status("Geri alındı")

    def redo_action(self):
        if not self.redo_stack:
            self.set_status("İleri al: kayıt yok")
            return
        self.undo_stack.append(self.snapshot_state())
        self.restore_state(self.redo_stack.pop())
        self.save_project_json()
        self.set_status("İleri alındı")

    def quantize_to_current_palette32(self):
        self.push_undo_state("quantize32")
        cells = self.get_active_cells()
        if not cells:
            return
        palette = self.get_palette32()
        for r, c in cells:
            rgb = hex_to_rgb(palette[self.pixels[r][c]])
            self.pixels[r][c] = self.nearest_palette32_slot(rgb)
        self.redraw_canvas()
        self.update_data_text()
        self.save_project_json()
        self.set_status(f"Normal 32 palete indirildi ({len(cells)} piksel)")

    def reset_palette_default(self):
        self.push_undo_state("palet_reset")
        old_palette = self.get_palette32()
        self.project["palette32_indices"] = list(range(32))
        changed = self.remap_active_pixels_by_luminance(old_palette)
        self.refresh_palette_buttons()
        self.redraw_canvas()
        self.update_data_text()
        self.save_project_json()
        self.set_status(f"Palet normal 32'ye döndü ({changed} piksel)")

    def invert_active_colors(self):
        self.push_undo_state("invert")
        cells = self.get_active_cells()
        if not cells:
            return
        palette = self.get_palette32()
        for r, c in cells:
            rr, gg, bb = hex_to_rgb(palette[self.pixels[r][c]])
            inverted = (255 - rr, 255 - gg, 255 - bb)
            self.pixels[r][c] = self.nearest_palette32_slot(inverted)
        self.redraw_canvas()
        self.update_data_text()
        self.save_project_json()
        self.set_status(f"Renkler invert edildi ({len(cells)} piksel)")

    def paint_cell_with_brush(self, r, c, color_slot):
        self.on_brush_size_changed()
        start = -(self.brush_size // 2)
        for dr in range(start, start + self.brush_size):
            for dc in range(start, start + self.brush_size):
                rr = r + dr
                cc = c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    self.pixels[rr][cc] = color_slot
                    self.redraw_pixel(rr, cc)

    def paint(self, event, color_slot):
        rc = self.event_to_cell(event)
        if rc is None:
            return
        r, c = rc
        self.paint_cell_with_brush(r, c, color_slot)
        self.update_data_text()

    def _set_pixel(self, r, c, color_slot):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.pixels[r][c] = color_slot

    def _line_points(self, r0, c0, r1, c1):
        points = []
        x0, y0 = c0, r0
        x1, y1 = c1, r1
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            points.append((y0, x0))
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return points

    def _stamp_brush(self, r, c, color_slot, size):
        start = -(size // 2)
        for dr in range(start, start + size):
            for dc in range(start, start + size):
                self._set_pixel(r + dr, c + dc, color_slot)

    def draw_line(self, r0, c0, r1, c1, color_slot, size):
        for rr, cc in self._line_points(r0, c0, r1, c1):
            self._stamp_brush(rr, cc, color_slot, size)

    def draw_rectangle(self, r0, c0, r1, c1, color_slot, size):
        top = min(r0, r1)
        bottom = max(r0, r1)
        left = min(c0, c1)
        right = max(c0, c1)
        self.draw_line(top, left, top, right, color_slot, size)
        self.draw_line(bottom, left, bottom, right, color_slot, size)
        self.draw_line(top, left, bottom, left, color_slot, size)
        self.draw_line(top, right, bottom, right, color_slot, size)

    def draw_ellipse(self, r0, c0, r1, c1, color_slot, size):
        top = min(r0, r1)
        bottom = max(r0, r1)
        left = min(c0, c1)
        right = max(c0, c1)
        cx = (left + right) / 2.0
        cy = (top + bottom) / 2.0
        rx = max((right - left) / 2.0, 0.5)
        ry = max((bottom - top) / 2.0, 0.5)
        steps = max(24, int((rx + ry) * 8))
        for i in range(steps + 1):
            t = (2.0 * math.pi * i) / steps
            cc = int(round(cx + rx * math.cos(t)))
            rr = int(round(cy + ry * math.sin(t)))
            self._stamp_brush(rr, cc, color_slot, size)

    def draw_triangle(self, r0, c0, r1, c1, color_slot, size):
        top = min(r0, r1)
        bottom = max(r0, r1)
        left = min(c0, c1)
        right = max(c0, c1)
        apex_c = (left + right) // 2
        p1 = (top, apex_c)
        p2 = (bottom, left)
        p3 = (bottom, right)
        self.draw_line(p1[0], p1[1], p2[0], p2[1], color_slot, size)
        self.draw_line(p2[0], p2[1], p3[0], p3[1], color_slot, size)
        self.draw_line(p3[0], p3[1], p1[0], p1[1], color_slot, size)

    def flood_fill(self, r, c, color_slot):
        target = self.pixels[r][c]
        if target == color_slot:
            return
        stack = [(r, c)]
        while stack:
            rr, cc = stack.pop()
            if not (0 <= rr < self.rows and 0 <= cc < self.cols):
                continue
            if self.pixels[rr][cc] != target:
                continue
            self.pixels[rr][cc] = color_slot
            stack.append((rr - 1, cc))
            stack.append((rr + 1, cc))
            stack.append((rr, cc - 1))
            stack.append((rr, cc + 1))
        self.redraw_canvas()
        self.update_data_text()

    def draw_shape_preview(self, r1, c1):
        if self.shape_start is None:
            return
        r0, c0 = self.shape_start
        x0 = c0 * self.pixel_size
        y0 = r0 * self.pixel_size
        x1 = (c1 + 1) * self.pixel_size
        y1 = (r1 + 1) * self.pixel_size
        self.canvas.delete("shape_preview")
        tool = self.active_tool_var.get()
        if tool == "dikdortgen":
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="#ecf0f1", width=2, dash=(4, 2), tags="shape_preview")
        elif tool == "cember":
            self.canvas.create_oval(x0, y0, x1, y1, outline="#ecf0f1", width=2, dash=(4, 2), tags="shape_preview")
        elif tool == "ucgen":
            left = min(x0, x1)
            right = max(x0, x1)
            top = min(y0, y1)
            bottom = max(y0, y1)
            self.canvas.create_polygon(
                (left + right) / 2,
                top,
                left,
                bottom,
                right,
                bottom,
                outline="#ecf0f1",
                fill="",
                width=2,
                dash=(4, 2),
                tags="shape_preview",
            )
        elif tool == "cizgi":
            cx0 = x0 + (self.pixel_size // 2)
            cy0 = y0 + (self.pixel_size // 2)
            cx1 = x1 - (self.pixel_size // 2)
            cy1 = y1 - (self.pixel_size // 2)
            self.canvas.create_line(cx0, cy0, cx1, cy1, fill="#ecf0f1", width=2, dash=(4, 2), tags="shape_preview")

    def redraw_pixel(self, r, c):
        color = "#222" if self.pixels[r][c] is None else self.get_palette32()[self.pixels[r][c]]
        x1, y1 = c * self.pixel_size, r * self.pixel_size
        x2, y2 = x1 + self.pixel_size, y1 + self.pixel_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333")

    def redraw_canvas(self):
        self.canvas.delete("all")
        self.canvas.config(width=self.cols * self.pixel_size, height=self.rows * self.pixel_size)
        for r in range(self.rows):
            for c in range(self.cols):
                self.redraw_pixel(r, c)
        self.draw_selection_overlay()

    def pack_bitmap_bytes(self):
        out = []
        for r in range(self.rows):
            for b in range(self.bytes_per_row):
                val = 0
                for bit in range(8):
                    c = b * 8 + bit
                    if c < self.cols and self.pixels[r][c] is not None:
                        val |= (1 << (7 - bit))
                out.append(val)
        return out

    def unpack_bitmap_bytes(self, data):
        need = self.rows * self.bytes_per_row
        data = (data + [0] * need)[:need]
        i = 0
        for r in range(self.rows):
            for b in range(self.bytes_per_row):
                val = data[i]
                i += 1
                for bit in range(8):
                    c = b * 8 + bit
                    if c < self.cols and not (val & (1 << (7 - bit))):
                        self.pixels[r][c] = None

    def flat_color_values(self):
        vals = []
        for r in range(self.rows):
            for c in range(self.cols):
                vals.append(0 if self.pixels[r][c] is None else int(self.pixels[r][c]))
        return vals

    def apply_flat_color_values(self, vals):
        i = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.pixels[r][c] is None:
                    i += 1
                    continue
                self.pixels[r][c] = clamp(int(vals[i]), 0, 31)
                i += 1

    def update_data_text(self):
        bitmap = self.pack_bitmap_bytes()
        colors5 = pack_5bit(self.flat_color_values())
        c64_bitmap = bytes_to_data_lines("BITMAP DATA", bitmap, line_len=self.bytes_per_row)
        c64_colors = bytes_to_data_lines("COLOR5 DATA", colors5, line_len=16)

        info = [
            f"; Boyut: {self.cols}x{self.rows} px, satir-byte: {self.bytes_per_row}",
            f"; 32'lik palette indexleri: {self.project['palette32_indices']}",
            "; C64-benzeri: bitmap + 5bit color stream",
            "",
            c64_bitmap,
            "",
            c64_colors,
        ]
        self.data_text.delete("1.0", tk.END)
        self.data_text.insert(tk.END, "\n".join(info))

    def draw_from_data(self):
        all_bytes = parse_hex_bytes(self.data_text.get("1.0", tk.END))
        bitmap_len = self.rows * self.bytes_per_row
        bitmap = all_bytes[:bitmap_len]
        color_stream = all_bytes[bitmap_len:]

        self.init_pixels()
        self.unpack_bitmap_bytes(bitmap)
        color_vals = unpack_5bit(color_stream, self.rows * self.cols)
        self.apply_flat_color_values(color_vals)

        self.redraw_canvas()
        self.update_data_text()

    def refresh_asset_list(self):
        self.asset_listbox.delete(0, tk.END)
        self.filtered_asset_indices = []
        self.refresh_category_filter_menu()
        for idx, asset in enumerate(self.project["assets"]):
            if not self._asset_matches_filter(asset):
                continue
            w = int(asset.get("width", 0))
            h = int(asset.get("height", 0))
            name = asset.get("name", "isimsiz")
            category = asset.get("category", "genel")
            mapped = asset.get("mapped_game_asset", "")
            mapped_tag = f" -> {mapped}" if mapped else ""
            self.asset_listbox.insert(tk.END, f"[{category}] {name} ({w}x{h}){mapped_tag}")
            row = self.asset_listbox.size() - 1
            self.asset_listbox.itemconfig(row, bg=self.category_display_color(category), fg="#ecf0f1")
            self.filtered_asset_indices.append(idx)
        self.update_thumbnail_preview()

    def _decode_asset_to_pixels(self, asset):
        w = int(asset.get("width", 0))
        h = int(asset.get("height", 0))
        if w <= 0 or h <= 0:
            return 0, 0, []

        bytes_per_row = (w + 7) // 8
        bitmap = parse_hex_bytes(asset.get("bitmap_hex", ""))
        need = h * bytes_per_row
        bitmap = (bitmap + [0] * need)[:need]
        colors = parse_hex_bytes(asset.get("color5_hex", ""))
        color_vals = unpack_5bit(colors, w * h)

        pixels = [[None for _ in range(w)] for _ in range(h)]
        i = 0
        for r in range(h):
            for b in range(bytes_per_row):
                val = bitmap[i]
                i += 1
                for bit in range(8):
                    c = b * 8 + bit
                    if c >= w:
                        continue
                    if val & (1 << (7 - bit)):
                        pixels[r][c] = clamp(int(color_vals[r * w + c]), 0, 31)
        return w, h, pixels

    def update_thumbnail_preview(self):
        self.thumb_canvas.delete("all")
        self.thumb_canvas.create_text(90, 60, text="Seçim yok", fill="#7f8c8d")
        if self.selected_asset_index is None:
            return
        asset = self.project["assets"][self.selected_asset_index]
        w, h, pixels = self._decode_asset_to_pixels(asset)
        if w <= 0 or h <= 0:
            self.thumb_canvas.delete("all")
            self.thumb_canvas.create_text(90, 60, text="Boş varlık", fill="#7f8c8d")
            return

        self.thumb_canvas.delete("all")
        cell = max(1, min(8, int(min(160 / max(w, 1), 100 / max(h, 1)))))
        ox = (180 - (w * cell)) // 2
        oy = (120 - (h * cell)) // 2
        p32 = self.get_palette32()
        for r in range(h):
            for c in range(w):
                slot = pixels[r][c]
                fill = "#1b1b1b" if slot is None else p32[slot]
                x1 = ox + c * cell
                y1 = oy + r * cell
                x2 = x1 + cell
                y2 = y1 + cell
                self.thumb_canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#101820")
        self.thumb_canvas.create_text(4, 4, anchor="nw", text=f"{w}x{h}", fill="#dfe6e9")

    def on_asset_selected(self, _evt=None):
        sel = self.asset_listbox.curselection()
        if not sel:
            self.selected_asset_index = None
            self.asset_info_label.config(text="Seçili parça yok")
            return
        idx = self.filtered_asset_indices[sel[0]]
        self.selected_asset_index = idx
        asset = self.project["assets"][idx]
        self.asset_name_var.set(asset.get("name", ""))
        self.asset_category_var.set(asset.get("category", "genel"))
        self.asset_purpose_var.set(asset.get("purpose", ""))
        self.asset_usage_var.set(asset.get("usage", ""))
        self.asset_mapped_var.set(asset.get("mapped_game_asset", ""))
        self.asset_info_label.config(
            text=(
                f"Ad: {asset.get('name', '')}\n"
                f"Kategori: {asset.get('category', 'genel')}\n"
                f"Amaç: {asset.get('purpose', '')}\n"
                f"Kullanım: {asset.get('usage', '')}\n"
                f"Oyun Eşleşmesi: {asset.get('mapped_game_asset', '')}\n"
                f"Boyut: {asset.get('width', 0)}x{asset.get('height', 0)}"
            )
        )
        # Yeni varlığa geçerken grid seçilen varlığın verisiyle (boşsa temiz) açılır.
        self.load_selected_asset_to_grid(save=False)
        self.update_thumbnail_preview()

    def new_asset(self):
        name = simpledialog.askstring("Yeni Parça", "Parça adı:")
        if not name:
            return
        w = simpledialog.askinteger("Genişlik", "Piksel genişliği:", minvalue=1, maxvalue=256)
        h = simpledialog.askinteger("Yükseklik", "Piksel yüksekliği:", minvalue=1, maxvalue=128)
        if w is None or h is None:
            return

        asset = self.default_asset(name=name, width=w, height=h)
        self.project["assets"].append(asset)
        self.refresh_asset_list()
        if self.filtered_asset_indices:
            self.asset_listbox.selection_clear(0, tk.END)
            self.asset_listbox.selection_set(len(self.filtered_asset_indices) - 1)
        self.on_asset_selected()
        self.save_project_json()

    def delete_asset(self):
        if self.selected_asset_index is None:
            return
        if not messagebox.askyesno("Sil", "Seçili parça silinsin mi?"):
            return
        self.project["assets"].pop(self.selected_asset_index)
        self.selected_asset_index = None
        self.refresh_asset_list()
        self.asset_info_label.config(text="Seçili parça yok")
        self.update_thumbnail_preview()
        self.save_project_json()

    def save_grid_to_selected_asset(self, notify=True):
        if self.selected_asset_index is None:
            messagebox.showinfo("Bilgi", "Önce soldan bir parça seçin.")
            return

        asset = self.project["assets"][self.selected_asset_index]
        asset["name"] = self.asset_name_var.get().strip() or asset.get("name", "isimsiz")
        asset["category"] = self.asset_category_var.get().strip() or "genel"
        asset["purpose"] = self.asset_purpose_var.get().strip()
        asset["usage"] = self.asset_usage_var.get().strip()
        asset["mapped_game_asset"] = self.asset_mapped_var.get().strip()
        asset["width"] = int(self.cols)
        asset["height"] = int(self.rows)
        asset["bitmap_hex"] = "".join(f"{b:02X}" for b in self.pack_bitmap_bytes())
        asset["color5_hex"] = "".join(f"{b:02X}" for b in pack_5bit(self.flat_color_values()))
        asset["source"] = "halidesennakismod"

        self.refresh_asset_list()
        self.on_asset_selected()
        self.update_thumbnail_preview()
        self.save_project_json()
        if notify:
            messagebox.showinfo("Kaydedildi", "Grid verisi seçili parçaya yazıldı.")

    def on_sync_game_assets(self):
        added = self.sync_game_assets_to_project(save=True)
        self.refresh_asset_list()
        if added:
            messagebox.showinfo("Senkron", f"{added} yeni oyun varlığı eklendi.")
        else:
            messagebox.showinfo("Senkron", "Yeni varlık bulunmadı, mevcut kayıtlar güncel.")

    def load_selected_asset_to_grid(self, save=True):
        if self.selected_asset_index is None:
            return
        asset = self.project["assets"][self.selected_asset_index]
        w = int(asset.get("width", self.cols))
        h = int(asset.get("height", self.rows))
        self.set_grid_size(h, w, keep_content=False)

        self.row_var.set(self.rows)
        self.col_var.set(self.cols)

        self.init_pixels()
        bitmap = parse_hex_bytes(asset.get("bitmap_hex", ""))
        colors = parse_hex_bytes(asset.get("color5_hex", ""))
        self.unpack_bitmap_bytes(bitmap)
        self.apply_flat_color_values(unpack_5bit(colors, self.rows * self.cols))

        self.redraw_canvas()
        self.update_data_text()
        self.update_thumbnail_preview()
        if save:
            self.save_project_json()

    def single_asset_to_text(self, asset):
        w = int(asset.get("width", 0))
        h = int(asset.get("height", 0))
        bytes_per_row = (w + 7) // 8 if w > 0 else 0
        bitmap = parse_hex_bytes(asset.get("bitmap_hex", ""))
        color5 = parse_hex_bytes(asset.get("color5_hex", ""))
        lines = [
            f"; name={asset.get('name', 'isimsiz')}",
            f"; category={asset.get('category', 'genel')}",
            f"; mapped_game_asset={asset.get('mapped_game_asset', '')}",
            f"; size={w}x{h}",
            f"; palette32_indices={self.project.get('palette32_indices', list(range(32)))}",
            "",
        ]
        lines.append(bytes_to_data_lines("BITMAP DATA", bitmap, line_len=max(1, bytes_per_row)))
        lines.append("")
        lines.append(bytes_to_data_lines("COLOR5 DATA", color5, line_len=16))
        return "\n".join(lines)

    def save_single_asset_file(self):
        if self.selected_asset_index is None:
            messagebox.showinfo("Bilgi", "Önce bir varlık seçin.")
            return
        self.save_grid_to_selected_asset(notify=False)
        asset = self.project["assets"][self.selected_asset_index]
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Text", "*.txt"), ("All", "*.*")],
            initialfile=f"{asset.get('name', 'asset')}.json",
        )
        if not path:
            return
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".json":
                payload = {
                    "asset_format": "halidesen_single_asset_v1",
                    "palette32_indices": list(self.project.get("palette32_indices", list(range(32)))),
                    "asset": dict(asset),
                }
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(payload, f, indent=2, ensure_ascii=False)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.single_asset_to_text(asset))
            messagebox.showinfo("Kaydedildi", "Seçili varlık dosyaya kaydedildi.")
        except Exception as exc:
            messagebox.showerror("Hata", f"Seçili varlık kaydedilemedi:\n{exc}")

    def load_single_asset_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("Text", "*.txt"), ("All", "*.*")])
        if not path:
            return
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".json":
                with open(path, "r", encoding="utf-8") as f:
                    obj = json.load(f)
                asset_obj = None
                palette = None
                if isinstance(obj, dict) and "asset" in obj and isinstance(obj.get("asset"), dict):
                    asset_obj = obj["asset"]
                    palette = obj.get("palette32_indices")
                elif isinstance(obj, dict) and "bitmap_hex" in obj and "color5_hex" in obj:
                    asset_obj = obj
                    palette = obj.get("palette32_indices")
                if asset_obj is None:
                    raise ValueError("JSON tek varlık formatı değil.")
                temp_asset = self.default_asset("json_asset", asset_obj.get("width", self.cols), asset_obj.get("height", self.rows))
                temp_asset.update(asset_obj)
                if isinstance(palette, list) and len(palette) == 32:
                    self.project["palette32_indices"] = [clamp(int(x), 0, 255) for x in palette]
                self.project["assets"].append(temp_asset)
                self.refresh_asset_list()
                self.asset_listbox.selection_clear(0, tk.END)
                if self.filtered_asset_indices:
                    self.asset_listbox.selection_set(len(self.filtered_asset_indices) - 1)
                self.on_asset_selected()
                self.save_project_json()
                messagebox.showinfo("Açıldı", "Tek varlık JSON içe aktarıldı.")
                return

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            size_match = re.search(r"size\s*=\s*(\d+)x(\d+)", text, re.IGNORECASE)
            if not size_match:
                raise ValueError("TXT içinde size=WxH satırı bulunamadı.")
            w = clamp(int(size_match.group(1)), 1, 256)
            h = clamp(int(size_match.group(2)), 1, 128)
            all_bytes = parse_hex_bytes(text)
            bytes_per_row = (w + 7) // 8
            bitmap_len = h * bytes_per_row
            bitmap = all_bytes[:bitmap_len]
            color5 = all_bytes[bitmap_len:]
            name_match = re.search(r"name\s*=\s*([^\n\r;]+)", text, re.IGNORECASE)
            asset_name = name_match.group(1).strip() if name_match else "txt_asset"
            temp_asset = self.default_asset(asset_name, w, h)
            temp_asset["bitmap_hex"] = "".join(f"{b:02X}" for b in bitmap)
            temp_asset["color5_hex"] = "".join(f"{b:02X}" for b in color5)
            self.project["assets"].append(temp_asset)
            self.refresh_asset_list()
            self.asset_listbox.selection_clear(0, tk.END)
            if self.filtered_asset_indices:
                self.asset_listbox.selection_set(len(self.filtered_asset_indices) - 1)
            self.on_asset_selected()
            self.save_project_json()
            messagebox.showinfo("Açıldı", "Tek varlık TXT içe aktarıldı.")
        except Exception as exc:
            messagebox.showerror("Hata", f"Tek varlık açılamadı:\n{exc}")

    def load_data_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("Text", "*.txt *.asm *.inc"), ("All", "*.*")])
        if not path:
            return
        ext = os.path.splitext(path)[1].lower()
        if ext == ".json":
            try:
                with open(path, "r", encoding="utf-8") as f:
                    obj = json.load(f)
                if isinstance(obj, dict) and "assets" in obj:
                    self.project = obj
                    self.ensure_project_schema()
                    self.sync_game_assets_to_project(save=False)
                    self.rows = int(self.project["grid"]["rows"])
                    self.cols = int(self.project["grid"]["cols"])
                    self.pixel_size = int(self.project["sizes"]["pixel_size"])
                    self.row_var.set(self.rows)
                    self.col_var.set(self.cols)
                    self.pixel_size_var.set(self.pixel_size)
                    self.emoji_size_var.set(int(self.project["sizes"]["emoji_size"]))
                    self.small_char_size_var.set(int(self.project["sizes"]["small_char_size"]))
                    self.tool_icon_size_var.set(int(self.project["sizes"]["tool_icon_size"]))
                    self.init_pixels()
                    self.refresh_asset_list()
                    self.redraw_canvas()
                    self.update_data_text()
                    self.update_size_preview()
                    self.save_project_json()
                    messagebox.showinfo("Açıldı", "JSON proje ve tüm varlık grafikleri yüklendi.")
                    return
                if isinstance(obj, dict) and "bitmap_hex" in obj and "color5_hex" in obj:
                    temp_asset = self.default_asset("json_asset", obj.get("width", self.cols), obj.get("height", self.rows))
                    temp_asset.update(obj)
                    self.project["assets"].append(temp_asset)
                    self.refresh_asset_list()
                    self.asset_listbox.selection_clear(0, tk.END)
                    if self.filtered_asset_indices:
                        self.asset_listbox.selection_set(len(self.filtered_asset_indices) - 1)
                    self.on_asset_selected()
                    self.save_project_json()
                    messagebox.showinfo("Açıldı", "JSON tek varlık yüklendi ve listeye eklendi.")
                    return
                raise ValueError("JSON içeriği desteklenen formatta değil.")
            except Exception as exc:
                messagebox.showerror("Hata", f"JSON açılamadı:\n{exc}")
                return

        with open(path, "r", encoding="utf-8") as f:
            self.data_text.delete("1.0", tk.END)
            self.data_text.insert(tk.END, f.read())
        self.draw_from_data()

    def save_data_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt"), ("JSON", "*.json"), ("All", "*.*")])
        if not path:
            return
        ext = os.path.splitext(path)[1].lower()
        if ext == ".json":
            try:
                # JSON kaydında sadece data text değil, tum varliklarin grafikleri de yazilir.
                self.project["grid"]["rows"] = int(self.rows)
                self.project["grid"]["cols"] = int(self.cols)
                self.project["sizes"]["pixel_size"] = int(self.pixel_size)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self.project, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Kaydedildi", "JSON proje ve tüm varlık grafikleri kaydedildi.")
                return
            except Exception as exc:
                messagebox.showerror("Hata", f"JSON kaydedilemedi:\n{exc}")
                return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.data_text.get("1.0", tk.END))

    def open_narrator(self):
        NarratorWindow(self.root, self.pixels, self.rows, self.cols, self.get_palette32())


class NarratorWindow(tk.Toplevel):
    def __init__(self, parent, pixels, rows, cols, palette32):
        super().__init__(parent)
        self.title("Kağıda Aktarma Rehberi")
        self.pixels = pixels
        self.rows = rows
        self.cols = cols
        self.palette32 = palette32
        self.curr_r = 0
        self.curr_c = 0

        self.setup_ui()
        self.update_display()
        self.bind("<Right>", lambda _e: self.next_bit())
        self.bind("<Left>", lambda _e: self.prev_bit())

    def setup_ui(self):
        self.info_label = tk.Label(self, text="", font=("Arial", 12, "bold"), pady=12, justify="left")
        self.info_label.pack()

        self.bit_status = tk.Label(self, text="", font=("Courier", 20), bg="black", fg="yellow", width=26, pady=14)
        self.bit_status.pack()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="<< GERİ", command=self.prev_bit, width=12).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="İLERİ >>", command=self.next_bit, width=12).pack(side=tk.LEFT, padx=4)

        tk.Label(self, text="Klavye: Sağ/Sol ok tuşları", fg="gray").pack()

    def update_display(self):
        slot = self.pixels[self.curr_r][self.curr_c]
        if slot is None:
            state = "BOŞ"
            color = "gray"
            slot_info = "-"
        else:
            state = "DOLU"
            color = self.palette32[slot]
            slot_info = f"{slot} ({self.palette32[slot]})"

        byte_no = (self.curr_c // 8) + 1
        bit_no = 7 - (self.curr_c % 8)
        self.info_label.config(
            text=(
                f"Satır: {self.curr_r + 1} / {self.rows}\n"
                f"Sütun: {self.curr_c + 1} / {self.cols}\n"
                f"Byte: {byte_no}, Bit: {bit_no}\n"
                f"Renk Slotu: {slot_info}"
            )
        )
        self.bit_status.config(text=state, fg=color)

    def next_bit(self):
        self.curr_c += 1
        if self.curr_c >= self.cols:
            self.curr_c = 0
            self.curr_r += 1
        if self.curr_r >= self.rows:
            self.curr_r = 0
            messagebox.showinfo("Bitti", "Desen sonuna geldiniz!")
        self.update_display()

    def prev_bit(self):
        self.curr_c -= 1
        if self.curr_c < 0:
            self.curr_c = self.cols - 1
            self.curr_r -= 1
        if self.curr_r < 0:
            self.curr_r = self.rows - 1
        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = C64MasterEditor(root)
    root.mainloop()