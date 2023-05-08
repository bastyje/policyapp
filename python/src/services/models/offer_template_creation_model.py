from datetime import date

from pydantic import BaseModel


class OfferTemplateCreationModel(BaseModel):
    name: str
    insurerId: int
    quotationAlgorithm: str
    validFrom: date
    validTo: date
