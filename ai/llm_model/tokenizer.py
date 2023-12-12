from typing import List

class LLM_tokenizer:
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self) -> None:
        pass

    @staticmethod
    def tokenize(text: str) -> List[float]:
        return [1.2, 3.3, 0.3]


if __name__ == '__main__':
    pass
