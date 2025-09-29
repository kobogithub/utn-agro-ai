#!/usr/bin/env python3
"""
MCP Server for Agro API
Exposes CRUD operations as MCP tools for LLM interaction
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Import database and CRUD operations
from database import SessionLocal
import crud
import schemas


# Create MCP server instance
app = Server("agro-api-mcp")


def get_db():
    """Get database session"""
    return SessionLocal()


# ========== FARMER TOOLS ==========
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        # Farmer tools
        Tool(
            name="list_farmers",
            description="Lista todos los agricultores registrados en la base de datos",
            inputSchema={
                "type": "object",
                "properties": {
                    "skip": {"type": "integer", "description": "Registros a saltar", "default": 0},
                    "limit": {"type": "integer", "description": "Máximo de registros", "default": 100}
                }
            }
        ),
        Tool(
            name="get_farmer",
            description="Obtiene un agricultor específico por su ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "farmer_id": {"type": "integer", "description": "ID del agricultor"}
                },
                "required": ["farmer_id"]
            }
        ),
        Tool(
            name="create_farmer",
            description="Crea un nuevo agricultor",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Nombre del agricultor"},
                    "email": {"type": "string", "description": "Email del agricultor"},
                    "region": {"type": "string", "description": "Región del agricultor"}
                },
                "required": ["name", "email", "region"]
            }
        ),
        Tool(
            name="update_farmer",
            description="Actualiza los datos de un agricultor existente",
            inputSchema={
                "type": "object",
                "properties": {
                    "farmer_id": {"type": "integer", "description": "ID del agricultor"},
                    "name": {"type": "string", "description": "Nuevo nombre (opcional)"},
                    "email": {"type": "string", "description": "Nuevo email (opcional)"},
                    "region": {"type": "string", "description": "Nueva región (opcional)"}
                },
                "required": ["farmer_id"]
            }
        ),
        Tool(
            name="delete_farmer",
            description="Elimina un agricultor de la base de datos",
            inputSchema={
                "type": "object",
                "properties": {
                    "farmer_id": {"type": "integer", "description": "ID del agricultor a eliminar"}
                },
                "required": ["farmer_id"]
            }
        ),

        # Crop tools
        Tool(
            name="list_crops",
            description="Lista todos los cultivos registrados",
            inputSchema={
                "type": "object",
                "properties": {
                    "skip": {"type": "integer", "description": "Registros a saltar", "default": 0},
                    "limit": {"type": "integer", "description": "Máximo de registros", "default": 100}
                }
            }
        ),
        Tool(
            name="get_crop",
            description="Obtiene un cultivo específico por su ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "crop_id": {"type": "integer", "description": "ID del cultivo"}
                },
                "required": ["crop_id"]
            }
        ),
        Tool(
            name="create_crop",
            description="Crea un nuevo cultivo",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Nombre del cultivo"},
                    "type": {"type": "string", "description": "Tipo de cultivo (ej: cereal, oleaginosa)"},
                    "variety": {"type": "string", "description": "Variedad del cultivo (opcional)"}
                },
                "required": ["name", "type"]
            }
        ),
        Tool(
            name="update_crop",
            description="Actualiza los datos de un cultivo existente",
            inputSchema={
                "type": "object",
                "properties": {
                    "crop_id": {"type": "integer", "description": "ID del cultivo"},
                    "name": {"type": "string", "description": "Nuevo nombre (opcional)"},
                    "type": {"type": "string", "description": "Nuevo tipo (opcional)"},
                    "variety": {"type": "string", "description": "Nueva variedad (opcional)"}
                },
                "required": ["crop_id"]
            }
        ),
        Tool(
            name="delete_crop",
            description="Elimina un cultivo de la base de datos",
            inputSchema={
                "type": "object",
                "properties": {
                    "crop_id": {"type": "integer", "description": "ID del cultivo a eliminar"}
                },
                "required": ["crop_id"]
            }
        ),

        # Plot tools
        Tool(
            name="list_plots",
            description="Lista todas las parcelas registradas con sus relaciones (agricultor y cultivo)",
            inputSchema={
                "type": "object",
                "properties": {
                    "skip": {"type": "integer", "description": "Registros a saltar", "default": 0},
                    "limit": {"type": "integer", "description": "Máximo de registros", "default": 100}
                }
            }
        ),
        Tool(
            name="get_plot",
            description="Obtiene una parcela específica por su ID con sus relaciones",
            inputSchema={
                "type": "object",
                "properties": {
                    "plot_id": {"type": "integer", "description": "ID de la parcela"}
                },
                "required": ["plot_id"]
            }
        ),
        Tool(
            name="create_plot",
            description="Crea una nueva parcela asociada a un agricultor",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Nombre de la parcela"},
                    "hectares": {"type": "number", "description": "Tamaño en hectáreas"},
                    "farmer_id": {"type": "integer", "description": "ID del agricultor dueño"},
                    "crop_id": {"type": "integer", "description": "ID del cultivo actual (opcional)"},
                    "planting_date": {"type": "string", "description": "Fecha de siembra ISO format (opcional)"}
                },
                "required": ["name", "hectares", "farmer_id"]
            }
        ),
        Tool(
            name="update_plot",
            description="Actualiza los datos de una parcela existente",
            inputSchema={
                "type": "object",
                "properties": {
                    "plot_id": {"type": "integer", "description": "ID de la parcela"},
                    "name": {"type": "string", "description": "Nuevo nombre (opcional)"},
                    "hectares": {"type": "number", "description": "Nuevo tamaño (opcional)"},
                    "farmer_id": {"type": "integer", "description": "Nuevo agricultor (opcional)"},
                    "crop_id": {"type": "integer", "description": "Nuevo cultivo (opcional)"},
                    "planting_date": {"type": "string", "description": "Nueva fecha de siembra (opcional)"}
                },
                "required": ["plot_id"]
            }
        ),
        Tool(
            name="delete_plot",
            description="Elimina una parcela de la base de datos",
            inputSchema={
                "type": "object",
                "properties": {
                    "plot_id": {"type": "integer", "description": "ID de la parcela a eliminar"}
                },
                "required": ["plot_id"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    db = get_db()

    try:
        # ========== FARMER OPERATIONS ==========
        if name == "list_farmers":
            skip = arguments.get("skip", 0)
            limit = arguments.get("limit", 100)
            farmers = crud.get_farmers(db, skip=skip, limit=limit)
            result = [schemas.Farmer.model_validate(f).model_dump() for f in farmers]
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "get_farmer":
            farmer_id = arguments["farmer_id"]
            farmer = crud.get_farmer(db, farmer_id=farmer_id)
            if not farmer:
                return [TextContent(type="text", text=json.dumps({"error": "Farmer not found"}))]
            result = schemas.FarmerWithPlots.model_validate(farmer).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "create_farmer":
            farmer_data = schemas.FarmerCreate(**arguments)
            # Check if email exists
            existing = crud.get_farmer_by_email(db, email=farmer_data.email)
            if existing:
                return [TextContent(type="text", text=json.dumps({"error": "Email already registered"}))]
            farmer = crud.create_farmer(db, farmer=farmer_data)
            result = schemas.Farmer.model_validate(farmer).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "update_farmer":
            farmer_id = arguments.pop("farmer_id")
            farmer_data = schemas.FarmerUpdate(**arguments)
            farmer = crud.update_farmer(db, farmer_id=farmer_id, farmer=farmer_data)
            if not farmer:
                return [TextContent(type="text", text=json.dumps({"error": "Farmer not found"}))]
            result = schemas.Farmer.model_validate(farmer).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "delete_farmer":
            farmer_id = arguments["farmer_id"]
            success = crud.delete_farmer(db, farmer_id=farmer_id)
            if not success:
                return [TextContent(type="text", text=json.dumps({"error": "Farmer not found"}))]
            return [TextContent(type="text", text=json.dumps({"message": "Farmer deleted successfully"}))]

        # ========== CROP OPERATIONS ==========
        elif name == "list_crops":
            skip = arguments.get("skip", 0)
            limit = arguments.get("limit", 100)
            crops = crud.get_crops(db, skip=skip, limit=limit)
            result = [schemas.Crop.model_validate(c).model_dump() for c in crops]
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "get_crop":
            crop_id = arguments["crop_id"]
            crop = crud.get_crop(db, crop_id=crop_id)
            if not crop:
                return [TextContent(type="text", text=json.dumps({"error": "Crop not found"}))]
            result = schemas.Crop.model_validate(crop).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "create_crop":
            crop_data = schemas.CropCreate(**arguments)
            crop = crud.create_crop(db, crop=crop_data)
            result = schemas.Crop.model_validate(crop).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "update_crop":
            crop_id = arguments.pop("crop_id")
            crop_data = schemas.CropUpdate(**arguments)
            crop = crud.update_crop(db, crop_id=crop_id, crop=crop_data)
            if not crop:
                return [TextContent(type="text", text=json.dumps({"error": "Crop not found"}))]
            result = schemas.Crop.model_validate(crop).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "delete_crop":
            crop_id = arguments["crop_id"]
            success = crud.delete_crop(db, crop_id=crop_id)
            if not success:
                return [TextContent(type="text", text=json.dumps({"error": "Crop not found"}))]
            return [TextContent(type="text", text=json.dumps({"message": "Crop deleted successfully"}))]

        # ========== PLOT OPERATIONS ==========
        elif name == "list_plots":
            skip = arguments.get("skip", 0)
            limit = arguments.get("limit", 100)
            plots = crud.get_plots(db, skip=skip, limit=limit)
            result = [schemas.PlotWithRelations.model_validate(p).model_dump() for p in plots]
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "get_plot":
            plot_id = arguments["plot_id"]
            plot = crud.get_plot(db, plot_id=plot_id)
            if not plot:
                return [TextContent(type="text", text=json.dumps({"error": "Plot not found"}))]
            result = schemas.PlotWithRelations.model_validate(plot).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "create_plot":
            plot_data = schemas.PlotCreate(**arguments)
            # Verify farmer exists
            farmer = crud.get_farmer(db, farmer_id=plot_data.farmer_id)
            if not farmer:
                return [TextContent(type="text", text=json.dumps({"error": "Farmer not found"}))]
            # Verify crop exists if provided
            if plot_data.crop_id:
                crop = crud.get_crop(db, crop_id=plot_data.crop_id)
                if not crop:
                    return [TextContent(type="text", text=json.dumps({"error": "Crop not found"}))]
            plot = crud.create_plot(db, plot=plot_data)
            result = schemas.Plot.model_validate(plot).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "update_plot":
            plot_id = arguments.pop("plot_id")
            plot_data = schemas.PlotUpdate(**arguments)
            plot = crud.update_plot(db, plot_id=plot_id, plot=plot_data)
            if not plot:
                return [TextContent(type="text", text=json.dumps({"error": "Plot not found"}))]
            result = schemas.Plot.model_validate(plot).model_dump()
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "delete_plot":
            plot_id = arguments["plot_id"]
            success = crud.delete_plot(db, plot_id=plot_id)
            if not success:
                return [TextContent(type="text", text=json.dumps({"error": "Plot not found"}))]
            return [TextContent(type="text", text=json.dumps({"message": "Plot deleted successfully"}))]

        else:
            return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    finally:
        db.close()


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())