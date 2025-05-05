import asyncio

async def mock_transcribe(audio_data: bytes) -> str:
    await asyncio.sleep(1)
    return "эй дом включи свет"
