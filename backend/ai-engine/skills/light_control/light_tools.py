import os
import yaml
import logging
import httpx

# путь до config/house.yaml внутри контейнера
CONFIG_PATH = os.path.join(os.getcwd(), "config", "house.yaml")
with open(CONFIG_PATH, encoding="utf-8") as f:
    house = yaml.safe_load(f)

# Конфигурация Home Assistant
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

# Логгер для HTTP-запросов к HA
logger = logging.getLogger("ai-engine.light_tools")
logger.setLevel(logging.INFO)


def find_device(text: str):
    low = text.lower()
    for room in house.get("rooms", []):
        room_id = room.get("id") or room.get("name")
        for dev_list in room.get("devices", {}).values():
            for dev in dev_list:
                for alias in dev.get("aliases", []):
                    if alias in low:
                        return room_id, dev["entity_id"]
    raise ValueError(f"Не нашёл устройство в тексте «{text}»")


def parse_brightness(text: str):
    import re
    m = re.search(r"(\d{1,3})\s*%", text)
    if not m:
        raise ValueError("Не смогли распознать процент яркости")
    pct = int(m.group(1))
    if not (0 <= pct <= 100):
        raise ValueError("Процент вне диапазона 0–100")
    return pct


async def turn_on_light(text: str) -> str:
    _, entity_id = find_device(text)
    domain = entity_id.split(".", 1)[0]
    service = "turn_on"
    url = f"{HA_URL}/api/services/{domain}/{service}"
    payload = {"entity_id": entity_id}
    logger.info(f"[HA] POST {url} → payload={payload}")
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=HEADERS, json=payload, timeout=10.0)
    resp.raise_for_status()
    return f"{domain.capitalize()} «{entity_id}» включен."


async def turn_off_light(text: str) -> str:
    _, entity_id = find_device(text)
    domain = entity_id.split(".", 1)[0]
    service = "turn_off"
    url = f"{HA_URL}/api/services/{domain}/{service}"
    payload = {"entity_id": entity_id}
    logger.info(f"[HA] POST {url} → payload={payload}")
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=HEADERS, json=payload, timeout=10.0)
    resp.raise_for_status()
    return f"{domain.capitalize()} «{entity_id}» выключен."


async def set_brightness(text: str) -> str:
    _, entity_id = find_device(text)
    domain = entity_id.split(".", 1)[0]
    if domain != "light":
        raise ValueError(f"Нельзя установить яркость для устройства {entity_id} (домен {domain})")
    pct = parse_brightness(text)
    service = "turn_on"
    url = f"{HA_URL}/api/services/light/{service}"
    payload = {"entity_id": entity_id, "brightness_pct": pct}
    logger.info(f"[HA] POST {url} → payload={payload}")
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=HEADERS, json=payload, timeout=10.0)
    resp.raise_for_status()
    return f"Яркость лампы «{entity_id}» установлена на {pct}%."
