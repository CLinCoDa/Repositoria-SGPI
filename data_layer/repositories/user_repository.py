from data_layer.models.user import User
from data_layer.database.database import db
from datetime import datetime

class UserRepository:
    def __init__(self):
        self.collection = db.users
    
    def find_by_username(self, username):
        """Busca usuario por username"""
        user_data = next((u for u in self.collection 
                         if u['username'] == username), None)
        
        if user_data:
            return self._to_model(user_data)
        return None
    
    def find_by_id(self, user_id):
        """Busca usuario por ID"""
        user_data = next((u for u in self.collection 
                         if u['id'] == user_id), None)
        
        if user_data:
            return self._to_model(user_data)
        return None
    
    def update_last_login(self, user_id):
        """Actualiza la fecha de último login"""
        for user in self.collection:
            if user['id'] == user_id:
                user['last_login'] = datetime.now()
                break
    
    def _to_model(self, data):
        """Convierte datos dict a objeto User"""
        return User(
            id=data['id'],
            username=data['username'],
            password_hash=data['password_hash'],
            email=data['email'],
            role=data['role'],
            full_name=data['full_name'],
            is_active=data['is_active'],
            created_at=data['created_at'],
            last_login=data.get('last_login')
        )