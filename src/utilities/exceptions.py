class DynamoDBError(Exception):
    """Exception class which represents a response error of DynamoDB"""


class ValidationError(Exception):
    """Exception class which represents a different story validation errors"""


class RootDoesNotExistValidationError(ValidationError):
    pass


class ExistsCircleValidationError(ValidationError):
    pass


class UnconnectedNodeValidationError(ValidationError):
    pass


class UnrelatedReferenceValidationError(ValidationError):
    pass
