import os
import yaml

# путь до config/house.yaml внутри контейнера
CONFIG_PATH = os.path.join(os.getcwd(), "config", "house.yaml")

with open(CONFIG_PATH, encoding="utf-8") as f:
    house = yaml.safe_load(f)

def find_device(text: str):
    low = text.lower()
    for room in house.get("rooms", []):
        room_id = room.get("id") or room.get("name")
        # devices — это словарь, где ключи: lights, switches и т.п.
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
