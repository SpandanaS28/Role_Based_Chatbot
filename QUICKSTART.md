# 🚀 Quick Start Guide

## Installation (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

###. Install Tesseract OCR (for image support)

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to `C:\Program Files\Tesseract-OCR`
3. Add to PATH or the app will guide you

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 3. Run the Application
```bash
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## Login Credentials

### Admin (Full Access)
```
Username: admin
Password: admin123
```

### Regular User (Query Only)
```
Username: user1
Password: user123
```

### Team Lead (Admin)
```
Username: teamlead
Password: lead123
```

---

## First Steps

### As Admin:
1. Login with admin credentials
2. Upload a document (PDF, DOCX, PPTX, XLSX, or image)
3. Click "📖 Process"
4. Select the document
5. Ask questions!

### As User:
1. Login with user credentials
2. Select an existing document
3. Ask questions
4. Generate outputs (summaries, study guides, etc.)

---

## Supported File Types

✅ PDF documents  
✅ Word (.docx, .doc)  
✅ PowerPoint (.pptx, .ppt)  
✅ Excel (.xlsx, .xls)  
✅ Images (.png, .jpg, .jpeg, .tiff, .bmp) - requires Tesseract  
✅ Text files (.txt, .md)

---

## Example Questions

- "What are the main points in this document?"
- "Summarize the compliance requirements"
- "What is the onboarding process?"
- "List all the steps mentioned"
- "Who is responsible for audits?"

---

## Generating Outputs

1. Select a document
2. Go to **Studio** panel (right side)
3. Choose a tab:
   - **📝 Summary**: Quick overview
   - **📚 Study Guide**: Detailed breakdown
   - **❓ FAQ**: Common questions
   - **🎧 Audio**: Text-to-speech overview

---

## Troubleshooting

### "Tesseract not found"
- Install Tesseract OCR (see step 2 above)
- For images only - PDFs/Word will still work

### "Model loading slow"
- First time downloads ~2GB model
- Subsequent starts are much faster (cached)

### "Login failed"
- Check spelling of username/password
- Case-sensitive!
- Default users are in users.json

### "Document won't process"
- Check file isn't corrupted
- Try a different file format
- Check file size (<50MB)

---

## Tips

💡 **Use Suggested Questions**: Click "✨ Generate Suggested Questions" for ideas  
💡 **Multiple Documents**: Process several, switch between them  
💡 **Save to Storage**: Use "💾 Save to OneDrive" for persistence  
💡 **Check Audit Log**: See all actions in `audit_log.txt`  
💡 **GPU Acceleration**: If you have NVIDIA GPU, it auto-detects and runs faster  

---

## Next Steps

- Upload your own documents
- Try different question types
- Generate study materials
- Explore role differences (admin vs user)
- Check the full README.md for advanced features

---

**Need Help?** Check README.md or walkthrough.md for detailed documentation.

**Ready to Go!** 🎉 Start with `streamlit run app.py`
