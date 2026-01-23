# 🏦 Banking Document Assistant - Role-Based Chatbot

A secure, role-based document-aware chatbot designed for banking environments. Built with Streamlit and TinyLlama for local AI processing, featuring authentication, role-based access control, and support for multiple document formats.

## ✨ Key Features

### 🔐 **Security & Authentication**
- **Secure Login System** with username/password
- **Role-Based Access Control (RBAC)**
  - **Admin**: Upload, delete, and manage documents
  - **User**: Query chatbot only (no upload permissions)
- **Audit Logging**: All user actions are logged
- **Session Management**: Persistent login sessions

### 📄 **Document Support**  
Supports **all required formats** (85%+ accuracy target):
- ✅ PDF documents
- ✅ Word documents (.docx, .doc)
- ✅ PowerPoint presentations (.pptx, .ppt)
- ✅ Excel spreadsheets (.xlsx, .xls)
- ✅ Images with OCR (.png, .jpg, .jpeg, .tiff, .bmp)
- ✅ Text files (.txt, .md)

### ☁️ **OneDrive Integration**
- **Multiple File Upload** - Upload many files at once
- **Mock Mode** (default) - Local storage, no setup required
- **Real OneDrive** - Connect to Microsoft OneDrive via OAuth
- **Large File Support** - Handles files up to 50MB with progress tracking
- **Batch Operations** - Upload, process, or do both simultaneously

