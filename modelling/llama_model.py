import gc
import logging
import typing as tp

from llama_cpp import Llama

from modelling import IModel
from kafka_client.data_model import Question


class LLamaModel(IModel):
    def __init__(self, checkpoint_path: str) -> None:
        self.is_loaded: bool = False
        self._model: Llama | None = None
        self._checkpoint_path: str = checkpoint_path

        self._possible_answers: str = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЫЭЮЯ"

    def get_answer(self, question: Question) -> int:
        response: dict[str, tp.Any] = self._model(self._format_question(question), max_tokens=2)
        if response["choices"][0]["text"].strip()[0] not in self._possible_answers[:len(question.answers)]:
            logging.warn("LLaMA answer is not in possible options!")
            return 0

        return self._possible_answers.index(response["choices"][0]["text"].strip()[0])

    def load(self) -> None:
        if self.is_loaded:
            return

        self.is_loaded = True
        self._model = Llama(model_path=self._checkpoint_path, seed=1337)

    def unload(self) -> None:
        self.is_loaded = False
        self._model = None
        gc.collect()

    def _format_question(self, question: Question) -> str:
        prompt: str = f"Вопрос: {question.text}\nВарианты ответа:\n"
        for symbol, answer in zip(self._possible_answers, question.answers):
            prompt += f"{symbol}: {answer.text}\n"
        prompt += "Правильный ответ: "
        return prompt
