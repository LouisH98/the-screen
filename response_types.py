from pydantic import BaseModel

class StatusResponse(BaseModel):
    slide: str
    brightness: float
    auto_rotate: bool
    rotation: int
