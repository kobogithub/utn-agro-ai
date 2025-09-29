#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de ejemplo
Run: python seed_data.py
"""

from datetime import datetime, timedelta
from database import SessionLocal, engine
import models
import crud
import schemas

# Create tables
models.Base.metadata.create_all(bind=engine)


def seed_database():
    """Populate database with sample data"""
    db = SessionLocal()

    try:
        print("🌱 Iniciando carga de datos de ejemplo...\n")

        # Create Farmers
        print("👨‍🌾 Creando agricultores...")
        farmers_data = [
            {"name": "Juan Pérez", "email": "juan.perez@agro.com", "region": "Zona Núcleo"},
            {"name": "María González", "email": "maria.gonzalez@campo.com", "region": "Pampa Húmeda"},
            {"name": "Carlos Rodríguez", "email": "carlos.rodriguez@rural.com", "region": "NOA"},
        ]

        farmers = []
        for data in farmers_data:
            farmer = schemas.FarmerCreate(**data)
            db_farmer = crud.create_farmer(db, farmer)
            farmers.append(db_farmer)
            print(f"  ✓ {db_farmer.name} - {db_farmer.region}")

        # Create Crops
        print("\n🌾 Creando cultivos...")
        crops_data = [
            {"name": "Soja", "type": "oleaginosa", "variety": "DM 4670"},
            {"name": "Maíz", "type": "cereal", "variety": "Pioneer 3080"},
            {"name": "Trigo", "type": "cereal", "variety": "ACA 315"},
            {"name": "Girasol", "type": "oleaginosa", "variety": "Aguará 6"},
            {"name": "Algodón", "type": "fibra", "variety": "Guazuncho 3"},
        ]

        crops = []
        for data in crops_data:
            crop = schemas.CropCreate(**data)
            db_crop = crud.create_crop(db, crop)
            crops.append(db_crop)
            print(f"  ✓ {db_crop.name} ({db_crop.type}) - {db_crop.variety}")

        # Create Plots
        print("\n📍 Creando parcelas...")
        plots_data = [
            {
                "name": "Lote Norte",
                "hectares": 120.5,
                "farmer_id": farmers[0].id,
                "crop_id": crops[0].id,  # Soja
                "planting_date": datetime.now() - timedelta(days=90),
            },
            {
                "name": "Lote Sur",
                "hectares": 85.0,
                "farmer_id": farmers[0].id,
                "crop_id": crops[1].id,  # Maíz
                "planting_date": datetime.now() - timedelta(days=60),
            },
            {
                "name": "Campo Central",
                "hectares": 200.0,
                "farmer_id": farmers[1].id,
                "crop_id": crops[2].id,  # Trigo
                "planting_date": datetime.now() - timedelta(days=120),
            },
            {
                "name": "Parcela Este",
                "hectares": 95.5,
                "farmer_id": farmers[1].id,
                "crop_id": crops[3].id,  # Girasol
                "planting_date": datetime.now() - timedelta(days=75),
            },
            {
                "name": "Lote Oeste",
                "hectares": 150.0,
                "farmer_id": farmers[2].id,
                "crop_id": crops[4].id,  # Algodón
                "planting_date": datetime.now() - timedelta(days=100),
            },
            {
                "name": "Reserva",
                "hectares": 50.0,
                "farmer_id": farmers[2].id,
                "crop_id": None,  # Sin cultivo asignado
                "planting_date": None,
            },
        ]

        for data in plots_data:
            plot = schemas.PlotCreate(**data)
            db_plot = crud.create_plot(db, plot)
            crop_name = next((c.name for c in crops if c.id == db_plot.crop_id), "Sin asignar")
            print(f"  ✓ {db_plot.name} - {db_plot.hectares} ha - Cultivo: {crop_name}")

        print("\n✅ Base de datos poblada exitosamente!")
        print(f"\n📊 Resumen:")
        print(f"   - {len(farmers)} agricultores")
        print(f"   - {len(crops)} cultivos")
        print(f"   - {len(plots_data)} parcelas")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()