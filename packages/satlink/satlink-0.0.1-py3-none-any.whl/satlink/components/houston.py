from .downlink import Downlink


class Houston(Exception):
    def __init__(self, message, code=500):
        message = f"Houston we have a problem! {message}"
        self.downlink = Downlink().code(code).text(message)
        super().__init__(message)
