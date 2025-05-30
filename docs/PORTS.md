# 📘 PORTS.md — Система кодирования портов и назначенные порты

## 📌 Формат портов

Каждому контейнеру назначается уникальный 4-значный порт по формуле:

```
5xyz
```

- `5` — всегда фиксированный префикс для локальной разработки
- `x` — тип компонента:
  - `0` — AI-ядро (`ai-engine`)
  - `1` — Шлюзы (`gateways`)
  - `2` — Сервисы (`services`)
  - `3` — Драйверы и низкоуровневые интерфейсы (`drivers`)
- `y` — подсистема:
  - `0` — AI-ядро, gateway (бизнес-логика)
  - `1` — Базы данных
  - `2` — Чат
  - `3` — Входящий аудиопоток
  - `4` — Выходящий аудиопоток
  - `5` — Компьютерное зрение
  - `6` — Захват экрана
  - `7` — Актуаторы (реле, моторы, выключатели)
  - `8` — Display (экран, выражения, визуализация)
- `z` — способ передачи данных / протокол:

| z  | Протокол / способ передачи данных             |
|:--:|-----------------------------------------------|
| 0  | USB / аналог / локальное подключение          |
| 1  | HTTP                                           |
| 2  | WebSocket                                      |
| 3  | Bluetooth / BLE                                |
| 4  | UDP                                            |
| 5  | TCP                                            |
| 6  | MQTT                                           |
| 7  | UART / Serial                                  |
| 8  | RTSP / MJPEG                                   |
| 9  | Комбинированный (HTTP + WS, MQTT + UART и др.)|

---

## 🎯 Назначенные порты

| Название              | Код `5xyz` | Тип      | Подсистема       | Протокол        |
|-----------------------|------------|----------|------------------|-----------------|
| ai-engine             | 5000       | Ядро     | AI               | HTTP            |
| gw-chat              | 5121       | Gateway  | Чат              | HTTP            |
| svc-frai-audio-in    | 5231       | Service  | Аудио (вход)     | HTTP            |
| svc-frai-audio-out   | 5241       | Service  | Аудио (выход)    | HTTP            |
| svc-dev-audio-in     | 5231       | Service  | Аудио (вход)     | HTTP            |
| svc-dev-audio-out    | 5241       | Service  | Аудио (выход)    | HTTP            |
| gw-frai              | 5181       | Gateway  | Display          | HTTP            |
| svc-stt              | 5231       | Service  | Аудио (вход)     | HTTP            |
| svc-tts              | 5241       | Service  | Аудио (выход)    | HTTP            |
| svc-vision           | 5251       | Service  | Комп. зрение     | HTTP            |
| svc-screen_vision    | 5261       | Service  | Экран            | HTTP            |
| svc-db               | 5211       | Service  | Базы данных      | HTTP            |
| drv-mic_usb          | 5330       | Driver   | Аудио (вход)     | USB             |

---

Готово для расширения. Дополните классификатор `z`, если появятся новые протоколы.
