from aiogram import types

from bot_controller.router import Router


router = Router(name=__name__)


@router.register(
    command="help",
    description="View all available commands",
)
async def send_welcome(message: types.Message) -> str:
    return message.answer("\n".join(router.command_list))


