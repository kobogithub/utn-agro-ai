from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Farmer Schemas
class FarmerBase(BaseModel):
    name: str
    email: EmailStr
    region: str


class FarmerCreate(FarmerBase):
    pass


class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    region: Optional[str] = None


class Farmer(FarmerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Crop Schemas
class CropBase(BaseModel):
    name: str
    type: str
    variety: Optional[str] = None


class CropCreate(CropBase):
    pass


class CropUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    variety: Optional[str] = None


class Crop(CropBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Plot Schemas
class PlotBase(BaseModel):
    name: str
    hectares: float
    planting_date: Optional[datetime] = None
    farmer_id: int
    crop_id: Optional[int] = None


class PlotCreate(PlotBase):
    pass


class PlotUpdate(BaseModel):
    name: Optional[str] = None
    hectares: Optional[float] = None
    planting_date: Optional[datetime] = None
    farmer_id: Optional[int] = None
    crop_id: Optional[int] = None


class Plot(PlotBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Extended schemas with relationships
class FarmerWithPlots(Farmer):
    plots: List[Plot] = []


class PlotWithRelations(Plot):
    farmer: Farmer
    crop: Optional[Crop] = None