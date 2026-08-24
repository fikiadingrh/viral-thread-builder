
import json
import random
import re
from datetime import datetime
from http.server import BaseHTTPRequestHandler

# ============================================================
# VIRAL CONTENT BUILDER LOGIC
# ============================================================

THREAD_TEMPLATES = {
    "hot_take": {
        "hook_patterns": [
            "Stop percaya sama {TOPIC}. Ini yang sebenarnya terjadi:",
            "Saya punya opini nggak populer tentang {TOPIC}:",
            "Semua orang salah soal {TOPIC}. Ini penjelasan jujur:",
            "{TOPIC} itu overrated. Kenapa saya bilang begitu? 👇",
            "Belum baca ini sebelum memutuskan soal {TOPIC}:",
        ],
        "body_structure": [
            "{NUM}. {CLAIM} 👇",
            "{NUM}. Kenapa orang mikir gini? Karena {COMMON_MISCONCEPTION}",
            "{NUM}. Tapi faktanya: {REAL_FACT}",
            "{NUM}. {COUNTER_EVIDENCE}",
            "{NUM}. Intinya: {CONCLUSION}",
        ],
        "cta_variants": [
            "Agree atau ada pendapat lain? 👇",
            "Ini hot take saya, gimana menurut kalian?",
            "Debat di reply section 👇",
        ],
    },
    "personal_story": {
        "hook_patterns": [
            "Dulu saya {NEGATIVE_STATE}, sekarang {POSITIVE_STATE}. Timeline nya:",
            "Gagal total di {TOPIC} tahun lalu. Ini yang saya pelajari:",
            "Kesalahan termahal yang pernah saya buat soal {TOPIC}:",
            "Masa-masa terberat saya soal {TOPIC}, dan cara bangkit:",
            "Kalau bisa balik waktu, saya bakal stop {BAD_HABIT} sejak awal",
        ],
        "body_structure": [
            "{NUM}. Awal mula: Saya awalnya mikir {FALSE_BELIEF}",
            "{NUM}. Masalah mulai kelihatan pas {TURNING_POINT}",
            "{NUM}. Titik terendah: {HIT_BOTTOM}",
            "{NUM}. Cara keluar: {SOLUTION}",
            "{NUM}. Hasil sekarang: {CURRENT_STATE}",
            "{NUM}. Lesson learned: {KEY_LESSON}",
        ],
        "cta_variants": [
            "Pernah ngalamin hal serupa? Cerita dong 👇",
            "Tips lain dari kalian untuk yang lagi struggle?",
            "Tag temen yang butuh baca ini 🙏",
        ],
    },
    "listicle": {
        "hook_patterns": [
            "{COUNT} {CATEGORY} terbaik {YEAR} versi pengalaman saya:",
            "Dari 50+ {CATEGORY} yang coba, ini {COUNT} yang worth it:",
            "Jangan beli {CATEGORY} sebelum liat list ini:",
            "Budget {BUDGET}? Ini {COUNT} {CATEGORY} yang wajib kamu tahu:",
        ],
        "body_structure": [
            "{NUM}. {PRODUCT_NAME}: {PRICE} | {WHY_WORTH_IT}",
            "{NUM}. {PRODUCT_NAME}: {PRICE} | {WHY_WORTH_IT}",
            "{NUM}. {PRODUCT_NAME}: {PRICE} | {WHY_WORTH_IT}",
            "{NUM}. {PRODUCT_NAME}: {PRICE} | {WHY_WORTH_IT}",
            "{NUM}. {PRODUCT_NAME}: {PRICE} | {WHY_WORTH_IT}",
        ],
        "cta_variants": [
            "Produk favorit kalian apa? Add ke list! 👇",
            "Mana yang paling menarik perhatian?",
            "Link review lengkap ada di bio 🔗",
        ],
    },
    "how_to": {
        "hook_patterns": [
            "Cara saya {ACHIEVE_GOAL} dalam {TIMEFRAME} (step by step):",
            "Tutorial {SKILL} untuk pemula, dari nol sampai mahir:",
            "Gampang kok, ini cara {DO_ACTION} tanpa ribet:",
            "90% orang nggak tahu cara {DO_ACTION} yang benar. Ini tutorialnya:",
        ],
        "body_structure": [
            "{NUM}. Step 1: {STEP_1_DETAIL}",
            "{NUM}. Step 2: {STEP_2_DETAIL} | Tips: {TIP_A}",
            "{NUM}. Step 3: {STEP_3_DETAIL} | Common mistake: {MISTAKE_A}",
            "{NUM}. Step 4: {STEP_4_DETAIL} | Pro tip: {PRO_TIP_A}",
            "{NUM}. Bonus: {BONUS_TIP}",
        ],
        "cta_variants": [
            "Save buat dipraktikkan nanti! 📌",
            "Follow buat tutorial lainnya 🙏",
            "Part 2 coming soon, stay tuned!",
        ],
    },
}


def generate_hooks(template_type, topic):
    tpl = THREAD_TEMPLATES.get(template_type, THREAD_TEMPLATES["listicle"])
    patterns = tpl["hook_patterns"]
    hooks = []
    for p in patterns:
        hook = (
            p.replace("{TOPIC}", topic)
            .replace("{CATEGORY}", topic)
            .replace("{YEAR}", str(datetime.now().year))
            .replace("{COUNT}", str(random.randint(5, 10)))
            .replace("{BUDGET}", f"{random.randint(50, 300)}rb")
            .replace("{TIMEFRAME}", random.choice(["2 minggu", "1 bulan", "30 hari"]))
        )
        hooks.append(hook)
    return hooks


