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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# Load environment variables
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not aai.settings.api_key:
    logger.error("ASSEMBLYAI_API_KEY not found in .env file.")
    raise ValueError("ASSEMBLYAI_API_KEY is missing.")

# Initialize FastAPI app
app = FastAPI(title="AI Voice Agent - Streaming", version="1.0.0")

# Base directory and uploads folder
BASE_DIR = Path(_file_).resolve().parent
UPLOADS_DIR = BASE_DIR / "Uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# WebSocket Audio Streaming with AssemblyAI Transcription
@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    """Receive PCM audio chunks from client and transcribe in real-time using AssemblyAI."""
    await websocket.accept()
    file_id = uuid4().hex
    file_path = UPLOADS_DIR / f"streamed_{file_id}.pcm"

    # Initialize AssemblyAI StreamingClient
    client = StreamingClient(
        StreamingClientOptions(
            api_key=aai.settings.api_key,
            api_host="streaming.assemblyai.com",
        )
    )

    # Create a queue for transcriptions
    transcription_queue = asyncio.Queue()

    # Define event handlers
    def on_begin(self: Type[StreamingClient], event: BeginEvent):
        logger.info(f"Session started: {event.id}")

    def on_turn(self: Type[StreamingClient], event: TurnEvent):
        logger.info(f"Transcript: {event.transcript} (End of turn: {event.end_of_turn})")
        if event.transcript:
            transcription_queue.put_nowait(event.transcript)
        if event.end_of_turn and not event.turn_is_formatted:
            params = StreamingParameters(sample_rate=16000, format_turns=True)
            self.set_params(params)

    def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
        logger.info(f"Session terminated: {event.audio_duration_seconds} seconds of audio processed")

    def on_error(self: Type[StreamingClient], error: StreamingError):
        logger.error(f"Streaming error: {error}")

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
        # Save audio to file for debugging (optional)
        with open(file_path, "wb") as f:
            while True:
                message = await websocket.receive()
                if "bytes" in message:
                    pcm_data = message["bytes"]
                    logger.debug(f"Received audio chunk of size: {len(pcm_data)} bytes")
                    f.write(pcm_data)  # Save to file for debugging
                    client.stream(pcm_data)
                elif message.get("text") == "EOF":
                    logger.info("Recording finished. Closing transcription session.")
                    break

                # Process queued transcriptions and send to client
                while not transcription_queue.empty():
                    transcript = await transcription_queue.get()
                    await websocket.send_text(transcript)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        client.disconnect(terminate=True)
        await websocket.close()

# Health Check
@app.get("/health")
async def health_check():
    return {
        "status": "AI Voice Agent Streaming Running!",
        "version": "1.0.0",
        "endpoints": [
            "/ws/audio"
        ]
    }

# App Initialization
app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
