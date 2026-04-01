from pydantic import BaseModel
from typing import Optional


# ── Menu Models (existing) ────────────────────────────────────────────────────

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    is_available: bool = True
    image_url: Optional[str] = None

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None


# ── Auth Models (new) ─────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    # role is always 'customer' for self-registration; enforced in the endpoint

class UserLogin(BaseModel):
    email: str
    password: str
    role: str   # 'customer' | 'admin' | 'rider'

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

class GoogleLogin(BaseModel):
    name: str
    email: str
    uid: str
