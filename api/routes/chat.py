from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from agents.orchestrator import run_agent

router = APIRouter()
connections = {}

@router.websocket("/ws/chat/{client_id}")
async def chat_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connections[client_id] = websocket
    history = []

    try:
        while True:
            data = await websocket.receive_json()
            query = data.get("message", "")
            if not query:
                continue

            async def send_chunk(text: str):
                await websocket.send_json({"type": "chunk", "text": text})

            response = await run_agent(query, history, send_chunk)
            await websocket.send_json({"type": "done"})

            history.append({"role": "user", "content": query})
            history.append({"role": "assistant", "content": response})

    except WebSocketDisconnect:
        connections.pop(client_id, None)