from aiogram import Bot
from aiogram.types import ChatIdUnion, Message
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
from typing import Dict

from anonflow.config import Config
from anonflow.moderation.models import (
    Events,
    ExecutorDeletionEvent,
    ModerationDecisionEvent,
    ModerationStartedEvent,
)
from anonflow.translator import Translator


class EventHandler:
    def __init__(self, bot: Bot, config: Config, translator: Translator):
        self.bot = bot
        self.config = config
        self.translator = translator

        self._messages: Dict[ChatIdUnion, Message] = {}

    async def handle(self, event: Events, message: Message):
        moderation_chat_ids = self.config.forwarding.moderation_chat_ids

        _ = self.translator.get()

        if isinstance(event, ModerationStartedEvent):
            self._messages[message.chat.id] = await message.answer(
                _("messages.user.moderation_pending", message=message)
            )
        elif isinstance(event, ModerationDecisionEvent):
            for chat_id in moderation_chat_ids:
                if event.approved:
                    await message.bot.send_message(
                        chat_id,
                        _(
                            "messages.staff.moderation_approved",
                            message=message,
                            explanation=event.explanation,
                        )
                    )
                else:
                    await message.bot.send_message(
                        chat_id,
                        _(
                            "messages.staff.moderation_rejected",
                            message=message,
                            explanation=event.explanation,
                        )
                    )

            with suppress(TelegramBadRequest):
                msg = self._messages.get(message.chat.id)
                if isinstance(msg, Message):
                    await msg.delete()

            if event.approved:
                await message.answer(_("messages.user.send_success", message=message))
            else:
                await message.answer(_("messages.user.moderation_rejected", message=message))
        elif isinstance(event, ExecutorDeletionEvent) and moderation_chat_ids:
            for chat_id in moderation_chat_ids:
                if event.success:
                    await message.bot.send_message(
                        chat_id,
                        _(
                            "messages.staff.deletion_success",
                            message=message,
                            message_id=event.message_id,
                        )
                    )
                else:
                    await message.bot.send_message(
                        chat_id,
                        _(
                            "messages.staff.deletion_failure",
                            message=message,
                            message_id=event.message_id,
                        )
                    )
