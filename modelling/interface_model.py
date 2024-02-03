from kafka_client.data_model import Question


class IModel:
    def __init__(self) -> None:
        self.is_loaded: bool = False

    def get_answer(self, question: Question) -> int:
        raise NotImplementedError("You need to override `get_answer` method inside children class!")

    def load(self) -> None:
        raise NotImplementedError("You need to override `load` method inside children class!")

    def unload(self) -> None:
        raise NotImplementedError("You need to override `unload` method inside children class!")
