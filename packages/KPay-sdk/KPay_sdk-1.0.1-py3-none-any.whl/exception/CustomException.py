class CustomException(Exception) :
    __code: int
    __message: str

    def __init__(self, code:int, message: str):
        super().__init__(message)
        self.__message = message
        self.__code = code

    def get_code(self) -> int:
        return self.__code

    def get_message(self) -> str:
        return self.__message