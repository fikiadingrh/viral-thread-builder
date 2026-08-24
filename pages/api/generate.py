import json
import random
import re
from datetime import datetime

def handler(request):
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }
    
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Method not allowed"})
        }
    
    try:
        data = request.get_json()
        topic = data.get("topic", "").strip()
        template = data.get("template", "listicle")
        
        if not topic or len(topic) < 3:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Topic harus minimal 3 karakter"})
            }
        
        # Template logic
        templates = {
            "hot_take": {
                "hooks": [
                    f"Stop percaya sama {topic}. Ini yang sebenarnya terjadi:",
                    f"Saya punya opini nggak populer tentang {topic}:",
                    f"Semua orang salah soal {topic}. Ini penjelasan jujur:",
                    f"{topic} itu overrated. Kenapa saya bilang begitu? 👇",
                    f"Belum baca ini sebelum memutuskan soal {topic}:",
                ],
                "body": [
                    "1. Ini sebenarnya underrated.",
                    "2. Kenapa orang mikir gini? Karena informasi lama yang nggak pernah di-update",
                    "3. Tapi faktanya: data terbaru nunjukin tren yang berbeda banget",
                    "4. Beberapa case study terbaru mendukung ini",
                    "5. Intinya: Nggak semua orang cocok, tapi worth to try"
                ],
                "cta": ["Agree atau ada pendapat lain? 👇", "Ini hot take saya, gimana menurut kalian?", "Debat di reply section 👇"]
            },
            "personal_story": {
                "hooks": [
                    f"Dulu saya struggle, sekarang berhasil. Timeline nya:",
                    f"Gagal total di {topic} tahun lalu. Ini yang saya pelajari:",
                    f"Kesalahan termahal yang pernah saya buat soal {topic}:",
                    f"Masa-masa terberat saya soal {topic}, dan cara bangkit:",
                ],
                "body": [
                    "1. Awal mula: Saya awalnya mikir semua akan gampang",
                    "2. Masalah mulai kelihatan pas realita mulai kerasa",
                    "3. Titik terendah: mentok dan pengen nyerah",
                    "4. Cara keluar: evaluasi total + ubah strategi",
                    "5. Hasil sekarang: jauh lebih baik dan stabil",
                    "6. Lesson learned: gagal itu data, bukan vonis"
                ],
                "cta": ["Pernah ngalamin hal serupa? Cerita dong 👇", "Tips lain dari kalian untuk yang lagi struggle?", "Tag temen yang butuh baca ini 🙏"]
            },
            "listicle": {
                "hooks": [
                    f"{random.randint(5,10)} {topic} terbaik {datetime.now().year} versi pengalaman saya:",
                    f"Dari 50+ {topic} yang coba, ini {random.randint(5,10)} yang worth it:",
                    f"Jangan beli {topic} sebelum liat list ini:",
                    f"Budget {random.randint(50,300)}rb? Ini {random.randint(5,10)} {topic} yang wajib kamu tahu:",
                ],
                "body": [
                    f"1. Produk A: {random.randint(25,499)}rb | Value for money, kualitas solid",
                    f"2. Produk B: {random.randint(25,499)}rb | Bahan premium, tahan lama",
                    f"3. Produk C: {random.randint(25,499)}rb | Best seller dengan rating 4.9",
                    f"4. Produk D: {random.randint(25,499)}rb | Hidden gem yang jarang orang tahu",
                    f"5. Produk E: {random.randint(25,499)}rb | Review-nya rata-rata positif banget"
                ],
                "cta": ["Produk favorit kalian apa? Add ke list! 👇", "Mana yang paling menarik perhatian?", "Link review lengkap ada di bio 🔗"]
            },
            "how_to": {
                "hooks": [
                    f"Cara saya sukses di {topic} dalam {random.choice(['2 minggu','1 bulan','30 hari'])} (step by step):",
                    f"Tutorial {topic} untuk pemula, dari nol sampai mahir:",
                    f"Gampang kok, ini cara mulai {topic} tanpa ribet:",
                    f"90% orang nggak tahu cara mulai {topic} yang benar. Ini tutorialnya:",
                ],
                "body": [
                    "1. Step 1: Siapkan semua tools yang diperlukan",
                    "2. Step 2: Ikuti langkah kedua dengan teliti | Tips: Jangan skip step apapun",
                    "3. Step 3: Review hasil kerjaan kamu | Mistake: Terburu-buru tanpa persiapan",
                    "4. Step 4: Iterasi berdasarkan feedback | Pro tip: Track progress setiap hari",
                    "5. Bonus: Tetap konsisten walaupun Capek"
                ],
                "cta": ["Save buat dipraktikkan nanti! 📌", "Follow buat tutorial lainnya 🙏", "Part 2 coming soon, stay tuned!"]
            }
        }
        
        selected = templates.get(template, templates["listicle"])
        
        hooks = selected["hooks"]
        thread = selected["body"] + [random.choice(selected["cta"])]
        
        # Optimization score
        total = len(thread)
        avg_len = sum(len(p) for p in thread) / max(total, 1)
        q_count = sum(p.count("?") for p in thread)
        has_cta = any(x in p.lower() for p in thread for x in ["?", "drop", "comment", "reply", "follow", "save", "tag"])
        
        issues = []
        suggestions = []
        
        if total < 3:
            issues.append("Thread terlalu pendek")
            suggestions.append("Tambah minimal 3 posts untuk retention")
        if total > 10:
            issues.append("Thread terlalu panjang")
            suggestions.append("Split jadi 2 thread terpisah")
        if q_count == 0:
            issues.append("Tidak ada pertanyaan")
            suggestions.append("Tambah 1-2 pertanyaan untuk picu reply")
        if not has_cta:
            suggestions.append("Tambah CTA di akhir thread")
        
        score = max(100 - len(issues) * 10, 0)
        times = ["06:00 WIB", "12:00 WIB", "18:00 WIB", "21:00 WIB"]
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": True,
                "data": {
                    "topic": topic,
                    "template": template,
                    "hooks": hooks,
                    "thread": thread,
                    "analysis": {
                        "total_posts": total,
                        "avg_char_length": round(avg_len),
                        "question_count": q_count,
                        "has_cta": has_cta,
                        "issues": issues,
                        "suggestions": suggestions,
                        "score": score
                    },
                    "optimal_times": times
                }
            })
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
