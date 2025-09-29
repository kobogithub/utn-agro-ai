from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Farmer(Base):
    """Agricultor - Farmer model"""
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    region = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    plots = relationship("Plot", back_populates="farmer", cascade="all, delete-orphan")


class Crop(Base):
    """Cultivo - Crop model"""
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False)  # e.g., "cereal", "leguminosa", "oleaginosa"
    variety = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    plots = relationship("Plot", back_populates="crop")


class Plot(Base):
    """Parcela - Plot/Field model"""
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    hectares = Column(Float, nullable=False)
    planting_date = Column(DateTime)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    farmer = relationship("Farmer", back_populates="plots")
    crop = relationship("Crop", back_populates="plots")