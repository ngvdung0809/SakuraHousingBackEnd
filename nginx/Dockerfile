FROM nginx
WORKDIR /etc/nginx
RUN rm /etc/nginx/nginx.conf
ADD nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/*
ADD customized.conf /etc/nginx/conf.d/
ADD uwsgi_params /etc/nginx/conf.d/
ADD wait-for-it.sh ./