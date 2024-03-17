import os
import pytest

from dotenv import load_dotenv

from kafka_client.data_model import Question, Answer
from modelling import DummyModel, GigaChatModel


@pytest.fixture
def question() -> Question:
    return Question(
        number=0,
        text="К какому уровню организации живой природы относится морская черепаха?",
        answers=[
            Answer(number=0, text="биосферному"),
            Answer(number=1, text="клеточному"),
            Answer(number=2, text="организменному"),
            Answer(number=3, text="популяционному"),
        ],
        llm_answer=None,
    )


@pytest.mark.parametrize(("num_answers",), [(1,), (3,), (5,), (10,)])
def test_dummy_model(question: Question, num_answers: int) -> None:
    model: DummyModel = DummyModel()
    assert 0 <= model.get_answer(question) < num_answers


def test_gigachat_model(question: Question) -> None:
    load_dotenv()
    model: GigaChatModel = GigaChatModel(credentials=os.getenv("GIGACHAT_CREDENTIALS", ""))
    model.load()
    assert model.get_answer(question) == 2
