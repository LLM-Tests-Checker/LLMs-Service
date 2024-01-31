import typing as tp

from datetime import datetime
from dataclasses import dataclass


@dataclass
class Answer:
    number: int
    text: str
    is_correct: bool

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "Answer":
        return Answer(number=data["number"], text=data["text"], is_correct=data["is_correct"])

    def to_dict(self) -> dict[str, tp.Any]:
        return {"number": self.number, "text": self.text, "is_correct": self.is_correct}


@dataclass
class Question:
    number: int
    text: str
    answers: list[Answer]

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "Question":
        return Question(
            number=data["number"],
            text=data["text"],
            answers=[Answer.from_dict(dict_answer) for dict_answer in data["answers"]],
        )

    def to_dict(self) -> dict[str, tp.Any]:
        return {
            "number": self.number,
            "text": self.text,
            "answers": [answer.to_dict() for answer in self.answers],
        }


@dataclass
class Test:
    id: int
    name: str
    description: str
    questions: list[Question]

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "Test":
        return Test(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            questions=[Question.from_dict(dict_question) for dict_question in data["questions"]],
        )

    def to_dict(self) -> dict[str, tp.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "descriptions": self.description,
            "questions": [question.to_dict() for question in self.questions],
        }


@dataclass
class LLMTestCheckRequest:
    id: int
    test: Test
    llm_slug: str

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "LLMTestCheckRequest":
        return LLMTestCheckRequest(
            id=data["id"],
            test=Test.from_dict(data["test"]),
            llm_slug=data["llm_slug"],
        )

    def to_dict(self) -> dict[str, tp.Any]:
        return {
            "id": self.id,
            "test": self.test.to_dict(),
            "llm_slug": self.llm_slug,
        }


@dataclass
class QueryCheckResult:
    llm_slug: str
    answers: tp.List[tp.Dict[str, int]]

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "QueryCheckResult":
        return QueryCheckResult(llm_slug=data["llm_slug"], answers=data["answers"])

    def to_dict(self) -> dict[str, tp.Any]:
        return {"llm_slug": self.llm_slug, "answers": self.answers}


@dataclass
class LLMTestCheckResult:
    id: int
    target_test_id: int
    created_at: datetime
    results: QueryCheckResult

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "LLMTestCheckResult":
        return LLMTestCheckResult(
            id=data["id"],
            target_test_id=data["target_test_id"],
            created_at=datetime.now(),
            results=QueryCheckResult.from_dict(data["result"])
        )

    def to_dict(self) -> dict[str, tp.Any]:
        return {
            "id": self.id,
            "target_test_id": self.target_test_id,
            "created_at": self.created_at,
            "results": self.results.to_dict(),
        }
