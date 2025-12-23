from typing import Optional

from aiogram import Router

from anonflow.config import Config
from anonflow.moderation import ModerationExecutor
from anonflow.translator import Translator

from .routers import InfoRouter, MediaRouter, StartRouter, TextRouter
from .utils import EventHandler, MessageManager


def build(
    config: Config,
    message_manager: MessageManager,
    translator: Translator,
    executor: Optional[ModerationExecutor] = None,
    event_handler: Optional[EventHandler] = None
):
    main_router = Router()

    main_router.include_routers(
        StartRouter(translator=translator),
        InfoRouter(translator=translator),
        TextRouter(
            config=config,
            message_manager=message_manager,
            translator=translator,
            moderation_executor=executor,
            event_handler=event_handler,
        ),
        MediaRouter(
            config=config,
            message_manager=message_manager,
            translator=translator,
            moderation_executor=executor,
            event_handler=event_handler,
        ),
    )

    return main_router
