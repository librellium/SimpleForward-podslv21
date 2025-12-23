from dataclasses import dataclass
from typing import Optional, Union

from aiogram.types import ChatIdUnion


@dataclass
class ExecutorDeletionEvent:
    success: bool
    message_id: Optional[ChatIdUnion] = None


@dataclass
class ModerationDecisionEvent:
    approved: bool
    explanation: str


@dataclass
class ModerationStartedEvent:
    pass


Events = Union[ExecutorDeletionEvent, ModerationDecisionEvent, ModerationStartedEvent]
