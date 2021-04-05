class Calculator():
    @staticmethod
    def calculate(input_value: int):
        f_n = f_n_next = 1
        input_value = input_value - 2
        while input_value > 0:
            f_n, f_n_next = f_n_next, f_n + f_n_next
            input_value -= 1
        return f_n_next
