from pydantic import BaseModel


class InsurerCreationModel(BaseModel):
    name: str
    krs: str
    taxId: str
