
### Day 18 – Turn Detection

This task focuses on using **AssemblyAI’s streaming API** to detect when a user has finished speaking (turn detection). Once a turn ends, the transcription is finalized and sent to the client over WebSockets. The client displays the transcription in the UI at the end of the turn.

---

#### Task Overview

* Enable turn detection with AssemblyAI’s streaming API
* Detect when the user stops speaking
* Send a WebSocket message to the client to indicate the end of the turn
* Display the transcription in the UI at the end of each turn

---

#### How It Works

1. User speaks into the microphone
2. Audio is streamed to AssemblyAI for real-time transcription
3. AssemblyAI signals when the user has stopped speaking (end of turn)
4. Backend sends a WebSocket message to the client notifying end of turn
5. Client displays the transcription on the UI

---

#### Tech Stack

* **Backend** – Python (FastAPI)
* **Streaming & Turn Detection** – AssemblyAI API
* **Communication** – WebSockets
* **Frontend** – HTML/JavaScript UI
* **Runtime** – Uvicorn

---

#### Setup Instructions

1. **Clone Repository**

```bash
git clone https://github.com/chaitravc/day18.git
cd day18
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
* requests
* websockets
* python-dotenv

---

#### Notes

This task demonstrates **real-time turn detection** with AssemblyAI. It enables smoother conversational flows by signaling when the user has finished speaking and displaying the final transcript in the UI.


