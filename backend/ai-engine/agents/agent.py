# agents/agent.py

from langchain.llms import OpenAI
from langchain.agents import Tool, initialize_agent, AgentType

# Импортируем ваши асинхронные функции из light_tools
from skills.light_control.light_tools import turn_on_light, turn_off_light, set_brightness

# Описываем инструменты, указывая и обычную, и асинхронную реализацию
tools = [
    Tool(
        name="turn_on_light",
        description="Включает лампу. Аргумент — текст с указанием комнаты и лампы.",
        func=turn_on_light,        # для синхронного вызова (англерплит)
        coroutine=turn_on_light,   # для асинхронного
    ),
    Tool(
        name="turn_off_light",
        description="Выключает лампу. Аргумент — текст с указанием комнаты и лампы.",
        func=turn_off_light,
        coroutine=turn_off_light,
    ),
    Tool(
        name="set_brightness",
        description="Устанавливает яркость лампы в процентах. В тексте должен быть процент, например «на 50%».",
        func=set_brightness,
        coroutine=set_brightness,
    ),
]

# Подключаем LLM
llm = OpenAI(model="gpt-4o-mini")

# Инициализируем агента, он подхватит async-корутины
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

async def handle_user_message(
    text: str,
    callbacks: list = None
) -> str:
    """
    Прогоняем текст через агент. 
    Если переданы callbacks (список BaseCallbackHandler), они будут вызваны.
    """
    # если агент асинхронный — вызываем arun
    return await agent.arun(text, callbacks=callbacks)
