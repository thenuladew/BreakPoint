import re

with open("platform/app.py", "r") as f:
    content = f.read()

replacement = """@app.route("/api/check_stage6_access")
def check_stage6_access():
    \"\"\"
    Nginx auth_request endpoint.
    Returns 200 if team has solved Stage 5 AND timer is active.
    Returns 403 otherwise.
    Token comes from X-Team-Token header forwarded by Nginx or session cookie.
    \"\"\"
    token = request.headers.get("X-Team-Token")
    if not token:
        token = session.get("team_token")
    if not token:
        abort(403)
    team = get_team_from_token(token)
    if not team:
        abort(403)

    solved = get_solved_stages(team["id"])
    if 5 not in solved:
        abort(403)

    timer = get_timer(team["id"])
    if timer["expired"]:
        abort(403)
"""

content = re.sub(
    r'@app\.route\("/api/check_stage6_access"\).*?if timer\["expired"\]:\n        abort\(403\)', 
    replacement, 
    content, 
    flags=re.DOTALL
)

with open("platform/app.py", "w") as f:
    f.write(content)

