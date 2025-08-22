

# Day 19 – Streaming LLM Responses

This task focuses on enabling the LLM to **stream its responses** in real-time. Once the **final transcript** is received from AssemblyAI, it is sent to the LLM API, which streams the response. The accumulated response is then printed to the console.

---

## Task Overview

* Capture **final transcript** from AssemblyAI
* Send transcript to **Google Gemini API** for response generation
* Enable **streaming response** from the LLM
* Print accumulated streaming output to console
* No changes required to the frontend UI

---

## How It Works

1. User speaks → Audio is transcribed with **AssemblyAI**
2. The **final transcript** is captured
3. Transcript is passed to the **Google Gemini API**
4. Gemini streams the response text chunk by chunk
5. The response is accumulated and displayed in the console

---

## Tech Stack

* **Backend** – Python (FastAPI)
* **LLM** – Google Gemini API
* **Speech-to-Text** – AssemblyAI API
* **Runtime** – Uvicorn


---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/chaitravc/day 19.git
cd day19
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file in the root directory:

```env
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

### 4. Run Server

```bash
uvicorn main:app --reload
```

---

## Example Output

When you run the service, the terminal prints streaming chunks of the LLM’s response, and finally the accumulated response:

```
Streaming response:
Hello, how can I help you today?
```

---

## Dependencies

* `fastapi`
* `uvicorn`
* `requests`
* `google-generativeai`
* `python-dotenv`

---

## Notes

* This task demonstrates **real-time LLM streaming integration**.
* The frontend remains unchanged from earlier tasks.

---
# Output


https://github.com/user-attachments/assets/ddb98724-109e-46dc-97fa-7050c570e9bb

