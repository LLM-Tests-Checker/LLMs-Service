import json
import typing as tp

from confluent_kafka import Consumer, Producer, Message
from kafka_client.data_model import LLMTestCheckRequest


class KafkaClient:
    def __init__(self, kafka_broker_ip: str, kafka_broker_port: int, request_topic_name: str):
        self.consumer: Consumer = Consumer({
            "bootstrap.servers": f"{kafka_broker_ip}:{kafka_broker_port}",
            "group.id": 0,
            "auto.offset.reset": "earliest",
        })
        self.consumer.subscribe([request_topic_name])

        self.producer: Producer = Producer({"bootstrap.servers": f"{kafka_broker_ip}:{kafka_broker_port}"})

    def requests_generator(self) -> tp.Generator[tp.Optional[LLMTestCheckRequest], None, None]:
        while True:
            message: Message = self.consumer.poll(timeout=1.0)

            if message is None:
                continue

            if message.error():
                print(f"Got message with error: {message.error()}")
                continue

            try:
                dict_request: dict[str, tp.Any] = json.loads(message.value())
                yield LLMTestCheckRequest.from_dict(dict_request)
            except json.JSONDecodeError as err:
                print(f"Can't decode request json: {err}")
            except Exception as err:
                print(f"Something went wrong in decoding request! Error: {err}")
