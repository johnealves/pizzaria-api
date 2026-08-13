from fastapi import status


class AppException(Exception):
    def __init__(
        self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        self.code = code
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class ProductNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            code="PRODUCT_NOT_FOUND",
            message="Product not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
