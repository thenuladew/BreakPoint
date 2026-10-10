import re

with open("proxy/nginx.conf", "r") as f:
    config = f.read()

# Replace the specific block in the port 8090 server
replacement = """    # ──────────────────────────────────────────────────────────
    # PORT 8090 – Stage 6: SOVEREIGN Authorization (UNLOCKED)
    # ──────────────────────────────────────────────────────────
    server {
        listen 8090;
        server_name _;

        set $upstream_stage6    http://stage6:5000;

        location / {
            limit_req zone=challenge_limit burst=10 nodelay;
            proxy_pass         $upstream_stage6;
            proxy_set_header   Host              $host;
            proxy_set_header   X-Real-IP         $remote_addr;
            proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        }
    }
}
"""

config = re.sub(
    r'    # ──────────────────────────────────────────────────────────\n    # PORT 8090.*?}\n}',
    replacement,
    config,
    flags=re.DOTALL
)

with open("proxy/nginx.conf", "w") as f:
    f.write(config)
