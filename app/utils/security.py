"""Security utilities for password hashing and JWT token management."""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError
from ..config import settings


# PBKDF2-HMAC-SHA256 configuration
_PBKDF2_ITERATIONS = 180_000
_SALT_BYTES = 16


def get_password_hash(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    
    Format: iterations$salt_hex$hash_hex
    
    Args:
        password: Plain password string
        
    Returns:
        Hashed password in format suitable for storage
    """
    pwd_bytes = password.encode("utf-8", errors="ignore")
    salt = secrets.token_bytes(_SALT_BYTES)
    hash_obj = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt, _PBKDF2_ITERATIONS)
    return f"{_PBKDF2_ITERATIONS}${salt.hex()}${hash_obj.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a stored hash.
    
    Args:
        plain_password: Plain password to verify
        hashed_password: Stored hash from get_password_hash()
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        parts = hashed_password.split("$")
        if len(parts) != 3:
            return False
        
        iterations = int(parts[0])
        salt = bytes.fromhex(parts[1])
        stored_hash = bytes.fromhex(parts[2])
        
        pwd_bytes = plain_password.encode("utf-8", errors="ignore")
        computed_hash = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt, iterations)
        
        return hmac.compare_digest(computed_hash, stored_hash)
    except Exception:
        return False


def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data to encode
        expires_delta: Token expiration time (defaults to settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, str]:
    """
    Decode and verify a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise e
