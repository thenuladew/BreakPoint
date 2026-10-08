FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf /etc/nginx/nginx.conf 2>/dev/null || true

COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /usr/share/nginx/html/

RUN chown -R nginx:nginx \
             /var/log/nginx \
             /usr/share/nginx/html

USER nginx

EXPOSE 80
