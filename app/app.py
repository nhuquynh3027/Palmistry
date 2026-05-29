import os
import threading
import numpy as np
import pickle
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
import math
import random

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# ── Fortune data ──────────────────────────────────────────────
Fortune_telling = {
    0: ("Bạn sở hữu trực giác sắc bén, tiếp thu kiến thức rất nhanh, nhưng cần rèn luyện tính kỷ luật để đạt kết quả xuất sắc.",
        "Thể trạng ổn định, tuy nhiên đừng bỏ bê việc nghỉ ngơi.",
        "Những rung động nhẹ nhàng đang đến, hãy để trái tim dẫn lối và người ấy sẽ nhận ra sự chân thành từ bạn."),
    1: ("Con đường học vấn đang rộng mở, sự kiên trì bền bỉ chính là chìa khóa giúp bạn chinh phục mọi đỉnh cao.",
        "Hệ tiêu hóa hơi nhạy cảm, bạn nên ưu tiên chế độ ăn uống thanh đạm.",
        "Một mối quan hệ dựa trên sự tin tưởng và thấu hiểu sẽ là điểm tựa tinh thần vững chắc cho bạn."),
    2: ("Bạn thường xuyên có những ý tưởng bay bổng, hãy cân bằng lại với thực tế để đạt hiệu quả cao nhất.",
        "Đôi mắt cần được chăm sóc, tránh nhìn màn hình quá lâu.",
        "Những tín hiệu tích cực đang đến gần, một người mới sẽ chủ động tiến về phía bạn với tâm thế chân thành."),
    3: ("Tố chất lãnh đạo tiềm ẩn giúp bạn luôn tỏa sáng khi làm việc nhóm, hãy tự tin thể hiện bản thân.",
        "Cần chú ý đến các khớp xương và duy trì vận động nhẹ nhàng mỗi ngày.",
        "Tình yêu lúc này đòi hỏi sự kiên nhẫn và niềm tin tuyệt đối, đừng để hiểu lầm làm lung lay tình cảm."),
    4: ("Tư duy sáng tạo và tâm hồn nghệ sĩ giúp bạn rất hợp với các lĩnh vực nhân văn, nghệ thuật.",
        "Tinh thần minh mẫn, vẻ ngoài tràn đầy sức sống.",
        "Dẫu đường tình đôi lúc có chút chông chênh, nhưng kết quả cuối cùng sẽ vô cùng ngọt ngào."),
    5: ("Bạn đang chịu khá nhiều áp lực, hãy học cách thả lỏng để não bộ làm việc hiệu quả hơn.",
        "Cần bổ sung dưỡng chất và tuân thủ giờ giấc nghỉ ngơi khoa học.",
        "Đừng quá khép kín, việc mở lòng và đón nhận những người bạn mới sẽ mang đến cơ hội bất ngờ."),
    6: ("Trí nhớ của bạn là một tài sản quý giá, hãy tận dụng nó để chinh phục những kiến thức khó.",
        "Chú ý theo dõi huyết áp và tránh xa những thực phẩm quá mặn.",
        "Một cuộc gặp gỡ bất ngờ từ quá khứ sẽ gợi lại những kỷ niệm đẹp hoặc mang đến cơ hội hàn gắn thú vị."),
    7: ("Sự chọn lọc tinh tế giúp bạn không bị quá tải trong biển kiến thức mênh mông.",
        "Sức đề kháng tốt, cơ thể ít khi gặp phải những cơn ốm vặt.",
        "Hai tâm hồn đồng điệu đang tìm đến nhau, đây là thời điểm vàng để vun đắp tình cảm bền lâu."),
    8: ("Sự nghiệp học hành đang thăng tiến vượt bậc như diều gặp gió, hãy tận dụng đà này.",
        "Việc duy trì thói quen tập luyện sẽ giúp cơ thể thêm dẻo dai.",
        "Mối quan hệ tiến triển theo chiều hướng chậm mà chắc, bền vững và đầy sự trân trọng."),
    9: ("Bạn dễ bị xao nhãng bởi các yếu tố bên ngoài, sự tập trung cao độ sẽ giúp bạn làm nên chuyện lớn.",
        "Cần kiểm soát căng thẳng và tìm đến những thú vui lành mạnh.",
        "Hãy kiên nhẫn, người xứng đáng nhất sẽ xuất hiện đúng thời điểm bạn sẵn sàng nhất."),
    10: ("Có quý nhân phù trợ trong con đường học vấn, mọi trở ngại sẽ sớm được hóa giải nếu bạn quyết tâm.",
         "Trạng thái cơ thể rất tốt, chỉ cần duy trì lối sống điều độ là ổn.",
         "Bạn rất có sức hút, nên cẩn thận kẻo sự đa sầu đa cảm khiến bạn khó đưa ra quyết định."),
    11: ("Nỗ lực gấp đôi so với hiện tại sẽ mang lại kết quả vượt ngoài mong đợi, đừng bỏ cuộc nhé.",
         "Chú ý đến đường hô hấp, tránh tiếp xúc nơi ô nhiễm.",
         "Một chuyện tình yêu đẹp đòi hỏi sự thành thật và vun vén từ cả hai phía, hãy luôn chân thành."),
    12: ("Bạn có năng khiếu đặc biệt với các con số hoặc kỹ thuật, hãy khai thác thế mạnh này.",
         "Đừng quên vận động vai gáy và lưng sau nhiều giờ làm việc.",
         "Người yêu bạn rất tinh tế, họ luôn biết cách làm cho bạn cảm thấy đặc biệt mỗi ngày."),
    13: ("Những ý tưởng độc đáo của bạn rất cần được chia sẻ, đừng ngần ngại bày tỏ quan điểm cá nhân.",
         "Cung cấp đủ nước cho cơ thể mỗi ngày là chìa khóa của sự tỉnh táo.",
         "Tuần này là cơ hội tốt để kết nối với một người cực kỳ hợp cạ với bạn."),
    14: ("Kiên trì là phẩm chất vàng, chỉ cần không nản chí bạn chắc chắn sẽ thành công.",
         "Cơ thể đang trong giai đoạn hồi phục và tràn đầy năng lượng.",
         "Những tranh cãi nhỏ chỉ là gia vị của tình yêu, hãy ngồi xuống nói chuyện thẳng thắn."),
    15: ("Tài năng thiên bẩm giúp bạn đạt được thành công sớm hơn dự định, hãy giữ vững phong độ.",
         "Bạn đang sở hữu nguồn năng lượng dồi dào.",
         "Người ấy coi bạn như món quà quý giá, hãy trân trọng và tận hưởng hạnh phúc này."),
}

