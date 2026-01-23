# OneDrive API Integration Guide

This guide will help you set up real OneDrive integration for the Banking Document Assistant.

## 🎯 Overview

The app supports two modes:
- **Mock Mode** (default): Uses local storage (no setup required)
- **OneDrive Mode**: Connects to your real Microsoft OneDrive account

## 📋 Prerequisites

- Microsoft Account (Outlook, Hotmail, or Office 365)
- Azure account (free tier works fine)

## 🚀 Setup Steps

### Step 1: Create Azure App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in with your Microsoft account
3. Navigate to **Azure Active Directory**
4. Click **App registrations** → **New registration**

### Step 2: Configure Your App

**Basic Information:**
- **Name**: `Banking Document Assistant` (or any name)
- **Supported account types**: Select one of:
  - "Accounts in any organizational directory and personal Microsoft accounts" (recommended)
  - "Personal Microsoft accounts only" (if using personal OneDrive)
- **Redirect URI**:
  - Platform: **Public client/native (mobile & desktop)**
  - URI: `http://localhost:8501`

Click **Register**

### Step 3: Get Your Client ID

1. After registration, you'll see the **Overview** page
2. Copy the **Application (client) ID**
   - Example: `12345678-1234-1234-1234-123456789abc`
3. Save this - you'll need it soon

### Step 4: Configure API Permissions

1. In your app, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Delegated permissions**
5. Add these permissions:
   - `Files.ReadWrite.All`
   - `User.Read`
6. Click **Add permissions**
7. (Optional) Click **Grant admin consent** if you have admin rights

### Step 5: Enable Public Client Flow

1. Go to **Authentication**
2. Scroll to **Advanced settings**
3. Find **Allow public client flows**
4. Set to **Yes**
5. Click **Save**

### Step 6: Configure Your Application

1. In your project folder, create a `.env` file (or copy from `.env.example`):

```bash
cp .env.example .env
```

2. Edit `.env` and add your Client ID:

```env
# OneDrive Configuration
ONEDRIVE_CLIENT_ID=your_client_id_here
USE_MOCK_ONEDRIVE=false

# AI Model Configuration (leave as is)
TINYLLAMA_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
MODEL_CACHE_DIR=./model_cache
MAX_NEW_TOKENS=512
TEMPERATURE=0.7

# Debug
DEBUG=false
```

3. Replace `your_client_id_here` with your actual Client ID from Step 3

## 🔐 Authentication Flow

When you run the app with OneDrive enabled:

1. Login as Admin
2. You'll see a **"🔐 Connect to OneDrive"** button
3. Click it - a browser window will open
4. Sign in to your Microsoft account
5. Grant permissions to the app
6. Return to the Streamlit app - it's now connected!

## 📤 Using OneDrive Features

### Multiple File Upload

1. Click **"Choose files (multiple allowed)"**
2. Select one or more files (hold Ctrl/Cmd for multiple)
3. Choose an action:
   - **💾 Save All to Storage**: Upload to OneDrive only
   - **📖 Process All**: Process locally without uploading
   - **💾+📖 Both**: Upload AND process

### Supported File Types

- PDF documents (.pdf)
- Word documents (.docx, .doc)
- PowerPoint (.pptx, .ppt)
- Excel (.xlsx, .xls)
- Images (.png, .jpg, .jpeg, .tiff, .bmp)
- Text files (.txt, .md)

### File Size Limits

- **Small files** (< 4MB): Simple upload
- **Large files** (4MB - 50MB): Chunked upload with progress bar

## 🔄 Switching Between Mock and OneDrive

### To use Mock (Local Storage):
```env
USE_MOCK_ONEDRIVE=true
```
- No authentication needed
- Files stored in `./onedrive_mock/` folder
- Good for testing

### To use Real OneDrive:
```env
USE_MOCK_ONEDRIVE=false
ONEDRIVE_CLIENT_ID=your_actual_client_id
```
- Requires authentication
- Files stored in your real OneDrive
- Accessible from anywhere

## 🌐 OneDrive API Features

The integration supports:

### ✅ Upload Operations
- Single file upload
- Multiple file upload (batch)
- Large file upload (chunked, with progress)
- Automatic file organization

### ✅ Download Operations
- Download files by name
- Download files by ID
- Stream large files

### ✅ List Operations
- List all files in root
- Filter by folder
- Get file metadata (size, modified date, etc.)

### ✅ Delete Operations
- Delete files by name or ID
- Admin-only permission enforcement

### ✅ Additional Features
- Create folders
- Get shareable links
- OAuth token caching (no re-login each time)

## ⚠️ Troubleshooting

### Issue: "ONEDRIVE_CLIENT_ID not configured"
**Solution**: Add your Client ID to `.env` file and set `USE_MOCK_ONEDRIVE=false`

### Issue: "Authentication failed"
**Solutions**:
1. Check your Client ID is correct
2. Ensure redirect URI is exactly `http://localhost:8501`
3. Verify API permissions are granted
4. Try clearing browser cache and re-authenticating

### Issue: "Upload failed: 401"
**Solution**: Re-authenticate. Token may have expired. Click "Connect to OneDrive" again.

### Issue: "Large file upload slow"
**Explanation**: Files >4MB are uploaded in chunks. This is normal and shows a progress bar.

### Issue: Mock mode still active
**Solution**: 
1. Check `.env` has `USE_MOCK_ONEDRIVE=false`
2. Restart the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 🔒 Security Considerations

### What the App Can Access:
- Only files in your OneDrive
- Your basic profile info (name, email)

### What It Cannot Access:
- Your password
- Other Microsoft services (Email, Calendar, etc.)
- Other users' files

### Best Practices:
- Use a dedicated OneDrive folder for the app
- Don't share your Client ID publicly if it has admin consent
- Regularly review app permissions in your Microsoft account

## 📊 API Limits

Microsoft Graph API has these limits:
- **Requests per second**: ~10-20 (plenty for this app)
- **File size**: Max 250 GB per file
- **Total storage**: Based on your OneDrive plan

## 🎓 Advanced Configuration

### Custom Folder Path

Edit `onedrive_service.py` to change default folder:

```python
# Instead of "root", use a specific folder
self.list_files(folder_path="BankingDocuments")
```

### Automatic Folder Creation

The app can create folders automatically:

```python
onedrive_service.create_folder("ComplianceDocs", parent_folder="root")
```

### Share Links

Get a shareable link for uploaded files:

```python
link = onedrive_service.get_share_link(file_id)
print(f"Share this: {link}")
```

## 📞 Support Resources

- [Microsoft Graph API Docs](https://docs.microsoft.com/en-us/graph/)
- [Azure App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)

## ✅ Quick Checklist

Before going live with OneDrive:

- [ ] Azure app created
- [ ] Client ID copied
- [ ] API permissions added (`Files.ReadWrite.All`, `User.Read`)
- [ ] Redirect URI set to `http://localhost:8501`
- [ ] Public client flow enabled
- [ ] `.env` file updated with Client ID
- [ ] `USE_MOCK_ONEDRIVE=false` in `.env`
- [ ] App restarted
- [ ] Authentication tested
- [ ] File upload tested

## 🎉 You're Ready!

Once setup is complete, all your documents will be:
- ✅ Stored in your real OneDrive
- ✅ Accessible from any device
- ✅ Backed up automatically by Microsoft
- ✅ Shareable with team members

---

**Note**: If you prefer to keep using mock storage for development/testing, simply keep `USE_MOCK_ONEDRIVE=true` in your `.env` file. No setup required!
