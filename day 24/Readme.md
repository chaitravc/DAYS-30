

# Agent Persona

This task focuses on giving the AI Voice Agent a **character and personality**.
A persona makes the agent more engaging, relatable, and fun to interact with. For today, I themed the UI around the **Masha and the Bear** cartoon, where the agent takes on the **Masha persona** — lively, playful, and adventurous.

---

## Task Overview

* Designed and added a **character persona** to the voice agent.
* Chose **Masha from Masha and the Bear** as the agent’s identity.
* Updated the **UI theme** to reflect the cartoon style.
* Customized the agent’s **tone, responses, and style** to match Masha’s fun personality.
* Explored how personas improve **user interaction and engagement**.

---

## How It Works

### Client Side

* Provides a **cartoon-inspired UI theme** (Masha and the Bear).
* Displays agent interactions with **personality-driven responses**.
* Plays back responses in a **Masha-styled voice** for immersive experience.

### Server Side

* Processes transcriptions and generates responses with an LLM.
* Applies **persona filters** to align responses with Masha’s playful character.
* Converts text responses into speech using **Murf AI TTS**.
* Streams the **personalized audio response** back to the client.

---

## Tech Stack

* **Frontend** – HTML, CSS, JavaScript (UI updates + persona styling)
* **Backend** – Python (FastAPI)
* **APIs** – AssemblyAI (Speech-to-Text), Gemini (LLM), Murf AI (Text-to-Speech)
* **Communication** – WebSockets
* **Runtime** – Uvicorn

---

## Setup Instructions

Clone Repository

```bash
git clone https://github.com/chaitravc/day24.git  
cd day24  
```

Install Dependencies

```bash
pip install -r requirements.txt  
```

Run Server

```bash
uvicorn main:app --reload  
```

Test the Agent

1. Open the frontend in your browser.
2. Speak into the microphone.
3. Your voice will be transcribed to text.
4. The agent will generate a  response.
5. The response will be spoken back in a **fun cartoon persona voice**.

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

A conversational AI voice agent with a **Masha persona** — playful, curious, and fun to interact with, wrapped in a **cartoon-inspired UI theme**.

