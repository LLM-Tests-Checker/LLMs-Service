import typing as tp

from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Answer:
    number: int
    text: str

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "Answer":
        return Answer(number=data["number"], text=data["text"])

    def to_dict(self) -> dict[str, tp.Any]:
        return {"number": self.number, "text": self.text}


@dataclass
class Question:
    number: int
    text: str
    answers: list[Answer]
    llm_answer: int | None

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "Question":
        return Question(
            number=data["number"],
            text=data["text"],
            answers=[Answer.from_dict(dict_answer) for dict_answer in data["answers"]],
            llm_answer=data.get("llm_answer", None),
        )

    def to_dict(self) -> dict[str, tp.Any]:
        return {
            "number": self.number,
            "text": self.text,
            "answers": [answer.to_dict() for answer in self.answers],
            "llm_answer": self.llm_answer,
        }


@dataclass
class Test:
    id: str
    name: str
    description: tp.Optional[str]
    questions: list[Question]

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "Test":
        return Test(
            id=data["id"],
            name=data["name"],
            description=data.get("description", None),
            questions=[Question.from_dict(dict_question) for dict_question in data["questions"]],
        )

    def to_dict(self) -> dict[str, tp.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "questions": [question.to_dict() for question in self.questions],
        }


@dataclass
class LLMTestCheckRequest:
    id: str
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
class LLMTestCheckResult:
    id: str
    target_test: Test
    created_at: datetime = field(default_factory=lambda: datetime.now())

    @staticmethod
    def from_dict(data: dict[str, tp.Any]) -> "LLMTestCheckResult":
        return LLMTestCheckResult(
            id=data["id"],
            target_test=Test.from_dict(data["target_test"]),
            created_at=data.get("created_at", datetime.now()),
        )

    def to_dict(self) -> dict[str, tp.Any]:
        return {
            "id": self.id,
            "target_test": self.target_test.to_dict(),
            "created_at": self.created_at,
        }

    def to_response_dict(self) -> dict[str, tp.Any]:
        return {
            "id": self.id,
            "target_test_id": self.target_test.id,
            "created_at": self.created_at.timestamp(),
            "answers": [
                {
                    "question_number": question.number,
                    "selected_answer_number": question.llm_answer,
                } for question in self.target_test.questions
            ]
        }
