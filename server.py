import logging

from kafka_client import KafkaClient, LLMTestCheckResult
from modelling import IModel, DummyModel


class TestCheckerServer:
    def __init__(self, kafka_broker_addr: str, kafka_broker_port: int, kafka_request_topic: str, kafka_response_topic: str):
        self.kafka_broker_ip: str = f"{kafka_broker_addr}:{kafka_broker_port}"
        self.kafka_request_topic: str = kafka_request_topic
        self.kafka_response_topic: str = kafka_response_topic

        self.kafka_client: KafkaClient = KafkaClient(kafka_broker_addr, kafka_broker_port, kafka_request_topic, kafka_response_topic)
        self.models: dict[str, IModel] = {
            "dummy_model": DummyModel(),
        }

    def run(self) -> None:
        logging.info(f"Running server is connected to {self.kafka_broker_ip}.")
        logging.info(f"Listening requests from `{self.kafka_request_topic}` topic.")
        logging.info(f"Responses will be sent to `{self.kafka_response_topic}` topic.")

        try:
            self._run_impl()
        except KeyboardInterrupt:
            logging.info("Server was manually interrupted. Stopping...")
        except Exception as err:
            logging.error(f"Server got exception: {err}. Stopping...")
        finally:
            self.stop()

    def stop(self) -> None:
        for model in self.models.values():
            model.unload()
        self.kafka_client.stop()

    def _run_impl(self) -> None:
        for request in self.kafka_client.requests_generator():
            logging.info(f"Got request with id=`{request.id}`")
            if request.llm_slug not in self.models:
                logging.warning(f"Model with llm_slug=`{request.llm_slug}` does not exists. This request is skipped.")
                continue

            self._load_requested_model(request.llm_slug)
            for question in request.test.questions:
                question.llm_answer = self.models[request.llm_slug].get_answer(question)

            self.kafka_client.send_response(LLMTestCheckResult(
                id=request.id,
                target_test=request.test,
                llm_slug=request.llm_slug,
            ))
            logging.info(f"Send response to request with id=`{request.id}`")

    def _load_requested_model(self, requested_llm_slug: str) -> None:
        if self.models[requested_llm_slug].is_loaded:
            return

        for model in self.models.values():
            model.unload()

        self.models[requested_llm_slug].load()
