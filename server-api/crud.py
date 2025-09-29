from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas


# ========== FARMER CRUD ==========
def get_farmer(db: Session, farmer_id: int) -> Optional[models.Farmer]:
    return db.query(models.Farmer).filter(models.Farmer.id == farmer_id).first()


def get_farmers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Farmer]:
    return db.query(models.Farmer).offset(skip).limit(limit).all()


def get_farmer_by_email(db: Session, email: str) -> Optional[models.Farmer]:
    return db.query(models.Farmer).filter(models.Farmer.email == email).first()


def create_farmer(db: Session, farmer: schemas.FarmerCreate) -> models.Farmer:
    db_farmer = models.Farmer(**farmer.model_dump())
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer


def update_farmer(db: Session, farmer_id: int, farmer: schemas.FarmerUpdate) -> Optional[models.Farmer]:
    db_farmer = get_farmer(db, farmer_id)
    if not db_farmer:
        return None

    update_data = farmer.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_farmer, key, value)

    db.commit()
    db.refresh(db_farmer)
    return db_farmer


def delete_farmer(db: Session, farmer_id: int) -> bool:
    db_farmer = get_farmer(db, farmer_id)
    if not db_farmer:
        return False
    db.delete(db_farmer)
    db.commit()
    return True


# ========== CROP CRUD ==========
def get_crop(db: Session, crop_id: int) -> Optional[models.Crop]:
    return db.query(models.Crop).filter(models.Crop.id == crop_id).first()


def get_crops(db: Session, skip: int = 0, limit: int = 100) -> List[models.Crop]:
    return db.query(models.Crop).offset(skip).limit(limit).all()


def create_crop(db: Session, crop: schemas.CropCreate) -> models.Crop:
    db_crop = models.Crop(**crop.model_dump())
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop


def update_crop(db: Session, crop_id: int, crop: schemas.CropUpdate) -> Optional[models.Crop]:
    db_crop = get_crop(db, crop_id)
    if not db_crop:
        return None

    update_data = crop.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_crop, key, value)

    db.commit()
    db.refresh(db_crop)
    return db_crop


def delete_crop(db: Session, crop_id: int) -> bool:
    db_crop = get_crop(db, crop_id)
    if not db_crop:
        return False
    db.delete(db_crop)
    db.commit()
    return True


# ========== PLOT CRUD ==========
def get_plot(db: Session, plot_id: int) -> Optional[models.Plot]:
    return db.query(models.Plot).filter(models.Plot.id == plot_id).first()


def get_plots(db: Session, skip: int = 0, limit: int = 100) -> List[models.Plot]:
    return db.query(models.Plot).offset(skip).limit(limit).all()


def get_plots_by_farmer(db: Session, farmer_id: int) -> List[models.Plot]:
    return db.query(models.Plot).filter(models.Plot.farmer_id == farmer_id).all()


def create_plot(db: Session, plot: schemas.PlotCreate) -> models.Plot:
    db_plot = models.Plot(**plot.model_dump())
    db.add(db_plot)
    db.commit()
    db.refresh(db_plot)
    return db_plot


def update_plot(db: Session, plot_id: int, plot: schemas.PlotUpdate) -> Optional[models.Plot]:
    db_plot = get_plot(db, plot_id)
    if not db_plot:
        return None

    update_data = plot.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plot, key, value)

    db.commit()
    db.refresh(db_plot)
    return db_plot


def delete_plot(db: Session, plot_id: int) -> bool:
    db_plot = get_plot(db, plot_id)
    if not db_plot:
        return False
    db.delete(db_plot)
    db.commit()
    return True