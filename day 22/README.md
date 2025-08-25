## Playing Streaming Audio

This task focuses on playing the audio data streamed from the backend directly in the client UI as it arrives. Unlike the previous step where we only streamed audio data to the client, here we ensure seamless playback by handling audio chunks in real time.

---

## Task Overview
- Receive audio chunks on the client side from the server  
- Play the audio in real time without waiting for the full file  
- Manage buffering to avoid interruptions in playback  
- Ensure smooth and continuous audio streaming  

---

## How It Works
1. **Server Side**
   - Streams audio data in chunks to the client over WebSockets  

2. **Client Side**
   - Receives audio data incrementally  
   - Buffers incoming audio chunks  
   - Plays audio seamlessly in the browser using an `AudioContext` or `MediaSource` API  

---

## Tech Stack
- **Frontend** – HTML, JavaScript (WebSockets + Audio playback)  
- **Backend** – Python (FastAPI)  
- **Communication** – WebSockets  
- **Runtime** – Uvicorn  

---

## Setup Instructions

### Clone Repository
```bash
git clone https://github.com/chaitravc/day22.git
cd day22
````

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server

```bash
uvicorn main:app --reload
```

### Test Streaming Audio

1. Open the frontend in your browser
2. Trigger audio playback
3. Audio data is received from the server in chunks
4. Listen as the audio plays seamlessly in real time

---

## Dependencies

* fastapi
* uvicorn
* websockets

---

## Notes

* This task validates the ability to **play audio as it streams**, rather than waiting for the full audio to download.
* Ensuring smooth playback is critical for building real-time conversational agents.
* Sets the stage for combining transcription (STT), LLM responses, and TTS in later tasks.

---

## Output

A **working streaming audio playback system** where the client plays audio as it is received from the server in chunks.





https://github.com/user-attachments/assets/f2c35a26-f6b8-485e-9a14-81c6d370243d


