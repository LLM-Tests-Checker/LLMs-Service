FROM python:3.12

WORKDIR /server
COPY . .

RUN pip install -U pip setuptools
RUN pip install -r requirements.txt

CMD ["python3", "run.py"]
