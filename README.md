

# 30 Days of AI Voice Challenge – Murf AI

An interactive journey of building **AI-powered Voice Agents** in 30 days, integrating cutting-edge APIs for **speech-to-text, natural language processing, and text-to-speech**.

This project highlights daily progress, showcasing how AI voice technology can be combined with real-time APIs to create powerful conversational systems.

---

##  What This Project Covers

* **Murf API** – Natural voice Text-to-Speech conversion
* **AssemblyAI API** – Speech-to-Text transcription
* **Google Gemini API** – Natural Language Understanding & Response Generation
* **FastAPI Backend** – Real-time API endpoints
* **Interactive Frontend** – Record, transcribe, and play AI-generated responses

---

##  Features

*  **Speech Recognition** – Convert spoken input to text (AssemblyAI)
*  **Intelligent Response** – AI-driven replies with Google Gemini
*  **Natural Voice Output** – Generate lifelike speech with Murf AI
*  **Real-Time Processing** – Powered by FastAPI and WebSockets
*  **Browser Interface** – Simple HTML/CSS/JS frontend

---

##  Tech Stack

* **Frontend** – HTML, CSS, JavaScript
* **Backend** – Python (FastAPI)
* **APIs** –

  * [Murf AI](https://murf.ai) – Text-to-Speech
  * [AssemblyAI](https://www.assemblyai.com) – Speech-to-Text
  * [Google Gemini](https://ai.google) – AI for NLP
* **Others** – WebSockets, Fetch API, dotenv for config

---

##  Project Structure

```
voice-agent/
│── .venv/                       # Virtual environment 
│── audio_outputs/               # Stores generated AI voice audio files
│── static/                      # Frontend static files
│   ├── index.html               # Main user interface
│   ├── index.js                 # Handles frontend logic & API calls
│   ├── style.css                # UI styling
│   └── screenshots/             # Daily progress screenshots
│── uploads/                     # Stores uploaded audio files
│── .env                         # Environment variables (API keys)
│── main.py                      # FastAPI backend
│── README.md                    # Documentation
│── requirements.txt             # Python dependencies
```

---

##  Setup & Installation

###  Clone Repository

```bash
git clone https://github.com/chaitravc/DAYS-30.git
cd DAYS-30
```

###  Install Dependencies

```bash
pip install -r requirements.txt
```

### Add Environment Variables

Create a `.env` file in the **root** directory:

```env
MURF_API_KEY=your_murf_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
```

###  Run Backend

```bash
uvicorn main:app --reload
```

Visit → [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Open Frontend

In browser →

```
http://127.0.0.1:8000/static/index.html
```

---

##  Workflow

1. User clicks **Record** and speaks
2. Audio → **AssemblyAI** (Speech-to-Text)
3. Text → **Google Gemini** (AI Response)
4. Reply → **Murf AI** (Voice Output)
5. Response is played back in the browser

---

## 📡 API Endpoint

| Method | Endpoint          | Description                         |
| ------ | ----------------- | ----------------------------------- |
| POST   | `/api/agent/chat` | Send audio & receive AI voice reply |

---

## 📦 Dependencies

* `fastapi`
* `uvicorn`
* `requests`
* `python-dotenv`
* `pydantic`

Install manually:

```bash
pip install fastapi uvicorn requests python-dotenv pydantic
```

---

##  30 Days Challenge

This repo documents my **daily progress** of building an AI Voice Agent:


✔ Day 20 – WebSocket-based streaming


---

##  Goal

To build and showcase an **end-to-end AI-powered Voice Agent** that can:

* Listen to speech
* Understand context
* Respond intelligently
* Speak back naturally

---



---

👉 Perfect for your **GitHub repo** documenting your 30 Days AI Voice Challenge.

Do you also want me to make a **shorter LinkedIn-style README summary** (like a project highlight) that you can share as a post?
