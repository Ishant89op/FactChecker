from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class Request(BaseModel):
    text: str = ""