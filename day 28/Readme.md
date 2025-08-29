

# Deployed Voice Agent

This task focuses on **deploying the AI Voice Agent** so that it can be publicly accessed. After building the full pipeline in earlier tasks, today’s milestone was about hosting the project on the cloud and making it available for real-world use.

The agent can handle user queries, transcribe speech to text, process the text with an LLM, generate a meaningful response, save chat history, convert text back to speech using Murf AI, and stream audio to the client — all now accessible through a deployed link.

---

## Task Overview

* Hosted the Voice Agent on **Render.com** (free tier)
* Configured environment variables and dependencies for deployment
* Allowed users to **fetch and add their own API keys** for:
  * Google Gemini (LLM)
  * AssemblyAI (STT)
  * Murf AI (TTS)
* Ensured smooth communication between client and server in a live environment
* Made the app publicly accessible for anyone to test

---

## How It Works

### Client Side

* Records audio via microphone
* Streams audio chunks to the server using WebSockets
* Plays back the audio response streamed from the server in real-time

### Server Side

* Receives and buffers audio chunks from the client
* Sends audio to AssemblyAI for transcription
* Processes transcribed text with Gemini (LLM) to generate a response
* Stores conversation history for context
* Converts response text to speech using Murf AI
* Streams the audio response back to the client over WebSockets

---

## Tech Stack

* **Frontend** – HTML, CSS, JavaScript (recording, streaming, audio playback)
* **Backend** – Python (FastAPI)
* **APIs** – AssemblyAI (Speech-to-Text), Gemini (LLM), Murf AI (Text-to-Speech)
* **Communication** – WebSockets
* **Runtime** – Uvicorn

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/chaitravc/day28.git  
cd day28  
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server Locally

```bash
uvicorn main:app --reload
```

### Test the Agent

1. Open the frontend in your browser
2. Speak into the microphone
3. Your voice will be transcribed to text
4. The LLM will generate a response
5. The response will be spoken back to you via Murf AI and streamed in real time

---

## Deployment

The agent is live here 👉 [https://masha-heree.onrender.com](https://masha-heree.onrender.com) 🎉

 **Note**: You need to fetch and enter your own API keys (Google Gemini, Murf AI, AssemblyAI) in the UI to generate outputs.

---

## Dependencies

* fastapi
* uvicorn
* websockets
* requests
* murf
* assemblyai
* murf
* tavily-python

---

## Output

A working **end-to-end conversational voice agent**, fully deployed. You can now talk to the system, get AI-generated responses, and hear them spoken back in real time — directly from the cloud.

