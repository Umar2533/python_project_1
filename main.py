import streamlit as st
import PyPDF2   # ✅ ab PyPDF2 use karenge

st.set_page_config(page_title="Chat with your PDF", page_icon="📄")

st.title("📄 Chat with your PDF (Simple Version)")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    st.success("✅ PDF Uploaded & Text Extracted")

    with st.expander("Preview Extracted Text"):
        st.write(text[:2000])

    query = st.text_input("Ask something about the PDF:")

    if query:
        if query.lower() in text.lower():
            start = text.lower().find(query.lower())
            end = start + 300
            answer = text[start:end]
            st.info(f"🔍 Found something related:\n\n{answer}")
        else:
            st.warning("❌ No exact match found in the PDF.")
