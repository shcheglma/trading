from pydantic import BaseModel


class Crypto(BaseModel):
    name: str
    cost: float
