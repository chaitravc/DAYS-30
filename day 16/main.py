import logging
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

# ---------------------------------------------------
# Configure logging
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# ---------------------------------------------------
# Initialize FastAPI app
# ---------------------------------------------------
app = FastAPI(title="AI Voice Agent - Streaming", version="1.0.0")

# Base directory and uploads folder
BASE_DIR = Path(_file_).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# ---------- WebSocket Audio Streaming ----------
# ---------------------------------------------------
@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    """Receive audio chunks from client and save them to a file."""
    await websocket.accept()
    file_id = uuid4().hex
    file_path = UPLOADS_DIR / f"streamed_{file_id}.webm"

    try:
        with open(file_path, "wb") as f:
            logger.info(f"Saving streamed audio to {file_path}")
            while True:
                message = await websocket.receive()
                if "bytes" in message:
                    f.write(message["bytes"])
                elif message.get("text") == "EOF":
                    logger.info("Recording finished. Closing file.")
                    break
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()

# ---------------------------------------------------
# ---------- Health Check ----------
# ---------------------------------------------------
@app.get("/health")
async def health_check():
    return {
        "status": "AI Voice Agent Streaming Running!",
        "version": "1.0.0",
        "endpoints": [
            "/ws/audio"
        ]
    }

# ---------------------------------------------------
# ---------- App Initialization ----------
# ---------------------------------------------------
app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
