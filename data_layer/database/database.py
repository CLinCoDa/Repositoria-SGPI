# data_layer/database.py
"""
Base de datos en memoria – prototipo SGPI
Soporta: users, convocatorias, solicitudes
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json

class Database:
    def __init__(self, persist_to_disk: bool = False, data_dir: str = "data"):
        self.persist_to_disk = persist_to_disk
        self.data_dir = Path(data_dir)
        if persist_to_disk:
            self.data_dir.mkdir(parents=True, exist_ok=True)

        # Colecciones
        self.users: List[Dict] = []
        self.convocatorias: List[Dict] = []
        self.solicitudes: List[Dict] = []

        # Cargar desde disco si corresponde
        if self.persist_to_disk:
            self._load_all()

    # ----------------- HELPERS -----------------
    def _next_id(self, collection: List[Dict]) -> int:
        return max([item.get("id", 0) for item in collection], default=0) + 1

    def _calc_estado(self, fecha_inicio: str, fecha_fin: str) -> str:
        today = datetime.now().date()
        inicio = datetime.fromisoformat(fecha_inicio).date()
        fin = datetime.fromisoformat(fecha_fin).date()
        if today < inicio:
            return "planificada"
        elif inicio <= today <= fin:
            return "registro"
        else:
            return "finalizada"

    # ----------------- USERS -----------------
    def add_user(self, user_data: Dict) -> Dict:
        user = dict(user_data)
        user["id"] = self._next_id(self.users)
        now = datetime.now().isoformat()
        user.setdefault("created_at", now)
        user.setdefault("updated_at", now)
        user.setdefault("status", "activo")
        self.users.append(user)
        if self.persist_to_disk:
            self._save_users()
        return user

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        return next((u for u in self.users if u["id"] == user_id), None)
    
    def find_user_by_username(self, username: str) -> Optional[Dict]:
        return next((u for u in self.users if u.get("username") == username), None)

    def update_user(self, user_id: int, updates: Dict) -> Optional[Dict]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for k, v in updates.items():
            if k not in ("id", "created_at"):
                user[k] = v
        user["updated_at"] = datetime.now().isoformat()
        if self.persist_to_disk:
            self._save_users()
        return user

    def delete_user(self, user_id: int, soft_delete: bool = True) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        if soft_delete:
            user["status"] = "inactivo"
            user["updated_at"] = datetime.now().isoformat()
        else:
            self.users = [u for u in self.users if u["id"] != user_id]
        if self.persist_to_disk:
            self._save_users()
        return True

    # ----------------- CONVOCATORIAS -----------------
    def add_convocatoria(self, conv_data: Dict) -> Dict:
        conv = dict(conv_data)
        conv["id"] = self._next_id(self.convocatorias)
        now = datetime.now().isoformat()
        conv.setdefault("created_at", now)
        conv.setdefault("updated_at", now)
        # calcular estado automáticamente si no viene
        if "estado" not in conv:
            conv["estado"] = self._calc_estado(conv["fecha_inicio"], conv["fecha_fin"])
        self.convocatorias.append(conv)
        if self.persist_to_disk:
            self._save_convocatorias()
        return conv
    
    def get_convocatoria_by_id(self, conv_id: int) -> Optional[Dict]:
        return next((c for c in self.convocatorias if c["id"] == conv_id), None)

    def update_convocatoria(self, conv_id: int, updates: Dict) -> Optional[Dict]:
        c = self.get_convocatoria_by_id(conv_id)
        if not c:
            return None
        c.update(updates)
        if self.persist_to_disk:
            self._save_convocatorias()
        return c

    def delete_convocatoria(self, conv_id: int) -> bool:
        before = len(self.convocatorias)
        self.convocatorias = [c for c in self.convocatorias if c["id"] != conv_id]
        if self.persist_to_disk:
            self._save_convocatorias()
        return len(self.convocatorias) < before

    # ----------------- SOLICITUDES -----------------
    def add_solicitud(self, sol_data: Dict) -> Dict:
        sol = dict(sol_data)
        sol["id"] = self._next_id(self.solicitudes)
        now = datetime.now().isoformat()
        sol.setdefault("created_at", now)
        sol.setdefault("updated_at", now)
        if "codigo" not in sol:
            tipo = (sol.get("tipo") or "XX").upper()[:2]
            year = datetime.now().year
            sol["codigo"] = f"{tipo}-{year}-{sol['id']:04d}"
        self.solicitudes.append(sol)
        if self.persist_to_disk:
            self._save_solicitudes()
        return sol

    def get_solicitud_by_id(self, sol_id: int) -> Optional[Dict]:
        return next((s for s in self.solicitudes if s["id"] == sol_id), None)
    
    def delete_solicitud(self, sol_id: int) -> bool:
        before = len(self.solicitudes)
        self.solicitudes = [s for s in self.solicitudes if s["id"] != sol_id]
        if self.persist_to_disk:
            self._save_solicitudes()
        return len(self.solicitudes) < before

    # ----------------- STATS & SEARCH -----------------
    def get_stats(self) -> Dict:
        return {
            "total_users": len(self.users),
            "total_convocatorias": len(self.convocatorias),
            "total_solicitudes": len(self.solicitudes),
            "last_updated": datetime.now().isoformat()
        }

    # ----------------- PERSISTENCIA -----------------
    def _load_all(self):
        self._load_users()
        self._load_convocatorias()
        self._load_solicitudes()

    def _load_users(self):
        f = self.data_dir / "users.json"
        if f.exists():
            with open(f, "r", encoding="utf-8") as fh:
                self.users = json.load(fh)

    def _save_users(self):
        f = self.data_dir / "users.json"
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(self.users, fh, ensure_ascii=False, indent=2)

    def _load_convocatorias(self):
        f = self.data_dir / "convocatorias.json"
        if f.exists():
            with open(f, "r", encoding="utf-8") as fh:
                self.convocatorias = json.load(fh)

    def _save_convocatorias(self):
        f = self.data_dir / "convocatorias.json"
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(self.convocatorias, fh, ensure_ascii=False, indent=2)

    def _load_solicitudes(self):
        f = self.data_dir / "solicitudes.json"
        if f.exists():
            with open(f, "r", encoding="utf-8") as fh:
                self.solicitudes = json.load(fh)

    def _save_solicitudes(self):
        f = self.data_dir / "solicitudes.json"
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(self.solicitudes, fh, ensure_ascii=False, indent=2)


# ----------------- SINGLETON -----------------
_db_instance: Optional[Database] = None

def get_database(persist_to_disk: bool = False, data_dir: str = "data") -> Database:
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(persist_to_disk=persist_to_disk, data_dir=data_dir)
    return _db_instance

# Alias para usar en todo el proyecto
db = get_database()



