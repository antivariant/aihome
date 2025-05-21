# skills/light_control/light_tools.py

import os
import httpx
from skills.light_control.parser import find_device, parse_brightness  # явный импорт без точки

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}


async def turn_on_light(text: str) -> str:
    room_id, entity_id = find_device(text)
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{HA_URL}/api/services/homeassistant/turn_on",
            json={"entity_id": entity_id},
            headers=HEADERS,
        )
        resp.raise_for_status()
    return f"Лампа «{entity_id}» в комнате «{room_id}» включена."


async def turn_off_light(text: str) -> str:
    room_id, entity_id = find_device(text)
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{HA_URL}/api/services/homeassistant/turn_off",
            json={"entity_id": entity_id},
            headers=HEADERS,
        )
        resp.raise_for_status()
    return f"Лампа «{entity_id}» в комнате «{room_id}» выключена."


async def set_brightness(text: str) -> str:
    room_id, entity_id = find_device(text)
    pct = parse_brightness(text)
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{HA_URL}/api/services/light/turn_on",
            json={"entity_id": entity_id, "brightness_pct": pct},
            headers=HEADERS,
        )
        resp.raise_for_status()
    return f"Яркость лампы «{entity_id}» в комнате «{room_id}» установлена на {pct}%."
