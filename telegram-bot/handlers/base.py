from aiogram import types

from bot_controller.router import Router
from core.server.agent import AgentAPI

router = Router(name=__name__)
agent_api = AgentAPI()


@router.register(
    command="help",
    description="View all available commands",
)
async def send_welcome(message: types.Message):
    return message.answer("\n".join(router.command_list))


@router.register()
async def knowledge_base_generate(message: types.Message):
    response = agent_api.generate(prompt=message.text, _for="knowledge-base")
    return message.answer(response)

@router.register(
    command="member",
    description="Ask agents questions related to Superteam member"
)
async def superteam_member_agent_generate(message: types.Message):
    response = agent_api.generate(prompt=message.text, _for="superteam-member")
    return message.answer(response)


