

## Day 15 – WebSocket Connection

This task focuses on building a WebSocket connection between the client and server. A WebSocket endpoint was created using FastAPI, and Postman was used as the client to test sending and receiving real-time messages.

### Task Overview

* Create a WebSocket endpoint `/ws` on the server
* Establish a WebSocket connection from the client (Postman)
* Send messages from client to server
* Receive echo responses from server in real time
* Explore real-time communication with WebSockets

### How It Works

1. Client connects to the server via the WebSocket endpoint `/ws`
2. Messages are sent from the client (Postman) to the server
3. Server echoes the received messages back to the client
4. Real-time communication is established without refreshing or polling

### Tech Stack

* **Backend** – Python (FastAPI)
* **WebSocket Communication** – FastAPI WebSocket
* **Client** – Postman WebSocket tester
* **Runtime** – Uvicorn

### Setup Instructions

**Clone Repository**

```bash
git clone https://github.com/chaitravc/day15.git
cd day15
```

**Install Dependencies**

```bash
pip install -r requirements.txt
```

**Run Server**

```bash
uvicorn main:app --reload
```

### Dependencies

* fastapi
* uvicorn
* websockets

### Notes

This task demonstrates the basics of WebSocket connections. It shows how to set up a server endpoint, connect a client, and exchange messages in real time.

# Output
<img width="1920" height="1020" alt="Screenshot 2025-08-16 143155" src="https://github.com/user-attachments/assets/c3464920-4d1b-4f3a-868b-d4c1310d87c5" />

<img width="1920" height="1020" alt="Screenshot 2025-08-16 143208" src="https://github.com/user-attachments/assets/27bdc6a2-9975-43cf-8eae-ba012a4d9350" />



