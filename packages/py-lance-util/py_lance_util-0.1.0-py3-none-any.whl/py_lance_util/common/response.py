class Response:
    def __init__(self, success: bool, message: str, data: dict, code: int):
        self.success = success
        self.message = message
        self.data = data
        self.code = code

    @classmethod
    def success(cls, data: dict = {}, message: str = ''):
        return cls(True, message, data, 200)

    @classmethod
    def error(cls, message: str = "", code: int = 500):
        return cls(False, message, None, code)
