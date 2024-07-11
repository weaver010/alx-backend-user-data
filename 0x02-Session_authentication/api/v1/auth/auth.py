#!/usr/bin/env python3
"""
Module that creates a class to manage
API authentication
"""
from flask import request
from typing import List, Optional, TypeVar
import os


class Auth:
    """
    Class template for the authentication
    system
    """
    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """
        Returns False if path is in excluded_path
        """
        if path is None:
            return True
        if excluded_path is None or len(excluded_path) == 0:
            return True
        if path:
            for exclude in excluded_path:
                last_tag = exclude.split('/')[-1]
                if last_tag.endswith('*'):
                    last_tag = last_tag[0:-1]
                    if last_tag in path:
                        return False
            if path in excluded_path or path + '/' in excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """
        Returns None or str accrding to request
        """
        if not request:
            return None
        authorization = request.headers.get('Authorization')
        if authorization:
            return authorization
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None or User according to request
        """
        print("should not be called")
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """
        if request is None:
            return None
        session = os.getenv('SESSION_NAME')
        cookie = request.cookies.get(session)
        return cookie
