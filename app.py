"""
Role-Based Document-Aware Chatbot
Banking environment document assistant with role-based access control
"""

import streamlit as st
import config
from modules import (
    init_session_state,
    load_custom_css,
    DocumentProcessor,
    AIService,
    OneDriveService,
    AudioService,
    AuthService,
    format_timestamp,
    format_file_size,
    get_file_icon
)

# Page configuration
st.set_page_config(
    page_title="Banking Document Assistant",
    page_icon="🏦",
    layout=config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()
load_custom_css()

# Initialize auth service
if 'auth_service' not in st.session_state:
    st.session_state.auth_service = AuthService()

# Initialize authentication state
if 'user' not in st.session_state:
    st.session_state.user = None

# ========== LOGIN PAGE ==========
def show_login_page():
    """Display login page"""
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem;">
            <h1 style="color: #5f6fd8;">🏦 Banking Document Assistant</h1>
            <p style="color: #6b7280; font-size: 1.1rem;">Secure Role-Based Document Chatbot</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username and password:
                    user_info = st.session_state.auth_service.authenticate(username, password)
                    
                    if user_info['authenticated']:
                        st.session_state.user = user_info
                        st.session_state.auth_service.log_action(username, "LOGIN", "Successful login")
                        st.success(f"✅ Welcome {user_info['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                        st.session_state.auth_service.log_action(username, "LOGIN_FAILED", "Invalid credentials")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        # Demo credentials info
        with st.expander("ℹ️ Demo Credentials"):
            st.markdown("""
            **Admin Account:**
            - Username: `admin`
            - Password: `admin123`
            - Can upload and manage documents
            
            **User Account:**
            - Username: `user1`
            - Password: `user123`
            - Can query chatbot only
            
            **Team Lead Account:**
            - Username: `teamlead`
            - Password: `lead123`
            - Admin privileges
            """)

# ========== MAIN APPLICATION ==========
def show_main_app():
    """Display main application with role-based access"""
    
    # Initialize services
    if 'ai_service' not in st.session_state:
        st.session_state.ai_service = AIService()
        st.session_state.ai_service.load_model()
    
    if 'onedrive_service' not in st.session_state:
        st.session_state.onedrive_service = OneDriveService(use_mock=config.USE_MOCK_ONEDRIVE)
    
    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown('<h1 class="gradient-header">🏦 Banking Document Assistant</h1>', unsafe_allow_html=True)
    with col2:
        role_color = "🔴" if st.session_state.user['role'] == "Admin" else "🔵"
        st.info(f"{role_color} **{st.session_state.user['role']}**\n{st.session_state.user['name']}")
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.auth_service.log_action(st.session_state.user['username'], "LOGOUT", "User logged out")
            st.session_state.user = None
            st.rerun()
    
    # ========== SIDEBAR: SOURCES PANEL ==========
    with st.sidebar:
        st.markdown("### 📁 Document Sources")
        st.markdown("---")
        
        # Admin-only document upload
        is_admin = st.session_state.auth_service.is_admin(st.session_state.user)
        
        if is_admin:
            st.markdown("### 📤 Upload Documents (Admin Only)")
            
            # OneDrive Authentication (if not using mock)
            if not config.USE_MOCK_ONEDRIVE:
                if 'onedrive_authenticated' not in st.session_state:
                    st.session_state.onedrive_authenticated = False
                
                if not st.session_state.onedrive_authenticated:
                    if st.button("🔐 Connect to OneDrive", use_container_width=True):
                        with st.spinner("Authenticating..."):
                            success = st.session_state.onedrive_service.authenticate()
                            st.session_state.onedrive_authenticated = success
                            if success:
                                st.rerun()
                else:
                    st.success("✅ OneDrive Connected")
            
            # Multiple file uploader
            uploaded_files = st.file_uploader(
                "Choose files (multiple allowed)",
                type=[ext.replace(".", "") for ext in config.ALLOWED_EXTENSIONS],
                help="Upload one or more documents to analyze",
                accept_multiple_files=True
            )
            
            if uploaded_files:
                st.info(f"📁 {len(uploaded_files)} file(s) selected")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💾 Save All to Storage"):
                        with st.spinner(f"Uploading {len(uploaded_files)} files..."):
                            results = st.session_state.onedrive_service.upload_multiple_files(uploaded_files)
                            
                            success_count = sum(1 for v in results.values() if v)
                            if success_count > 0:
                                st.success(f"✅ Uploaded {success_count}/{len(uploaded_files)} files!")
                                st.session_state.auth_service.log_action(
                                    st.session_state.user['username'],
                                    "UPLOAD_DOCUMENTS",
                                    f"Uploaded {success_count} files"
                                )
                                st.rerun()
                            else:
                                st.error("❌ Upload failed")
                
                with col2:
                    if st.button("📖 Process All"):
                        with st.spinner("Processing documents..."):
                            for uploaded_file in uploaded_files:
                                doc_data = DocumentProcessor.process_file(
                                    uploaded_file.name,
                                    uploaded_file
                                )
                                
                                if "error" not in doc_data:
                                    st.session_state.uploaded_files.append(doc_data)
                                    st.session_state.document_content[doc_data['filename']] = doc_data['text']
                            
                            if uploaded_files:
                                st.session_state.current_document = st.session_state.uploaded_files[-1]
                                st.session_state.auth_service.log_action(
                                    st.session_state.user['username'],
                                    "PROCESS_DOCUMENTS",
                                    f"Processed {len(uploaded_files)} files"
                                )
                                st.success(f"✅ Processed {len(uploaded_files)} documents!")
                                st.rerun()
                
                with col3:
                    if st.button("💾+📖 Both"):
                        with st.spinner("Uploading and processing..."):
                            # Upload first
                            results = st.session_state.onedrive_service.upload_multiple_files(uploaded_files)
                            
                            # Then process
                            for uploaded_file in uploaded_files:
                                doc_data = DocumentProcessor.process_file(
                                    uploaded_file.name,
                                    uploaded_file
                                )
                                
                                if "error" not in doc_data:
                                    st.session_state.uploaded_files.append(doc_data)
                                    st.session_state.document_content[doc_data['filename']] = doc_data['text']
                            
                            if uploaded_files:
                                st.session_state.current_document = st.session_state.uploaded_files[-1]
                                success_count = sum(1 for v in results.values() if v)
                                st.session_state.auth_service.log_action(
                                    st.session_state.user['username'],
                                    "UPLOAD_AND_PROCESS",
                                    f"Uploaded and processed {len(uploaded_files)} files"
                                )
                                st.success(f"✅ Uploaded ({success_count}) & Processed ({len(uploaded_files)}) documents!")
                                st.rerun()
        else:
            st.info("📌 Document upload is restricted to Admins")
        
        #  OneDrive Section (All users can view)
        st.markdown("---")
        with st.expander("☁️ Document Storage", expanded=True):
            if config.USE_MOCK_ONEDRIVE:
                st.caption("📌 Using local storage")
            
            if st.button("🔄 Refresh Files"):
                st.session_state.onedrive_files = st.session_state.onedrive_service.list_files()
            
            # Display storage files
            storage_files = st.session_state.onedrive_service.list_files()
            if storage_files:
                st.markdown(f"**{len(storage_files)} files:**")
                for file in storage_files:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.text(f"{get_file_icon(file['name'])} {file['name']}")
                    with col2:
                        if st.button("📖", key=f"process_storage_{file['name']}", help="Process this file"):
                            content = st.session_state.onedrive_service.download_file(file['name'])
                            if content:
                                import io
                                doc_data = DocumentProcessor.process_file(
                                    file['name'],
                                    io.BytesIO(content)
                                )
                                if "error" not in doc_data:
                                    st.session_state.uploaded_files.append(doc_data)
                                    st.session_state.current_document = doc_data
                                    st.session_state.document_content[doc_data['filename']] = doc_data['text']
                                    st.success("✅ Loaded from storage!")
                                    st.rerun()
            else:
                st.write("No files in storage")
        
        # Display processed documents
        st.markdown("---")
        st.markdown("### 📚 Processed Documents")
        
        if st.session_state.uploaded_files:
            for i, doc in enumerate(st.session_state.uploaded_files):
                with st.container():
                    st.markdown(
                        f"""
                        <div class="source-card">
                            <div style="font-weight: 600;">{get_file_icon(doc['filename'])} {doc['filename']}</div>
                            <div style="font-size: 0.85rem; color: #6b7280;">
                                {doc['metadata'].get('word_count', 0)} words
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📖 Select", key=f"open_{i}"):
                            st.session_state.current_document = doc
                            st.rerun()
                    with col2:
                        if is_admin and st.button("🗑️ Remove", key=f"remove_{i}"):
                            st.session_state.uploaded_files.pop(i)
                            st.session_state.auth_service.log_action(
                                st.session_state.user['username'],
                                "DELETE_DOCUMENT",
                                f"Removed {doc['filename']}"
                            )
                            st.rerun()
        else:
            st.info("No documents processed yet")
    
    # ========== MAIN AREA: CHAT PANEL ==========
    main_col, studio_col = st.columns([2, 1])
    
    with main_col:
        st.markdown("### 💬 Document Q&A Chatbot")
        
        # Display current document info
        if st.session_state.current_document:
            doc = st.session_state.current_document
            st.success(f"📄 Active: **{doc['filename']}** ({doc['metadata'].get('word_count', 0)} words)")
            
            # Suggested questions
            if 'suggested_questions' not in st.session_state:
                st.session_state.suggested_questions = []
            
            if st.button("✨ Generate Suggested Questions"):
                with st.spinner("Generating suggestions..."):
                    text = doc['text']
                    questions = st.session_state.ai_service.suggest_questions(text)
                    st.session_state.suggested_questions = questions
                    st.session_state.auth_service.log_action(
                        st.session_state.user['username'],
                        "GENERATE_QUESTIONS",
                        f"For {doc['filename']}"
                    )
            
            if st.session_state.suggested_questions:
                st.markdown("**💡 Suggested Questions:**")
                for q in st.session_state.suggested_questions:
                    if st.button(q, key=f"suggested_{q}"):
                        st.session_state.messages.append({"role": "user", "content": q})
                        with st.spinner("Thinking..."):
                            response = st.session_state.ai_service.chat_with_document(
                                q, doc['text'], doc['filename']
                            )
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            st.session_state.auth_service.log_action(
                                st.session_state.user['username'],
                                "ASK_QUESTION",
                                f"Q: {q[:50]}..."
                            )
                        st.rerun()
        
        st.markdown("---")
        
        # Chat messages display
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                role = msg["role"]
                content = msg["content"]
                
                if role == "user":
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                            <div style="max-width: 70%; background: #e0e7ff; padding: 1rem; border-radius: 1rem;">
                                <div style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem;">
                                    👤 You
                                </div>
                                <div>{content}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                            <div style="max-width: 70%; background: #f3f4f6; padding: 1rem; border-radius: 1rem;">
                                <div style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem;">
                                    🤖 Assistant
                                </div>
                                <div>{content}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
        # Chat input
        if st.session_state.current_document:
            user_input = st.chat_input("Ask a question about your document...")
            
            if user_input:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Generate AI response with citation
                with st.spinner("Thinking..."):
                    response = st.session_state.ai_service.chat_with_document(
                        user_input,
                        st.session_state.current_document['text'],
                        st.session_state.current_document['filename']
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.auth_service.log_action(
                        st.session_state.user['username'],
                        "ASK_QUESTION",
                        f"Q: {user_input[:100]}..."
                    )
                
                st.rerun()
        else:
            st.info("👈 Select or upload a document to start chatting!")
    
    # ========== STUDIO PANEL: OUTPUTS ==========
    with studio_col:
        st.markdown("### 🎨 Generate Outputs")
        
        if st.session_state.current_document:
            doc = st.session_state.current_document
            text = doc['text']
            
            # Action buttons in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "📚 Study Guide", "❓ FAQ", "🎧 Audio"])
            
            with tab1:
                if st.button("Generate Summary", use_container_width=True):
                    with st.spinner("Creating summary..."):
                        summary = st.session_state.ai_service.generate_summary(text)
                        st.session_state.outputs.append({
                            "type": "Summary",
                            "content": summary,
                            "timestamp": format_timestamp(),
                            "source": doc['filename']
                        })
                        st.session_state.auth_service.log_action(
                            st.session_state.user['username'],
                            "GENERATE_SUMMARY",
                            doc['filename']
                        )
                        st.rerun()
            
            with tab2:
                if st.button("Generate Study Guide", use_container_width=True):
                    with st.spinner("Creating study guide..."):
                        guide = st.session_state.ai_service.generate_study_guide(text)
                        st.session_state.outputs.append({
                            "type": "Study Guide",
                            "content": guide,
                            "timestamp": format_timestamp(),
                            "source": doc['filename']
                        })
                        st.session_state.auth_service.log_action(
                            st.session_state.user['username'],
                            "GENERATE_GUIDE",
                            doc['filename']
                        )
                        st.rerun()
            
            with tab3:
                if st.button("Generate FAQ", use_container_width=True):
                    with st.spinner("Creating FAQ..."):
                        faq = st.session_state.ai_service.generate_faq(text)
                        st.session_state.outputs.append({
                            "type": "FAQ",
                            "content": faq,
                            "timestamp": format_timestamp(),
                            "source": doc['filename']
                        })
                        st.session_state.auth_service.log_action(
                            st.session_state.user['username'],
                            "GENERATE_FAQ",
                            doc['filename']
                        )
                        st.rerun()
            
            with tab4:
                if st.button("Generate Audio Overview", use_container_width=True):
                    with st.spinner("Creating audio..."):
                        summary = st.session_state.ai_service.generate_summary(text)
                        audio_path = AudioService.generate_overview(summary)
                        
                        if audio_path and not audio_path.startswith("Error"):
                            st.audio(audio_path)
                            st.success("🎧 Audio ready!")
                            st.session_state.auth_service.log_action(
                                st.session_state.user['username'],
                                "GENERATE_AUDIO",
                                doc['filename']
                            )
                        else:
                            st.error(audio_path)
            
            # Display outputs
            st.markdown("---")
            st.markdown("**📊 Generated Outputs:**")
            
            if st.session_state.outputs:
                for i, output in enumerate(reversed(st.session_state.outputs)):
                    with st.expander(f"{output['type']} - {output.get('source', 'Unknown')}", expanded=i == 0):
                        st.markdown(
                            f"""
                            <div class="output-card">
                                <div style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem;">
                                    {output['timestamp']}
                                </div>
                                {output['content']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.info("No outputs generated yet")
        
        else:
            st.info("👈 Select a document to generate outputs")
    
    # Footer with statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Documents Processed", len(st.session_state.uploaded_files))
    with col2:
        st.metric("Questions Asked", len([m for m in st.session_state.messages if m['role'] == 'user']))
    with col3:
        st.metric("Outputs Generated", len(st.session_state.outputs))
    with col4:
        st.metric("Your Role", st.session_state.user['role'])

# ========== ROUTE TO APPROPRIATE PAGE ==========
if st.session_state.user is None:
    show_login_page()
else:
    show_main_app()
