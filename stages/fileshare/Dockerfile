FROM nginx:1.27-alpine

# Remove default conf
RUN rm /etc/nginx/conf.d/default.conf /etc/nginx/nginx.conf 2>/dev/null || true

# Copy our full standalone config
COPY nginx.conf /etc/nginx/nginx.conf

# Pre-create dirs needed by nginx worker and log, owned by nginx user
RUN mkdir -p /usr/share/nginx/html \
    && chown -R nginx:nginx \
             /var/log/nginx \
             /usr/share/nginx/html

USER nginx

EXPOSE 80
