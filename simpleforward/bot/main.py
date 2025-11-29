from aiogram import Router

from simpleforward.config import models

from .message_manager import MessageManager
from .routers.photo import PhotoRouter
from .routers.start import StartRouter
from .routers.text import TextRouter


def build(forwarding_config: models.Forwarding,
          message_manager: MessageManager):
    main_router = Router()

    main_router.include_routers(
        StartRouter(),
        TextRouter(forwarding_config,
                   message_manager),
        PhotoRouter(forwarding_config,
                    message_manager)
    )

    return main_router