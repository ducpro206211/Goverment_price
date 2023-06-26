FROM python:3.8.5-slim-buster

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --upgrade -r /code/requirements.txt
COPY . /code

#CMD ["/bin/bash", "-c", "cd app/;uvicorn main:app --host 0.0.0.0 --port 9000"]