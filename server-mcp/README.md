# Agro MCP Server - Dockerized

Servidor MCP (Model Context Protocol) dockerizado para exponer operaciones CRUD como herramientas para LLMs - UTN Course Material

## 📋 Descripción

Este servidor MCP dockerizado:
- Expone 15 herramientas CRUD (Farmers, Crops, Plots) a LLMs como Claude
- Usa comunicación STDIO (stdin/stdout) según el protocolo MCP
- Comparte la base de datos SQLite con `server-api`
- Se ejecuta como contenedor Docker independiente

## 🚀 Instalación y Uso

### Opción 1: Docker Compose Standalone

```bash
cd server-mcp

# Construir y levantar el servicio
docker-compose up -d

# Ver logs
docker-compose logs -f agro-mcp

# Detener el servicio
docker-compose down
```

### Opción 2: Con el API REST (Recomendado)

Usar el `docker-compose.yaml` principal en la raíz del proyecto que levanta ambos servicios.

```bash
cd /home/kobo/projects/me/utn-agro-ai

# Levantar ambos servicios (API + MCP)
docker-compose up -d

# Ver estado
docker-compose ps

# Logs del MCP server
docker-compose logs -f agro-mcp

# Detener ambos servicios
docker-compose down
```

## ⚙️ Configuración en Claude Desktop

El servidor MCP dockerizado se configura de manera diferente que la versión local:

**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "agro-api": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--network=host",
        "-v", "/home/kobo/projects/me/utn-agro-ai/server-api/data:/app/data",
        "agro-mcp:latest"
      ]
    }
  }
}
```

**Nota**: Primero construye la imagen con `docker-compose build` o `docker build -t agro-mcp .`

## 🛠️ Herramientas MCP Disponibles

### Farmers (Agricultores)
- `list_farmers` - Lista todos los agricultores
- `get_farmer` - Obtiene un agricultor por ID
- `create_farmer` - Crea un nuevo agricultor
- `update_farmer` - Actualiza un agricultor
- `delete_farmer` - Elimina un agricultor

### Crops (Cultivos)
- `list_crops` - Lista todos los cultivos
- `get_crop` - Obtiene un cultivo por ID
- `create_crop` - Crea un nuevo cultivo
- `update_crop` - Actualiza un cultivo
- `delete_crop` - Elimina un cultivo

### Plots (Parcelas)
- `list_plots` - Lista todas las parcelas con relaciones
- `get_plot` - Obtiene una parcela por ID
- `create_plot` - Crea una nueva parcela
- `update_plot` - Actualiza una parcela
- `delete_plot` - Elimina una parcela

## 🔗 Testing con MCP Inspector

Para probar el servidor MCP localmente (sin Docker):

```bash
# Instalar inspector
npm install -g @modelcontextprotocol/inspector

# Ejecutar inspector con Docker
docker run --rm -i -v $(pwd)/data:/app/data agro-mcp | npx @modelcontextprotocol/inspector -
```

O directamente con Python:

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

## 📊 Estructura del Proyecto

```
server-mcp/
├── mcp_server.py        # MCP server implementation
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # CRUD operations
├── requirements.txt     # Dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yaml  # Docker Compose orchestration
├── .dockerignore        # Docker ignore patterns
├── .gitignore           # Git ignore patterns
└── README.md            # This file
```

## 🔄 Sincronización con server-api

El MCP server comparte la misma base de datos que el API REST:

- **Volumen compartido**: `../server-api/data:/app/data`
- **Base de datos**: `agro_api.db` en el directorio `data/`
- **Sincronización automática**: Cambios en la API se reflejan en MCP y viceversa

## 🎓 Propósito Educativo

Este proyecto demuestra:
- Implementación de servidores MCP con Python
- Comunicación STDIO para protocolos LLM
- Compartir volúmenes Docker entre servicios
- Arquitectura de microservicios (API REST + MCP Server)
- Integración de LLMs con bases de datos relacionales

## 📝 Notas Técnicas

- **STDIO**: El MCP server usa stdin/stdout para comunicación
- **Sin puertos**: No expone puertos HTTP como el API REST
- **Volumen compartido**: Accede a la misma BD que `server-api`
- **Protocolo MCP**: Sigue la especificación de Model Context Protocol
- **JSON-RPC**: Usa JSON-RPC 2.0 para mensajes

## 🐛 Troubleshooting

### El servidor no responde
```bash
# Verificar logs
docker-compose logs agro-mcp

# Verificar que la imagen se construyó correctamente
docker images | grep agro-mcp

# Reconstruir
docker-compose build --no-cache
```

### Base de datos no encontrada
```bash
# Verificar que server-api/data existe
ls -la ../server-api/data/

# Inicializar BD desde server-api
cd ../server-api
python seed_data.py
```

### Claude Desktop no detecta las herramientas
1. Verificar que la imagen está construida: `docker images`
2. Reiniciar Claude Desktop completamente
3. Verificar logs de Claude Desktop
4. Probar primero con MCP Inspector