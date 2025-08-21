# llm_service.py
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import os
import websockets
import json
import asyncio
from uuid import uuid4
import re  # For sentence splitting

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.murf_api_key = os.getenv("MURF_API_KEY")
        self.context_id = "day20-static-context"  # Static context_id for Murf to avoid context limit errors
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in .env file.")
            raise ValueError("Gemini API key is missing.")
        if not self.murf_api_key:
            logger.warning("MURF_API_KEY not found in .env file.")
            raise ValueError("Murf API key is missing.")
        genai.configure(api_key=self.api_key)

    async def receive_loop(self, ws):
        audio_chunks = []
        chunk_count = 1
        try:
            while True:
                response = await ws.recv()
                data = json.loads(response)
                #logger.info(f"Murf response: {json.dumps(data, indent=2)}")
                if "audio" in data and data["audio"]:
                    base64_chunk = data["audio"]
                    max_len = 64
                    if len(base64_chunk) > max_len:
                        truncated_chunk = f"{base64_chunk[:30]}...{base64_chunk[-30:]}"
                    else:
                        truncated_chunk = base64_chunk
                    print(f"[murf ai][chunk {chunk_count}] {truncated_chunk}")
                    audio_chunks.append(base64_chunk)
                    chunk_count += 1
                if data.get("final"):
                    logger.info("Murf confirms final audio chunk received.")
                    break
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            logger.error(f"Error in receive loop: {str(e)}")
        return audio_chunks

    async def stream_llm(self, text: str) -> tuple[str, list]:
        """Stream response from Gemini LLM, send sentences to Murf via WebSocket, and accumulate response."""
        if not self.api_key:
            raise ValueError("Gemini API key is missing.")
        if not text or not text.strip():
            logger.warning("Empty text received, skipping Gemini and Murf.")
            return "", []
        try:
            uri = (
                f"wss://api.murf.ai/v1/speech/stream-input"
                f"?api-key={self.murf_api_key}"
                f"&sample_rate=44100"
                f"&channel_type=MONO"
                f"&format=WAV"
            )
            async with websockets.connect(uri) as ws:
                voice_config = {
                    "context_id": self.context_id,
                    "voice_config": {
                        "voiceId": "en-US-darnell",
                        "style": "Conversational"
                    }
                }
                await ws.send(json.dumps(voice_config))
                receiver_task = asyncio.create_task(self.receive_loop(ws))
                model = genai.GenerativeModel("gemini-1.5-flash")
                stream = model.generate_content(text, stream=True)
                sentence_buffer = ""
                accumulated_response = ""
                print("\nGEMINI STREAMING RESPONSE \n")
                for chunk in stream:
                    if chunk.text:
                        accumulated_response += chunk.text
                        sentence_buffer += chunk.text
                        print(chunk.text, end="", flush=True)

                        sentences = re.split(r'(?<=[.?!])\s+', sentence_buffer)

                        if len(sentences) > 1:
                            for sentence in sentences[:-1]:
                                if sentence.strip():
                                    text_msg = {
                                        "context_id": self.context_id,
                                        "text": sentence.strip(),
                                        "end": False
                                    }
                                    await ws.send(json.dumps(text_msg))
                            sentence_buffer = sentences[-1]

                if sentence_buffer.strip():
                    text_msg = {
                        "context_id": self.context_id,
                        "text": sentence_buffer.strip(),
                        "end": True
                    }
                    await ws.send(json.dumps(text_msg))

                print("\nEND OF GEMINI STREAM \n")

                audio_chunks = await receiver_task

                if not accumulated_response:
                    raise ValueError("No response from Gemini LLM stream.")

                return accumulated_response, audio_chunks
        except genai.types.generation_types.BlockedPromptException as e:
            logger.error(f"Gemini blocked prompt: {str(e)}")
            raise
        except genai.types.generation_types.StopCandidateException as e:
            logger.error(f"Gemini stopped generation: {str(e)}")
            raise
        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f"Murf WebSocket closed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise