class DynamoDBError(Exception):
    """Exception class which represents a response error of DynamoDB"""


class ValidationError(Exception):
    """Exception class which represents a different story validation errors"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class RootDoesNotExistValidationError(ValidationError):
    def __init__(self, message="The Root node does not exist"):
        super().__init__(message)


class ExistsCircleValidationError(ValidationError):
    def __init__(self, message="The story has branch from which there is no end"):
        super().__init__(message)


class UnconnectedNodeValidationError(ValidationError):
    def __init__(self, message):
        super().__init__(message="The story has unused node")


class UnrelatedReferenceValidationError(ValidationError):
    def __init__(self, message="The story node has link to uncreated branch"):
        super().__init__(message)