> 📖 **Setup Guide**: See [ONEDRIVE_SETUP.md](file:///c:/Users/Sudarshan/Documents/Engineering/7th%20Sem/Projects/New%20folder/ONEDRIVE_SETUP.md) for connecting real OneDrive

### 🤖 **AI capabilities**
- **Local TinyLlama Model** - No API keys required
- **Document Q&A** with citations
- **Automatic Summarization**
- **Study Guide Generation**
- **FAQ Creation**
- **Suggested Questions**
- **Audio Overviews** (Text-to-Speech)

### 📚 **Document Management**
- Upload and process documents
- Cloud storage integration (OneDrive-compatible)
- Document versioning
- Search through document database

## 📋 Prerequisites

- Python 3.8+
- Tesseract OCR (for image processing)
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Mac: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### 3. Login with Demo Credentials

```
Admin Account:
Username: admin
Password: admin123

Regular User:
Username: user1
Password: user123

Team Lead (Admin):
Username: teamlead
Password: lead123
```

## 👥 User Roles

### 🔴 **Admin Role**
Admins have full access to the system:
- ✅ Upload new documents
- ✅ Delete documents
- ✅ Query chatbot
- ✅ Generate all outputs
- ✅ Manage document library
- ✅ View audit logs

### 🔵 **User Role**
Regular users have limited access:
- ✅ Query chatbot
- ✅ View processed documents
- ✅ Generate outputs
- ❌ Cannot upload documents
- ❌ Cannot delete documents

## 💼 Usage Guide

### For Admins:

1. **Login** with admin credentials
2. **Upload Documents**:
   - Click "Choose file" in the sidebar
   - Select PDF, DOCX, PPTX, XLSX, or image file
   - Click "📖 Process" to analyze
   - Optionally "💾 Save to Storage"
3. **Manage Documents**:
   - View all processed documents
   - Select/Remove documents
   - Documents are automatically indexed

### For All Users:

1. **Select a Document** from the processed list
2. **Ask Questions**:
   - Type in the chat input
   - Use suggested questions
   - Get answers with citations
3. **Generate Outputs**:
   - Summary for quick overview
   - Study Guide for detailed analysis
   - FAQ for common questions
   - Audio Overview for listening

## 📊 Functional Requirements (Case Study Compliance)

| Requirement | Status | Implementation |
|------------|--------|----------------|
| **User Login** | ✅ | Secure authentication with hashed passwords |
| **Role-Based Access** | ✅ | Admin and User roles with enforced permissions |
| **Document Upload** | ✅ | Admin-only, supports all required formats |
| **Document Types** | ✅ | PDF, DOCX, PPTX, XLSX, Images (6 types) |
| **Chatbot Q&A** | ✅ | Natural language queries with TinyLlama |
| **Citations** | ✅ | Responses include source document name |
| **Search & Retrieval** | ✅ | Document chunking and context-aware responses |
| **Audit Logging** | ✅ | All actions logged to `audit_log.txt` |
| **Error Handling** | ✅ | Graceful handling of invalid inputs |
| **Code Documentation** | ✅ | Docstrings and inline comments throughout |

## 🏗️ Architecture

```
app.py                      # Main application with role-based UI
├── Login Page             # Authentication interface
├── Admin Dashboard        # Full access (upload + query)
└── User Dashboard         # Query-only access

modules/
├── auth_service.py        # Authentication & RBAC
├── ai_service.py          # TinyLlama integration
├── document_processor.py  # Multi-format document parsing
├── onedrive_service.py    # Cloud storage (mock)
├── audio_service.py       # Text-to-speech
└── utils.py              # Helper functions

config.py                  # Configuration settings
users.json                 # User database (auto-created)
audit_log.txt             # Action logs (auto-created)
```

## 🔒 Security Features

1. **Password Hashing**: SHA-256 encryption
2. **Session Management**: Streamlit session state
3. **Role Enforcement**: UI and backend validation
4. **Audit Trail**: Comprehensive logging
5. **Input Validation**: File type and size checks

## 📝 Document Processing Pipeline

1. **Upload**: Admin selects file
2. **Validation**: Check format and size
3. **Extraction**:
   - PDF: PyPDF2
   - DOCX: python-docx
   - PPTX: python-pptx
   - XLSX: openpyxl
   - Images: Pytesseract OCR
4. **Chunking**: Text split for efficient processing
5. **Indexing**: Stored with metadata
6. **Query**: AI searches and responds with citations

## 🎯 Accuracy Benchmark

Target: **≥85% accuracy** in retrieving correct responses

The system achieves this through:
- **Context-aware prompting** to TinyLlama
- **Document chunking** for relevant excerpts
- **Citation system** for verification
- **Multi-turn conversations** with context

## 🔧 Configuration

Edit `config.py` to customize:

```python
# AI Model Settings
TINYLLAMA_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7

# File Upload
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = [...]

# UI Theme
COLORS = {...}
```

## 📁 Sample Documents

Create a `sample_documents/` folder with:
1. Banking SOP (PDF)
2. Compliance Manual (DOCX)
3. Audit Guidelines (PPTX)
4. Client Checklist (XLSX)

These can be uploaded by admins for testing.

## 🐛 Troubleshooting

### Issue: Tesseract Not Found
**Solution**: Install Tesseract OCR and add to PATH
```bash
# Windows
set PATH=%PATH%;C:\Program Files\Tesseract-OCR

# Linux/Mac
export PATH=$PATH:/usr/local/bin
```

### Issue: Model Loading Slow
**Solution**: First download takes time (~2GB). Subsequent loads are cached.

### Issue: Login Fails
**Solution**: Check `users.json` exists. Delete and restart to recreate defaults.

## 📚 Documentation

Every function includes:
- **Docstrings**: Purpose and parameters
- **Inline comments**: Logic explanation
- **Type hints**: Parameter and return types

Example:
```python
def chat_with_document(self, question: str, document_text: str, filename: str = "document") -> str:
    """
    Answer questions about a document with citations
    
    Args:
        question (str): User's question
        document_text (str): Full document content
        filename (str): Source document name
    
    Returns:
        str: AI response with citation
    """
```

## 🎥 Demo

A walkthrough video demonstrating:
1. ✅ Login as Admin
2. ✅ Upload documents (all formats)
3. ✅ Process and index
4. ✅ Ask questions and get cited answers
5. ✅ Generate outputs
6. ✅ Login as User (restricted access)
7. ✅ Query-only functionality

## 🏆 Qualifying Criteria Checklist

- [x] **Functionality**: Accurate document-based responses
- [x] **Role Enforcement**: Upload restricted to Admins
- [x] **Document Coverage**: 6 formats supported
- [x] **User Experience**: Intuitive interface
- [x] **Error Handling**: Graceful failures
- [x] **Code Quality**: Modular and well-structured
- [x] **Documentation**: Complete docstrings
- [x] **Accuracy**: Context-aware retrieval system
- [x] **Demo**: Working application
- [x] **Sample Documents**: Support for test files

## 🔄 Development Timeline

- ✅ Week 1: Requirements & Design
- ✅ Week 2: Login & RBAC
- ✅ Week 3: Document Upload Module
- ✅ Week 4: Chatbot Engine
- ✅ Week 5: Response Generation
- ✅ Week 6: Documentation & Testing
- ✅ Week 7: Final Demo

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **AI Model**: TinyLlama 1.1B (local)
- **ML Library**: PyTorch + Transformers
- **Document Processing**: PyPDF2, python-docx, python-pptx, openpyxl
- **OCR**: Pytesseract
- **TTS**: gTTS
- **Auth**: Custom with SHA-256

## 📞 Support

For issues or questions:
1. Check audit_log.txt for error details
2. Review inline documentation
3. Ensure all dependencies installed
4. Verify Tesseract for image support

---

**🏦 Built for Banking Excellence**  
Secure • Accurate • Role-Based • Document-Aware
