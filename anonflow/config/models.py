from typing import List, Literal, Optional, TypeAlias

from pydantic import BaseModel, SecretStr

SlowmodeMode: TypeAlias = Literal["global", "user"]
ForwardingType: TypeAlias = Literal["text", "photo", "video"]
ModerationType: TypeAlias = Literal["omni", "gpt"]
LoggingLevel: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Bot(BaseModel):
    token: Optional[SecretStr] = None
    timeout: int = 10


class BehaviorSlowmode(BaseModel):
    enabled: bool = True
    mode: SlowmodeMode = "user"
    delay: float = 120


class BehaviorSubscriptionRequirement(BaseModel):
    enabled: bool = True
    channel_ids: Optional[List[int]] = None


class Behavior(BaseModel):
    slowmode: BehaviorSlowmode = BehaviorSlowmode()
    subscription_requirement: BehaviorSubscriptionRequirement = BehaviorSubscriptionRequirement()


class Forwarding(BaseModel):
    moderation_chat_ids: Optional[List[int]] = None
    publication_channel_ids: Optional[List[int]] = None
    types: List[ForwardingType] = ["text", "photo", "video"]


class OpenAI(BaseModel):
    api_key: Optional[SecretStr] = None
    timeout: int = 10
    max_retries: int = 0


class Moderation(BaseModel):
    enabled: bool = True
    model: str = "gpt-5-mini"
    types: List[ModerationType] = ["omni", "gpt"]


class Logging(BaseModel):
    level: LoggingLevel = "INFO"
    fmt: Optional[str] = "%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] %(message)s"
    date_fmt: Optional[str] = "%Y-%m-%d %H:%M:%S"


class Config(BaseModel):
    bot: Bot = Bot()
    behavior: Behavior = Behavior()
    forwarding: Forwarding = Forwarding()
    openai: OpenAI = OpenAI()
    moderation: Moderation = Moderation()
    logging: Logging = Logging()
