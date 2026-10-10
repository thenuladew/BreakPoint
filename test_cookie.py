with open("proxy/nginx.conf", "r") as f:
    c = f.read()
c = c.replace(
    "log_format main '$remote_addr - $remote_user [$time_local] '", 
    "log_format main '$remote_addr - $remote_user [$time_local] [COOKIE: $http_cookie] '"
)
with open("proxy/nginx.conf", "w") as f:
    f.write(c)
