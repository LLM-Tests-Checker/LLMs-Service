import os
import pytest

from dotenv import load_dotenv

from kafka_client.data_model import Question, Answer
from modelling import DummyModel, GigaChatModel, GPT4Model, LLamaModel


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


def test_dummy_model(question: Question) -> None:
    model: DummyModel = DummyModel()
    assert 0 <= model.get_answer(question) < 4


def test_gigachat_model(question: Question) -> None:
    load_dotenv()
    model: GigaChatModel = GigaChatModel(credentials=os.getenv("GIGACHAT_CREDENTIALS", ""))
    model.load()
    assert model.get_answer(question) == 2


def test_gpt4_model(question: Question) -> None:
    load_dotenv()
    model: GPT4Model = GPT4Model(credentials=os.getenv("GPT4_CREDENTIALS", ""))
    model.load()
    assert model.get_answer(question) == 2


def test_llama_model(question: Question) -> None:
    load_dotenv()
    model: LLamaModel = LLamaModel(checkpoint_path="...")
    model.load()
    assert model.get_answer(question) == 2
