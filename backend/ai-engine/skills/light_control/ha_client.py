# skills/light_control/ha_client.py

import os
from httpx import AsyncClient, HTTPError

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

class AsyncHAClient:
    def __init__(self):
        self.client = AsyncClient(base_url=HA_URL, headers={
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json",
        })

    async def call_service(self, domain: str, service: str, payload: dict):
        url = f"/api/services/{domain}/{service}"
        try:
            resp = await self.client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except HTTPError as e:
            # логируем или пробрасываем дальше
            raise RuntimeError(f"HA service error {e.response.status_code}: {e.response.text}") from e
