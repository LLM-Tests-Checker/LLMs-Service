class IModel:
    def __init__(self) -> None:
        raise NotImplementedError("You need to override `__init__` method inside children class!")

    def get_answer(self, query: str, asnwers: list[str]) -> int:
        raise NotImplementedError("You need to override `get_answer` method inside children class!")
