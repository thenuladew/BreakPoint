import re

with open("platform/app.py", "r") as f:
    content = f.read()

replacement = """@app.route("/api/check_stage6_access")
def check_stage6_access():
    \"\"\"
    Nginx auth_request endpoint.
    \"\"\"
    import sys
    print("CHECK_STAGE6: headers=", dict(request.headers), file=sys.stderr)
    print("CHECK_STAGE6: cookies=", request.cookies, file=sys.stderr)
    print("CHECK_STAGE6: session=", dict(session), file=sys.stderr)
    
    token = request.headers.get("X-Team-Token")
    if not token:
        token = session.get("team_token")
    if not token:
        print("CHECK_STAGE6: No token found", file=sys.stderr)
        abort(403)
        
    team = get_team_from_token(token)
    if not team:
        print("CHECK_STAGE6: Invalid team for token", token, file=sys.stderr)
        abort(403)

    solved = get_solved_stages(team["id"])
    print("CHECK_STAGE6: solved=", solved, file=sys.stderr)
    if 5 not in solved:
        print("CHECK_STAGE6: Stage 5 not solved", file=sys.stderr)
        abort(403)

    timer = get_timer(team["id"])
    if timer["expired"]:
        print("CHECK_STAGE6: Timer expired", file=sys.stderr)
        abort(403)
        
    print("CHECK_STAGE6: Access GRANTED", file=sys.stderr)
    return "OK", 200
"""

# Replace the current check_stage6_access block
content = re.sub(
    r'@app\.route\("/api/check_stage6_access"\).*?if timer\["expired"\]:\n        abort\(403\)', 
    replacement, 
    content, 
    flags=re.DOTALL
)

with open("platform/app.py", "w") as f:
    f.write(content)
