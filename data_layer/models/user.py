from datetime import datetime, date
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import hashlib
import uuid

class UserRole(Enum):
    """Roles de usuario en el sistema"""
    ADMINISTRADOR = 'administrador'
    GESTOR = 'gestor'
    DOCENTE = 'docente'
    COORDINADOR = 'coordinador'

class UserStatus(Enum):
    """Estados de la cuenta de usuario"""
    ACTIVO = 'activo'
    INACTIVO = 'inactivo'


class UserDepartment(Enum):
    """Departamentos o facultades"""
    CATI_UG = 'cati-ug'  # Dirección de Investigación
    FACULTAD_INGENIERIA = 'facultad_ingenieria'
    FACULTAD_SALUD = 'facultad_salud'
    FACULTAD_SOCIALES = 'facultad_sociales'
    FACULTAD_CIENCIAS = 'facultad_ciencias'
    ADMINISTRACION = 'administracion'

@dataclass
class UserProfile:
    """Perfil extendido del usuario"""
    cedula: Optional[str] = None
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    especialidad: Optional[str] = None
    def to_dict(self):
        return {k: v.isoformat() 
                if isinstance(v, date) 
                else v 
                for k, 
                v in asdict(self).items() 
                if v is not None}

@dataclass
class UserPermissions:
    """Permisos específicos del usuario"""
    # Módulos de acceso
    puede_ver_dashboard: bool = True
    puede_gestionar_convocatorias: bool = False
    puede_gestionar_solicitudes: bool = False
    puede_gestionar_usuarios: bool = False
    puede_ver_reportes: bool = False
    puede_exportar_datos: bool = False
    
    # Acciones específicas
    puede_crear_convocatorias: bool = False
    puede_publicar_convocatorias: bool = False
    puede_validar_solicitudes: bool = False
    puede_prevalidar_solicitudes: bool = False
    puede_ver_todas_solicitudes: bool = False
    
    def to_dict(self):
        return asdict(self)

@dataclass
class UserLoginHistory:
    """Historial de inicio de sesión"""
    id: str
    user_id: int
    login_date: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[str] = None
    success: bool = True
    failure_reason: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'login_date': self.login_date.isoformat(),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'location': self.location,
            'success': self.success,
            'failure_reason': self.failure_reason
        }

