class LLM_model:
    _self = None
    model = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self) -> None:
        pass

    def generate_text(self) -> str:
        return 'abc wiktor chuj'


if __name__ == '__main__':
    print(LLM_model().generate_text())
