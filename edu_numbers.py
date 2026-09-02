#!/usr/bin/env python3
"""
אפליקציית לימוד מספרים 1-10 לגן הילדים - עם אנימציות

Educational app: learning numbers 1-10 with animations (Tkinter)

Run:  python3 edu_numbers.py   (after: sudo dnf install python3-tkinter)
"""

import math
import random
import tkinter as tk
from tkinter import font as tkfont
from bidi.algorithm import get_display

_rtl = get_display

# ---------------------------------------------------------------- data ----
HEBREW_NAMES = [
    "", _rtl("אחת"), _rtl("שתיים"), _rtl("שלוש"), _rtl("ארבע"), _rtl("חמש"),
    _rtl("שש"), _rtl("שבע"), _rtl("שמונה"), _rtl("תשע"), _rtl("עשר"),
]

OBJECT_COLORS = [
    "#FFD54F", "#FF8A80", "#81C784", "#81D4FA",
    "#CE93D8", "#FFAB91", "#A5D6A7", "#F48FB1",
]

PALETTE = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
           "#FFEAA7", "#DDA0DD", "#98D8C8", "#F67280"]

MAX_NUM = 10


# ------------------------------------------------------------- geometry ---
def balanced_grid(n):
    if n <= 4:
        return (1, n)
    if n <= 6:
        return (2, 3)
    if n == 8:
        return (2, 4)
    if n == 9:
        return (3, 3)
    if n == 10:
        return (2, 5)
    return (2, (n + 1) // 2)


# ---------------------------------------------------------- star shape ----
def draw_star(canvas, cx, cy, r, fill, outline="", tag=""):
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append(cx + rad * math.cos(ang))
        pts.append(cy - rad * math.sin(ang))
    return canvas.create_polygon(pts, fill=fill, outline=outline,
                                 width=2, tags=tag, smooth=False)


class NumberApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(_rtl("לומדים מספרים 1–10"))
        self.configure(bg="#FDF6E3")

        self._normalize_dpi()
        self._setup_fonts()
        self._setup_bindings()

        self.container = tk.Frame(self, bg="#FDF6E3")
        self.container.pack(fill="both", expand=True)

        self.show_home()

    # ------------------------------------------------------------- setup --
    def _normalize_dpi(self):
        try:
            self.tk.call("tk", "scaling", 1.5)
        except Exception:
            pass

    def _setup_fonts(self):
        self.big_font = tkfont.Font(family="DejaVu Sans", size=120, weight="bold")
        self.title_font = tkfont.Font(family="DejaVu Sans", size=46, weight="bold")
        self.medium_font = tkfont.Font(family="DejaVu Sans", size=34, weight="bold")
        self.small_font = tkfont.Font(family="DejaVu Sans", size=24, weight="bold")
        self.btn_font = tkfont.Font(family="DejaVu Sans", size=24, weight="bold")

    def _setup_bindings(self):
        self.bind("<Escape>", lambda e: self.destroy())

    # --------------------------------------------------------- clear scr --
    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ------------------------------------------------------------ widgets --
    def make_button(self, parent, text, cmd, bg, fg="white", size=None):
        font = size or self.btn_font
        return tk.Button(parent, text=text, command=cmd, font=font,
                         bg=bg, fg=fg, activebackground=bg,
                         activeforeground=fg, relief="flat", bd=0,
                         cursor="hand2", padx=20, pady=10)

    def header(self, title, subtitle=None):
        head = tk.Frame(self.container, bg="#FDF6E3")
        head.pack(fill="x", pady=(14, 2))
        tk.Label(head, text=title, font=self.title_font, bg="#FDF6E3",
                 fg="#5D4037").pack()
        if subtitle:
            tk.Label(head, text=subtitle, font=self.medium_font,
                     bg="#FDF6E3", fg="#8D6E63").pack()
        return head

    # ------------------------------------------------------------ home ----
    def show_home(self):
        self.clear()
        self.header(_rtl("🎈 לומדים מספרים 1–10 🎈"),
                    _rtl("בואו נשחק ולומדים ביחד!"))

        body = tk.Frame(self.container, bg="#FDF6E3")
        body.pack(expand=True)

        grid = tk.Frame(body, bg="#FDF6E3")
        grid.pack(pady=20)

        modes = [
            (0, 0, _rtl("לומדה"), "⭐", "#FF6B6B", self.show_learn),
            (0, 1, _rtl("ספירה"), "🔢", "#45B7D1", self.show_count),
            (1, 0, _rtl("זיהוי"), "❓", "#96CEB4", self.show_quiz),
            (1, 1, _rtl("כמות"), "📊", "#DDA0DD", self.show_quantity),
        ]
        for r, c, text, icon, color, cmd in modes:
            btn_frame = tk.Frame(grid, bg=color, padx=6, pady=6)
            btn_frame.grid(row=r, column=c, padx=15, pady=15)
            icon_lbl = tk.Label(btn_frame, text=icon, font=("DejaVu Sans", 48),
                                bg=color, fg="white")
            icon_lbl.pack(pady=(10, 0))
            btn_lbl = tk.Label(btn_frame, text=text, font=self.medium_font,
                               bg=color, fg="white")
            btn_lbl.pack(pady=(0, 10), padx=20)
            for w in (btn_frame, icon_lbl, btn_lbl):
                w.bind("<Button-1>", lambda e, cmd=cmd: cmd())
                w.config(cursor="hand2")

    # ------------------------------------------------- quantity quiz ----
    def show_quantity(self):
        self.clear()
        self.score = 0
        self.header(_rtl(" finde את הכמות!"), _rtl("לוחצים על הספרה המתאימה"))

        self.feedback = tk.Label(self.container, text="", font=self.medium_font,
                                 bg="#FDF6E3")
        self.feedback.pack(pady=8)

        self.canvas = tk.Canvas(self.container, bg="#FDF6E3", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=6)

        self.score_label = tk.Label(self.container, text=_rtl("נקודות: 0"),
                                    font=self.small_font, bg="#FDF6E3", fg="#5D4037")
        self.score_label.pack(pady=4)

        bar = tk.Frame(self.container, bg="#FDF6E3")
        bar.pack(fill="x", pady=8)
        self.make_button(bar, _rtl("שאלה חדשה"), self.new_quantity_question,
                         "#45B7D1").pack(side="left", padx=12)
        self.make_button(bar, "🏠", self.show_home, "#FFEAA7",
                         fg="#5D4037").pack(side="top")

        self.new_quantity_question()

    def new_quantity_question(self):
        self.feedback.config(text="")
        target = random.randint(1, MAX_NUM)
        others = random.sample([x for x in range(1, MAX_NUM + 1) if x != target], 2)
        options = [target] + others
        random.shuffle(options)
        self.q_target = target
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 300
        rows, cols = balanced_grid(target)
        cw, ch = w / (cols + 1), h / (rows + 1)
        r = min(cw, ch) * 0.28
        for i in range(target):
            row, col = divmod(i, cols)
            cx = cw * (col + 1 - ((cols - 1) / 2))
            cy = ch * (row + 1 + (0.3 if rows > 1 else 0.0))
            oid = draw_star(self.canvas, cx, cy, r, random.choice(OBJECT_COLORS),
                            tag="qobj")
            self.canvas.tag_bind(oid, "<Button-1>", lambda e: None)
        self.feedback.config(text=_rtl("כמה כוכבים רואים?"))
        self._q_target = target
        self._q_options = options
        self._place_quantity_options(w, h, target, options)

    def _place_quantity_options(self, w, h, target, options):
        self.canvas.delete("qopt")
        bar_y = h * 0.88
        n = len(options)
        cw = w / (n + 1)
        r = 44
        for i, val in enumerate(options):
            cx = cw * (i + 1 - ((n - 1) / 2))
            oid = self.canvas.create_oval(cx - r, bar_y - r, cx + r, bar_y + r,
                                          fill=random.choice(PALETTE),
                                          outline="", tags="qopt")
            self.canvas.create_text(cx, bar_y, text=str(val),
                                    font=self.medium_font, fill="white",
                                    tags="qopt")
            self.canvas.tag_bind(oid, "<Button-1>",
                                 lambda e, v=val: self._check_quantity(v))

    def _check_quantity(self, val):
        if val == self._q_target:
            self.score += 1
            self.feedback.config(text=_rtl("נכון! כל הכבוד!"), fg="#2E7D32")
            self.score_label.config(text=_rtl(f"נקודות: {self.score}"))
            self._confetti(self.canvas)
            self.canvas.after(800, self.new_quantity_question)
        else:
            self.feedback.config(text=_rtl("נסו שוב!"), fg="#E53935")

    # ---------------------------------------------------------- number line -
    def _make_number_line(self, parent):
        frame = tk.Frame(parent, bg="#FDF6E3")
        frame.pack(fill="x", side="bottom", pady=(4, 8))
        self._nl_labels = []
        for i in range(1, 11):
            lbl = tk.Label(frame, text=str(i), font=self.small_font,
                           bg="#FDF6E3", fg="#5D4037", width=3)
            lbl.pack(side="left", padx=2)
            lbl.bind("<Button-1>", lambda e, num=i: self._nl_click(num))
            self._nl_labels.append(lbl)
        return frame

    def _nl_click(self, num):
        pass

    def _nl_highlight(self, n):
        if not hasattr(self, "_nl_labels"):
            return
        for i, lbl in enumerate(self._nl_labels):
            if i + 1 == n:
                lbl.config(bg="#FF6B6B", fg="white",
                           font=tkfont.Font(family="DejaVu Sans", size=24, weight="bold"))
            else:
                lbl.config(bg="#FDF6E3", fg="#5D4037",
                           font=self.small_font)

    # ------------------------------------------------------- confetti ----
    def _confetti(self, canvas):
        gen = getattr(self, "_confetti_gen", 0) + 1
        self._confetti_gen = gen
        w = canvas.winfo_width() or 800
        h = canvas.winfo_height() or 500
        particles = []
        for _ in range(20):
            x = random.uniform(w * 0.2, w * 0.8)
            y = random.uniform(h * 0.1, h * 0.3)
            vx = random.uniform(-3, 3)
            vy = random.uniform(-6, -2)
            r = random.uniform(4, 9)
            color = random.choice(PALETTE)
            oid = canvas.create_oval(x - r, y - r, x + r, y + r,
                                     fill=color, outline="", tags="confetti")
            particles.append({"id": oid, "vx": vx, "vy": vy})
        self._confetti_particles = particles
        self._confetti_frame(canvas, gen)

    def _confetti_frame(self, canvas, gen):
        if gen != getattr(self, "_confetti_gen", 0):
            return
        h = canvas.winfo_height() or 500
        alive = []
        for p in self._confetti_particles:
            oid, vx, vy = p["id"], p["vx"], p["vy"]
            try:
                coords = canvas.coords(oid)
            except Exception:
                continue
            if not coords or coords[1] > h + 20:
                canvas.delete(oid)
                continue
            p["vy"] = vy + 0.3
            p["vx"] = vx * 0.99
            canvas.move(oid, p["vx"], p["vy"])
            alive.append(p)
        self._confetti_particles = alive
        if alive:
            canvas.after(30, self._confetti_frame, canvas, gen)
        else:
            canvas.delete("confetti")

    # --------------------------------------------------------- learn ------
    def show_learn(self):
        self.clear()
        self.quiz_num = 1
        self.learn_counted = 0

        head = tk.Frame(self.container, bg="#FDF6E3")
        head.pack(fill="x", pady=6)
        big = tk.Frame(head, bg="#FDF6E3")
        big.pack(expand=True)

        self.num_label = tk.Label(big, text="1", font=self.big_font,
                                  bg="#FDF6E3", fg="#FF6B6B")
        self.num_label.pack()

        self.name_label = tk.Label(big, text="",
                                   font=self.medium_font, bg="#FDF6E3",
                                   fg="#45B7D1")
        self.name_label.pack()

        self.canvas = tk.Canvas(self.container, bg="#FDF6E3",
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

        self._make_number_line(self.container)

        bar = tk.Frame(self.container, bg="#FDF6E3")
        bar.pack(fill="x", pady=10)
        self.prev_btn = self.make_button(bar, _rtl("◀ הקודם"), self.learn_prev, "#45B7D1")
        self.prev_btn.pack(side="left", padx=15)
        self.home_btn = self.make_button(bar, "🏠", self.show_home, "#FFEAA7",
                                         fg="#5D4037")
        self.home_btn.pack(side="top", padx=15)
        self.next_btn = self.make_button(bar, _rtl("הבא ▶"), self.learn_next, "#FF6B6B")
        self.next_btn.pack(side="right", padx=15)

        self.render_learn()

    def learn_next(self):
        if self.quiz_num < MAX_NUM:
            self.quiz_num += 1
            self.render_learn()

    def learn_prev(self):
        if self.quiz_num > 1:
            self.quiz_num -= 1
            self.render_learn()

    def render_learn(self):
        n = self.quiz_num
        self.learn_counted = 0
        self.num_label.config(text=str(n), fg=random.choice(PALETTE))
        self.name_label.config(text="")
        self.canvas.delete("all")
        self._nl_highlight(n)
        self._place_learn_objects(n)

    def _place_learn_objects(self, n):
        self.canvas.delete("obj")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 500
        rows, cols = balanced_grid(n)
        cw, ch = w / (cols + 1), h / (rows + 1)
        r = min(cw, ch) * 0.32
        self._learn_objects = []
        for i in range(n):
            row, col = divmod(i, cols)
            cx = cw * (col + 1 - ((cols - 1) / 2))
            cy = ch * (row + 1 + (0.3 if rows > 1 else 0.0))
            oid = draw_star(self.canvas, cx, cy, r, "#B0BEC5", tag="obj")
            self.canvas.tag_bind(oid, "<Button-1>", self._learn_click)
            self._learn_objects.append(oid)

    def _learn_click(self, event):
        oid = self.canvas.find_withtag("current")[0]
        if oid not in self._learn_objects:
            return
        if self.canvas.itemcget(oid, "fill") == "#B0BEC5":
            self.canvas.itemconfig(oid, fill=random.choice(OBJECT_COLORS))
            self.learn_counted += 1
            self.name_label.config(text=HEBREW_NAMES[self.learn_counted])
            if self.learn_counted == self.quiz_num:
                self._confetti(self.canvas)
                self.num_label.config(fg="#2E7D32")
                self.canvas.after(1200, lambda: self.num_label.config(
                    fg=random.choice(PALETTE)))

    # ---------------------------------------------------------- count -----
    def show_count(self):
        self.clear()
        self.quiz_num = 1
        self.counted = 0

        self.header(_rtl("ספירה! לוחצים על הכוכבים"))

        self.count_label = tk.Label(self.container, text="0", font=self.big_font,
                                    bg="#FDF6E3", fg="#45B7D1")
        self.count_label.pack()

        self.canvas = tk.Canvas(self.container, bg="#FDF6E3", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

        self._make_number_line(self.container)

        bar = tk.Frame(self.container, bg="#FDF6E3")
        bar.pack(fill="x", pady=10)
        self.make_button(bar, _rtl("חדש"), lambda: self.new_count_session(), "#45B7D1").pack(side="left", padx=15)
        self.make_button(bar, "🏠", self.show_home, "#FFEAA7", fg="#5D4037").pack(side="top")

        self.new_count_session()

    def new_count_session(self):
        self.quiz_num = random.randint(1, MAX_NUM)
        self.counted = 0
        self.count_label.config(text="0", fg="#45B7D1")
        self.canvas.delete("all")
        self._nl_highlight(self.quiz_num)
        self.count_objects = self.place_objects_count()
        for oid in self.count_objects:
            self.canvas.itemconfig(oid, state="normal")

    def place_objects_count(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 500
        rows, cols = balanced_grid(self.quiz_num)
        cw, ch = w / (cols + 1), h / (rows + 1)
        r = min(cw, ch) * 0.32
        ids = []
        for i in range(self.quiz_num):
            row, col = divmod(i, cols)
            cx = cw * (col + 1 - ((cols - 1) / 2))
            cy = ch * (row + 1 + (0.3 if rows > 1 else 0.0))
            oid = draw_star(self.canvas, cx, cy, r, "#B0BEC5", tag="cobj")
            self.canvas.tag_bind(oid, "<Button-1>", self._count_click)
            ids.append(oid)
        return ids

    def _count_click(self, event):
        oid = self.canvas.find_withtag("current")[0]
        if oid not in self.count_objects:
            return
        if self.canvas.itemcget(oid, "fill") == "#B0BEC5":
            self.canvas.itemconfig(oid, fill=random.choice(OBJECT_COLORS))
            self.counted += 1
            self.count_label.config(text=HEBREW_NAMES[self.counted])
            self._bounce(self.canvas, oid)
            if self.counted == self.quiz_num:
                self._confetti(self.canvas)
                self.count_label.config(text=_rtl("יופי!"), fg="#FF6B6B")
                self.canvas.after(1500, lambda: self.count_label.config(
                    text=str(self.quiz_num), fg="#45B7D1"))

    def celebrate(self):
        self._confetti(self.canvas)
        self.count_label.config(text=_rtl("יופי!"), fg="#FF6B6B")
        self.canvas.after(1500, lambda: self.count_label.config(
            text=str(self.quiz_num), fg="#45B7D1"))

    # ----------------------------------------------------------- quiz -----
    def show_quiz(self):
        self.clear()
        self.score = 0
        self.quiz_num = 1

        self.header(_rtl("מצא את המספר!"), _rtl("לוחצים על הספרה הנכונה"))

        self.feedback = tk.Label(self.container, text="", font=self.medium_font,
                                 bg="#FDF6E3")
        self.feedback.pack(pady=8)

        self.canvas = tk.Canvas(self.container, bg="#FDF6E3", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=6)

        self.score_label = tk.Label(self.container, text=_rtl("נקודות: 0"),
                                    font=self.small_font, bg="#FDF6E3", fg="#5D4037")
        self.score_label.pack(pady=4)

        bar = tk.Frame(self.container, bg="#FDF6E3")
        bar.pack(fill="x", pady=8)
        self.make_button(bar, _rtl("שאלה חדשה"), self.new_quiz, "#45B7D1").pack(side="left", padx=12)
        self.make_button(bar, "🏠", self.show_home, "#FFEAA7", fg="#5D4037").pack(side="top")

        self.new_quiz()

    def new_quiz(self):
        self.feedback.config(text="")
        target = random.randint(1, MAX_NUM)
        others = random.sample([x for x in range(1, MAX_NUM + 1) if x != target], 2)
        options = [target] + others
        random.shuffle(options)
        self.target = target
        self.options = options

        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 260
        n = len(options)
        cw = w / (n + 1)
        r = 70
        self.feedback.config(text=_rtl(f"איפה המספר {self.target}?"))

        for i, val in enumerate(options):
            cx = cw * (i + 1 - ((n - 1) / 2))
            cy = h / 2
            oid = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                          fill=random.choice(PALETTE),
                                          outline="", tags="qopt")
            self.canvas.create_text(cx, cy, text=str(val), font=self.medium_font,
                                    fill="white", tags="qopt")
            self.canvas.tag_bind(oid, "<Button-1>",
                                 lambda e, v=val: self.check_choice(v))

    def check_choice(self, val):
        if val == self.target:
            self.score += 1
            self.feedback.config(text=_rtl("נכון! כל הכבוד!"), fg="#2E7D32")
            self.score_label.config(text=_rtl(f"נקודות: {self.score}"))
            self._confetti(self.canvas)
            self.canvas.after(800, self.new_quiz)
        else:
            self.feedback.config(text=_rtl("נסו שוב!"), fg="#E53935")

    # ------------------------------------------------- math (חיבור/חיסור) --
    def show_math(self):
        self.clear()
        self.math_score = 0
        self.math_answered = False

        self.header(_rtl("חיבור וחיסור"),
                    _rtl("סופרים, פותרים ובוחרים את התשובה!"))

        self.math_op_label = tk.Label(self.container, text="",
                                      font=self.big_font, bg="#FDF6E3",
                                      fg="#7E57C2")
        self.math_op_label.pack(pady=8)

        self.math_feedback = tk.Label(self.container, text="",
                                      font=self.medium_font, bg="#FDF6E3")
        self.math_feedback.pack(pady=2)

        self.math_canvas = tk.Canvas(self.container, bg="#FDF6E3",
                                     highlightthickness=0)
        self.math_canvas.pack(fill="both", expand=True, padx=20, pady=6)

        self.math_answers = tk.Frame(self.container, bg="#FDF6E3")
        self.math_answers.pack(pady=8)

        self.math_score_label = tk.Label(self.container,
                                         text=_rtl("נקודות: 0"),
                                         font=self.small_font, bg="#FDF6E3",
                                         fg="#5D4037")
        self.math_score_label.pack(pady=2)

        bar = tk.Frame(self.container, bg="#FDF6E3")
        bar.pack(fill="x", pady=8)
        self.make_button(bar, _rtl("שאלה חדשה"), self.new_math_question,
                         "#45B7D1").pack(side="left", padx=12)
        self.make_button(bar, "🏠", self.show_home, "#FFEAA7",
                         fg="#5D4037").pack(side="top")

        self.new_math_question()

    def new_math_question(self):
        """יוצר תרגיל חיבור או חיסור פשוט עם תוצאה עד 10."""
        self.math_answered = False
        self.math_feedback.config(text="", fg="#5D4037")
        self.math_operation = random.choice(["+", "-"])

        if self.math_operation == "+":
            a = random.randint(1, 6)
            b = random.randint(1, 10 - a)
        else:
            a = random.randint(2, 8)
            b = random.randint(1, a - 1)

        self.math_a, self.math_b = a, b
        self.math_answer = a + b if self.math_operation == "+" else a - b

        plus = _rtl(f"{a}  +  {b}")
        minus = _rtl(f"{a}  -  {b}")
        self.math_op_label.config(
            text=plus if self.math_operation == "+" else minus,
            fg="#7E57C2")

        # אפשרויות תשובה (תמיד 3 אפשרויות שונות, כולל הנכונה)
        candidates = []
        for d in (-2, -1, 1, 2):
            v = self.math_answer + d
            if 0 <= v <= 10 and v != self.math_answer:
                candidates.append(v)
        candidates = list(dict.fromkeys(candidates))
        while len(candidates) < 2:
            v = random.randint(0, 10)
            if v != self.math_answer and v not in candidates:
                candidates.append(v)
        options = [self.math_answer] + random.sample(candidates, 2)
        random.shuffle(options)

        for w in self.math_answers.winfo_children():
            w.destroy()
        for val in options:
            btn = self.make_button(self.math_answers, str(val),
                                   lambda v=val: self.check_math(v),
                                   random.choice(PALETTE))
            btn.pack(side="left", padx=12, ipadx=24, ipady=8)

        self._animate_math()

    def _animate_math(self):
        """בנה את קבוצת העצמים לאנימציה של חיבור/חיסור."""
        self.math_canvas.delete("all")
        gen = getattr(self, "_math_gen", 0) + 1
        self._math_gen = gen

        w = self.math_canvas.winfo_width() or 800
        h = self.math_canvas.winfo_height() or 320
        a, b = self.math_a, self.math_b
        r = 34
        x0, x1 = w * 0.25, w * 0.70
        y_base = h * 0.55
        gap = r * 2.6

        # מיקומי הכוכבים של הקבוצות
        first = [(x0 + (i - (a - 1) / 2) * gap - gap * 0.5, y_base)
                 for i in range(a)]
        second = [(x1 + (i - (b - 1) / 2) * gap - gap * 0.5, y_base)
                  for i in range(b)]

        # מצייר את הקבוצה הראשונה מיד
        self._math_group = {"gen": gen, "add": self.math_operation == "+",
                            "first": first, "second": second,
                            "first_objs": [], "second_objs": []}
        for cx, cy in first:
            color = random.choice(OBJECT_COLORS)
            oid = draw_star(self.math_canvas, cx, cy, r, color,
                            tag="madd objects")
            self._math_group["first_objs"].append(oid)

        sign_x = (x0 + x1) / 2
        self._op_tag = self.math_canvas.create_text(
            sign_x, y_base, text=_rtl("+" if self.math_operation == "+" else "−"),
            font=self.big_font, fill="#7E57C2")

        # אנימציה של החלק השני
        self._math_idx = 0
        self._math_seq(gen)

    def _math_seq(self, gen):
        """מעלה (חיבור) או מעלימה (חיסור) את הכוכבים של הקבוצה השנייה, אחד-אחד."""
        if gen != self._math_gen:
            return
        g = self._math_group
        idx = self._math_idx
        second = g["second"]

        if not g["add"] and idx >= len(second):
            # משלים גם את סימן הפעולה ואת העצמים הנשארים
            self.math_canvas.delete(self._op_tag)
            return

        if idx < len(second):
            cx, cy = second[idx]
            if g["add"]:
                oid = draw_star(self.math_canvas, cx, cy, 34,
                                random.choice(OBJECT_COLORS), tag="madd objects")
                g["second_objs"].append(oid)
                self._bounce(self.math_canvas, oid)
            else:
                # הופך אותו לקצת אפור ואז מוחק באנימציה
                oid = draw_star(self.math_canvas, cx, cy, 34, "#B0BEC5",
                                tag="madd objects")
                g["second_objs"].append(oid)
                self.math_canvas.after(300, self._vanish, oid, gen)
            self._math_idx += 1
            self.math_canvas.after(g["add"] and 200 or 400,
                                   self._math_seq, gen)

    def _bounce(self, canvas, oid):
        """אנימציית קפיצה קטנה: מגדל הכוכב בהדרגה."""
        gen = self._math_gen
        for k in range(4):
            s = 0.3 + 0.7 * k / 3
            canvas.after(k * 40, lambda k=k, s=s, oid=oid:
                         self._scale_obj(canvas, oid, s, gen))

    def _scale_obj(self, canvas, oid, s, gen):
        if gen != self._math_gen:
            return
        try:
            base = canvas.bbox(oid)
        except Exception:
            return
        if not base:
            return
        cx = (base[0] + base[2]) / 2
        cy = (base[1] + base[3]) / 2
        r = 34 * s
        pts = []
        for i in range(10):
            ang = math.pi / 2 + i * math.pi / 5
            rad = r if i % 2 == 0 else r * 0.45
            pts.append(cx + rad * math.cos(ang))
            pts.append(cy - rad * math.sin(ang))
        canvas.coords(oid, *pts)

    def _vanish(self, oid, gen):
        """מעלים כוכב בהדרגה (חיסור)."""
        if gen != self._math_gen:
            return
        for k, alpha in enumerate([1.0, 0.6, 0.3, 0.0]):
            canvas = self.math_canvas
            canvas.after(k * 90, lambda canvas=canvas, oid=oid, a=alpha:
                         self._fade(canvas, oid, a, gen))

    def _fade(self, canvas, oid, alpha, gen):
        if gen != self._math_gen:
            return
        try:
            canvas.itemconfig(oid, fill=self._dim_color(alpha))
        except Exception:
            return
        if alpha == 0.0:
            canvas.delete(oid)

    @staticmethod
    def _dim_color(alpha):
        # אפור ככל שמתעמעם - פשוט מחזיר אפור בהיר עד כהה לפי אלפא
        gray = int(255 * alpha)
        return f"#{gray:02x}{gray:02x}{gray:02x}"

    def check_math(self, val):
        if self.math_answered:
            return
        self.math_answered = True
        if val == self.math_answer:
            self.math_score += 1
            self.math_feedback.config(text=_rtl("נכון! כל הכבוד!"),
                                      fg="#2E7D32")
            self.math_score_label.config(
                text=_rtl(f"נקודות: {self.math_score}"))
            self._confetti(self.math_canvas)
            self.math_canvas.after(800, self.new_math_question)
        else:
            self.math_feedback.config(text=_rtl("נסו שוב!"), fg="#E53935")
            self.math_answered = False


def main():
    app = NumberApp()
    try:
        app.state("zoomed")
    except Exception:
        app.geometry("1000x700")
    app.mainloop()


if __name__ == "__main__":
    main()
