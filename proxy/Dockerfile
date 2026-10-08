FROM nginx:1.27-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom config
COPY nginx.conf /etc/nginx/nginx.conf

# Pre-create all dirs the nginx worker needs to write to,
# owned by the nginx user. Do this as root before USER switch.
# /tmp/nginx.pid is used by our config (avoids needing /var/run write)
RUN mkdir -p /var/cache/nginx/client_temp \
             /var/cache/nginx/proxy_temp \
             /var/cache/nginx/fastcgi_temp \
             /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp \
    && chown -R nginx:nginx \
             /var/cache/nginx \
             /var/log/nginx \
             /etc/nginx/conf.d

USER nginx

EXPOSE 8080 8081 8082 8084 8090
