import libmav
from pydantic import BaseModel


class MavlinkMessage(BaseModel):
    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_mavlink(cls, message: libmav.Message):
        return cls(**message.to_dict())
