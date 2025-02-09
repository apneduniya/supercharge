from aiogram import types

from bot_controller.router import Router
from core.server.agent import AgentAPI

router = Router(name=__name__)
agent_api = AgentAPI()


@router.register(
    command="help",
    description="View all available commands",
)
async def send_welcome(message: types.Message) -> str:
    return message.answer("\n".join(router.command_list))


@router.register()
async def generate(message: types.Message) -> str:
    response = agent_api.generate(prompt=message.text)

    return message.answer(response)


