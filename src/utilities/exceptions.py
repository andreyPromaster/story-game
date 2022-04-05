class DynamoDBError(Exception):
    """Exception class which represents a response error of DynamoDB"""


class ValidationError(Exception):
    """Exception class which represents a different story validation errors"""

    MESSAGE = None

    def __init__(self, *args):
        super().__init__(args[0] if args else self.MESSAGE)


class RootDoesNotExistValidationError(ValidationError):
    MESSAGE = "The provided root node does not exist"


class ExistsCircleValidationError(ValidationError):
    MESSAGE = "The story branch has no end"


class UnconnectedNodeValidationError(ValidationError):
    MESSAGE = "The story has unused node"


class UnrelatedReferenceValidationError(ValidationError):
    MESSAGE = "The story node has link to uncreated branch"


class ParseGraphError(ValidationError):
    MESSAGE = "The story item has unsupported structure"
