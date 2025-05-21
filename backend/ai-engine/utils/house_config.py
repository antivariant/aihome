# utils/house_config.py

import inspect
# Патч для совместимости pymorphy2 с Python 3.11+
_fullargspec = inspect.getfullargspec
inspect.getargspec = lambda func: _fullargspec(func)[:4]

from pathlib import Path
import yaml
from pymorphy2 import MorphAnalyzer

# Загрузка конфига дома
_CFG_PATH = Path(__file__).parent.parent / "config" / "house.yaml"
_DATA = yaml.safe_load(_CFG_PATH.read_text(encoding="utf-8"))

_morph = MorphAnalyzer()

def _lemmatize(text: str) -> set[str]:
    """Простая лемматизация текста через pymorphy2."""
    tokens = text.lower().split()
    return { _morph.parse(tok)[0].normal_form for tok in tokens }

def parse_room_device(text: str) -> dict:
    """
    Выделяет из текста room_id и device_id (entity_id) лампы.
    Возвращает словарь {'room_id': ..., 'device_id': ...} или None-поля при неудаче.
    """
    lemmas = _lemmatize(text)
    room_id = None
    device_id = None

    # 1) Поиск комнаты
    for room in _DATA["rooms"]:
        aliases = [room["id"], room.get("name", "")] + room.get("aliases", [])
        for alias in aliases:
            if set(_lemmatize(alias)).issubset(lemmas):
                room_id = room["id"]
                break
        if room_id:
            break

    # 2) Поиск устройства (лампы)
    rooms_to_search = (
        [r for r in _DATA["rooms"] if r["id"] == room_id]
        if room_id
        else _DATA["rooms"]
    )
    for room in rooms_to_search:
        for dev in room.get("devices", {}).get("lights", []):
            aliases = [dev.get("entity_id"), dev.get("name", "")] + dev.get("aliases", [])
            for alias in aliases:
                if set(_lemmatize(alias)).issubset(lemmas):
                    device_id = dev["entity_id"]
                    if not room_id:
                        room_id = room["id"]
                    break
            if device_id:
                break
        if device_id:
            break

    return {"room_id": room_id, "device_id": device_id}

def get_device_info(room_id: str, device_id: str) -> dict:
    """
    Возвращает dict с описанием устройства из house.yaml
    по заданным room_id и entity_id.
    """
    for room in _DATA["rooms"]:
        if room["id"] == room_id:
            for dev in room.get("devices", {}).get("lights", []):
                if dev.get("entity_id") == device_id:
                    return dev
    return {}
