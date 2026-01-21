from pydantic import BaseModel

class Service(BaseModel):
    online: bool = False