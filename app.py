from flask import Flask, jsonify
import os

app = Flask(__name__)

# Log dosyasının yolu (Render'da /app/logs.txt olacak)
LOG_FILE = "/app/logs.txt"

def search_logs(keyword):
    if not os.path.exists(LOG_FILE):
        return {"error": "logs.txt dosyası bulunamadı", "results": []}
    
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
        "results": results[:150]
    }

@app.route('/')
def home():
    return "Log API Çalışıyor! Örnek: /netflix"

@app.route('/<keyword>')
def search(keyword):
    result = search_logs(keyword)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
