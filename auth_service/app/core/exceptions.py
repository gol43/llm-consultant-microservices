from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Базовый класс"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"
    
    def __init__(self):
        # Наследуемся, чтобы правильно передать сетевую ошибку приложения и вызывать саму ошибку правильно
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsError(BaseHTTPException):
    """Ошибка 409: когда пытаемся зарегистрировать занятый email"""
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email уже существует"

class InvalidCredentialsError(BaseHTTPException):
    """Ошибка 401: когда при логине ввели неверные данные"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный email или пароль"

class InvalidTokenError(BaseHTTPException):
    """Ошибка 401: когда токен подделан или поврежден"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Невалидный токен"

class TokenExpiredError(BaseHTTPException):
    """Ошибка 401: когда время жизни JWT вышло (exp в payload)"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"

class UserNotFoundError(BaseHTTPException):
    """Ошибка 404: когда ищем юзера в базе, а его там нет"""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"

class PermissionDeniedError(BaseHTTPException):
    """Ошибка 403: когда токен верный, но прав (например, админских) не хватает"""
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Доступ запрещен"