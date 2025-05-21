# skills/light_control/ha_client.py

import os
import httpx

HA_URL   = os.getenv("HA_URL")    # http://192.168.31.81:8123
HA_TOKEN = os.getenv("HA_TOKEN")

class AsyncHAClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=HA_URL,
            headers={"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"},
            timeout=10.0,
        )

    async def call_service(self, domain: str, service: str, payload: dict):
        url = f"/api/services/{domain}/{service}"
        resp = await self._client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    async def turn_on(self, entity_id: str):
        return await self.call_service("switch", "turn_on", {"entity_id": entity_id})

    async def turn_off(self, entity_id: str):
        return await self.call_service("switch", "turn_off", {"entity_id": entity_id})

    async def close(self):
        await self._client.aclose()
