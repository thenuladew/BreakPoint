import re
with open("platform/app.py", "r") as f:
    content = f.read()

replacement = """@app.route("/api/check_stage6_access")
def check_stage6_access():
    token = request.headers.get("X-Team-Token")
    if not token:
        token = session.get("team_token")
    if not token:
        return "No token", 403
        
    team = get_team_from_token(token)
    if not team:
        return f"Invalid team {token}", 403

    solved = get_solved_stages(team["id"])
    if 5 not in solved:
        return f"Stage 5 not solved. Solved: {solved}", 403

    timer = get_timer(team["id"])
    if timer["expired"]:
        return "Timer expired", 403
        
    return "OK", 200
"""

content = re.sub(
    r'@app\.route\("/api/check_stage6_access"\).*?return "OK", 200', 
    replacement, 
    content, 
    flags=re.DOTALL
)

with open("platform/app.py", "w") as f:
    f.write(content)
