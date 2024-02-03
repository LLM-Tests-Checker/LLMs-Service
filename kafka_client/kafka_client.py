import json
import typing as tp

from confluent_kafka import Consumer, Producer, Message, KafkaError
from kafka_client.data_model import LLMTestCheckRequest, LLMTestCheckResult


class KafkaClient:
    def __init__(self, kafka_broker_addr: str, kafka_broker_port: int, request_topic: str, response_topic: str):
        self.request_topic: str = request_topic
        self.response_topic: str = response_topic

        self.consumer: Consumer = Consumer({
            "bootstrap.servers": f"{kafka_broker_addr}:{kafka_broker_port}",
            "group.id": 0,
            "auto.offset.reset": "earliest",
        })
        self.consumer.subscribe([request_topic])

        self.producer: Producer = Producer({"bootstrap.servers": f"{kafka_broker_addr}:{kafka_broker_port}"})

    def requests_generator(self) -> tp.Generator[LLMTestCheckRequest, None, None]:
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

            self.producer.flush()

    def send_response(self, response: LLMTestCheckResult) -> None:
        self.producer.produce(
            topic=self.response_topic,
            value=json.dumps(response.to_response_dict()).encode("utf-8"),
            on_delivery=self._delivery_report,
        )

    def stop(self) -> None:
        self.consumer.close()

    def _delivery_report(self, error: KafkaError, message: Message) -> None:
        if error is not None:
            print(f"Response delivery failed: {error}")
