# F.R.A.I. API Endpoints

| Service           | Method  | Path                        | Direction              | Description                                                                                       |
|-------------------|--------|-----------------------------|------------------------|---------------------------------------------------------------------------------------------------|
| `gw-chat`         | POST   | `/question`                 | Front → gw-chat        | Принимает из UI текст или файл, логирует, шлёт в `gw-hub` → ждёт ответ → возвращает UI.           |
| `gw-chat`         | POST   | `/upload`                   | Front → gw-chat        | Общая загрузка файлов (скриншоты, MD, Excel и т.п.), логирует, сохраняет и возвращает метаданные.   |
| `gw-hub`          | POST   | `/process/question`         | gw-* → gw-hub          | Получает «вопрос» от любого шлюза, логирует, шлёт в `ai-engine` → возвращает ответ шлюзу.         |
| `gw-hub`          | POST   | `/process/event`            | gw-* → gw-hub          | Принимает «событие» (триггер), логирует, пересылает в `ai-engine` или обратно на шлюз.             |
| `ai-engine`       | POST   | `/process`                  | gw-hub → ai-engine     | Основная AI-логика: получает `AgentInput`, возвращает `AgentOutput`.                               |
| `gw-frai`         | POST   | `/voice-question`           | svc-audio-in → gw-frai | Принимает аудио от микрофона, логирует, шлёт в STT, далее на `/process/question`.                 |
| `gw-frai`         | POST   | `/camera-event`             | svc-vision → gw-frai   | Принимает события CV (поза/лицо), логирует, шлёт в `/process/question`.                           |
| `gw-frai`         | POST   | `/chat-question`            | gw-chat → gw-frai      | Альтернативный вход для текстовых вопросов через `gw-chat`.                                        |
| `gw-frai`         | POST   | `/trigger/schedule`         | ai-engine → gw-frai    | Принимает веб-триггер от планировщика (расписание), шлёт в `/process/event` или WS.               |
| `gw-frai`         | POST   | `/trigger/event`            | External → gw-frai     | Общий вебхук-эндпоинт для Home Assistant, Jira, ai-home и т.п.                                     |
| `gw-frai`         | WS     | `/ws`                       | Bi-directional         | WebSocket-канал для пушей обратно в UI/устройства (tts-звук, видео-фреймы, уведомления).         |
| `svc-audio-in`    | POST   | `/transcribe`               | gw-frai → svc-stt      | STT-сервис: принимает `audio/*`, возвращает текст.                                                 |
| `svc-vision`      | POST   | `/analyze`                  | drv-camera → svc-vision| CV-сервис: кадр → события (поза, действие, лицо).                                                 |
| `svc-tts`         | POST   | `/synthesize`               | gw-frai → svc-tts      | TTS-сервис: текст → аудиофайл.                                                                   |
| `svc-audio-out`   | POST   | `/play`                     | gw-frai → svc-audio-out| Проигрывает готовый аудиофайл на целевом устройстве.                                             |
| `all services`    | GET    | `/health`                   | any → any              | Статус-чек (Liveness/Readiness).                                                                  |
