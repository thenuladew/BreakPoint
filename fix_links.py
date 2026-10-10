import re
with open("platform/templates/dashboard.html", "r") as f:
    content = f.read()
content = re.sub(r'http://localhost:([0-9]+)', r'http://{{ request.host.split(":")[0] }}:\1', content)
with open("platform/templates/dashboard.html", "w") as f:
    f.write(content)
