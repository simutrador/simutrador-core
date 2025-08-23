from __future__ import annotations

import asyncio
import json

import websockets
from simutrador_core.models.websocket import HealthStatus, WSMessage


async def main() -> None:
    url = "ws://127.0.0.1:8000/ws/health"
    async with websockets.connect(url) as ws:
        raw = await ws.recv()
        if isinstance(raw, (bytes, bytearray)):
            payload = json.loads(raw.decode("utf-8"))
        else:
            payload = json.loads(raw)
        msg = WSMessage.model_validate(payload)
        hs = HealthStatus.model_validate(msg.data)
        print(
            f"Received message: type={msg.type}, status={hs.status}, version={hs.server_version}"
        )


if __name__ == "__main__":
    asyncio.run(main())
