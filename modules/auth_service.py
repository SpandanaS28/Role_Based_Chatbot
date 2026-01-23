"""
Authentication module for role-based access control
"""
import streamlit as st
import hashlib
import json
import os
from datetime import datetime


class AuthService:
    """Handle user authentication and role-based access"""
    
    def __init__(self, users_file="users.json"):
        self.users_file = users_file
        self.init_users()
    
    def init_users(self):
        """Initialize default users if file doesn't exist"""
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "role": "Admin",
                    "name": "Administrator"
                },
                "user1": {
                    "password": self.hash_password("user123"),
                    "role": "User",
                    "name": "Regular User"
                },
                "teamlead": {
                    "password": self.hash_password("lead123"),
                    "role": "Admin",
                    "name": "Team Lead"
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> dict:
        """Authenticate user and return user info"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users:
                hashed_pw = self.hash_password(password)
                if users[username]["password"] == hashed_pw:
                    return {
                        "username": username,
                        "role": users[username]["role"],
                        "name": users[username]["name"],
                        "authenticated": True
                    }
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
        
        return {"authenticated": False}
    
    def is_admin(self, user_info: dict) -> bool:
        """Check if user has admin role"""
        return user_info.get("role") == "Admin"
    
    def log_action(self, username: str, action: str, details:str = ""):
        """Log user actions for audit trail"""
        log_file = "audit_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {username} ({action}): {details}\n"
        
        with open(log_file, 'a') as f:
            f.write(log_entry)
    
    def add_user(self, username: str, password: str, role: str, name: str) -> bool:
        """Add new user (Admin only function)"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users:
                return False  # User already exists
            
            users[username] = {
                "password": self.hash_password(password),
                "role": role,
                "name": name
            }
            
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return True
        except Exception as e:
            st.error(f"Error adding user: {str(e)}")
            return False
