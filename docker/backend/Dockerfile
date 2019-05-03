FROM python:3.5

RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/DECODEproject/bcnnow.git
WORKDIR /bcnnow
RUN pip install -r apps/backend/requirements.txt
CMD python apps/backend/api/v0
