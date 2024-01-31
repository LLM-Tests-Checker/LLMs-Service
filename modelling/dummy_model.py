import random


class DummyModel:
    def get_answer(self, query: str, answers: list[str]) -> int:
        return random.randint(0, len(answers) - 1)