class User:
    """Modelo principal de usuario"""
    
    def __init__(
        self,
        id: int,
        username: str,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.DOCENTE,
        full_name: str = "",
        status: UserStatus = UserStatus.ACTIVO,
        department: Optional[UserDepartment] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None,
        permissions: Optional[UserPermissions] = None
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role if isinstance(role, UserRole) else UserRole(role)
        self.full_name = full_name
        self.status = status if isinstance(status, UserStatus) else UserStatus(status)
        self.department = department
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.last_login = last_login
        self.permissions = permissions or self._get_default_permissions()
        self.login_history: List[UserLoginHistory] = []
    
    # ============ MÉTODOS DE FÁBRICA ============
    
    @classmethod
    def create(
        cls,
        username: str,
        email: str,
        password: str,
        full_name: str = "",
        role: UserRole = UserRole.DOCENTE,
        department: Optional[UserDepartment] = None
    ) -> 'User':
        """Crea un nuevo usuario con contraseña hasheada"""
        from business_logic.utils.password_utils import hash_password
        
        password_hash = hash_password(password)
        
        return cls(
            id=0,  # Se asignará al guardar en BD
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role=role,
            department=department
        )
    
    @classmethod
    def create_admin(cls) -> 'User':
        """Crea usuario administrador por defecto"""
        return cls.create(
            username='admin',
            email='admin@sgpi.edu',
            password='Admin123!',
            full_name='Administrador del Sistema',
            role=UserRole.ADMINISTRADOR,
            department=UserDepartment.CATI_UG
        )
    
    @classmethod
    def create_gestor(cls, department: UserDepartment) -> 'User':
        """Crea usuario gestor de departamento"""
        dept_name = department.value.replace('_', ' ').title()
        return cls.create(
            username=f'gestor_{department.value}',
            email=f'gestor.{department.value}@sgpi.edu',
            password='Gestor123!',
            full_name=f'Gestor {dept_name}',
            role=UserRole.GESTOR,
            department=department
        )
    
    @classmethod
    def create_docente(
        cls,
        username: str,
        email: str,
        full_name: str,
        department: UserDepartment
    ) -> 'User':
        """Crea usuario docente"""
        return cls.create(
            username=username,
            email=email,
            password='Docente123!',
            full_name=full_name,
            role=UserRole.DOCENTE,
            department=department
        )
    
    # ============ MÉTODOS DE INSTANCIA ============
    
    def update_profile(self, **kwargs) -> None:
        """Actualiza el perfil del usuario"""
        valid_fields = ['cedula', 'telefono', 'direccion', 
                       'fecha_nacimiento', 'genero', 
                       'titulo_academico', 'especialidad',
                       'foto_perfil', 'biografia']
        
        for key, value in kwargs.items():
            if key in valid_fields and hasattr(self.profile, key):
                setattr(self.profile, key, value)
        
        self.updated_at = datetime.now()
    
    def change_password(self, new_password: str) -> None:
        """Cambia la contraseña del usuario"""
        from business_logic.utils.password_utils import hash_password
        
        self.password_hash = hash_password(new_password)
        self.updated_at = datetime.now()
    
    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña es correcta"""
        from business_logic.utils.password_utils import verify_password
        return verify_password(password, self.password_hash)
    
    def record_login(
        self,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        location: Optional[str] = None,
        success: bool = True,
        failure_reason: Optional[str] = None
    ) -> None:
        """Registra un intento de login"""
        login_record = UserLoginHistory(
            id=str(uuid.uuid4()),
            user_id=self.id,
            login_date=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            location=location,
            success=success,
            failure_reason=failure_reason
        )
        
        self.login_history.append(login_record)
        
        if success:
            self.last_login = datetime.now()
        
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """Activa la cuenta del usuario"""
        self.status = UserStatus.ACTIVO
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """Desactiva la cuenta del usuario"""
        self.status = UserStatus.INACTIVO
        self.updated_at = datetime.now()
    
    def is_active(self) -> bool:
        """Verifica si la cuenta está activa"""
        return self.status == UserStatus.ACTIVO
    
    def has_permission(self, permission_name: str) -> bool:
        """Verifica si el usuario tiene un permiso específico"""
        if hasattr(self.permissions, permission_name):
            return getattr(self.permissions, permission_name)
        return False
    
    def can_access_module(self, module_name: str) -> bool:
        """Verifica si el usuario puede acceder a un módulo"""
        permission_map = {
            'dashboard': 'puede_ver_dashboard',
            'convocatorias': 'puede_gestionar_convocatorias',
            'solicitudes': 'puede_gestionar_solicitudes',
            'usuarios': 'puede_gestionar_usuarios',
            'reportes': 'puede_ver_reportes'
        }
        
        if module_name in permission_map:
            return self.has_permission(permission_map[module_name])
        
        return False
    
    # ============ SERIALIZACIÓN ============
    
    def to_dict(self, include_password: bool = False) -> Dict[str, Any]:
        """Convierte el usuario a diccionario"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'full_name': self.full_name,
            'status': self.status.value,
            'department': self.department.value if self.department else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'profile': self.profile.to_dict(),
            'permissions': self.permissions.to_dict(),
            'login_history_count': len(self.login_history),
            'is_active': self.is_active()
        }
        
        if include_password:
            data['password_hash'] = self.password_hash
        
        return data
    
    def to_minimal_dict(self) -> Dict[str, Any]:
        """Versión minimalista para listados"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role.value,
            'department': self.department.value if self.department else None,
            'status': self.status.value,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    # ============ MÉTODOS PRIVADOS ============
    
    def _get_default_permissions(self) -> UserPermissions:
        """Obtiene permisos por defecto según el rol"""
        permissions = UserPermissions()
        
        if self.role == UserRole.ADMINISTRADOR:
            permissions.puede_gestionar_convocatorias = True
            permissions.puede_crear_convocatorias = True
            permissions.puede_publicar_convocatorias = True
            permissions.puede_gestionar_usuarios = True
            permissions.puede_ver_reportes = True
            permissions.puede_exportar_datos = True
            
        
        elif self.role == UserRole.GESTOR:
            permissions.puede_prevalidar_solicitudes = True
            permissions.puede_ver_todas_solicitudes = True
            permissions.puede_ver_todas_solicitudes = True
        
        elif self.role == UserRole.DOCENTE:
            permissions.puede_gestionar_solicitudes = True
            permissions.puede_exportar_datos = True
        
        elif self.role == UserRole.COORDINADOR:
            permissions.puede_gestionar_convocatorias = True
            permissions.puede_gestionar_solicitudes = True
            permissions.puede_ver_reportes = True
            permissions.puede_exportar_datos = True
            permissions.puede_validar_solicitudes = True
            permissions.puede_ver_todas_solicitudes = True
            permissions.puede_crear_convocatorias = True
            permissions.puede_publicar_convocatorias = True
        
        return permissions
    
    # ============ MÉTODOS MÁGICOS ============
    
    def __str__(self) -> str:
        return f"User({self.id}: {self.username} - {self.full_name})"
    
    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}' role='{self.role.value}'>"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)