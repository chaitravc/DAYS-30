

### Day 17 – WebSockets and AssemblyAI

This task focuses on using **AssemblyAI’s Python SDK** to transcribe streaming audio data sent from the client to the server. The transcription can be printed directly in the Python server console or displayed on the UI.

---

#### Task Overview

* Stream audio data from the client to the server over WebSockets
* Use AssemblyAI’s Python SDK to transcribe the audio in real time
* Print the transcription in the server console or display it on the UI
* Ensure the audio is sent in **16kHz, 16-bit, mono PCM** format

---

#### How It Works

1. Client captures audio from the microphone
2. Audio data is sent to the backend server over WebSockets
3. Server passes the audio stream to AssemblyAI’s Python SDK
4. AssemblyAI transcribes the streaming audio in real time
5. Transcription is printed on the server console or shown in the UI

---

#### Tech Stack

* **Backend** – Python (FastAPI)
* **Streaming & Transcription** – AssemblyAI Python SDK
* **Communication** – WebSockets
* **Frontend** – HTML/JavaScript UI
* **Runtime** – Uvicorn

---

#### Setup Instructions

1. **Clone Repository**

```bash
git clone https://github.com/chaitravc/day17.git
cd day17
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Add Environment Variables**
   Create a `.env` file in the root directory:

```env
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
```

4. **Run Server**

```bash
uvicorn main:app --reload
```

---



#### Dependencies

* fastapi
* uvicorn
* websockets
* assemblyai
* python-dotenv

---

#### Notes

This task demonstrates **real-time audio transcription** using AssemblyAI’s Python SDK. By combining WebSockets with AssemblyAI, audio streams from the client can be processed into live transcriptions, forming the backbone of interactive AI voice agents.

<img width="1920" height="1080" alt="Screenshot 2025-08-18 190823" src="https://github.com/user-attachments/assets/f6378238-5003-4144-b2c0-eaad7f421487" />
