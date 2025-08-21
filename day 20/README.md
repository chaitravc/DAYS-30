


# Day 20 – Murf WebSockets

This task focuses on sending the **LLM’s streaming response** to **Murf** using WebSockets. Murf processes the incoming text and returns the audio in **base64 encoded format**, which is then printed to the console.

---

## Task Overview

* Connect to **Murf API** via WebSockets
* Send **streaming response** from the LLM to Murf
* Receive **audio output** in base64 encoding
* Print base64 audio data in the console
* No changes required to the frontend UI

---

## How It Works

1. User speaks → Audio is transcribed with **AssemblyAI**
2. The **final transcript** is processed by **Google Gemini**
3. Gemini generates a **streaming response**
4. Response text is sent to **Murf API** over WebSockets
5. Murf returns **base64 audio chunks**
6. Audio base64 is printed in the console

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/chaitravc/day 20.git
cd day20
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file in the root directory:

```env
MURF_API_KEY=your_murf_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

### 4. Run Server

```bash
uvicorn main:app --reload
```

---

## Example Output

When you run the service, the console displays **base64-encoded audio** returned from Murf:

```
Streaming base64 audio response:
UklGRiQAAABXQVZFZm10IBAAAAABAAEA...
```

---

## Dependencies

* `fastapi`
* `uvicorn`
* `requests`
* `google-generativeai`
* `websockets`
* `python-dotenv`

---

## Notes

* This task demonstrates **real-time audio generation using WebSockets**.
* Base64 audio can be decoded and played back in the frontend later.

---


