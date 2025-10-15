from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RentItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    daily_rate: float = Field(..., gt=0)

class RentCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    customer_phone: str = Field(..., min_length=10)
    customer_email: Optional[str] = None
    customer_id_number: Optional[str] = None
    start_date: str  
    end_date: str    
    items: List[RentItemCreate]
    payment_method: str = Field(..., pattern='^(cash|card|mobile)$')
    deposit_percentage: Optional[float] = Field(0.2, ge=0, le=1)

class RentReturn(BaseModel):
    actual_return_date: str  
    items: List[dict] 

class RentItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str]
    quantity: int
    daily_rate: float
    number_of_days: int
    subtotal: float
    returned: bool
    condition_on_return: Optional[str]
    
    class Config:
        from_attributes = True

class RentResponse(BaseModel):
    id: int
    rent_number: str
    customer_name: str
    customer_phone: str
    customer_email: Optional[str]
    start_date: datetime
    end_date: datetime
    actual_return_date: Optional[datetime]
    subtotal: float
    deposit_amount: float
    late_fee: float
    total_amount: float
    payment_method: str
    payment_status: str
    rental_status: str
    created_at: datetime
    items: List[RentItemResponse]
    
    class Config:
        from_attributes = True