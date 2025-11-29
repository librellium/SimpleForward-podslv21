from typing import List, Literal, Optional, TypeAlias

from pydantic import BaseModel, SecretStr

ForwardingType: TypeAlias = Literal["text", "photo", "video"]
LoggingLevel: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class Bot(BaseModel):
    token: Optional[SecretStr] = None
    timeout: int = 10

class Forwarding(BaseModel):
    target_chat_id: Optional[int] = None
    message_template: str = "У вас новое сообщение!\n%s"
    types: List[ForwardingType] = ["text"]

class Logging(BaseModel):
    level: LoggingLevel = "INFO"
    fmt: Optional[str] = "%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] %(message)s"
    date_fmt: Optional[str] = "%Y-%m-%d %H:%M:%S"