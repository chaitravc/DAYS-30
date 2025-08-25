 ## Complete Voice Agent

This task focuses on connecting all the components built in the previous days to create a fully working conversational AI voice agent.  
The agent can handle user queries, transcribe speech to text, process the text with an LLM, generate a meaningful response, save chat history, convert text back to speech using Murf AI, and stream audio to the client.

---

## Task Overview
- Record audio on the client side  
- Stream audio to the server over WebSockets  
- Transcribe audio using AssemblyAI (STT)  
- Process transcription with an LLM API  
- Save conversation history for context  
- Convert generated response into speech using Murf AI (TTS)  
- Stream the synthesized audio response back to the client  
- Code is slightly different from the UI but works fine according to the task
---

## How It Works
1. **Client Side**
   - Records audio via the microphone  
   - Streams audio chunks to the server using WebSockets  
   - Plays back the audio response streamed from the server in real-time  

2. **Server Side**
   - Receives and buffers audio chunks from the client  
   - Sends audio to **AssemblyAI** for transcription  
   - Processes transcribed text with an **LLM API** to generate a response  
   - Stores conversation history in memory or a database  
   - Converts response text to speech using **Murf AI**  
   - Streams the audio response back to the client over WebSockets  

---

## Tech Stack
- **Frontend** – HTML, CSS, JavaScript (recording, streaming, audio playback)  
- **Backend** – Python (FastAPI)  
- **APIs** – AssemblyAI (Speech-to-Text), Gemini (LLM), Murf AI (Text-to-Speech)  
- **Communication** – WebSockets  
- **Runtime** – Uvicorn  

---

## Setup Instructions

### Clone Repository
```bash
git clone https://github.com/chaitravc/day23.git
cd day23
````

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server

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

## Dependencies

* fastapi
* uvicorn
* websockets
* requests
* murf
* assemblyai

---

## Notes

* This marks the **completion of the core voice agent pipeline**.
* All pieces — audio streaming, STT, LLM, TTS, and real-time playback — are now connected.

---

## Output

A **working end-to-end conversational voice agent** where you can talk to the system, get AI-generated responses, and hear them spoken back to you in real time.

```




https://github.com/user-attachments/assets/3b75fcb5-15f3-4c9f-a9ec-df8008f457dc

