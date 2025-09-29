# Docker Setup - Agro API + MCP Server

Guía completa para ejecutar el API REST y el MCP Server con Docker

## 📦 Arquitectura

Este proyecto incluye dos servicios dockerizados:

1. **agro-api** (`server-api/`): API REST con FastAPI
   - Puerto: `8000`
   - Endpoints HTTP para CRUD
   - Documentación Swagger: http://localhost:8000/docs

2. **agro-mcp** (`server-mcp/`): Servidor MCP
   - Sin puertos expuestos (usa STDIO)
   - 15 herramientas para LLMs
   - Comparte BD con agro-api

Ambos servicios comparten la misma base de datos SQLite en `server-api/data/agro_api.db`.

## 🚀 Inicio Rápido

### Levantar Ambos Servicios

```bash
# Desde la raíz del proyecto
docker-compose up -d

# Ver logs de ambos servicios
docker-compose logs -f

# Ver solo logs del API
docker-compose logs -f agro-api

# Ver solo logs del MCP
docker-compose logs -f agro-mcp
```

### Poblar la Base de Datos

```bash
# Ejecutar script de seed data
docker-compose exec agro-api python seed_data.py
```

### Verificar Servicios

```bash
# Estado de los contenedores
docker-compose ps

# Probar API REST
curl http://localhost:8000/
curl http://localhost:8000/farmers/

# Abrir Swagger UI
open http://localhost:8000/docs
```

## 🔧 Comandos Útiles

### Gestión de Servicios

```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (¡borra la BD!)
docker-compose down -v

# Reiniciar servicios
docker-compose restart

# Reconstruir imágenes
docker-compose build

# Reconstruir sin caché
docker-compose build --no-cache

# Levantar solo un servicio
docker-compose up -d agro-api
docker-compose up -d agro-mcp
```

### Logs y Debug

```bash
# Ver logs desde el inicio
docker-compose logs

# Seguir logs en tiempo real
docker-compose logs -f

# Últimas 100 líneas de logs
docker-compose logs --tail=100

# Logs de un servicio específico
docker-compose logs -f agro-api
docker-compose logs -f agro-mcp
```

### Acceso a Contenedores

```bash
# Ejecutar comandos en agro-api
docker-compose exec agro-api python seed_data.py
docker-compose exec agro-api python -c "import models; print('OK')"

# Shell interactivo
docker-compose exec agro-api bash
docker-compose exec agro-mcp bash

# Ver archivos de la base de datos
docker-compose exec agro-api ls -la /app/data/
```

## ⚙️ Configuración MCP en Claude Desktop

### Opción 1: Usando el Contenedor Docker

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
        "--network=utn-agro-ai_agro-network",
        "-v", "/home/kobo/projects/me/utn-agro-ai/server-api/data:/app/data",
        "utn-agro-ai-agro-mcp"
      ]
    }
  }
}
```

### Opción 2: Usando Python Directamente (Desarrollo)

```json
{
  "mcpServers": {
    "agro-api": {
      "command": "python",
      "args": ["/home/kobo/projects/me/utn-agro-ai/server-mcp/mcp_server.py"]
    }
  }
}
```

**Nota**: Reinicia Claude Desktop después de cambiar la configuración.

## 📊 Estructura de Volúmenes

```
server-api/data/        # Volumen compartido
└── agro_api.db         # Base de datos SQLite

Ambos contenedores montan este directorio:
- agro-api:  monta ./server-api/data -> /app/data
- agro-mcp:  monta ./server-api/data -> /app/data
```

## 🔄 Flujo de Trabajo

### 1. Desarrollo del API REST

```bash
# Levantar solo el API
docker-compose up -d agro-api

# Hacer cambios en server-api/
# Los cambios requieren rebuild

# Reconstruir y reiniciar
docker-compose build agro-api
docker-compose restart agro-api
```

### 2. Desarrollo del MCP Server

```bash
# Levantar ambos servicios
docker-compose up -d

# Configurar Claude Desktop (ver arriba)
# Reiniciar Claude Desktop

# Probar herramientas en Claude
# Ejemplo: "Lista todos los agricultores"
```

### 3. Testing y Debug

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ejecutar tests
docker-compose exec agro-api pytest

# Acceder a la BD directamente
docker-compose exec agro-api python
>>> from database import SessionLocal
>>> from crud import get_farmers
>>> db = SessionLocal()
>>> farmers = get_farmers(db)
>>> print(farmers)
```

## 🧪 Testing

### Test del API REST

```bash
# Health check
curl http://localhost:8000/

# Crear agricultor
curl -X POST "http://localhost:8000/farmers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Farmer",
    "email": "test@example.com",
    "region": "Test Region"
  }'

# Listar agricultores
curl http://localhost:8000/farmers/
```

### Test del MCP Server

```bash
# Con MCP Inspector (requiere Node.js)
npm install -g @modelcontextprotocol/inspector

# Ejecutar inspector conectado al contenedor
docker run --rm -i \
  -v $(pwd)/server-api/data:/app/data \
  utn-agro-ai-agro-mcp | npx @modelcontextprotocol/inspector -
```

## 🐛 Troubleshooting

### El contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs agro-api
docker-compose logs agro-mcp

# Verificar puertos ocupados
sudo netstat -tulpn | grep 8000

# Reconstruir desde cero
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Base de datos corrupta

```bash
# Backup
cp server-api/data/agro_api.db server-api/data/agro_api.db.backup

# Eliminar BD y recrear
rm server-api/data/agro_api.db
docker-compose restart
docker-compose exec agro-api python seed_data.py
```

### Claude Desktop no detecta las herramientas

1. Verificar que las imágenes están construidas:
   ```bash
   docker images | grep agro
   ```

2. Verificar la red Docker:
   ```bash
   docker network ls | grep agro
   ```

3. Probar manualmente el MCP server:
   ```bash
   docker run --rm -i \
     -v $(pwd)/server-api/data:/app/data \
     utn-agro-ai-agro-mcp
   ```

4. Reiniciar Claude Desktop completamente

### Problemas de permisos en data/

```bash
# Dar permisos al directorio
chmod -R 755 server-api/data/

# Si persiste, ejecutar como root
docker-compose exec -u root agro-api chown -R root:root /app/data
```

## 📝 Notas Importantes

- **Persistencia**: La BD se guarda en `server-api/data/` y persiste entre reinicios
- **Sincronización**: Cambios en el API se reflejan automáticamente en el MCP server
- **Network**: Ambos servicios están en la misma red Docker (`agro-network`)
- **Health Checks**: El API incluye health checks, el MCP espera a que el API esté healthy

## 🎓 Para la Clase

### Demostración 1: API REST
```bash
docker-compose up -d agro-api
# Abrir http://localhost:8000/docs
# Demostrar CRUD operations en Swagger
```

### Demostración 2: MCP Server
```bash
docker-compose up -d
# Configurar Claude Desktop
# Demostrar herramientas en Claude
# "Lista todos los agricultores"
# "Crea un nuevo cultivo de soja"
```

### Demostración 3: Sincronización
```bash
# Terminal 1: API REST
curl -X POST http://localhost:8000/farmers/ -d '...'

# Terminal 2: Claude Desktop
# "Lista los agricultores"
# El nuevo agricultor aparece inmediatamente
```