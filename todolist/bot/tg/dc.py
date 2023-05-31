from dataclasses import dataclass, field
from typing import Optional, List, Type

import marshmallow_dataclass
from marshmallow import EXCLUDE, Schema


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    type: str
    first_name: str
    last_name: Optional[str]
    title: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    chat: Chat
    from_: User = field(metadata={'data_key': 'from'})
    text: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class Update:
    update_id: int
    message: Optional[Message]

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[Update] = field(default_factory=list)

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE


# ----------------------------------------------------------------
# create schemas entities
GetUpdatesResponseSchema: Type[Schema] = marshmallow_dataclass.class_schema(GetUpdatesResponse)
SendMessageResponseSchema: Type[Schema] = marshmallow_dataclass.class_schema(SendMessageResponse)