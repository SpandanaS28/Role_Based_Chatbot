"""
Configuration file for NotebookLM Clone
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application Settings
APP_TITLE = "NotebookLM Clone"
APP_ICON = "📚"
LAYOUT = "wide"

# OneDrive Configuration
ONEDRIVE_CONFIG = {
    "client_id": os.getenv("ONEDRIVE_CLIENT_ID", ""),
    "client_secret": os.getenv("ONEDRIVE_CLIENT_SECRET", ""),
    "tenant_id": os.getenv("ONEDRIVE_TENANT_ID", "common"),
    "redirect_uri": os.getenv("ONEDRIVE_REDIRECT_URI", "http://localhost:8501"),
    "scopes": ["Files.ReadWrite", "User.Read"],
    "authority": "https://login.microsoftonline.com/common",
}

# AI Configuration - TinyLlama Local Model
TINYLLAMA_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MODEL_CACHE_DIR = "./model_cache"
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7

# Feature Flags
USE_MOCK_ONEDRIVE = os.getenv("USE_MOCK_ONEDRIVE", "true").lower() == "true"
USE_MOCK_AI = os.getenv("USE_MOCK_AI", "false").lower() == "true"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# File Upload Settings
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".txt", ".md", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"]

# UI Colors (matching NotebookLM)
COLORS = {
    "primary": "#5f6fd8",
    "secondary": "#8b5cf6", 
    "accent": "#6366f1",
    "background": "#ffffff",
    "surface": "#f8f9fa",
    "text_primary": "#1f2937",
    "text_secondary": "#6b7280",
    "border": "#e5e7eb",
}
