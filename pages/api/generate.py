import json
import random
from datetime import datetime

def handler(request):
    """Vercel serverless handler"""
    
    # CORS
    cors_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": ""
        }
    
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": cors_headers,
            "body": json.dumps({"error": "Only POST method allowed"})
        }
    
    try:
        body = request.get_json(silent=True)
        if not body:
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({"error": "Invalid JSON body"})
            }
        
        topic = body.get("topic", "")
        if not topic or len(str(topic).strip()) < 3:
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({"error": "Topic must be at least 3 characters"})
            }
        
        topic = str(topic).strip()
        template = body.get("template", "listicle")
        
        # Templates
        templates = {
            "hot_take": {
                "hooks": [
                    f"Stop percaya sama {topic}. Ini fakta sebenarnya:",
                    f"Opini nggak populer saya tentang {topic}:",
                    f"Semua orang salah soal {topic}. Ini penjelasannya:",
                    f"{topic} itu overrated. Kenapa? 👇",
                ],
                "body": [
                    "1. Banyak yang percaya mitos lama",
                    "2. Faktanya: data terbaru beda total",
                    "3. Case study terbaru dukung ini",
                    "4. Intinya: worth to try tapi bukan untuk semua orang"
                ],
                "cta": ["Agree atau disagree?", "Apa pendapat kalian?", "Debat di reply 👇"]
            },
            "listicle": {
                "hooks": [
                    f"{random.randint(5,10)} {topic} terbaik tahun ini:",
                    f"Jangan beli {topic} sebelum baca list ini:",
                    f"Dari 50+ {topic} yang saya coba, ini top ones:",
                ],
                "body": [
                    f"1. Produk A: {random.randint(50,500)}rb | Value for money",
                    f"2. Produk B: {random.randint(50,500)}rb | Kualitas premium",
                    f"3. Produk C: {random.randint(50,500)}rb | Best seller",
                    f"4. Produk D: {random.randint(50,500)}rb | Hidden gem",
                    f"5. Produk E: {random.randint(50,500)}rb | Rating tinggi"
                ],
                "cta": ["Mana favorit kalian?", "Add produk lain di comment!", "Link di bio 🔗"]
            },
            "how_to": {
                "hooks": [
                    f"Cara mulai {topic} untuk pemula (step by step):",
                    f"Tutorial {topic} dari nol sampai mahir:",
                    f"Gampang kok, ini cara {topic} tanpa ribet:",
                ],
                "body": [
                    "1. Step 1: Siapkan tools yang diperlukan",
                    "2. Step 2: Ikuti langkah dengan teliti",
                    "3. Step 3: Review hasil kerjaan",
                    "4. Step 4: Iterasi berdasarkan feedback",
                    "5. Bonus: Konsisten tiap hari"
                ],
                "cta": ["Save buat nanti dipraktikkan!", "Follow buat tutorial lainnya", "Part 2 coming soon"]
            },
            "personal_story": {
                "hooks": [
                    f"Gagal total di {topic} tahun lalu. Ini pelajarannya:",
                    f"Masa terberat saya soal {topic} dan cara bangkit:",
                    f"Kesalahan termahal saya di {topic}:"
                ],
                "body": [
                    "1. Awalnya saya mikir semuanya gampang",
                    "2. Realita: mental dan hampir nyerah",
                    "3. Titik balik: evaluasi total",
                    "4. Cara keluar: ubah strategi",
                    "5. Hasil: jauh lebih baik sekarang"
                ],
                "cta": ["Pernah ngalamin hal serupa?", "Share pengalaman kalian 👇", "Tag temen yang butuh ini"]
            }
        }
        
        selected = templates.get(template, templates["listicle"])
        
        hooks = selected["hooks"]
        body_text = selected["body"]
        cta_text = random.choice(selected["cta"])
        
        thread = body_text + [cta_text]
        
        # Analysis
        total_posts = len(thread)
        avg_len = sum(len(p) for p in thread) / max(total_posts, 1)
        question_count = sum(p.count("?") for p in thread)
        has_cta = any(x in "".join(thread).lower() for x in ["?", "drop", "comment", "follow", "save"])
        
        issues = []
        suggestions = []
        
        if total_posts < 3:
            issues.append("Thread terlalu pendek")
            suggestions.append("Tambah minimal 3 posts")
        if total_posts > 10:
            issues.append("Thread terlalu panjang")
            suggestions.append("Split jadi 2 thread")
        if question_count == 0:
            issues.append("Tidak ada pertanyaan")
            suggestions.append("Tambah 1-2 pertanyaan untuk picu reply")
        if not has_cta:
            suggestions.append("Tambah CTA di akhir")
        
        score = max(100 - len(issues) * 10, 0)
        optimal_times = ["06:00 WIB", "12:00 WIB", "18:00 WIB", "21:00 WIB"]
        
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({
                "success": True,
                "data": {
                    "topic": topic,
                    "template": template,
                    "hooks": hooks,
                    "thread": thread,
                    "analysis": {
                        "total_posts": total_posts,
                        "avg_char_length": round(avg_len),
                        "question_count": question_count,
                        "has_cta": has_cta,
                        "issues": issues,
                        "suggestions": suggestions,
                        "score": score
                    },
                    "optimal_times": optimal_times
                }
            })
            
    except Exception as e:
        # Log error untuk debug
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({
                "error": str(e),
                "debug": "Check Vercel function logs for details"
            })
        }
