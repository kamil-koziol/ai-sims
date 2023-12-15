from typing import List
import requests
import json

HOST = 'localhost'
PORT = '8889'


class LLM_model:
    _self = None
    model = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self) -> None:
        pass

    @staticmethod
    def generate_text(prompt: str) -> str:
        body = {"text": prompt}
        body = json.dumps(body)
        response = requests.post(f'http://{HOST}:{PORT}/generate', data=body)
        return response


class EmbendingModel:
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self) -> None:
        pass

    @staticmethod
    def tokenize(text: str) -> List[float]:
        body = {"text": text}
        body = json.dumps(body)
        response = requests.post(f'http://{HOST}:{PORT}/embed', data=body)
        return response


if __name__ == '__main__':
    print(LLM_model().generate_text('Who is John Cena').content)
