# 📘 Общий формат архитектуры HUB / SERVICE / DRIVER

## 1. 📥📤 Определение входа и выхода
Все компоненты системы рассматриваются как **сигнальные узлы**, имеющие:
- **вход** — сигнал, получаемый извне (например, аудио с микрофона, текст от пользователя, HTTP-запрос);
- **выход** — результат, который компонент генерирует и передаёт другим (например, WAV-файл, JSON-ответ, управляющая команда).

🔁 Если компонент обрабатывает данные в обе стороны, он разбивается логически на две подсистемы:

### Примеры:
- `drv-mic-usb`:
  - вход: аналоговый звук с микрофона
  - выход: WAV-файл (в папке `./data/drv-mic-usb/audio`)

- `svc-tts-piper`:
  - вход: JSON с текстом
  - выход: путь к WAV-файлу (в `./data/svc-tts/shared-wav`)

- `gw-dev`:
  - вход: сигналы от устройств (аудио, видео, текст)
  - выход: команды или медиа от AI (TTS, изображения, действия)

- `gw-hub`:
  - вход: от всех шлюзов (данные устройств)
  - выход: маршрутизирует результат AI в нужный шлюз

---

## 2. 🌐 Протоколы обмена и типы данных

### 📦 Общие правила:
- Медиа (аудио/видео/изображения): **передаются как путь к файлу** в volume
- Данные: передаются в JSON с обязательными метаданными (`device_id`, `input_type`, и т.д.)

### 🔊 Аудио:
- Формат: WAV 16kHz mono
- Хранение: `./data/<сервис>/shared-wav/<uuid>.wav`
- Источники: микрофоны (drv), AI (TTS), внешние источники (stream)

### 📹 Видео и изображения:
- Кадры/видео передаются как `file_path`
- Формат: JPG / PNG (изображения), MP4 (видео)
- Используются:
  - `wav2lip` (анимированное лицо)
  - `sadtalker`, `screen-snapshots`, `camera` (вход)

---

## 3. 🔗 Интерфейсы передачи данных (контракты)

### Общий формат (от любого шлюза в AI или обратно):
```json
{
  "device_id": "frai-001",
  "device_type": "frai",        // frai, dev, chat
  "user_id": "user-xyz",         // если определён
  "input_type": "voice",         // "voice", "text", "image", "video"
  "input_data": "path/to/file.wav" // или текст, base64, URL
}
```

### A. ai-engine -> gw-hub
```json
{
  "device_id": "frai-001",
  "response_type": "voice", // или "text", "image", "video", "action"
  "response_data": "path/to/tts.wav"
}
```

### B. gw-hub -> ai-engine
```json
{
  "device_id": "dev-003",
  "device_type": "dev",
  "user_id": null,
  "input_type": "voice",
  "input_data": "path/to/dev-003-1682030912.wav"
}
```

### C. gw-hub -> gw-frai
```json
{
  "device_id": "frai-001",
  "response_type": "video", // или "voice", "text"
  "response_data": "path/to/wav2lip.mp4"
}
```

### D. gw-hub -> gw-chat
```json
{
  "device_id": "chat-007",
  "response_type": "text",
  "response_data": "Конечно, сейчас включу свет в кухне."
}
```

### E. gw-hub -> gw-dev
```json
{
  "device_id": "dev-003",
  "response_type": "voice",
  "response_data": "path/to/dev-003-reply.wav"
}
```

### F. gw-frai / gw-chat / gw-dev -> gw-hub
```json
{
  "device_id": "frai-001",
  "input_type": "voice",
  "input_data": "path/to/frai-001-input.wav"
}
```

---

## 4. 🔊 Архитектура потоков микрофона

### 🔸 Драйвер (`drv-*`):
- определяет `device_id` (уникальный ID устройства)
- определяет `isFrai` (true/false, принадлежность устройству frai)
- ⚠️ `device_id` — это не ID отдельного микрофона, камеры или динамика, а ID **интегрального устройства взаимодействия с пользователем** (например: одна колонка `frai` или `dev`), включающего сразу все 3 составляющих (ввод, вывод, изображение)
- сигнал, пришедший от `device_id=1` должен выводиться **на то же устройство с `device_id=1`** (динамик/экран)

```json
{
  "device_id": "frai-001",
  "isFrai": true,
  "audio_path": "path/to/stream.wav"
}
```

### 🔸 Сервис (`svc-audio-in`):
- фильтрует, нормализует
- ищет hotword ("эй, дом", "эй, фрэй" и т.п.)
- если найдено — начинает запись до молчания (5с) или тайм-аут (2 мин)
- передаёт `wav` в STT
- возвращает:
```json
{
  "device_id": "frai-001",
  "isFrai": true,
  "input_type": "voice",
  "input_data": "path/to/recorded.wav"
}
```

### 🔸 Gateway (`gw-frai` / `gw-dev`):
- принимает аудио
- вызывает определение `user_id`:
  - `gw-frai`: голос + лицо
  - `gw-dev`: голос / другие способы
- формирует полный запрос и отправляет на `gw-hub`

---

## 🧹 TODO / Расширение
- Уточнить формат `action` (для актуаторов)
- Добавить контракты `image` и `video` в оба направления
- Стандартизировать `user_id` и его определение по biometrics (позже)
- Разделить `hotword dict` и `silence/VAD thresholds` по YAML конфигу
- Создать контракт AI-инструкций для подсказок (интонации, фразы)

---

Готово для фиксации как архитектурный стандарт системы AI Agent.