class CalculateRequest:
    def __init__(self, number: int):
        self.number = number


class CalculateResponse:
    def __init__(self, result: int):
        self.output_value = result