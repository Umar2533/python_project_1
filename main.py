# # main.py
# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from src.routers import data_handler

# app = FastAPI(
#     title="CAG Project API Chat with Your Documents",
#     description="An API For uploading PDF, querying and chatting with your documents",
#     version="1.0.0",
# )

# # CORS - allow local development origins (Streamlit runs on 8501)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # in production restrict to your frontend origin(s)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(
#     data_handler.router,
#     prefix="/api/v1",
#     tags=["Data Handling - chat with your documents"],
# )


# @app.get("/", response_class=HTMLResponse, tags=["Root"])
# async def read_root():
#     return """
#     <html>
#         <head>
#             <title>CAG Project API</title>
#         </head>
#         <body>
#             <h1>Welcome to the CAG Project API</h1>
#             <p>Use the <code>/api/v1</code> endpoints to interact with the API.</p>
#             <p>Visit <a href="/docs">/docs</a> for the interactive API documentation.</p>
#         </body>
#     </html>
#     """

import streamlit as st
import pypdf


st.set_page_config(page_title="Chat with your PDF", page_icon="📄")

st.title("📄 Chat with your PDF (Simple Version)")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    # Extract text
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    st.success("✅ PDF Uploaded & Text Extracted")

    # Show preview
    with st.expander("Preview Extracted Text"):
        st.write(text[:2000])  # sirf pehle 2000 chars show kar rahe hain

    # Query box
    query = st.text_input("Ask something about the PDF:")

    if query:
        # simple keyword search
        if query.lower() in text.lower():
            start = text.lower().find(query.lower())
            end = start + 300
            answer = text[start:end]
            st.info(f"🔍 Found something related:\n\n{answer}")
        else:
            st.warning("❌ No exact match found in the PDF.")

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)


