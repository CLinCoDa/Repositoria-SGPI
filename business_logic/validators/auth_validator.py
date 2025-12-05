from business_logic.exceptions.auth_exceptions import AuthenticationError
import re

class AuthValidator:
    @staticmethod
    def validate_password(password, username=None, email=None):
        """Valida que la contraseña cumpla la política"""
        violations = []
        
        # Longitud mínima
        if len(password) < 8:
            violations.append("Mínimo 8 caracteres")
        
        # Mayúsculas y minúsculas
        if not re.search(r'[A-Z]', password):
            violations.append("Al menos una mayúscula")
        if not re.search(r'[a-z]', password):
            violations.append("Al menos una minúscula")
        
        # Números
        if not re.search(r'\d', password):
            violations.append("Al menos un número")
        
        # Caracteres especiales
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            violations.append("Al menos un carácter especial")
        
        # No contener username o email
        if username and username.lower() in password.lower():
            violations.append("No puede contener el nombre de usuario")
        
        if email:
            email_local = email.split('@')[0]
            if email_local.lower() in password.lower():
                violations.append("No puede contener parte del email")
        
        return True
    
    @staticmethod
    def validate_username(username):
        """Valida formato de username"""
        if not username or len(username) < 3:
            raise AuthenticationError("Username debe tener al menos 3 caracteres")
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise AuthenticationError("Username solo puede contener letras, números y _")
        
        return True