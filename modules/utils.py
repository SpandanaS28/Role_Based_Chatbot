"""
Utility functions for the NotebookLM clone
"""
import streamlit as st
from datetime import datetime
from typing import Any, Dict, List
import re


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    if "current_document" not in st.session_state:
        st.session_state.current_document = None
    
    if "document_content" not in st.session_state:
        st.session_state.document_content = {}
    
    if "outputs" not in st.session_state:
        st.session_state.outputs = []
    
    if "onedrive_authenticated" not in st.session_state:
        st.session_state.onedrive_authenticated = False
    
    if "onedrive_files" not in st.session_state:
        st.session_state.onedrive_files = []


def format_timestamp(timestamp: datetime = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%I:%M %p")


def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def extract_citations(text: str) -> List[str]:
    """Extract citation markers from text"""
    # Look for [1], [2], etc.
    citations = re.findall(r'\[(\d+)\]', text)
    return list(set(citations))


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def get_file_icon(filename: str) -> str:
    """Get emoji icon based on file extension"""
    ext = filename.lower().split('.')[-1]
    icons = {
        'pdf': '📄',
        'docx': '📝',
        'doc': '📝',
        'txt': '📃',
        'md': '📋',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'png': '🖼️',
    }
    return icons.get(ext, '📎')


def create_message_html(role: str, content: str, timestamp: str = None) -> str:
    """Create styled HTML for chat messages"""
    if timestamp is None:
        timestamp = format_timestamp()
    
    if role == "user":
        color = "#e0e7ff"
        align = "flex-end"
        avatar = "👤"
    else:
        color = "#f3f4f6"
        align = "flex-start"
        avatar = "🤖"
    
    return f"""
    <div style="display: flex; justify-content: {align}; margin-bottom: 1rem;">
        <div style="max-width: 70%; background: {color}; padding: 1rem; border-radius: 1rem;">
            <div style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem;">
                {avatar} {role.title()} • {timestamp}
            </div>
            <div>{content}</div>
        </div>
    </div>
    """


def load_custom_css():
    """Load custom CSS for enhanced styling"""
    st.markdown("""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        
        /* Card styling */
        .stButton button {
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* File uploader styling */
        .uploadedFile {
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
            padding: 0.5rem;
        }
        
        /* Chat messages */
        .chat-message {
            padding: 1rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Source card */
        .source-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 0.75rem;
            transition: all 0.3s ease;
        }
        
        .source-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-color: #5f6fd8;
        }
        
        /* Studio output card */
        .output-card {
            background: #f8f9fa;
            border-left: 4px solid #5f6fd8;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Gradient header */
        .gradient-header {
            background: linear-gradient(135deg, #5f6fd8 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
