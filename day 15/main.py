import logging
import shutil
import asyncio
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File, APIRouter, HTTPException, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect

from services.stt_service import SpeechToTextService
from services.tts_service import TextToSpeechService
from services.llm_service import LLMService
from schemas.models import TTSRequest, ChatResponse, UploadResponse

# ---------------------------------------------------
# Configure logging
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------
# Initialize FastAPI app FIRST ✅
# ---------------------------------------------------
app = FastAPI(title="AI Voice Agent - Combined", version="1.6.0")

# Base directory and uploads folder
BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Initialize services
stt_service = SpeechToTextService()
tts_service = TextToSpeechService()
llm_service = LLMService()

# In-memory chat history (for demo)
chat_history_store = {}

# API router for REST endpoints
api_router = APIRouter(prefix="/api")

# ---------------------------------------------------
# ---------- TTS Endpoint ----------
# ---------------------------------------------------
@api_router.post("/text-to-speech", response_model=ChatResponse)
async def generate_speech(request: TTSRequest):
    """Convert text to speech using Murf."""
    try:
        audio_url = await tts_service.generate_speech(request.text, request.voice_id, request.style)
        return ChatResponse(
            transcript=request.text,
            llm_response=request.text,
            audio_url=audio_url
        )
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------
# ---------- Upload Audio ----------
# ---------------------------------------------------
@api_router.post("/upload-audio/", response_model=UploadResponse)
async def upload_audio(file: UploadFile = File(...)):
    """Save uploaded file to uploads/ and return info."""
    file_path = None
    try:
        # Validate file type and size
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Audio files only.")

        file_path = UPLOADS_DIR / f"{uuid4().hex}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_stats = file_path.stat()
        return UploadResponse(
            filename=file.filename,
            content_type=file.content_type,
            size_in_bytes=file_stats.st_size
        )
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    finally:
        if file_path and file_path.exists():
            try:
                file_path.unlink()  # Clean up temporary file
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {file_path}: {str(e)}")


# ---------------------------------------------------
# ---------- Transcribe Audio ----------
# ---------------------------------------------------
@api_router.post("/transcribe/file", response_model=ChatResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe audio using AssemblyAI."""
    file_path = None
    try:
        file_path = UPLOADS_DIR / f"{uuid4().hex}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcript = await stt_service.transcribe_audio(file_path)
        return ChatResponse(transcript=transcript, llm_response=transcript, audio_url="")
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {file_path}: {str(e)}")


# ---------------------------------------------------
# ---------- Echo Bot ----------
# ---------------------------------------------------
@api_router.post("/tts/echo", response_model=ChatResponse)
async def echo_bot(file: UploadFile = File(...)):
    """Transcribe audio and generate same text as audio."""
    file_path = None
    try:
        file_path = UPLOADS_DIR / f"{uuid4().hex}_{file.filename or f'recorded_{int(asyncio.get_event_loop().time())}.webm'}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcript = await stt_service.transcribe_audio(file_path)
        audio_url = await tts_service.generate_speech(transcript, voice_id="en-US-ken", style="Conversational")
        return ChatResponse(transcript=transcript, llm_response=transcript, audio_url=audio_url)
    except Exception as e:
        logger.error(f"EchoBot error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"EchoBot failed: {str(e)}")
    finally:
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {file_path}: {str(e)}")


# ---------------------------------------------------
# ---------- LLM Query with Gemini ----------
# ---------------------------------------------------
@api_router.post("/llm/query", response_model=ChatResponse)
async def llm_query(file: UploadFile = File(...)):
    """Transcribe audio, query Gemini LLM, and return text/audio response."""
    file_path = None
    try:
        file_path = UPLOADS_DIR / f"{uuid4().hex}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcript = await stt_service.transcribe_audio(file_path)
        llm_response = await llm_service.query_llm(transcript)
        audio_url = await tts_service.generate_speech(llm_response, voice_id="en-US-ken", style="Conversational")
        return ChatResponse(transcript=transcript, llm_response=llm_response, audio_url=audio_url)
    except Exception as e:
        logger.error(f"LLM query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM query failed: {str(e)}")
    finally:
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {file_path}: {str(e)}")


# ---------------------------------------------------
# ---------- Chat History Agent ----------
# ---------------------------------------------------
@api_router.post("/agent/chat/{session_id}", response_model=ChatResponse)
async def chat_with_agent(session_id: str, file: UploadFile = File(...)):
    """Chat with history: transcribe audio, maintain history, query LLM, return audio."""
    file_path = None
    try:
        file_path = UPLOADS_DIR / f"{uuid4().hex}_{file.filename or f'recorded_{int(asyncio.get_event_loop().time())}.webm'}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe audio
        transcript = await stt_service.transcribe_audio(file_path)

        # Manage chat history
        if session_id not in chat_history_store:
            chat_history_store[session_id] = []
        chat_history = chat_history_store[session_id]
        chat_history.append({"role": "user", "content": transcript})

        # Query LLM with history
        llm_response = await llm_service.query_llm_with_history(chat_history)
        chat_history.append({"role": "assistant", "content": llm_response})

        # Limit history to last 10 messages
        chat_history_store[session_id] = chat_history[-10:]

        # Generate audio
        audio_url = await tts_service.generate_speech(llm_response, voice_id="en-US-ken", style="Conversational")
        return ChatResponse(transcript=transcript, llm_response=llm_response, audio_url=audio_url)
    except Exception as e:
        logger.error(f"Chat agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat agent failed: {str(e)}")
    finally:
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {file_path}: {str(e)}")


# ---------------------------------------------------
# ---------- WebSocket Endpoint ----------
# ---------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Establish a WebSocket connection and echo back received messages."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()


# ---------------------------------------------------
# ---------- Health Check ----------
# ---------------------------------------------------
@api_router.get("/health")
async def health_check():
    return {
        "status": "AI Voice Agent Running!",
        "version": "1.6.0",
        "endpoints": [
            "/api/text-to-speech",
            "/api/upload-audio/",
            "/api/transcribe/file",
            "/api/tts/echo",
            "/api/llm/query",
            "/agent/chat/{session_id}",
            "/ws"
        ]
    }


# ---------------------------------------------------
# ---------- App Initialization ----------
# ---------------------------------------------------
app.include_router(api_router)
app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
