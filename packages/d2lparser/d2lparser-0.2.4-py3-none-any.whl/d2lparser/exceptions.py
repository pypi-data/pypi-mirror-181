

class NoDataException(Exception):
    def __init__(self, data, message="Message has no data available"):
        self.data = data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.data} -> {self.message}'


class HeaderException(Exception):
    pass


class PayloadException(Exception):
    def __init__(self, data, data_len, message="Message is too short for message length"):
        self.data = data
        self.data_len = data_len
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.data} ({self.data_len}) -> {self.message}'
