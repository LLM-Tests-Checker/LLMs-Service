import pytest
import typing as tp

from dotenv import load_dotenv

from server import TestCheckerServer
from kafka_client import KafkaClient
from kafka_client.data_model import LLMTestCheckRequest, LLMTestCheckResult, Test, Question, Answer


class MockKafkaClient(KafkaClient):
    def __init__(self, tests: list[Test], llm_slug: str):
        self._tests: list[Test] = tests
        self._llm_slug: str = llm_slug
        self._responses: list[LLMTestCheckResult] = []

    def requests_generator(self) -> tp.Generator[LLMTestCheckRequest, None, None]:
        for idx, test in enumerate(self._tests):
            yield LLMTestCheckRequest(
                id=str(idx),
                test=test,
                llm_slug=self._llm_slug,
            )

    def send_response(self, response: LLMTestCheckResult) -> None:
        self._responses.append(response)

    def stop(self) -> None:
        pass


@pytest.fixture
def test() -> Test:
    return Test(
        id="0",
        name="Тест по биологии за 6 класс.",
        description=None,
        questions=[
            Question(
                number=0,
                text="Фотосинтез называют также:",
                answers=[
                    Answer(number=0, text="почвенным питанием"),
                    Answer(number=1, text="дополнительным питанием"),
                    Answer(number=2, text="воздушным питанием"),
                ],
                llm_answer=None,
            ),
            Question(
                number=1,
                text="Хлоропластом называется:",
                answers=[
                    Answer(number=0, text="Часть листа, в которой происходит фотосинтез"),
                    Answer(number=1, text="Бесцветная пластида, в которой запасаются питательные вещества"),
                    Answer(number=2, text="Цветная пластида, которая придает окраску цветам"),
                    Answer(number=3, text="Зеленая пластида, в которой осуществляется фотосинтез"),
                ],
                llm_answer=None,
            ),
            Question(
                number=2,
                text="В результате фотосинтеза образуется:",
                answers=[
                    Answer(number=0, text="белки"),
                    Answer(number=1, text="крахмал"),
                    Answer(number=2, text="жиры"),
                    Answer(number=3, text="соли"),
                ],
                llm_answer=None,
            ),
            Question(
                number=3,
                text="Органические вещества двигаются из листьев к корням и цветам:",
                answers=[
                    Answer(number=0, text="По сосудам древесины"),
                    Answer(number=1, text="По ситовидным трубкам"),
                    Answer(number=2, text="По древесным волокнам"),
                    Answer(number=3, text="По камбию"),
                ],
                llm_answer=None,
            ),
            Question(
                number=4,
                text="Организмы, обладающие способностью сами образовывать органические вещества, называются:",
                answers=[
                    Answer(number=0, text="автотрофы"),
                    Answer(number=1, text="хемотрофы"),
                    Answer(number=2, text="гетеротрофы"),
                    Answer(number=3, text="потребители"),
                ],
                llm_answer=None,
            ),
            Question(
                number=5,
                text="фотосинтез протекает в:",
                answers=[
                    Answer(number=0, text="корнях"),
                    Answer(number=1, text="цветках"),
                    Answer(number=2, text="листьях"),
                    Answer(number=3, text="плодах"),
                ],
                llm_answer=None,
            ),
            Question(
                number=6,
                text="В результате фотосинтеза выделяется:",
                answers=[
                    Answer(number=0, text="вода"),
                    Answer(number=1, text="углекислый газ"),
                    Answer(number=2, text="чистый воздух"),
                    Answer(number=3, text="кислород"),
                ],
                llm_answer=None,
            ),
            Question(
                number=7,
                text="Космическая роль растений заключается в:",
                answers=[
                    Answer(number=0, text="образовании органических веществ"),
                    Answer(number=1, text="преобразовании энергии солнечного света"),
                    Answer(number=2, text="поглощение углекислого газа"),
                    Answer(number=3, text="выделение кислорода"),
                ],
                llm_answer=None,
            ),
            Question(
                number=8,
                text="Выберите неверное утверждение:",
                answers=[
                    Answer(number=0, text="в процессе фотосинтеза выделяется углекислый газ"),
                    Answer(number=1, text="для фотосинтеза необходим свет"),
                    Answer(number=2, text="для фотосинтеза необходим углекислый газ"),
                    Answer(number=3, text="в результате фотосинтеза образуются органические вещества"),
                ],
                llm_answer=None,
            ),
            Question(
                number=9,
                text="В результате фотосинтеза образуется",
                answers=[
                    Answer(number=0, text="вода"),
                    Answer(number=0, text="кислород"),
                    Answer(number=0, text="железо"),
                    Answer(number=0, text="углекислый газ"),
                ],
                llm_answer=None,
            ),
        ],
    )


def test_server(test: Test) -> None:
    server: TestCheckerServer = TestCheckerServer("localhost", 9999, "llm_tests_launch_tasks", "llm_tests_results")
    server.kafka_client = MockKafkaClient([test], "dummy")
    server.run()

    for question in server.kafka_client._responses[0].target_test.questions:
        assert question.llm_answer is not None
        assert 0 <= question.llm_answer < len(question.answers)

    server.stop()


def test_server_with_gigachat_model(test: Test) -> None:
    load_dotenv()
    server: TestCheckerServer = TestCheckerServer("localhost", 999, "llm_tests_launch_tasks", "llm_tests_results")
    server.kafka_client = MockKafkaClient([test], "gigachat")
    server.run()

    num_correct_answers: int = 0
    correct_answers: list[int] = [2, 3, 1, 1, 0, 2, 3, 1, 0, 1]
    for question, correct_answer in zip(server.kafka_client._responses[0].target_test.questions, correct_answers):
        assert question.llm_answer is not None
        num_correct_answers += (correct_answer == question.llm_answer)

    assert num_correct_answers > 5
    server.stop()
