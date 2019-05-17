FROM httpd:2.4

# COPY ./public-html/ /usr/local/apache2/htdocs/

RUN apt-get update
RUN apt-get install -y git

# RUN rm -rf /usr/local/apache2/htdocs
RUN git clone --single-branch --branch dev https://github.com/DECODEproject/bcnnow.git

RUN cp -R bcnnow/apps/frontend/* /usr/local/apache2/htdocs/
