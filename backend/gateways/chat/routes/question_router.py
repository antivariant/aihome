from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED
from config import API_TOKEN, GW_HUB_URL, UPLOAD_DIR, uploads_col, get_hub_client
from models.utils.logging_service import make_human_logger, make_tech_logger
from models.contracts.chat.agent_input import AgentInput
import os, uuid, time, shutil

router = APIRouter()

@router.post("/question")
async def send_input(
    request: Request,
    device_id: str = Form(...),
    user_id:   str = Form(...),
    text:      str = Form(None),
    file:      UploadFile = File(None),
    client=Depends(get_hub_client)
):
    # Инициализируем контекст сессии и взаимодействия
    session_id = str(uuid.uuid4())
    interaction_id = str(uuid.uuid4())

    # Создаём логгеры
    hlog = make_human_logger("gw-chat", session_id, interaction_id)
    tlog = make_tech_logger("gw-chat", session_id, interaction_id)

    hlog(f"Получен запрос от пользователя {user_id} c устройства {device_id}","gw-chat")

    # Аутентификация
    auth = request.headers.get("Authorization", "")
    if auth.replace("Bearer ", "") != API_TOKEN:
        tlog(
            "ERROR",
            headers=dict(request.headers),
            error="Unauthorized"
        )
        hlog("Ошибка аутентификации", "gw-chat")
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Обработка файла (если передан)
    input_type, filename = "text", None
    if file:
        ext = os.path.splitext(file.filename)[1]
        file_uuid = uuid.uuid4().hex
        filename = f"{file_uuid}{ext}"
        path = os.path.join(UPLOAD_DIR, filename)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(path, "wb") as dst:
            shutil.copyfileobj(file.file, dst)

        content_type = file.content_type.lower()
        input_type = "image" if content_type.startswith("image/") else "file"

        # Сохраняем метаданные в БД
        uploads_col.insert_one({
            "_id": file_uuid,
            "original_name": file.filename,
            "stored_path": f"uploads/{filename}",
            "content_type": content_type,
            "device_id": device_id,
            "user_id": user_id,
            "timestamp": int(time.time()),
            "input_type": input_type,
            "description": "Загружено пользователем через чат"
        })

        # Логируем сохранение файла
        hlog(
            message=f"Сохранил файл {file.filename} в базу данных (id={file_uuid})",
            target="gw-hub"
        )
        tlog(
            level="INFO",
            action="save_upload",
            original_name=file.filename,
            stored_path=f"uploads/{filename}",
            file_uuid=file_uuid,
            content_type=content_type,
            device_id=device_id,
            user_id=user_id
        )

    # Формируем и отправляем AgentInput на центральный хаб
    agent_input = AgentInput(
        device_id=device_id,
        user_id=user_id,
        input_type=input_type,
        input_data=(f"uploads/{filename}" if filename else text.strip()),
        session_id=session_id,
        interaction_id=interaction_id
    )

    hlog("Отправляю хабу для обработки", "gw-hub")
    resp = await client.post(f"{GW_HUB_URL}/process/question", json=agent_input.model_dump(), timeout=60.0)
    data = resp.json()
    data.update(session_id=session_id, interaction_id=interaction_id)
    return data
