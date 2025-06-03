# EXAMPLE @example_track_context("sample_service.md")
"""
Sample authentication service for demonstration.
Updated comment to test minor changes.
"""

import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class AuthService:
    """Authentication service for handling user login and token management."""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.active_sessions = {}

    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return self.hash_password(password) == hashed

    def generate_token(self, user_id: str, expires_in: int = 3600) -> str:
        """Generate a JWT token for a user."""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def login(self, username: str, password: str, user_data: Dict[str, str]) -> Optional[str]:
        """Authenticate a user and return a token."""
        stored_hash = user_data.get('password_hash')
        if stored_hash and self.verify_password(password, stored_hash):
            token = self.generate_token(user_data['user_id'])
            self.active_sessions[user_data['user_id']] = {
                'token': token,
                'login_time': datetime.utcnow()
            }
            return token
        return None

    def logout(self, user_id: str) -> bool:
        """Log out a user by removing their session."""
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
            return True
        return False

    def is_authenticated(self, token: str) -> bool:
        """Check if a token is valid and user is authenticated."""
        payload = self.verify_token(token)
        if payload:
            user_id = payload.get('user_id')
            return user_id in self.active_sessions
        return False

    def refresh_token(self, old_token: str) -> Optional[str]:
        """Refresh an existing token if it's still valid."""
        payload = self.verify_token(old_token)
        if payload:
            user_id = payload.get('user_id')
            if user_id in self.active_sessions:
                return self.generate_token(user_id)
        return None


def create_auth_service(secret: str) -> AuthService:
    """Factory function to create an AuthService instance."""
    return AuthService(secret)


def validate_user_credentials(username: str, password: str) -> bool:
    """Validate user credentials format."""
    if not username or len(username) < 3:
        return False
    if not password or len(password) < 8:
        return False
    return True
