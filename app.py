from flask import Flask, jsonify
import os

app = Flask(__name__)

LOG_FILE = "logs.txt"

def search_logs(keyword):
    if not os.path.exists(LOG_FILE):
        return {"error": "logs.txt dosyası bulunamadı!", "results": []}
    
    results = []
    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            if keyword.lower() in line.lower():
                results.append({
                    "line": line_num,
                    "content": line.strip()
                })
    
    return {
        "status": "success",
        "keyword": keyword,
        "total_found": len(results),
        "results": results[:100]   # Maksimum 100 sonuç
    }

@app.route('/')
def home():
    return """
    <h1>Log API Çalışıyor ✅</h1>
    <p>Kullanım: /kelime</p>
    <p>Örnek: <a href="/netflix">/netflix</a> veya <a href="/spotify">/spotify</a></p>
    """

@app.route('/<keyword>')
def search(keyword):
    result = search_logs(keyword)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
