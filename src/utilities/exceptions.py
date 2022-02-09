class DynamoDBError(Exception):
    """Exception class which represents a response error of DynamoDB"""


class ValidationError(Exception):
    """Exception class which represents a different story validation errors"""


class RootDoesNotExistValidationError(ValidationError):
    def __init__(self, *args):
        MESSAGE = "The provided root node does not exist"
        super().__init__(args[0] if args else MESSAGE)


class ExistsCircleValidationError(ValidationError):
    def __init__(self, *args):
        MESSAGE = "The story branch has no end"
        super().__init__(args[0] if args else MESSAGE)


class UnconnectedNodeValidationError(ValidationError):
    def __init__(self, *args):
        MESSAGE = "The story has unused node"
        super().__init__(args[0] if args else MESSAGE)


class UnrelatedReferenceValidationError(ValidationError):
    def __init__(self, *args):
        MESSAGE = "The story node has link to uncreated branch"
        super().__init__(args[0] if args else MESSAGE)


class ParseGraphError(ValidationError):
    def __init__(self, *args):
        MESSAGE = "The story item has unsupported structure"
        super().__init__(args[0] if args else MESSAGE)
