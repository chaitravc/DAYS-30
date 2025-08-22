

### Day 16 – Streaming Audio

This task focuses on **recording and streaming audio** from the client to the server using WebSockets, and saving the received audio data to a file. No transcription, LLM processing, or TTS is required for this task.

---

#### Task Overview

* Record audio on the client side
* Stream audio data to the server over WebSockets at regular intervals
* Receive binary audio data on the server
* Save the received audio data into a file
* Breakage of the existing UI is expected and acceptable for this task

---

#### How It Works

1. Client records audio from the microphone
2. Instead of accumulating chunks locally, the client streams audio chunks to the server using WebSockets
3. Server receives the audio data as binary messages
4. Server writes the audio data to a file for storage

---

#### Tech Stack

* **Frontend** – HTML/JavaScript (for audio recording & WebSocket client)
* **Backend** – Python (FastAPI)
* **Communication** – WebSockets
* **Runtime** – Uvicorn

---

#### Setup Instructions

1. **Clone Repository**

```bash
git clone https://github.com/chaitravc/day16.git
cd day16
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run Server**

```bash
uvicorn main:app --reload
```

4. **Test Recording**

* Open the frontend in your browser
* Speak into the microphone
* Audio data is streamed to the backend and saved as a file

---



#### Dependencies

* fastapi
* uvicorn
* websockets

---

#### Notes

This task demonstrates the **foundation of real-time audio streaming**. By saving streamed audio to a file, we validate that the client-server pipeline works correctly before introducing transcription (AssemblyAI), LLM responses, or text-to-speech (Murf AI) in later tasks.

---

## Output

<img width="1920" height="1020" alt="Screenshot 2025-08-17 113227" src="https://github.com/user-attachments/assets/c474c1f4-0e5e-4a24-84ac-ed517ab52546" />


