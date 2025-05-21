import asyncio
from .parser import find_device, parse_brightness
from .ha_client import AsyncHAClient

async def _turn_on_light(text: str) -> str:
    room_id, device_id = find_device(text)
    client = AsyncHAClient()
    await client.call_service("switch", "turn_on", {"entity_id": device_id})
    return f"Включаю «{device_id}» в комнате «{room_id}»."

def turn_on_light(text: str) -> str:
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_turn_on_light(text))
    finally:
        loop.close()

async def _turn_off_light(text: str) -> str:
    room_id, device_id = find_device(text)
    client = AsyncHAClient()
    await client.call_service("switch", "turn_off", {"entity_id": device_id})
    return f"Выключаю «{device_id}» в комнате «{room_id}»."

def turn_off_light(text: str) -> str:
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_turn_off_light(text))
    finally:
        loop.close()

async def _set_brightness(text: str) -> str:
    room_id, device_id = find_device(text)
    brightness = parse_brightness(text)
    client = AsyncHAClient()
    await client.call_service("light", "turn_on", {
        "entity_id": device_id,
        "brightness_pct": brightness
    })
    return f"Устанавливаю яркость «{device_id}» в комнате «{room_id}» на {brightness}%."

def set_brightness(text: str) -> str:
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_set_brightness(text))
    finally:
        loop.close()
