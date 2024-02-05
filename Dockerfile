FROM python:3.12

WORKDIR /server
COPY . .

RUN pip install -U pip setuptools
RUN pip install -r requirements.txt

ENV KAFKA_BROKER_ADDR=localhost
ENV KAFKA_BROKER_PORT=29092
ENV KAFKA_REQUEST_TOPIC=llm_tests_launch_tasks
ENV KAFKA_RESPONSE_TOPIC=llm_tests_results

CMD ["python3", "run.py"]
