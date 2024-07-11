#!/usr/bin/env python3
"""
Module containing class SeesionAuth
inheriting from Auth and implementing
Session Authentication
"""
from api.v1.auth.auth import Auth
from typing import Optional
from uuid import uuid4
from models.user import User
from typing import TypeVar, Optional


class SessionAuth(Auth):
    """
    Contains Session Authentication
    implementation
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Optional[str]:
        """
        Creates a Session ID for a user_id
        """
        if not user_id or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """
        Returns a User ID based on a Session ID
        """
        if not session_id or type(session_id) != str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User based on a cookie value
        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session for logout functionality
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        try:
            del self.user_id_by_session_id[session_id]
        except Exception as e:
            pass
        return True
