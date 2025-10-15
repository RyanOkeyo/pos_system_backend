from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)

class SaleCreate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    items: List[SaleItemCreate]
    payment_method: str = Field(..., pattern='^(cash|card|mobile)$')
    discount_amount: Optional[float] = Field(0, ge=0)

class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str]
    quantity: int
    unit_price: float
    subtotal: float
    
    class Config:
        from_attributes = True

class SaleResponse(BaseModel):
    id: int
    sale_number: str
    customer_name: Optional[str]
    customer_phone: Optional[str]
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    payment_method: str
    payment_status: str
    created_at: datetime
    items: List[SaleItemResponse]
    
    class Config:
        from_attributes = True