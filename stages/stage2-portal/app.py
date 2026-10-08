from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def stub(path):
    return "<h1 style='font-family:monospace;color:#00ff88;background:#0a0c10;padding:40px'>Stage 2 – Contractor Portal (Under Construction)</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
