class AppError(Exception):
    """Error controlado de la aplicación, convertido a JSON por el manejador global."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, 404)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Solo admin"):
        super().__init__(message, 403)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, 401)
