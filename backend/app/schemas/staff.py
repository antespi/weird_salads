from pydantic import BaseModel


class Credentials(BaseModel):
    pin: int


class Staff(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
