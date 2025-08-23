# main.py
import logging
from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent,
)
from typing import Type
import os
from dotenv import load_dotenv
import asyncio
from concurrent.futures import TimeoutError
import json
from services.llm_service import LLMService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not aai.settings.api_key:
    raise ValueError("ASSEMBLYAI_API_KEY is missing.")

# Initialize FastAPI app
app = FastAPI(title="AI Voice Agent - Streaming", version="1.0.0")

# Base directory and uploads folder
BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "Uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Global WebSocket connection storage
active_websockets = {}


# WebSocket Audio Streaming with AssemblyAI Transcription
@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    """Receive PCM audio chunks from client and transcribe in real-time using AssemblyAI."""
    await websocket.accept()
    file_id = uuid4().hex
    file_path = UPLOADS_DIR / f"streamed_{file_id}.pcm"

    # Store WebSocket connection for audio streaming
    connection_id = uuid4().hex
    active_websockets[connection_id] = websocket

    # Initialize LLMService with WebSocket connection
    llm_service = LLMService(websocket)

    # Initialize AssemblyAI StreamingClient
    client = StreamingClient(
        StreamingClientOptions(
            api_key=aai.settings.api_key,
            api_host="streaming.assemblyai.com",
        )
    )

    # Get the event loop for WebSocket communication
    loop = asyncio.get_event_loop()

    # Define event handlers
    def on_begin(_: Type[StreamingClient], event: BeginEvent):
        try:
            msg = {"type": "session", "message": f"Session started: {event.id}"}
            asyncio.run_coroutine_threadsafe(
                websocket.send_json(msg), loop
            ).result(timeout=5)
        except TimeoutError:
            pass
        except Exception:
            pass

    def on_turn(_: Type[StreamingClient], event: TurnEvent):
        is_formatted = hasattr(event, 'turn_is_formatted') and event.turn_is_formatted
        if event.end_of_turn:
            try:
                msg = {"type": "end_of_turn"}
                asyncio.run_coroutine_threadsafe(
                    websocket.send_json(msg), loop
                ).result(timeout=5)
            except TimeoutError:
                pass
            except Exception:
                pass
        if is_formatted and event.end_of_turn:
            try:
                msg = {"type": "transcript", "text": event.transcript}
                asyncio.run_coroutine_threadsafe(
                    websocket.send_json(msg), loop
                ).result(timeout=5)
                # Stream LLM response for final transcript
                asyncio.run_coroutine_threadsafe(
                    llm_service.stream_llm(event.transcript), loop
                )
            except TimeoutError:
                pass
            except Exception as e:
                logger.error(f"Error in on_turn handler: {str(e)}")

    def on_terminated(_: Type[StreamingClient], event: TerminationEvent):
        try:
            msg = {"type": "termination", "message": f"Session ended: {event.audio_duration_seconds}s processed"}
            asyncio.run_coroutine_threadsafe(
                websocket.send_json(msg), loop
            ).result(timeout=5)
        except TimeoutError:
            pass
        except Exception:
            pass

    def on_error(_: Type[StreamingClient], error: StreamingError):
        try:
            msg = {"type": "error", "message": str(error)}
            asyncio.run_coroutine_threadsafe(
                websocket.send_json(msg), loop
            ).result(timeout=5)
        except TimeoutError:
            pass
        except Exception:
            pass

    # Register event handlers
    client.on(StreamingEvents.Begin, on_begin)
    client.on(StreamingEvents.Turn, on_turn)
    client.on(StreamingEvents.Termination, on_terminated)
    client.on(StreamingEvents.Error, on_error)

    # Connect to AssemblyAI streaming service
    client.connect(
        StreamingParameters(
            sample_rate=16000,
            format_turns=True,
        )
    )

    try:
        with open(file_path, "wb") as f:
            while True:
                message = await websocket.receive()
                if "bytes" in message:
                    pcm_data = message["bytes"]
                    f.write(pcm_data)
                    client.stream(pcm_data)
                elif message.get("text") == "EOF":
                    break
    except WebSocketDisconnect:
        pass
    except Exception as err:
        try:
            await websocket.send_json({"type": "error", "message": str(err)})
        except:
            pass
    finally:
        # Clean up WebSocket connection
        if connection_id in active_websockets:
            del active_websockets[connection_id]
        client.disconnect(terminate=True)
        await websocket.close()


# Health Check
@app.get("/health")
async def health_check():
    return {
        "status": "AI Voice Agent Streaming Running!",
        "version": "1.0.0",
        "endpoints": ["/ws/audio"],
    }


# App Initialization
app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
