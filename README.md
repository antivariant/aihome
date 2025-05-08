
# Проект: Инфраструктура AI-агентов для умного дома на базе Home Assistant

## 🎯 Цель

Создание расширяемой архитектуры системы AI-агентов, использующих ChatGPT (через OpenAI API) и другие компоненты для управления домом, личными задачами, обучением и взаимодействием с Jira и другими платформами. Основной управляющий интеллект — не Home Assistant, а надстройка над ним в виде Docker-контейнера с LangChain-агентами.

---

## 🧱 Инфраструктура

### 💻 Аппаратное обеспечение

| Устройство                         | Назначение                  | Подключение   | ID в HA (если есть)                  |
|-----------------------------------|-----------------------------|---------------|--------------------------------------|
| Raspberry Pi 4 Model B (8Gb)      | Центральный управляющий узел| LAN (Ethernet)| -                                    |
| USB Web-камера A4Tech PK-720MJ    | Микрофон и камера           | USB           | -                                    |
| Внешние динамики                  | Аудиовыход                  | 3.5mm Jack    | -                                    |
| Настольная лампа (ESP32)          | Управляемое освещение       | WiFi          | `switch.sonoff_10002ed516`           |
| Google Home Hub                   | Мультимедиа + UI            | WiFi          | `media_player.my_room_hub`          |
| Yeelight Ceiling                  | Основной свет + сценарии    | WiFi          | `light.yeelight_ceiling_nightlight` |
| Телевизор                         | AirPlay/медиа               | LAN           | `media_player.airplay_myroomtv`     |
| Датчик влажности                  | Сенсор                      | ZigBee/WiFi   | `sensor.humidity_158d00022c656c`    |
| Датчик давления                   | Сенсор                      | ZigBee/WiFi   | `sensor.pressure_158d00022c656c`    |
| Датчик температуры                | Сенсор                      | ZigBee/WiFi   | `sensor.temperature_158d00022c656c` |
| Выключатели коридора              | Освещение                   | ZigBee/WiFi   | `switch.light_hallway`, `switch.light_coridor` |

---

## ⚙️ Программное обеспечение

### Основное ПО на Raspberry Pi

- Raspberry Pi OS Lite (64-bit)
- Docker
- Home Assistant OS (Core 2025.4.4 / Supervisor 2025.04.1)

### Облачные и внешние сервисы

- ChatGPT Plus (OpenAI API)
- Jira (интеграция планируется)
- Netflix (для мультимедийных сценариев)

---

## 🌐 Сеть и доступ

| Название                   | Адрес                                 |
|----------------------------|----------------------------------------|
| Локальный интерфейс HA     | `https://homeassistant.local:8123/`   |
| Внешний доступ             | `https://ha.aihome.buzz/`             |
| SSH-доступ к Pi            | `ssh user@192.168.31.81` (постоянный IP, закреплён по MAC-адресу) |

---

## 📡 Коммуникация компонентов

| Источник → Назначение       | Цель                                | Механизм             |
|-----------------------------|--------------------------------------|----------------------|
| `Mic` → `Whisper`           | Преобразование речи в текст          | PulseAudio + STT     |
| `openWakeWord` → `Assist`   | Активация по ключевому слову        | локально             |
| `Assist` → `ChatGPT Agent`  | Обработка команд                     | OpenAI API           |
| `Agent` → `HA API`          | Управление устройствами              | REST API / WebSocket |
| `Camera` → `Vision Agent`   | Распознавание объектов/контекста     | RTSP / HTTP          |
| `Agent` → `TTS`             | Озвучка ответа                       | HTTP / gRPC          |
| `TTS` → `Speaker Service`   | Воспроизведение речи                 | MQTT / REST          |
| `Agent` → `Face Display`    | Отображение состояния/эмоций         | MQTT / REST          |
| `Agent` → `Actuator Control`| Управление сервомоторами и LED-индикаторами | MQTT / REST  |  

---


---

## 🔌 Порты микросервисов

| Сервис               | Название в Compose      | Порт  |
|----------------------|-------------------------|-------|
| STT (Speech-to-Text) | `stt-service`           | `5060` |
| TTS (Text-to-Speech) | `tts-service`           | `5061` |
| Vision Engine        | `vision-agent`          | `5062` |
| DB API               | `db-service`            | `5063` |
| Audio Input Gateway  | `audio-stream-gateway`  | `5070` |
| Audio Output Gateway | `speaker-service`       | `5071` |
| Chat Gateway         | `chat-gateway`          | `5072` |
| Actuator Control     | `actuator-control`      | `5073` |
| Face Display         | `face-display`          | `5074` |
| AI Engine            | `ai-agent-core`         | `5080` |
| Redis                | `redis`                 | `6379` |
| MongoDB              | `mongo`                 | `27017` |
| MQTT Broker          | `mqtt-1`                | `1883` |


## 📊 План развития
... (содержимое этого раздела неважно, т.к. перед ним будет вставка)
