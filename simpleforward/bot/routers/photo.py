import asyncio
from asyncio import CancelledError
from typing import Dict, List

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InputMediaPhoto, InputMediaVideo, Message

from simpleforward.bot.message_manager import MessageManager
from simpleforward.config import models


class PhotoRouter(Router):
    def __init__(self,
                 forwarding_config: models.Forwarding,
                 message_manager: MessageManager):
        super().__init__()

        self.config = forwarding_config
        self.message_manager = message_manager

        self.media_groups: Dict[int, dict] = {}
        self.media_groups_tasks: Dict[int, asyncio.Task] = {}
        self.media_groups_lock = asyncio.Lock()

        self._register_handlers()

    def _register_handlers(self):
        @self.message(F.photo | F.video)
        async def on_photo(message: Message, bot: Bot):
            if "photo" not in self.config.types and "video" not in self.config.types:
                return

            def can_send_media(msgs: List[Message]):
                photos = len([msg for msg in msgs if msg.photo])
                videos = len([msg for msg in msgs if msg.video])

                if (photos and "photo" in self.config.types) or (videos and "video" in self.config.types):
                    return True
                else:
                    return False

            def get_media(msg: Message):
                caption = self.config.message_template.format(text=msg.caption) if msg.caption else None
                parse_mode = "HTML" if msg.caption else None

                if msg.photo and "photo" in self.config.types:
                    return InputMediaPhoto(
                        media=msg.photo[-1].file_id,
                        caption=caption,
                        parse_mode=parse_mode
                    )
                elif msg.video and "video" in self.config.types:
                    return InputMediaVideo(
                        media=msg.video.file_id,
                        caption=caption,
                        parse_mode=parse_mode
                    )

            async def process_messages(messages: list[Message]):
                if not messages: return

                reply_to_message_id = messages[0].message_id

                try:
                    if can_send_media(messages):
                        if len(messages) > 1:
                            group_message_id = (await bot.send_media_group(
                                self.config.target_chat_id,
                                [
                                    get_media(msg)
                                    for msg in messages
                                ]
                            ))[0].message_id
                        elif len(messages) == 1:
                            msg = messages[0]

                            func = bot.send_photo if msg.photo else bot.send_video
                            file_id = msg.photo[-1].file_id if msg.photo else msg.video.file_id

                            group_message_id = (await func(
                                self.config.target_chat_id,
                                file_id,
                                caption=self.config.message_template.format(text=msg.caption or ""),
                                parse_mode="HTML"
                            )).message_id

                        self.message_manager.add(reply_to_message_id, group_message_id, message.chat.id)
                        await message.answer("✅ Сообщение успешно отправлено!")
                except (TelegramBadRequest, TelegramForbiddenError) as e:
                    await message.answer(f'❌ Не удалось отправить сообщение: "{e}"')

            media_group_id = message.media_group_id

            async def await_media_group():
                try:
                    await asyncio.sleep(2)
                    async with self.media_groups_lock:
                        messages = self.media_groups.pop(media_group_id, [])
                        self.media_groups_tasks.pop(media_group_id, None)
                    await process_messages(messages)
                except CancelledError:
                    pass

            if media_group_id:
                self.media_groups.setdefault(media_group_id, []).append(message)

                task = self.media_groups_tasks.get(media_group_id)
                if task: task.cancel()

                self.media_groups_tasks[media_group_id] = asyncio.create_task(await_media_group())
                return

            await process_messages([message])