def build_thread(template_type, topic):
    tpl = THREAD_TEMPLATES.get(template_type, THREAD_TEMPLATES["listicle"])
    body = tpl["body_structure"]
    ctas = tpl["cta_variants"]

    defaults = {
        "NUM": "",
        "CLAIM": f"{topic.capitalize()} itu sebenarnya underrated.",
        "COMMON_MISCONCEPTION": "informasi lama yang nggak pernah di-update",
        "REAL_FACT": "data terbaru nunjukin tren yang berbeda banget",
        "COUNTER_EVIDENCE": "Beberapa case study terbaru mendukung ini",
        "CONCLUSION": "Nggak semua orang cocok, tapi worth to try",
        "PRODUCT_NAME": random.choice(
            ["Produk A", "Produk B", "Produk C", "Produk D", "Produk E"]
        ),
        "PRICE": f"{random.randint(25, 499)}rb",
        "WHY_WORTH_IT": random.choice(
            [
                "Value for money, kualitas solid",
                "Bahan premium, tahan lama",
                "Best seller dengan rating 4.9",
                "Hidden gem yang jarang orang tahu",
                "Review-nya rata-rata positif banget",
            ]
        ),
        "STEP_1_DETAIL": "Siapkan semua tools yang diperlukan",
        "STEP_2_DETAIL": "Ikuti langkah kedua dengan teliti",
        "STEP_3_DETAIL": "Review hasil kerjaan kamu",
        "STEP_4_DETAIL": "Iterasi berdasarkan feedback",
        "TIP_A": "Jangan skip step apapun",
        "MISTAKE_A": "Terburu-buru tanpa persiapan",
        "PRO_TIP_A": "Track progress setiap hari",
        "BONUS_TIP": "Tetap konsisten walaupun Capek",
        "NEGATIVE_STATE": "struggle banget",
        "POSITIVE_STATE": "alhamdulillah berhasil",
        "FALSE_BELIEF": "semua akan gampang",
        "TURNING_POINT": "realita mulai kerasa",
        "HIT_BOTTOM": "mentok dan pengen nyerah",
        "SOLUTION": "evaluasi total + ubah strategi",
        "CURRENT_STATE": "jauh lebih baik dan stabil",
        "KEY_LESSON": "gagal itu data, bukan vonis",
        "BAD_HABIT": "nunda dan overthinking",
        "ACHIEVE_GOAL": f"sukses di {topic}",
        "SKILL": topic,
        "DO_ACTION": f"mulai {topic}",
    }

    posts = []
    for i, s in enumerate(body[:5], 1):
        defaults["NUM"] = str(i)
        posts.append(s.format(**defaults))

    posts.append("\n" + random.choice(ctas))
    return posts


def optimize_thread(thread):
    total = len(thread)
    avg_len = sum(len(p) for p in thread) / max(total, 1)
    q_count = sum(p.count("?") for p in thread)
    has_cta = any(
        "?" in p
        or "drop" in p.lower()
        or "comment" in p.lower()
        or "reply" in p.lower()
        or "follow" in p.lower()
        or "save" in p.lower()
        or "tag" in p.lower()
        for p in thread
    )

    issues = []
    suggestions = []

    if total < 3:
        issues.append("Thread terlalu pendek")
        suggestions.append("Tambah minimal 3 posts untuk retention yang lebih baik")
    if total > 10:
        issues.append("Thread terlalu panjang")
        suggestions.append("Pertimbangkan untuk split jadi 2 thread terpisah")
    if q_count == 0:
        issues.append("Tidak ada pertanyaan")
        suggestions.append("Tambah 1-2 pertanyaan terbuka untuk picu reply")
    if not has_cta:
        suggestions.append("Tambah CTA (call-to-action) di akhir thread")

    score = 100 - len(issues) * 10
    score = max(score, 0)

    return {
        "total_posts": total,
        "avg_char_length": round(avg_len),
        "question_count": q_count,
        "has_cta": has_cta,
        "issues": issues,
        "suggestions": suggestions,
        "score": score,
    }


def optimal_times():
    return ["06:00 WIB", "12:00 WIB", "18:00 WIB", "21:00 WIB"]


# ============================================================
# VERCEL SERVERLESS HANDLER
# ============================================================

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._set_headers()
        self.end_headers()
        msg = json.dumps({
            "status": "ok",
            "message": "Viral Thread Builder API is running. Send POST request with topic and template.",
        })
        self.wfile.write(msg.encode())

    def do_POST(self):
        self._set_headers()
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            topic = data.get("topic", "").strip()
            template = data.get("template", "listicle")

            if not topic or len(topic) < 3:
                self.send_response(400)
                self._set_headers()
                self.wfile.write(
                    json.dumps({"error": "Topic harus minimal 3 karakter"}).encode()
                )
                return

            hooks = generate_hooks(template, topic)
            thread = build_thread(template, topic)
            analysis = optimize_thread(thread)
            times = optimal_times()

            self.send_response(200)
            self._set_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "success": True,
                        "data": {
                            "topic": topic,
                            "template": template,
                            "hooks": hooks,
                            "thread": thread,
                            "analysis": analysis,
                            "optimal_times": times,
                        },
                    }
                ).encode()
            )

        except Exception as e:
            self.send_response(500)
            self._set_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def _set_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
