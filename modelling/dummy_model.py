import random

from modelling import IModel
from kafka_client.data_model import Question


class DummyModel(IModel):
    def get_answer(self, question: Question) -> int:
        return random.randint(0, len(question.answers) - 1)

    def load(self) -> None:
        self.is_loaded = True

    def unload(self) -> None:
        self.is_loaded = False
