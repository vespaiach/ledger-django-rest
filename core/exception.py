import json


def throw_validation_error(message, extra={}):
    raise AppValidationError(message, extra)


class AppValidationError(Exception):
    def __init__(self, message, extra={}):
        super().__init__(message)

        self.extra = extra
        self.message = message

    def to_json(self):
        return json.dumps(dict(message=self.message, extra=self.extra))
