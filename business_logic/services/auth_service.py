from data_layer.repositories.user_repository import UserRepository
from business_logic.utils.password_utils import verify_password
from business_logic.exceptions.auth_exceptions import (
    UserNotFoundError,
    InvalidPasswordError,
    UserInactiveError,
)

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def authenticate(self, username, password):
        """
        Autentica un usuario con username y password
        """
        # 1. Buscar usuario por username
        user = self.user_repo.find_by_username(username)
        
        if not user:
            raise UserNotFoundError("Usuario no encontrado")
        
        # 2. Verificar si está activo
        if not user.is_active:
            raise UserInactiveError("Usuario inactivo")
        
        # 3. Verificar contraseña
        if not verify_password(password, user.password_hash):
            raise InvalidPasswordError("Contraseña incorrecta")
        
        # 4. Registrar intento de login
        self.user_repo.update_last_login(user.id)
        
        # 5. Retornar usuario (sin password)
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'full_name': user.full_name,
            'department': user.department
        }
    
    def get_user_by_id(self, user_id):
        """Obtiene usuario por ID"""
        return self.user_repo.find_by_id(user_id)
    
    def change_password(self, user_id, old_password, new_password):
        """Cambia la contraseña del usuario"""
        # Lógica para cambiar contraseña
        pass