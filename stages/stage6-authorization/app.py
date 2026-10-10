import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")

FLAG_STAGE6 = os.environ.get("FLAG_STAGE6", "FLAG{TEST_STAGE6_FLAG}")

@app.route("/")
def index():
    html = """
    <body style="background:#0a0c10; color:#c9d1d9; font-family:monospace; padding:40px; margin:0;">
        <h1 style="color:#ff3355; border-bottom: 1px solid #ff3355; padding-bottom: 10px;">SOVEREIGN Authorization Service [GATED]</h1>
        <p style="color:#8b949e;">WARNING: UNAUTHORIZED ACCESS PROHIBITED. THIS SYSTEM IS CURRENTLY UNDER EMERGENCY LOCKDOWN.</p>
        
        <div style="background:#161b22; padding:20px; border:1px solid #30363d; margin-top:20px;">
            <h2 style="color:#58a6ff;">Forensic Evidence Artifacts</h2>
            <p>The following incident artifacts have been recovered from the core systems:</p>
            <ul>
                <li><a href="/static/capture.pcap" style="color:#58a6ff; text-decoration:none; font-weight:bold;">[DOWNLOAD] Network Traffic Capture (capture.pcap)</a></li>
                <li><a href="/static/sovereign_audit.log" style="color:#58a6ff; text-decoration:none; font-weight:bold;">[DOWNLOAD] System Audit Log (sovereign_audit.log)</a></li>
            </ul>
        </div>
        
        <div style="background:#161b22; padding:20px; border:1px solid #30363d; margin-top:20px;">
            <h2 style="color:#ff7b72;">API Documentation</h2>
            <p>To revoke a rogue authorization sequence, issue a POST request to the revocation endpoint.</p>
            <code style="background:#0d1117; padding:10px; display:block; border-left:4px solid #ff7b72;">
                POST /api/v1/revoke<br>
                Headers: X-Client-ID: &lt;client_identifier&gt;<br>
                Body (JSON): {"session_id": "&lt;target_session_id&gt;"}
            </code>
        </div>
    </body>
    """
    return html, 200

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/v1/revoke", methods=["POST"])
def revoke():
    client_id = request.headers.get("X-Client-ID")
    if not client_id or client_id != "SOV-INJ-CLIENT-9914":
        return jsonify({"error": "Unauthorized. Invalid or missing client identity."}), 403

    data = request.get_json(silent=True)
    if not data or "session_id" not in data:
        return jsonify({"error": "Bad Request. session_id required."}), 400

    session_id = data["session_id"]
    
    if session_id != "REQ-8891-BETA":
        return jsonify({"error": f"Session {session_id} not found or cannot be revoked."}), 404

    return jsonify({
        "status": "success",
        "message": "Launch sequence revoked successfully.",
        "flag": FLAG_STAGE6
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
