# agents/agent.py

from langchain_community.llms import OpenAI
from langchain.agents import Tool, initialize_agent, AgentType

# теперь импортируем из light_control уже синхронные обёртки
from skills.light_control.light_tools import turn_on_light, turn_off_light, set_brightness

tools = [
    Tool(
        name="turn_on_light",
        func=turn_on_light,
        description="Включает лампу. Аргумент — текст с указанием комнаты и лампы."
    ),
    Tool(
        name="turn_off_light",
        func=turn_off_light,
        description="Выключает лампу. Аргумент — текст с указанием комнаты и лампы."
    ),
    Tool(
        name="set_brightness",
        func=set_brightness,
        description="Устанавливает яркость лампы в процентах. В тексте должен быть процент, например «на 50%»."
    ),
]

llm = OpenAI(model="gpt-4o-mini")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
