from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from anonflow.bot.utils.template_renderer import TemplateRenderer


class InfoRouter(Router):
    def __init__(self, template_renderer: TemplateRenderer):
        super().__init__()

        self.renderer = template_renderer

        self._register_handlers()

    def _register_handlers(self):
        @self.message(Command("info"))
        async def on_start(message: Message):
            await message.answer(
                await self.renderer.render("commands/info.j2", message=message)
            )
