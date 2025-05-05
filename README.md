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

## 📊 План развития

1. MVP: агент, включающий лампу по голосовой команде.
2. Визуализация: обработка изображения с камеры (сидит/ушёл/спит).
3. Интеграция с Jira.
4. Образовательный режим: диалоги, напоминания, обучение.
5. Ассистент распорядка дня.

---

## 🧩 Сервис баз данных (`db-service`)

Сервис `db-service` предоставляет абстракцию для хранения данных как в краткосрочной (Redis), так и в долгосрочной (MongoDB) памяти. Он используется всеми агентами и шлюзами для унифицированного доступа к данным.

### 📦 Основные функции

| Категория       | Назначение                                  | База           |
|----------------|----------------------------------------------|----------------|
| Краткосрочная   | Кэш контекста, промежуточные сообщения       | Redis          |
| Долгосрочная    | История, медиафайлы, ID-данные               | MongoDB        |

### 🧹 Архитектура

```
db-service/
├── app.py                      # Точка входа
├── Dockerfile
├── clients/
│   ├── redis_client.py         # Класс работы с Redis
│   └── mongo_client.py         # Класс работы с MongoDB
├── interfaces/
│   └── context_storage.py      # Общий интерфейс доступа к хранилищу
└── models/
    └── context.py              # Pydantic-модели данных (например, FileInfo, SessionState)
```

### 🔌 API (в разработке)

| Метод       | Путь                        | Описание                                      |
|-------------|-----------------------------|-----------------------------------------------|
| `POST`      | `/context/save`             | Сохранить произвольный JSON в MongoDB         |
| `POST`      | `/context/cache`            | Сохранить данные во временное хранилище Redis |
| `GET`       | `/context/load/{session}`   | Получить все данные по `session_id`           |

### 📚 Примеры моделей

```python
# models/context.py

class FileInfo(BaseModel):
    file_id: str
    filename: str
    device_id: str
    user_id: str
    uploaded_at: datetime
    file_type: str  # image, audio, video, etc.
```

---

## 📂 Структура проекта

```
ai-agents-home/
├── .env
├── README.md
├── docker-compose.yaml
├── config/
│   ├── langchain_config.yaml
│   ├── devices.yaml
│   └── mqtt/
├── data/
│   ├── mqtt/
│   ├── redis/
│   └── mongo/
├── log/
│   └── mqtt/
├── ai-agent-core/
│   ├── agents/
│   ├── services/
│   ├── skills/
│   ├── utils/
│   └── main.py
├── models/
│   ├── whisper/
│   ├── tts/
│   └── vision/
├── services/
│   ├── audio-stream-gateway/
│   ├── stt-service/
│   ├── vision-agent/
│   ├── tts-service/
│   ├── speaker-service/
│   ├── face-display/
│   ├── actuator-control/
│   └── db-service/
```

---

## 📚 Примечания

- Все HA-интеграции уже работают
- Используется OpenAI API для естественного языка
- В архитектуре предусмотрена маршрутизация по `device_id`
- Все сервисы могут быть масштабированы (до 10 устройств)
- Обратная связь от ESP32 происходит через MQTT
