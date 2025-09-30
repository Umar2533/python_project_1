# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routers import data_handler

app = FastAPI(
    title="CAG Project API Chat with Your Documents",
    description="An API For uploading PDF, querying and chatting with your documents",
    version="1.0.0",
)

# CORS - allow local development origins (Streamlit runs on 8501)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production restrict to your frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    data_handler.router,
    prefix="/api/v1",
    tags=["Data Handling - chat with your documents"],
)


@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def read_root():
    return """
    <html>
        <head>
            <title>CAG Project API</title>
        </head>
        <body>
            <h1>Welcome to the CAG Project API</h1>
            <p>Use the <code>/api/v1</code> endpoints to interact with the API.</p>
            <p>Visit <a href="/docs">/docs</a> for the interactive API documentation.</p>
        </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
