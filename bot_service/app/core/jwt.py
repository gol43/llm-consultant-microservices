from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


def decode_and_validate(token: str) -> dict:
    """Декодирует JWT и проверяет его"""
    try:
        # Пытаемся расшифровать токен, используя наш секретный ключ
        # Если секрет не совпадает с тем, что в auth-service, то получим JWTError
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALG]
        )
        
        if "sub" not in payload:
            raise ValueError("Некорректный токен: отсутствует идентификатор пользователя")
            
        return payload

    except ExpiredSignatureError:
        raise ValueError("Срок действия токена истек")
        
    except JWTError:
        raise ValueError("Невалидный токен")