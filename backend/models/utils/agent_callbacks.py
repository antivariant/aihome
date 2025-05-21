# models/utils/agent_callbacks.py
from langchain.callbacks.base import BaseCallbackHandler
from models.utils.logging_service import make_human_logger

class AgentMongoLogger(BaseCallbackHandler):
    def __init__(
        self,
        session_id: str,
        interaction_id: str,
        actor: str = "ai-engine",
        target: str = "gw-hub",
    ):
        self.hlog = make_human_logger(actor, session_id, interaction_id)
        self.target = target

    def on_agent_action(self, action, **kwargs):
        # Логируем накопленный до этого момента текст мысли
        if hasattr(action, "log") and action.log:
            self.hlog(action.log.strip(), self.target)
        self.hlog(f"Action: {action.tool}", self.target)
        self.hlog(f"Action Input: {action.tool_input}", self.target)

    def on_tool_end(self, output, **kwargs):
        self.hlog(f"Observation: {output}", self.target)

    def on_agent_finish(self, finish, **kwargs):
        # finish.return_values обычно содержит {'output': ...}
        out = finish.return_values.get("output")
        self.hlog(f"Final Answer: {out}", self.target)
