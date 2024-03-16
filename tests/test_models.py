import os
import pytest

from dotenv import load_dotenv

from kafka_client.data_model import Question
from modelling import DummyModel, GigaChatModel


@pytest.mark.parametrize(("num_answers",), [(1,), (3,), (5,), (10,)])
def test_dummy_model(num_answers: int) -> None:
    model: DummyModel = DummyModel()
    question: Question = Question.from_dict({
        "number": 0,
        "text": "Question 0",
        "answers": [{"number": i, "text": f"Answer {i}"} for i in range(num_answers)]
    })
    assert 0 <= model.get_answer(question) < num_answers


def test_gigachat_model() -> None:
    load_dotenv()
    model: GigaChatModel = GigaChatModel(credentials=os.getenv("GIGACHAT_CREDENTIALS", ""))
    model.load()
    question: Question = Question.from_dict({
        "number": 0,
        "text": "К какому уровню организации живой природы относится морская черепаха?",
        "answers": [
            {"number": 0, "text": "биосферному"},
            {"number": 1, "text": "клеточному"},
            {"number": 2, "text": "организменному"},
            {"number": 3, "text": "популяционному"},
        ]
    })

    assert model.get_answer(question) == 2
