"""
OneDrive Service with Microsoft Graph API Integration
Supports real OneDrive authentication and file operations
"""
import streamlit as st
from typing import List, Dict, Optional
import os
import requests
from datetime import datetime
import json
from msal import PublicClientApplication
import config


class OneDriveService:
    """OneDrive service with real Microsoft Graph API integration"""
    
    def __init__(self, use_mock=True):
        self.use_mock = use_mock
        self.mock_storage = "./onedrive_mock"
        
        # Microsoft Graph API endpoints
        self.graph_api_endpoint = "https://graph.microsoft.com/v1.0"
        self.scopes = ["Files.ReadWrite.All", "User.Read"]
        
        # MSAL application
        self.app = None
        self.access_token = None
        
        if use_mock:
            # Create mock storage directory
            if not os.path.exists(self.mock_storage):
                os.makedirs(self.mock_storage)
        else:
            # Initialize MSAL for real OneDrive
            self._init_msal()
    
    def _init_msal(self):
        """Initialize MSAL Public Client Application"""
        if not config.ONEDRIVE_CONFIG.get('client_id'):
            st.warning("⚠️ OneDrive Client ID not configured. Using mock storage.")
            self.use_mock = True
            return
        
        try:
            self.app = PublicClientApplication(
                client_id=config.ONEDRIVE_CONFIG['client_id'],
                authority=config.ONEDRIVE_CONFIG['authority']
            )
        except Exception as e:
            st.error(f"Error initializing OneDrive: {str(e)}")
            self.use_mock = True
    
    def authenticate(self) -> bool:
        """Authenticate with Microsoft OneDrive"""
        if self.use_mock:
            return True
        
        try:
            # Try to get token from cache first
            accounts = self.app.get_accounts()
            if accounts:
                result = self.app.acquire_token_silent(self.scopes, account=accounts[0])
                if result and "access_token" in result:
                    self.access_token = result["access_token"]
                    return True
            
            # Interactive authentication required
            result = self.app.acquire_token_interactive(scopes=self.scopes)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                st.success("✅ Connected to OneDrive!")
                return True
            else:
                st.error(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                return False
                
        except Exception as e:
            st.error(f"OneDrive authentication error: {str(e)}")
            return False
    
    def _make_graph_request(self, endpoint: str, method: str = "GET", data: bytes = None, headers: dict = None) -> Optional[dict]:
        """Make a request to Microsoft Graph API"""
        if not self.access_token:
            st.error("Not authenticated with OneDrive")
            return None
        
        url = f"{self.graph_api_endpoint}{endpoint}"
        request_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        if headers:
            request_headers.update(headers)
        
        try:
            if method == "GET":
                response = requests.get(url, headers=request_headers)
            elif method == "POST":
                response = requests.post(url, headers=request_headers, data=data)
            elif method == "PUT":
                response = requests.put(url, headers=request_headers, data=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=request_headers)
            else:
                return None
            
            if response.status_code in [200, 201, 204]:
                return response.json() if response.content else {"success": True}
            else:
                st.error(f"OneDrive API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Request error: {str(e)}")
            return None
    
    def list_files(self, folder_path: str = "root") -> List[Dict]:
        """List files in OneDrive folder"""
        files = []
        
        if self.use_mock:
            # Mock implementation
            if os.path.exists(self.mock_storage):
                for filename in os.listdir(self.mock_storage):
                    filepath = os.path.join(self.mock_storage, filename)
                    if os.path.isfile(filepath):
                        files.append({
                            "name": filename,
                            "size": os.path.getsize(filepath),
                            "modified": datetime.fromtimestamp(os.path.getmtime(filepath)),
                            "path": filepath,
                            "type": "mock"
                        })
        else:
            # Real OneDrive API
            endpoint = f"/me/drive/{folder_path}/children"
            result = self._make_graph_request(endpoint)
            
            if result and "value" in result:
                for item in result["value"]:
                    if "file" in item:  # Only files, not folders
                        files.append({
                            "name": item["name"],
                            "size": item.get("size", 0),
                            "modified": datetime.fromisoformat(item["lastModifiedDateTime"].replace("Z", "+00:00")),
                            "path": item["id"],
                            "type": "onedrive",
                            "webUrl": item.get("webUrl", "")
                        })
        
        return files
    
    def upload_file(self, file_content, filename: str, folder_path: str = "root") -> bool:
        """Upload file to OneDrive"""
        try:
            if self.use_mock:
                # Mock implementation
                filepath = os.path.join(self.mock_storage, filename)
                with open(filepath, "wb") as f:
                    f.write(file_content.getvalue())
                return True
            else:
                # Real OneDrive API - Simple upload for files < 4MB
                file_bytes = file_content.getvalue()
                file_size = len(file_bytes)
                
                if file_size < 4 * 1024 * 1024:  # Less than 4MB
                    # Simple upload
                    endpoint = f"/me/drive/{folder_path}:/{filename}:/content"
                    headers = {"Content-Type": "application/octet-stream"}
                    
                    url = f"{self.graph_api_endpoint}{endpoint}"
                    response = requests.put(
                        url,
                        headers={
                            "Authorization": f"Bearer {self.access_token}",
                            "Content-Type": "application/octet-stream"
                        },
                        data=file_bytes
                    )
                    
                    if response.status_code in [200, 201]:
                        return True
                    else:
                        st.error(f"Upload failed: {response.status_code}")
                        return False
                else:
                    # Large file upload session (for files > 4MB)
                    return self._upload_large_file(file_bytes, filename, folder_path)
                    
        except Exception as e:
            st.error(f"Upload error: {str(e)}")
            return False
    
    def _upload_large_file(self, file_bytes: bytes, filename: str, folder_path: str = "root") -> bool:
        """Upload large file using upload session"""
        try:
            # Create upload session
            endpoint = f"/me/drive/{folder_path}:/{filename}:/createUploadSession"
            session_result = self._make_graph_request(endpoint, method="POST")
            
            if not session_result or "uploadUrl" not in session_result:
                return False
            
            upload_url = session_result["uploadUrl"]
            file_size = len(file_bytes)
            chunk_size = 320 * 1024  # 320 KB chunks
            
            # Upload in chunks
            progress = st.progress(0)
            for i in range(0, file_size, chunk_size):
                chunk = file_bytes[i:i + chunk_size]
                chunk_end = min(i + chunk_size, file_size) - 1
                
                headers = {
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {i}-{chunk_end}/{file_size}"
                }
                
                response = requests.put(upload_url, headers=headers, data=chunk)
                
                if response.status_code not in [200, 201, 202]:
                    st.error(f"Chunk upload failed: {response.status_code}")
                    return False
                
                # Update progress
                progress.progress(min((i + chunk_size) / file_size, 1.0))
            
            progress.empty()
            return True
            
        except Exception as e:
            st.error(f"Large file upload error: {str(e)}")
            return False
    
    def upload_multiple_files(self, files: list, folder_path: str = "root") -> Dict[str, bool]:
        """Upload multiple files at once"""
        results = {}
        
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        for i, file in enumerate(files):
            progress_text.text(f"Uploading {file.name}... ({i+1}/{len(files)})")
            success = self.upload_file(file, file.name, folder_path)
            results[file.name] = success
            progress_bar.progress((i + 1) / len(files))
        
        progress_text.empty()
        progress_bar.empty()
        
        return results
    
    def download_file(self, filename: str = None, file_id: str = None) -> Optional[bytes]:
        """Download file from OneDrive"""
        if self.use_mock:
            # Mock implementation
            if filename:
                filepath = os.path.join(self.mock_storage, filename)
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        return f.read()
        else:
            # Real OneDrive API
            if file_id:
                endpoint = f"/me/drive/items/{file_id}/content"
            elif filename:
                endpoint = f"/me/drive/root:/{filename}:/content"
            else:
                return None
            
            url = f"{self.graph_api_endpoint}{endpoint}"
            
            try:
                response = requests.get(
                    url,
                    headers={"Authorization": f"Bearer {self.access_token}"}
                )
                
                if response.status_code == 200:
                    return response.content
                else:
                    st.error(f"Download failed: {response.status_code}")
                    return None
                    
            except Exception as e:
                st.error(f"Download error: {str(e)}")
                return None
        
        return None
    
    def delete_file(self, filename: str = None, file_id: str = None) -> bool:
        """Delete file from OneDrive"""
        try:
            if self.use_mock:
                # Mock implementation
                if filename:
                    filepath = os.path.join(self.mock_storage, filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        return True
            else:
                # Real OneDrive API
                if file_id:
                    endpoint = f"/me/drive/items/{file_id}"
                elif filename:
                    endpoint = f"/me/drive/root:/{filename}"
                else:
                    return False
                
                result = self._make_graph_request(endpoint, method="DELETE")
                return result is not None
                
        except Exception as e:
            st.error(f"Delete error: {str(e)}")
            return False
        
        return False
    
    def create_folder(self, folder_name: str, parent_folder: str = "root") -> bool:
        """Create a folder in OneDrive"""
        if self.use_mock:
            folder_path = os.path.join(self.mock_storage, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            return True
        else:
            endpoint = f"/me/drive/{parent_folder}/children"
            data = json.dumps({
                "name": folder_name,
                "folder": {},
                "@microsoft.graph.conflictBehavior": "rename"
            }).encode()
            
            result = self._make_graph_request(endpoint, method="POST", data=data)
            return result is not None
    
    def get_share_link(self, file_id: str) -> Optional[str]:
        """Get shareable link for a file"""
        if self.use_mock:
            return f"mock://localhost/{file_id}"
        else:
            endpoint = f"/me/drive/items/{file_id}/createLink"
            data = json.dumps({
                "type": "view",
                "scope": "anonymous"
            }).encode()
            
            result = self._make_graph_request(endpoint, method="POST", data=data)
            
            if result and "link" in result:
                return result["link"].get("webUrl")
            
            return None
