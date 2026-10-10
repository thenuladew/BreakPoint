with open("proxy/nginx.conf", "r") as f:
    config = f.read()

replacement = """        location /api/v1/revoke {
            limit_req zone=challenge_limit burst=10 nodelay;
            proxy_pass         $upstream_stage6;
            proxy_set_header   Host              $host;
            proxy_set_header   X-Real-IP         $remote_addr;
            proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        }

        location / {"""

config = config.replace("        location / {", replacement)

with open("proxy/nginx.conf", "w") as f:
    f.write(config)
