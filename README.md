# Проект: Инфраструктура AI-агентов для умного дома на базе Home Assistant

## Цель

Создание расширяемой архитектуры системы AI-агентов, использующих ChatGPT (через OpenAI API) и другие компоненты для управления домом, личными задачами, обучением и взаимодействием с Jira и другими платформами. Основной управляющий интеллект — не Home Assistant, а надстройка над ним в виде Docker-контейнера с LangChain-агентами.

---

## 🧱 Инфраструктура

### 💻 Аппаратное обеспечение

| Устройство | Назначение | Подключение | ID в HA (если есть) |
|-----------|-----------|-------------|----------------------|
| Raspberry Pi 4 Model B (8Gb) | Центральный управляющий узел | LAN (Ethernet) | - |
| USB Web-камера A4Tech PK-720MJ | Микрофон и камера | USB | - |
| Внешние динамики | Аудиовыход | 3.5mm Jack | - |
| Настольная лампа (ESP32) | Управляемое освещение | WiFi | `switch.sonoff_10002ed516` |
| Google Home Hub | Мультимедиа + UI | WiFi | `media_player.my_room_hub` |
| Yeelight Ceiling | Основной свет + сценарии | WiFi | `light.yeelight_ceiling_nightlight` |
| Телевизор | AirPlay/медиа | LAN | `media_player.airplay_myroomtv` |
| Датчик влажности | Сенсор | ZigBee/WiFi | `sensor.humidity_158d00022c656c` |
| Датчик давления | Сенсор | ZigBee/WiFi | `sensor.pressure_158d00022c656c` |
| Датчик температуры | Сенсор | ZigBee/WiFi | `sensor.temperature_158d00022c656c` |
| Выключатели коридора | Освещение для экспериментов | ZigBee/WiFi | `switch.light_hallway`, `switch.light_coridor` |

---

## ⚙️ Программное обеспечение

### Основное ПО на Raspberry Pi

- Raspberry Pi OS Lite(64-bit)
- Docker
- Home Assistant OS (Core 2025.4.4 / Supervisor 2025.04.1)
- MotionEye (в виде плагина Home Assistant)
- HA Add-ons:
  - Assist Microphone
  - openWakeWord (wake word: "Nabu")
  - Whisper (faster-whisper) — STT (Speech-to-Text)
  - Piper — TTS (Text-to-Speech)
  - Speech-to-Phrase

### Облачные и внешние сервисы

- ChatGPT Plus (OpenAI API)
- Jira (в планах)
- Netflix (для сценариев)

---

## 🔌 Сеть и адреса

| Название | Адрес |
|---------|-------|
| Локальный интерфейс HA | `https://raspberrypi.local:8123/` (планируется `https://homeassistant.local:8123/`) |
| Внешний доступ через DuckDNS | `https://antivariant.duckdns.org:8123/` |
| SSH-доступ к Pi | `ssh pi@192.168.31.81` (пароль `masterkey`) |

---

## 📡 Коммуникация компонентов

| Источник → Назначение | Цель | Механизм |
|-----------------------|------|----------|
| `Mic` → `Whisper` | Преобразование речи в текст | PulseAudio + STT |
| `openWakeWord` → `Assist Mic` | Активация по ключевому слову | локально |
| `Assist` → `Dialog System (ChatGPT)` | Обработка текста | OpenAI API |
| `Dialog System` → `HA API` | Включение устройств | REST API / WebSocket |
| `MotionEye` (как плагин HA) → (в будущем Vision Agent) | Обработка видео | RTSP / HTTP |

---

## 📊 План развития

1. **Настройка и тестирование MVP-агента**, включающего лампу по команде.
2. **Agent-визуализация**: обработка изображения с камеры и распознавание контекста (сидит/лежит/ушёл).
3. **Интеграция с Jira**: создание и управление задачами через голос.
4. **Образовательный ассистент**: регулярные напоминания и диалоги на изучаемых языках.
5. **Ежедневные рутины**: ИИ как тренер для соблюдения распорядка дня.

---

## ⚒️ Архитектура и масштабирование

Система поддерживает до 10 устройств с микрофоном, камерой и динамиком (например, ESP32-CAM + I2S-динамик). Все сервисы масштабируемы и используют `device_id` для идентификации источника и получателя.

### 🧩 docker-compose.yml (без Home Assistant)

Внешние сервисы:
- MQTT брокер
- Аудио-шлюз
- STT (распознавание)
- Vision Agent
- LangChain Agent
- TTS (озвучка)
- Speaker Service (воспроизведение)

Все компоненты обрабатывают потоки с `device_id` и возвращают ответы адресно.

### 📂 Структура проекта

```
ai-agents-home/
├── docker-compose.yml
├── .env
├── config/
│   ├── langchain_config.yaml
│   ├── devices.yaml
│   └── mqtt/
├── ai-agent-core/
│   └── ...
├── services/
│   ├── audio-stream-gateway/
│   ├── stt-service/
│   ├── vision-agent/
│   ├── tts-service/
│   └── speaker-service/
├── models/
│   ├── whisper/
│   ├── tts/
│   └── vision/
├── data/
├── log/
└── README.md
```

---

## 📚 Примечания

- Все интеграции устройств уже настроены в HA
- ChatGPT используется как облачная LLM
- Задача: перенаправлять распознанную речь в агент через API, а не просто выполнять HA-интенты
- Цель: Home Assistant — вспомогательный слой, а не основная система принятия решений
- В архитектуре уже предусмотрено масштабирование до 10+ устройств с `device_id`, включая маршрутизацию речи, команд и воспроизведения
