from dataclasses import dataclass
from core2.model import Item

@dataclass
class Result:
    site_name: str
    items: list[Item]