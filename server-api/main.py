from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agro API",
    description="API REST para gestión agrícola - UTN MCP Course",
    version="1.0.0"
)


# ========== FARMER ENDPOINTS ==========
@app.post("/farmers/", response_model=schemas.Farmer, status_code=status.HTTP_201_CREATED, tags=["Farmers"])
def create_farmer(farmer: schemas.FarmerCreate, db: Session = Depends(get_db)):
    """Crear un nuevo agricultor"""
    db_farmer = crud.get_farmer_by_email(db, email=farmer.email)
    if db_farmer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_farmer(db=db, farmer=farmer)


@app.get("/farmers/", response_model=List[schemas.Farmer], tags=["Farmers"])
def read_farmers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de agricultores"""
    farmers = crud.get_farmers(db, skip=skip, limit=limit)
    return farmers


@app.get("/farmers/{farmer_id}", response_model=schemas.FarmerWithPlots, tags=["Farmers"])
def read_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """Obtener un agricultor por ID con sus parcelas"""
    db_farmer = crud.get_farmer(db, farmer_id=farmer_id)
    if db_farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return db_farmer


@app.put("/farmers/{farmer_id}", response_model=schemas.Farmer, tags=["Farmers"])
def update_farmer(farmer_id: int, farmer: schemas.FarmerUpdate, db: Session = Depends(get_db)):
    """Actualizar un agricultor"""
    db_farmer = crud.update_farmer(db, farmer_id=farmer_id, farmer=farmer)
    if db_farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return db_farmer


@app.delete("/farmers/{farmer_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Farmers"])
def delete_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """Eliminar un agricultor"""
    success = crud.delete_farmer(db, farmer_id=farmer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return None


# ========== CROP ENDPOINTS ==========
@app.post("/crops/", response_model=schemas.Crop, status_code=status.HTTP_201_CREATED, tags=["Crops"])
def create_crop(crop: schemas.CropCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cultivo"""
    return crud.create_crop(db=db, crop=crop)


@app.get("/crops/", response_model=List[schemas.Crop], tags=["Crops"])
def read_crops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de cultivos"""
    crops = crud.get_crops(db, skip=skip, limit=limit)
    return crops


@app.get("/crops/{crop_id}", response_model=schemas.Crop, tags=["Crops"])
def read_crop(crop_id: int, db: Session = Depends(get_db)):
    """Obtener un cultivo por ID"""
    db_crop = crud.get_crop(db, crop_id=crop_id)
    if db_crop is None:
        raise HTTPException(status_code=404, detail="Crop not found")
    return db_crop


@app.put("/crops/{crop_id}", response_model=schemas.Crop, tags=["Crops"])
def update_crop(crop_id: int, crop: schemas.CropUpdate, db: Session = Depends(get_db)):
    """Actualizar un cultivo"""
    db_crop = crud.update_crop(db, crop_id=crop_id, crop=crop)
    if db_crop is None:
        raise HTTPException(status_code=404, detail="Crop not found")
    return db_crop


@app.delete("/crops/{crop_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Crops"])
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    """Eliminar un cultivo"""
    success = crud.delete_crop(db, crop_id=crop_id)
    if not success:
        raise HTTPException(status_code=404, detail="Crop not found")
    return None


# ========== PLOT ENDPOINTS ==========
@app.post("/plots/", response_model=schemas.Plot, status_code=status.HTTP_201_CREATED, tags=["Plots"])
def create_plot(plot: schemas.PlotCreate, db: Session = Depends(get_db)):
    """Crear una nueva parcela"""
    # Verify farmer exists
    farmer = crud.get_farmer(db, farmer_id=plot.farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    # Verify crop exists if crop_id is provided
    if plot.crop_id:
        crop = crud.get_crop(db, crop_id=plot.crop_id)
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")

    return crud.create_plot(db=db, plot=plot)


@app.get("/plots/", response_model=List[schemas.PlotWithRelations], tags=["Plots"])
def read_plots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de parcelas con relaciones"""
    plots = crud.get_plots(db, skip=skip, limit=limit)
    return plots


@app.get("/plots/{plot_id}", response_model=schemas.PlotWithRelations, tags=["Plots"])
def read_plot(plot_id: int, db: Session = Depends(get_db)):
    """Obtener una parcela por ID con sus relaciones"""
    db_plot = crud.get_plot(db, plot_id=plot_id)
    if db_plot is None:
        raise HTTPException(status_code=404, detail="Plot not found")
    return db_plot


@app.put("/plots/{plot_id}", response_model=schemas.Plot, tags=["Plots"])
def update_plot(plot_id: int, plot: schemas.PlotUpdate, db: Session = Depends(get_db)):
    """Actualizar una parcela"""
    db_plot = crud.update_plot(db, plot_id=plot_id, plot=plot)
    if db_plot is None:
        raise HTTPException(status_code=404, detail="Plot not found")
    return db_plot


@app.delete("/plots/{plot_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Plots"])
def delete_plot(plot_id: int, db: Session = Depends(get_db)):
    """Eliminar una parcela"""
    success = crud.delete_plot(db, plot_id=plot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plot not found")
    return None


# ========== HEALTH CHECK ==========
@app.get("/", tags=["Health"])
def root():
    """Health check endpoint"""
    return {
        "message": "Agro API is running",
        "version": "1.0.0",
        "endpoints": {
            "farmers": "/farmers/",
            "crops": "/crops/",
            "plots": "/plots/",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)