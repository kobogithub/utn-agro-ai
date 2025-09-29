# Agro API - FastAPI + MCP Server

API REST para gestión agrícola con servidor MCP integrado - UTN Course Material

## 📋 Descripción

Este proyecto combina:
- **API REST** con FastAPI para operaciones CRUD sobre datos agrícolas
- **Servidor MCP** (Model Context Protocol) que expone las operaciones como herramientas para LLMs
- **Base de datos SQLite** con 3 tablas relacionadas

### Modelo de Datos

1. **Farmers (Agricultores)**: Información de productores agrícolas
2. **Crops (Cultivos)**: Catálogo de cultivos disponibles
3. **Plots (Parcelas)**: Parcelas de tierra asociadas a agricultores y cultivos

## 🚀 Instalación

```bash
cd server-api

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 🐳 Uso con Docker (Recomendado)

### Iniciar con Docker Compose

```bash
cd server-api

# Construir y levantar el servicio
docker-compose up -d

# Ver logs
docker-compose logs -f

# Poblar la base de datos con datos de ejemplo
docker-compose exec agro-api python seed_data.py

# Detener el servicio
docker-compose down
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

**Nota**: La base de datos se persiste en el directorio `./data/` del host.

### Comandos Docker Útiles

```bash
# Reconstruir la imagen
docker-compose build

# Ver estado de contenedores
docker-compose ps

# Ejecutar comandos dentro del contenedor
docker-compose exec agro-api python seed_data.py

# Ver logs en tiempo real
docker-compose logs -f agro-api

# Detener y eliminar volúmenes
docker-compose down -v
```

## 🔧 Uso sin Docker

### 1. Ejecutar el API REST

```bash
python main.py
```

O con uvicorn directamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

### 2. Ejecutar el Servidor MCP

```bash
python mcp_server.py
```

El servidor MCP usa STDIO para comunicación y debe ser configurado en Claude Desktop o similar.

## 📡 Endpoints del API

### Farmers (Agricultores)

- `POST /farmers/` - Crear agricultor
- `GET /farmers/` - Listar agricultores
- `GET /farmers/{farmer_id}` - Obtener agricultor con sus parcelas
- `PUT /farmers/{farmer_id}` - Actualizar agricultor
- `DELETE /farmers/{farmer_id}` - Eliminar agricultor

### Crops (Cultivos)

- `POST /crops/` - Crear cultivo
- `GET /crops/` - Listar cultivos
- `GET /crops/{crop_id}` - Obtener cultivo
- `PUT /crops/{crop_id}` - Actualizar cultivo
- `DELETE /crops/{crop_id}` - Eliminar cultivo

### Plots (Parcelas)

- `POST /plots/` - Crear parcela
- `GET /plots/` - Listar parcelas con relaciones
- `GET /plots/{plot_id}` - Obtener parcela con relaciones
- `PUT /plots/{plot_id}` - Actualizar parcela
- `DELETE /plots/{plot_id}` - Eliminar parcela

## 🛠️ Herramientas MCP

El servidor MCP expone 15 herramientas:

### Farmers
- `list_farmers` - Lista todos los agricultores
- `get_farmer` - Obtiene un agricultor por ID
- `create_farmer` - Crea un nuevo agricultor
- `update_farmer` - Actualiza un agricultor
- `delete_farmer` - Elimina un agricultor

### Crops
- `list_crops` - Lista todos los cultivos
- `get_crop` - Obtiene un cultivo por ID
- `create_crop` - Crea un nuevo cultivo
- `update_crop` - Actualiza un cultivo
- `delete_crop` - Elimina un cultivo

### Plots
- `list_plots` - Lista todas las parcelas con relaciones
- `get_plot` - Obtiene una parcela por ID
- `create_plot` - Crea una nueva parcela
- `update_plot` - Actualiza una parcela
- `delete_plot` - Elimina una parcela

## 🧪 Ejemplos de Uso

### Crear un Agricultor (cURL)

```bash
curl -X POST "http://localhost:8000/farmers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "region": "Zona Núcleo"
  }'
```

### Crear un Cultivo (Python)

```python
import requests

response = requests.post("http://localhost:8000/crops/", json={
    "name": "Soja RR",
    "type": "oleaginosa",
    "variety": "DM 4670"
})
print(response.json())
```

### Crear una Parcela (cURL)

```bash
curl -X POST "http://localhost:8000/plots/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lote Norte",
    "hectares": 120.5,
    "farmer_id": 1,
    "crop_id": 1,
    "planting_date": "2024-10-15T00:00:00"
  }'
```

## ⚙️ Configuración MCP en Claude Desktop

Agregar al archivo de configuración de Claude Desktop:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "agro-api": {
      "command": "python",
      "args": ["/ruta/completa/server-api/mcp_server.py"],
      "env": {}
    }
  }
}
```

Reiniciar Claude Desktop después de la configuración.

## 📊 Estructura del Proyecto

```
server-api/
├── main.py              # FastAPI application
├── mcp_server.py        # MCP server implementation
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # CRUD operations
├── seed_data.py         # Script to populate database
├── requirements.txt     # Dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yaml  # Docker Compose orchestration
├── .gitignore           # Git ignore patterns
├── README.md            # This file
├── data/                # Database directory (Docker volume)
│   └── agro_api.db      # SQLite database (Docker)
└── agro_api.db          # SQLite database (local, created on first run)
```

## 🎓 Propósito Educativo

Este proyecto es material didáctico para el curso de UTN sobre:
- Desarrollo de APIs REST con FastAPI
- Integración de bases de datos con SQLAlchemy
- Implementación de servidores MCP para LLMs
- Arquitectura CRUD completa
- Validación con Pydantic
- Containerización con Docker y Docker Compose
- Persistencia de datos con volúmenes Docker

## 📝 Notas

- La base de datos SQLite se crea automáticamente al ejecutar la aplicación
- Los modelos incluyen relaciones uno-a-muchos (Farmer → Plots, Crop → Plots)
- El MCP server permite que LLMs interactúen directamente con la base de datos
- Todos los endpoints incluyen validación de datos con Pydantic

## 🔗 Testing con MCP Inspector

Para probar el servidor MCP:

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

Esto abrirá una interfaz web para inspeccionar y probar las herramientas MCP.