import random
from kafka_client.data_model import Question
from modelling import IModel


class DummyModel(IModel):
    def get_answer(self, question: Question) -> int:
        return random.randint(0, len(question.answers) - 1)

    def load(self) -> None:
        self.is_loaded = True

    def unload(self) -> None:
        self.is_loaded = False
