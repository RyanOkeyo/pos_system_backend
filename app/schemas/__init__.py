from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    sale_price: float = Field(..., gt=0)
    rent_price_per_day: Optional[float] = Field(None, ge=0)
    quantity_in_stock: int = Field(0, ge=0)
    barcode: Optional[str] = None
    sku: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    sale_price: Optional[float] = Field(None, gt=0)
    rent_price_per_day: Optional[float] = Field(None, ge=0)
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    barcode: Optional[str] = None
    sku: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    sale_price: float
    rent_price_per_day: Optional[float]
    quantity_in_stock: int
    quantity_rented: int
    barcode: Optional[str]
    sku: Optional[str]
    
    class Config:
        from_attributes = True