from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float

class Invoice(BaseModel):
    invoice_number: str
    date: str = Field(description="Дата в формате ГГГГ-ММ-ДД")
    vendor: str
    currency: str = Field(description="Код валюты, например RUB")
    items: list[LineItem]
    total: float