FROM python:3.7

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN mkdir data

COPY main.py ./main.py

RUN python3 main.py