# ── Palette ───────────────────────────────────────────────────
VOID        = "#07060f"        # deepest background
INK         = "#0d0b1e"        # card bg
MIST        = "#161230"        # subtle section bg
BORDER      = "#2a2250"        # default border
BORDER_G    = "#4a3c1e"        # gold-toned border
GOLD        = "#d4a853"        # primary accent
GOLD_BRIGHT = "#f0cc80"        # highlights
GOLD_DIM    = "#6b5228"        # muted gold
SILVER      = "#c8c0d8"        # body text
SILVER_DIM  = "#6e6680"        # dimmed text
WHITE       = "#f4f0ff"        # headings
CRIMSON     = "#c0334a"        # error
JADE        = "#3db87a"        # success
PURPLE      = "#8b6fd4"        # accent

assets = None

# ── Model helpers ─────────────────────────────────────────────
def load_all_assets():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, 'palm_model.h5')
    full_model = load_model(model_path, compile=False)
    feature_extractor = Model(
        inputs=full_model.inputs,
        outputs=full_model.get_layer('feature_layer').output
    )
    with open(os.path.join(BASE_DIR, 'class_names.pkl'), 'rb') as f:
        class_indices = pickle.load(f)
        class_names = {v: k for k, v in class_indices.items()}
    with open(os.path.join(BASE_DIR, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    with open(os.path.join(BASE_DIR, 'kmeans_model.pkl'), 'rb') as f:
        kmeans_model = pickle.load(f)
    return full_model, feature_extractor, class_names, scaler, kmeans_model

def predict_palmistry(img_path):
    global assets
    if assets is None:
        assets = load_all_assets()
    full_model, feature_extractor, class_names, scaler, kmeans_model = assets
    img = image.load_img(img_path, target_size=(224, 224))
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0) / 255.0
    preds = full_model.predict(arr, verbose=0)
    idx = int(np.argmax(preds[0]))
    conf = float(np.max(preds[0]) * 100)
    hand_type = class_names[idx]
    raw_feat = feature_extractor.predict(arr, verbose=0)
    scaled = scaler.transform(raw_feat)
    cluster = int(kmeans_model.predict(scaled)[0])
    study, health, love = Fortune_telling.get(cluster, ("—", "—", "—"))
    return hand_type, conf, cluster, study, health, love

# ── Divider helper ─────────────────────────────────────────────
def make_divider(parent, bg=INK, gold=GOLD_DIM):
    f = tk.Frame(parent, bg=bg)
    f.pack(fill="x", pady=8)
    tk.Frame(f, bg=gold, height=1).pack(fill="x", side="left", expand=True, padx=(0, 8))
    tk.Label(f, text="✦", font=("Georgia", 8), fg=gold, bg=bg).pack(side="left")
    tk.Frame(f, bg=gold, height=1).pack(fill="x", side="left", expand=True, padx=(8, 0))
    return f

# ── Main App ──────────────────────────────────────────────────
class PalmApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ Bói Chỉ Tay AI ✦")
        self.geometry("820x750")
        self.minsize(700, 740)
        self.configure(bg=VOID)
        self.resizable(True, True)

        self.img_path = None
        self.back_image = None
        self.back_photo = None
        self._anim_id = None
        self._dots = 0

        self._load_back_image()
        self._build_ui()

    def _load_back_image(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        back_path = os.path.join(BASE_DIR, 'back.jpg')
        if os.path.exists(back_path):
            try:
                # Mở và giữ bản gốc PIL Image để tính toán tỉ lệ khi kéo giãn cửa sổ
                self.back_image = Image.open(back_path).convert("RGBA")
            except Exception as e:
                print(f"Không thể load ảnh banner back.jpg: {e}")

    # ── UI Construction ───────────────────────────────────────
    def _build_ui(self):
        outer = tk.Frame(self, bg=VOID)
        outer.pack(fill="both", expand=True)

        self.canvas_scroll = tk.Canvas(outer, bg=VOID, highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=self.canvas_scroll.yview,
                          bg=INK, troughcolor=VOID, activebackground=GOLD_DIM)
        self.canvas_scroll.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas_scroll.pack(side="left", fill="both", expand=True)

        self.main_frame = tk.Frame(self.canvas_scroll, bg=VOID)
        self.win_id = self.canvas_scroll.create_window((0, 0), window=self.main_frame, anchor="nw")

        self.main_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas_scroll.bind("<Configure>", self._on_canvas_configure)
        self.canvas_scroll.bind_all("<MouseWheel>",
            lambda e: self.canvas_scroll.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._build_hero()
        self._build_upload_card()
        self._build_result_section()
        self._build_footer()

    def _on_frame_configure(self, e):
        self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))

    def _on_canvas_configure(self, e):
        self.canvas_scroll.itemconfig(self.win_id, width=e.width)

    # ── Hero Header ───────────────────────────────────────────
    def _build_hero(self):
        # Frame chứa ảnh banner đóng vai trò làm phần đầu
        self.hero_frame = tk.Frame(self.main_frame, bg=VOID)
        self.hero_frame.pack(fill="x")

        # Label chuyên dụng chịu trách nhiệm hiển thị ảnh back.jpg
        self.banner_lbl = tk.Label(self.hero_frame, bg=VOID, bd=0, highlightthickness=0)
        self.banner_lbl.pack(fill="x")

        def on_banner_resize(e):
            if self.back_image and e.width > 100:
                # Tính toán lại chiều cao dựa theo tỉ lệ gốc của bức ảnh nhằm tránh bóp méo
                orig_w, orig_h = self.back_image.size
                new_h = int((e.width / orig_w) * orig_h)
                
                # Tránh resize nếu chiều cao tính toán ra không hợp lệ
                if new_h > 0:
                    resized_img = self.back_image.resize((e.width, new_h), Image.LANCZOS)
                    self.back_photo = ImageTk.PhotoImage(resized_img)
                    self.banner_lbl.configure(image=self.back_photo)

        # Lắng nghe sự kiện co giãn của Frame chứa để cập nhật kích cỡ ảnh liên tục
        self.hero_frame.bind("<Configure>", on_banner_resize)

        # Thanh viền vàng cắt chân bên dưới Banner
        sep_frame = tk.Frame(self.main_frame, bg=VOID)
        sep_frame.pack(fill="x", padx=0)
        tk.Frame(sep_frame, bg=GOLD_DIM, height=1).pack(fill="x")

    # ── Upload Card ───────────────────────────────────────────
    def _build_upload_card(self):
        wrapper = tk.Frame(self.main_frame, bg=VOID)
        wrapper.pack(fill="x", padx=44, pady=(24, 0))

        outer_border = tk.Frame(wrapper, bg=GOLD_DIM, padx=1, pady=1)
        outer_border.pack(fill="x")

        self.upload_frame = tk.Frame(outer_border, bg=INK)
        self.upload_frame.pack(fill="x")

        inner = tk.Frame(self.upload_frame, bg=INK)
        inner.pack(padx=36, pady=30, fill="x")

        tag_frame = tk.Frame(inner, bg=INK)
        tag_frame.pack(fill="x", pady=(0, 18))
        tk.Frame(tag_frame, bg=BORDER_G, height=1).pack(fill="x", side="left", expand=True)
        tk.Label(tag_frame, text="  DÂNG BÀN TAY  ", font=("Georgia", 8, "bold"),
                 fg=GOLD, bg=INK, padx=8).pack(side="left")
        tk.Frame(tag_frame, bg=BORDER_G, height=1).pack(fill="x", side="left", expand=True)

        drop_outer = tk.Frame(inner, bg=BORDER, padx=1, pady=1)
        drop_outer.pack(fill="x")
        self.drop_btn = tk.Button(
            drop_outer,
            text="""🤲
Chọn ảnh bàn tay của bạn
""",                                              
            font=("Georgia", 11, "italic"),
            fg=SILVER_DIM, bg=MIST,
            activebackground=INK, activeforeground=GOLD,
            relief="flat", cursor="hand2",
            bd=0, highlightthickness=0,
            command=self._pick_file
        )
        self.drop_btn.pack(fill="x", ipady=18)

        self.preview_outer = tk.Frame(inner, bg=INK)
        self.preview_outer.pack(pady=(16, 0))
        self.preview_label = tk.Label(self.preview_outer, bg=INK)
        self.preview_label.pack()

        self.file_lbl = tk.Label(inner, text="", font=("Georgia", 9, "italic"),
                                  fg=SILVER_DIM, bg=INK)
        self.file_lbl.pack(pady=(4, 0))

        make_divider(inner, bg=INK)

        self.predict_btn = tk.Button(
            inner,
            text="✦   Giải Mã Vận Mệnh   ✦",
            font=("Georgia", 12, "bold"),
            fg=VOID, bg=GOLD_DIM,
            activebackground=GOLD, activeforeground=VOID,
            relief="flat", cursor="hand2",
            bd=0, highlightthickness=0,
            state="disabled",
            command=self._start_prediction
        )
        self.predict_btn.pack(fill="x", ipady=13)

        self.status_lbl = tk.Label(inner, text="", font=("Georgia", 10, "italic"),
                                    fg=SILVER_DIM, bg=INK)
        self.status_lbl.pack(pady=(10, 2))

    # ── Result Section ────────────────────────────────────────
    def _build_result_section(self):
        self.result_frame = tk.Frame(self.main_frame, bg=VOID)

        wrapper = tk.Frame(self.result_frame, bg=VOID)
        wrapper.pack(fill="x", padx=44, pady=(22, 0))

        top_outer = tk.Frame(wrapper, bg=GOLD_DIM, padx=1, pady=1)
        top_outer.pack(fill="x", pady=(0, 16))
        top_card = tk.Frame(top_outer, bg=INK)
        top_card.pack(fill="x")
        top_inner = tk.Frame(top_card, bg=INK)
        top_inner.pack(padx=28, pady=18, fill="x")

        title_row = tk.Frame(top_inner, bg=INK)
        title_row.pack(fill="x")
        tk.Label(title_row, text="✦  THIÊN CƠ ĐÃ HÉ LỘ  ✦",
                 font=("Georgia", 14, "bold"), fg=GOLD_BRIGHT, bg=INK).pack()

        make_divider(top_inner, bg=INK)

        badge_frame = tk.Frame(top_inner, bg=MIST, padx=1, pady=1)
        badge_frame.pack(pady=(4, 12))
        badge_inner = tk.Frame(badge_frame, bg=MIST)
        badge_inner.pack()
        self.hand_lbl = tk.Label(badge_inner, text="—",
                                  font=("Georgia", 11), fg=GOLD, bg=MIST,
                                  padx=24, pady=6)
        self.hand_lbl.pack()

        conf_frame = tk.Frame(top_inner, bg=INK)
        conf_frame.pack(fill="x")
        row = tk.Frame(conf_frame, bg=INK)
        row.pack(fill="x")
        tk.Label(row, text="ĐỘ CHÍNH XÁC", font=("Georgia", 8, "bold"),
                 fg=SILVER_DIM, bg=INK).pack(side="left")
        self.conf_pct_lbl = tk.Label(row, text="—", font=("Georgia", 9, "bold"),
                                      fg=GOLD_BRIGHT, bg=INK)
        self.conf_pct_lbl.pack(side="right")

        bar_track = tk.Frame(conf_frame, bg="#1c1836", height=5)
        bar_track.pack(fill="x", pady=(6, 0))
        bar_track.pack_propagate(False)
        self.conf_bar = tk.Frame(bar_track, bg=GOLD, height=5)
        self.conf_bar.place(x=0, y=0, relheight=1, relwidth=0)

        scroll_outer = tk.Frame(wrapper, bg=GOLD_DIM, padx=1, pady=1)
        scroll_outer.pack(fill="x")
        scroll_card = tk.Frame(scroll_outer, bg=INK)
        scroll_card.pack(fill="x")
        sc = tk.Frame(scroll_card, bg=INK)
        sc.pack(padx=32, pady=24, fill="x")

        self.cluster_lbl = tk.Label(sc, text="—", font=("Georgia", 9, "italic"),
                                     fg=SILVER_DIM, bg=INK)
        self.cluster_lbl.pack(pady=(0, 18))

        fortune_data = [
            ("study_lbl",  "📚", "HỌC TẬP",  GOLD,    "#1a1528"),
            ("health_lbl", "🌿", "SỨC KHỎE", JADE,    "#0f1a14"),
            ("love_lbl",   "💞", "TÌNH DUYÊN", PURPLE, "#130f1e"),
        ]
        for attr, icon, title, accent, item_bg in fortune_data:
            item_border = tk.Frame(sc, bg=accent, padx=1, pady=1)
            item_border.pack(fill="x", pady=(0, 12))
            item_card = tk.Frame(item_border, bg=item_bg)
            item_card.pack(fill="x")
            item_inner = tk.Frame(item_card, bg=item_bg)
            item_inner.pack(padx=20, pady=14, fill="x", anchor="w")

            head = tk.Frame(item_inner, bg=item_bg)
            head.pack(fill="x", anchor="w")
            tk.Label(head, text=f"{icon}  {title}",
                     font=("Georgia", 9, "bold"), fg=accent, bg=item_bg).pack(side="left")

            lbl = tk.Label(item_inner, text="—",
                           font=("Georgia", 11, "italic"),
                           fg=SILVER, bg=item_bg,
                           wraplength=580, justify="left")
            lbl.pack(anchor="w", pady=(6, 0))
            setattr(self, attr, lbl)

        make_divider(sc, bg=INK)

        self.reset_btn = tk.Button(
            sc,
            text="↺   Xem Lại Lần Nữa",
            font=("Georgia", 10), fg=GOLD_DIM, bg=INK,
            activebackground=MIST, activeforeground=GOLD,
            relief="flat", cursor="hand2",
            bd=0,
            highlightthickness=1, highlightbackground=BORDER,
            command=self._reset, pady=10
        )
        self.reset_btn.pack(pady=(6, 4))

    # ── Footer ────────────────────────────────────────────────
    def _build_footer(self):
        f = tk.Frame(self.main_frame, bg=VOID)
        f.pack(fill="x", pady=(22, 24))
        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", padx=44, pady=(0, 12))
        tk.Label(f, text="✦  Palmistry AI System  ✦",
                 font=("Georgia", 9), fg=GOLD_DIM, bg=VOID).pack()
        tk.Label(f, text="Kết quả chỉ mang tính chất chiêm nghiệm giải trí hữu ích  ·  Hãy luôn vững tin vào chính mình",
                 font=("Georgia", 8, "italic"), fg=SILVER_DIM, bg=VOID).pack(pady=(4, 0))

    # ── Actions ───────────────────────────────────────────────
    def _pick_file(self):
        path = filedialog.askopenfilename(
            title="Chọn ảnh bàn tay",
            filetypes=[("Ảnh", "*.jpg *.jpeg *.png *.bmp *.webp"), ("Tất cả", "*.*")]
        )
        if not path:
            return
        self.img_path = path

        pil = Image.open(path).convert("RGB")
        pil.thumbnail((260, 200), Image.LANCZOS)
        bordered = Image.new("RGB", (pil.width + 4, pil.height + 4), (74, 60, 30))
        bordered.paste(pil, (2, 2))
        photo = ImageTk.PhotoImage(bordered)
        self.preview_label.configure(image=photo)
        self.preview_label._img = photo

        self.file_lbl.configure(text=os.path.basename(path))
        self.predict_btn.configure(state="normal", bg=GOLD, fg=VOID,
                                   activebackground=GOLD_BRIGHT)
        self.status_lbl.configure(text="", fg=SILVER_DIM)
        self.result_frame.pack_forget()

    def _start_prediction(self):
        if not self.img_path:
            return
        self.predict_btn.configure(state="disabled", bg=GOLD_DIM)
        self.result_frame.pack_forget()
        self._dots = 0
        self._animate_loading()
        threading.Thread(target=self._run_prediction, daemon=True).start()

    def _animate_loading(self):
        msgs = [
            "Tinh tú đang căn chỉnh quỹ đạo",
            "Đọc những đường chỉ tay huyền bí",
            "Linh hồn vũ trụ đang lên tiếng",
            "Vận mệnh đang được giải mã",
        ]
        dots = "·" * (self._dots % 4)
        self._dots += 1
        msg_idx = (self._dots // 4) % len(msgs)
        self.status_lbl.configure(text=f"◈  {msgs[msg_idx]} {dots}", fg=GOLD_DIM)
        self._anim_id = self.after(480, self._animate_loading)

    def _run_prediction(self):
        try:
            hand_type, conf, cluster, study, health, love = predict_palmistry(self.img_path)
            self.after(0, self._show_result, hand_type, conf, cluster, study, health, love)
        except Exception as e:
            self.after(0, self._show_error, str(e))

    def _show_result(self, hand_type, conf, cluster, study, health, love):
        if self._anim_id:
            self.after_cancel(self._anim_id)
        self.status_lbl.configure(text="◈  Hoàn tất · Thiên cơ đã được hé lộ", fg=JADE)
        self.predict_btn.configure(state="normal", bg=GOLD, fg=VOID,
                                   activebackground=GOLD_BRIGHT)

        self.hand_lbl.configure(text=f"  {hand_type}  ✦  Dạng Bàn Tay  ")
        self.conf_pct_lbl.configure(text=f"{conf:.1f}%")
        self.conf_bar.place(relwidth=min(conf / 100, 1.0))
        self.cluster_lbl.configure(text=f"✦  Vận Mệnh Nhóm {cluster + 1} / 16  ✦")
        self.study_lbl.configure(text=study)
        self.health_lbl.configure(text=health)
        self.love_lbl.configure(text=love)

        self.result_frame.pack(fill="x", pady=(0, 10))
        self.canvas_scroll.after(120, lambda: self.canvas_scroll.yview_moveto(0.38))

    def _show_error(self, msg):
        if self._anim_id:
            self.after_cancel(self._anim_id)
        self.status_lbl.configure(text=f"⚠  Lỗi: {msg}", fg=CRIMSON)
        self.predict_btn.configure(state="normal", bg=GOLD, fg=VOID)

    def _reset(self):
        if self._anim_id:
            self.after_cancel(self._anim_id)
        self.img_path = None
        self.preview_label.configure(image="")
        self.file_lbl.configure(text="")
        self.status_lbl.configure(text="", fg=SILVER_DIM)
        self.predict_btn.configure(state="disabled", bg=GOLD_DIM, fg=VOID)
        self.conf_bar.place(relwidth=0)
        self.result_frame.pack_forget()
        self.canvas_scroll.yview_moveto(0)


if __name__ == "__main__":
    app = PalmApp()
    app.mainloop()