from typing import Optional, Union

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    price: int
    description: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductPartial(ProductBase):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[int, None] = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
