FROM python:3.5.6

RUN apt-get update
RUN apt-get install -y git
RUN git clone --single-branch --branch dev https://github.com/DECODEproject/bcnnow.git
RUN pip install -r bcnnow/apps/backend/requirements.txt

CMD python /bcnnow/apps/backend/api/v0/app.py