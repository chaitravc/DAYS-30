

## Agent Revamp – UI & Configurable API Keys

This task focuses on revamping the AI Voice Agent’s **UI/UX** and making the system more **flexible** by allowing users to provide their own **API keys**. Instead of relying only on `.env` files, users can now enter API keys directly in the app UI, making the setup more customizable and user-friendly.

---

## Task Overview

* Revamped the UI for a cleaner and more intuitive experience.
* Added a **config section** where users can enter their own API keys for STT, TTS, and LLM services.
* Ensured the system prioritizes **user-provided API keys** over `.env` defaults.
* Performed **code cleanup** to improve readability, maintainability, and scalability.
* Enhanced UI/UX flow for better interaction and smoother navigation.

---

## How It Works

### Client Side

* Updated UI with a **config panel** to enter API keys.
* Stores user API keys for the active session and uses them in requests.
* Provides a cleaner layout and smoother navigation for better usability.

### Server Side

* Accepts API keys sent from the client and applies them dynamically.
* Falls back to `.env` keys only if user-provided keys are missing.
* Cleaned and optimized backend code for better performance and maintainability.

---

## Tech Stack

* **Frontend** – HTML, CSS, JavaScript (UI updates + config panel)
* **Backend** – Python (FastAPI)
* **APIs** – AssemblyAI (Speech-to-Text), Gemini (LLM), Murf AI (Text-to-Speech)
* **Communication** – WebSockets
* **Runtime** – Uvicorn

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/chaitravc/day27.git  
cd day27  
```

### Install Dependencies

```bash
pip install -r requirements.txt  
```

### Run Server

```bash
uvicorn main:app --reload  
```

### Test the Agent

1. Open the frontend in your browser.
2. Enter your **API keys** in the config section.
3. Speak into the microphone.
4. Your voice will be transcribed to text.
5. The agent will generate a response using the configured APIs.
6. The response will be spoken back with TTS.

---

## Dependencies

* fastapi
* uvicorn
* websockets
* requests
* murf
* assemblyai

---

## Output

A **revamped AI Voice Agent** with a **cleaner UI**, **configurable API keys**, and **optimized backend code**—making it more **flexible, customizable, and ready for future enhancements**.








Uploading WhatsApp Video 2025-08-28 at 3.42.45 PM.mp4…

