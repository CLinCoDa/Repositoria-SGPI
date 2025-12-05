"""
Excepciones específicas para el módulo de autenticación
"""

class AuthException(Exception):
    """Clase base para todas las excepciones de autenticación"""
    
    def __init__(self, message="Error de autenticación", details=None):
        self.message = message
        self.details = details or {}
        self.code = "AUTH_ERROR"
        super().__init__(self.message)
    
    def to_dict(self):
        """Convierte la excepción a diccionario para respuestas API"""
        return {
            'success': False,
            'error': self.code,
            'message': self.message,
            'details': self.details
        }


class AuthenticationError(AuthException):
    """Error al autenticar credenciales"""
    
    def __init__(self, message="Credenciales inválidas", details=None):
        super().__init__(message, details)
        self.code = "AUTHENTICATION_FAILED"


class UserNotFoundError(AuthException):
    """Usuario no encontrado"""
    
    def __init__(self, username=None, details=None):
        message = f"Usuario no encontrado"
        if username:
            message = f"Usuario '{username}' no encontrado"
        
        details = details or {}
        if username:
            details['username'] = username
            
        super().__init__(message, details)
        self.code = "USER_NOT_FOUND"


class InvalidPasswordError(AuthException):
    """Contraseña incorrecta"""
    
    def __init__(self, username=None, details=None):
        message = "Contraseña incorrecta"
        if username:
            message = f"Contraseña incorrecta para usuario '{username}'"
            
        details = details or {}
        if username:
            details['username'] = username
            
        super().__init__(message, details)
        self.code = "INVALID_PASSWORD"


class UserInactiveError(AuthException):
    """Usuario inactivo/deshabilitado"""
    
    def __init__(self, username=None, details=None):
        message = "Usuario inactivo"
        if username:
            message = f"Usuario '{username}' está inactivo"
            
        details = details or {}
        if username:
            details['username'] = username
            
        super().__init__(message, details)
        self.code = "USER_INACTIVE"

class TokenExpiredError(AuthException):
    """Token JWT expirado"""
    
    def __init__(self, token_type="access", details=None):
        message = f"Token {token_type} expirado"
        
        details = details or {}
        details['token_type'] = token_type
        
        super().__init__(message, details)
        self.code = "TOKEN_EXPIRED"


class InvalidTokenError(AuthException):
    """Token JWT inválido"""
    
    def __init__(self, token_type="access", reason=None, details=None):
        message = f"Token {token_type} inválido"
        if reason:
            message = f"Token {token_type} inválido: {reason}"
            
        details = details or {}
        details['token_type'] = token_type
        if reason:
            details['reason'] = reason
            
        super().__init__(message, details)
        self.code = "INVALID_TOKEN"


class SessionExpiredError(AuthException):
    """Sesión expirada"""
    
    def __init__(self, details=None):
        super().__init__("Sesión expirada", details)
        self.code = "SESSION_EXPIRED"

