

### Day 21 – Streaming Audio Data to Client

This task focuses on streaming audio data from the server to the client in real-time. The audio is sent as **base64-encoded chunks** over WebSockets, accumulated into an array on the client, and acknowledgements of received data are printed in the console.

---

#### Task Overview

* Stream base64 audio data from the server to the client
* Accumulate audio chunks in an array for further handling
* Print acknowledgement messages in the client console
* No need to play the audio directly in the `<audio>` element

---

#### How It Works

1. Server generates audio output (base64-encoded).
2. Audio data is streamed chunk by chunk over WebSockets.
3. Client receives each audio chunk and appends it to an array.
4. Client console prints acknowledgement for each received audio chunk.

---

#### Tech Stack

* **Backend** – Python (FastAPI)
* **Streaming** – WebSockets
* **Speech-to-Text** – AssemblyAI API
* **LLM** – Google Gemini API
* **Text-to-Speech** – Murf AI
* **Runtime** – Uvicorn

---

#### Setup Instructions

1. **Clone Repository**

```bash
git clone https://github.com/chaitravc/day21.git
cd day21
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Add Environment Variables**
   Create a `.env` file in the root directory:

```env
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
GOOGLE_API_KEY=your_gemini_api_key
MURF_API_KEY=your_murf_api_key
```

4. **Run Server**

```bash
uvicorn main:app --reload
```

---

#### Example Output

When you run the service, the terminal prints acknowledgements of received audio data:

```
Received audio chunk [base64 data]
Acknowledgement: Audio data received successfully
```

---

#### Dependencies

* fastapi
* uvicorn
* requests
* websockets
* google-generativeai
* python-dotenv

---

#### Notes

This task demonstrates **real-time audio streaming integration** using WebSockets. The audio is received and acknowledged on the client, while the frontend remains unchanged.

## Output
<img width="1920" height="1080" alt="Screenshot 2025-08-22 150448" src="https://github.com/user-attachments/assets/bf23ee7c-0b50-4290-91cd-d8567210eb41" />

<img width="1920" height="1020" alt="Screenshot 2025-08-22 150504" src="https://github.com/user-attachments/assets/32688d67-91d9-4657-8988-98b707f138c8" />
<img width="1920" height="1020" alt="Screenshot 2025-08-22 150527" src="https://github.com/user-attachments/assets/df7f6ccb-2bb1-4ad2-8e3c-6141b7090ded" />
