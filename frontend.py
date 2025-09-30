import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8001/api/v1"

# ============ Page Config ============
st.set_page_config(
    page_title="📄 PDF Query Assistant",
    page_icon="🤖",
    layout="wide"
)

# ============ Custom Dark Theme CSS ============
st.markdown("""
    <style>
        body, .main {
            background-color: #1E1E1E;
            color: #E5E5E5;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-title {
            text-align: center;
            color: #10A37F;
            font-size: 32px;
            margin-bottom: 15px;
        }
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #D3D3D3;
            padding: 20px;
        }
        .sidebar-title {
            color: #10A37F;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .stRadio > label {
            display: block;
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 8px;
            background-color: #333333;
            color: #10A37F;
            cursor: pointer;
            transition: all 0.3s ease;
        }
            
        .stRadio > label:hover {
            background-color: #10A37F;
            color: white;
        }
        .stButton > button {
            background-color: #10A37F;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border: none;
        }
        .stButton > button:hover {
            background-color: #0E866A;
        }
        /* Chat bubbles */
        .chat-user {
            background-color: #2563EB;
            color: white;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            text-align: right;
        }
        .chat-bot {
            background-color: #10A37F;
            color: white;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📄 PDF Query Assistant</h1>', unsafe_allow_html=True)

# ============ Sidebar Navigation ============
st.sidebar.markdown('<div class="sidebar-title">📌 Navigation</div>', unsafe_allow_html=True)
menu = st.sidebar.radio(
    "Navigation",
    ["📤 Upload", "📥 Retrieve", "✏️ Update", "🗑️ Delete", "🤖 Chat with PDF"],
    label_visibility="collapsed"
)

# ------------------ Upload ------------------
if menu == "📤 Upload":
    st.subheader("📤 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key="upload_file")

    if uploaded_file and st.button("Upload", key="upload_btn"):
        with st.spinner("Uploading and processing..."):
            response = requests.post(
                f"{API_BASE}/uploadfile",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")},
            )

        if response.status_code == 201:
            result = response.json()
            st.success(f"✅ {result['message']}")
            st.info(f"📌 File ID: `{result['file_id']}`")
            st.session_state["last_file_id"] = result["file_id"]
        else:
            st.error(f"❌ Upload failed: {response.text}")


# ------------------ Retrieve ------------------
elif menu == "📥 Retrieve":
    st.subheader("📥 Retrieve File Data")
    file_id = st.text_input("Enter File ID", value=st.session_state.get("last_file_id", ""), key="retrieve_id")

    if st.button("Retrieve", key="retrieve_btn"):
        if not file_id:
            st.warning("⚠️ Please provide a File ID.")
        else:
            response = requests.get(f"{API_BASE}/uploadfile/{file_id}")
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ {result['message']}")
                st.write("**File Name:**", result["file_name"])
                st.text_area("Extracted Text", result["text"], height=250, key="retrieve_text")
            else:
                st.error(f"❌ Retrieval failed: {response.text}")


# ------------------ Update ------------------
elif menu == "✏️ Update":
    st.subheader("✏️ Update PDF File")
    file_id = st.text_input("Enter File ID to Update", value=st.session_state.get("last_file_id", ""), key="update_id")
    updated_file = st.file_uploader("Choose New PDF File", type=["pdf"], key="update_file")

    if updated_file and st.button("Update", key="update_btn"):
        with st.spinner("Updating file..."):
            response = requests.put(
                f"{API_BASE}/uploadfile/{file_id}",
                files={"file": (updated_file.name, updated_file, "application/pdf")},
            )

        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result['message']}")
        else:
            st.error(f"❌ Update failed: {response.text}")


# ------------------ Delete ------------------
elif menu == "🗑️ Delete":
    st.subheader("🗑️ Delete PDF File")
    file_id = st.text_input("Enter File ID to Delete", value=st.session_state.get("last_file_id", ""), key="delete_id")

    if st.button("Delete", key="delete_btn"):
        with st.spinner("Deleting file..."):
            response = requests.delete(f"{API_BASE}/uploadfile/{file_id}")

        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result['message']}")
        else:
            st.error(f"❌ Delete failed: {response.text}")


# ------------------ Query with LLM ------------------
elif menu == "🤖 Chat with PDF":
    st.subheader("🤖 Chat with PDF")
    file_id = st.text_input("Enter File ID", value=st.session_state.get("last_file_id", ""), key="query_id")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_area("Ask a Question", key="query_text")

    if st.button("Send", key="query_btn"):
        if not file_id or not user_question.strip():
            st.warning("⚠️ Please provide both File ID and Question.")
        else:
            with st.spinner("Getting answer from LLM..."):
                response = requests.get(
                    f"{API_BASE}/query_pdf/{file_id}",
                    params={"question": user_question},
                )

            if response.status_code == 200:
                result = response.json()
                answer = result["answer"]

                st.session_state.chat_history.append(("user", user_question))
                st.session_state.chat_history.append(("bot", answer))
            else:
                st.error(f"❌ Query failed: {response.text}")

    # Display chat bubbles
    for sender, msg in st.session_state.chat_history:
        if sender == "user":
            st.markdown(f'<div class="chat-user">🧑 {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">🤖 {msg}</div>', unsafe_allow_html=True)

