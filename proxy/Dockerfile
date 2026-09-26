FROM nginx:1.27-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom config
COPY nginx.conf /etc/nginx/nginx.conf

# Run as non-root (nginx user already exists in alpine image)
RUN chown -R nginx:nginx /var/cache/nginx /var/run /var/log/nginx

USER nginx

EXPOSE 8080 8081 8082 8084 8090
