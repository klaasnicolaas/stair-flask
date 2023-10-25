FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# # chown all the files to the nginx user
# RUN chown -R nginx:nginx /etc/nginx

# # change to the nginx user
# USER nginx
