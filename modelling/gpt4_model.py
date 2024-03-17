import logging

from openai import OpenAI
from openai.types.chat import ChatCompletion

from modelling import IModel
from kafka_client.data_model import Question


class GPT4Model(IModel):
    def __init__(self, credentials: str) -> None:
        self.is_loaded: bool = False
        self.credentials: str = credentials
        self._model: OpenAI | None = None

        self._possible_answers: str = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЫЭЮЯ"

    def get_answer(self, question: Question) -> int:
        assert self.is_loaded and self._model is not None, "You need load model first, call `load()` method."

        response: ChatCompletion = self._model.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ниже приведен вопрос с множественным выбором. "
                                              "Твой ответ должен содержать единственный символ - букву правильного ответа."},
                {"role": "user", "content": self._format_question(question)},
            ],
        )

        if response.choices[0].message.content is None:
            logging.warn("GPT-4 answer is None!")
            return 0

        if response.choices[0].message.content[0] not in self._possible_answers[:len(question.answers)]:
            logging.warn("GPT-4 answer is not in possible options!")
            return 0

        return self._possible_answers.index(response.choices[0].message.content[0])

    def load(self) -> None:
        if self.is_loaded:
            return

        self.is_loaded = True
        self.model = OpenAI(api_key=self.credentials)

    def unload(self) -> None:
        self.is_loaded = False
        self._model = None

    def _format_question(self, question: Question) -> str:
        prompt: str = f"Вопрос: {question.text}\nВарианты ответа:\n"
        for symbol, answer in zip(self._possible_answers, question.answers):
            prompt += f"{symbol}: {answer.text}\n"
        prompt += "Правильный ответ: "
        return prompt
