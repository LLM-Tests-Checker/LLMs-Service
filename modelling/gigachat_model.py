import logging

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole, ChatCompletion

from modelling import IModel
from kafka_client.data_model import Question


class GigaChatModel(IModel):
    def __init__(self, credentials: str) -> None:
        self.is_loaded: bool = False
        self.credentials: str = credentials
        self._model: GigaChat | None = None

        self._possible_answers: str = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЫЭЮЯ"

    def get_answer(self, question: Question) -> int:
        assert self.is_loaded and self._model is not None, "You need load model first, call `load()` method."

        payload: Chat = Chat(
            max_tokens=2,
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content="Ниже приведен вопрос с множественным выбором. "
                            "Твой ответ должен содержать единственный символ - букву правильного ответа.",
                ),
                Messages(
                    role=MessagesRole.USER,
                    content=self._format_question(question),
                )
            ],
        )

        response: ChatCompletion = self._model.chat(payload=payload)
        if response.choices[0].message.content[0] not in self._possible_answers[:len(question.answers)]:
            logging.warn("Gigachat answer is not in possible options!")
            return 0

        return self._possible_answers.index(response.choices[0].message.content[0])

    def load(self) -> None:
        if self.is_loaded:
            return

        self.is_loaded = True
        self._model = GigaChat(model="GigaChat-Pro", credentials=self.credentials, verify_ssl_certs=False)

    def unload(self) -> None:
        self.is_loaded = False
        self._model = None

    def _format_question(self, question: Question) -> str:
        prompt: str = f"Вопрос: {question.text}\nВарианты ответа:\n"
        for symbol, answer in zip(self._possible_answers, question.answers):
            prompt += f"{symbol}: {answer.text}\n"
        prompt += "Правильный ответ: "
        return prompt
