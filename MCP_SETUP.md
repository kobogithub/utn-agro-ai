# Configuración MCP Server con Claude Desktop

Guía rápida para usar el servidor MCP dockerizado con Claude Desktop

## ✅ Paso 1: Construir la Imagen

```bash
# Desde la raíz del proyecto
docker build -t agro-mcp:latest -f server-mcp/Dockerfile server-mcp/

# Verificar que se creó
docker images | grep agro-mcp
```

## ✅ Paso 2: Preparar la Base de Datos

```bash
# Asegúrate de que existe el directorio data
mkdir -p server-api/data

# Opción A: Crear BD con el API REST
docker-compose up -d agro-api
docker-compose exec agro-api python seed_data.py
docker-compose down

# Opción B: Ejecutar localmente (requiere Python + deps)
cd server-api
python main.py &
python seed_data.py
kill %1
```

## ✅ Paso 3: Configurar Claude Desktop

### Linux
Edita: `~/.config/Claude/claude_desktop_config.json`

### macOS
Edita: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
Edita: `%APPDATA%\Claude\claude_desktop_config.json`

### Contenido del archivo:

```json
{
  "mcpServers": {
    "agro-api": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "/home/kobo/projects/me/utn-agro-ai/server-api/data:/app/data",
        "agro-mcp:latest"
      ]
    }
  }
}
```

**IMPORTANTE**: Cambia la ruta absoluta `/home/kobo/projects/me/utn-agro-ai/` por tu ruta real.

## ✅ Paso 4: Reiniciar Claude Desktop

1. Cierra Claude Desktop completamente
2. Vuelve a abrir Claude Desktop
3. Verifica que aparezcan las herramientas MCP en la interfaz

## 🧪 Paso 5: Probar

En Claude Desktop, prueba comandos como:

```
Lista todos los agricultores
```

```
Crea un agricultor llamado Pedro con email pedro@test.com en la región Pampa Húmeda
```

```
Muéstrame todas las parcelas con sus cultivos
```

## 🔍 Verificación Manual

### Probar el contenedor directamente:

```bash
# Test interactivo (Ctrl+D para salir)
docker run --rm -i \
  -v /home/kobo/projects/me/utn-agro-ai/server-api/data:/app/data \
  agro-mcp:latest
```

### Con MCP Inspector:

```bash
# Instalar inspector (una vez)
npm install -g @modelcontextprotocol/inspector

# Ejecutar inspector
docker run --rm -i \
  -v $(pwd)/server-api/data:/app/data \
  agro-mcp:latest | npx @modelcontextprotocol/inspector -
```

Esto abrirá una interfaz web donde puedes probar las 15 herramientas MCP visualmente.

## 📋 Herramientas Disponibles

Una vez configurado, Claude tendrá acceso a:

### Farmers (Agricultores)
- `list_farmers` - Listar todos
- `get_farmer` - Obtener por ID
- `create_farmer` - Crear nuevo
- `update_farmer` - Actualizar
- `delete_farmer` - Eliminar

### Crops (Cultivos)
- `list_crops` - Listar todos
- `get_crop` - Obtener por ID
- `create_crop` - Crear nuevo
- `update_crop` - Actualizar
- `delete_crop` - Eliminar

### Plots (Parcelas)
- `list_plots` - Listar todas
- `get_plot` - Obtener por ID
- `create_plot` - Crear nueva
- `update_plot` - Actualizar
- `delete_plot` - Eliminar

## 🐛 Troubleshooting

### Claude no detecta las herramientas

1. **Verificar imagen:**
   ```bash
   docker images | grep agro-mcp
   ```

2. **Verificar configuración:**
   - Archivo existe en la ubicación correcta
   - Ruta absoluta correcta en el volumen
   - JSON válido (sin trailing commas)

3. **Verificar base de datos:**
   ```bash
   ls -la server-api/data/
   # Debe existir agro_api.db
   ```

4. **Logs de Claude Desktop:**
   - **Linux**: `~/.config/Claude/logs/`
   - **macOS**: `~/Library/Logs/Claude/`
   - **Windows**: `%APPDATA%\Claude\logs\`

### Error "database locked"

```bash
# Detener procesos que usen la BD
docker-compose down
lsof server-api/data/agro_api.db
```

### Permisos

```bash
# Dar permisos al directorio data
chmod -R 755 server-api/data/
```

## 🔄 Actualizar la Imagen

Si haces cambios al código del MCP server:

```bash
# Reconstruir imagen
docker build -t agro-mcp:latest -f server-mcp/Dockerfile server-mcp/

# NO necesitas reiniciar Claude Desktop
# Claude creará un nuevo contenedor en cada invocación
```

## 💡 Consejos

1. **Base de datos compartida**: El MCP server y el API REST pueden compartir la misma BD
2. **Sin red Docker necesaria**: Con `docker run --rm` no necesitas la red bridge
3. **Stateless**: Cada invocación de Claude crea un contenedor nuevo y lo destruye al terminar
4. **Performance**: El contenedor inicia en ~1-2 segundos

## 📚 Comandos Útiles

```bash
# Ver configuración actual de Claude
cat ~/.config/Claude/claude_desktop_config.json

# Copiar configuración de ejemplo
cp claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json

# Editar configuración
nano ~/.config/Claude/claude_desktop_config.json

# Verificar que Docker funciona
docker run --rm hello-world

# Probar el MCP manualmente
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  docker run --rm -i \
  -v $(pwd)/server-api/data:/app/data \
  agro-mcp:latest
```

## ✨ Alternativa: Docker Compose

Si prefieres usar docker-compose en lugar de docker run:

```json
{
  "mcpServers": {
    "agro-api": {
      "command": "docker",
      "args": [
        "compose",
        "-f",
        "/home/kobo/projects/me/utn-agro-ai/server-mcp/docker-compose.yaml",
        "run",
        "--rm",
        "agro-mcp"
      ]
    }
  }
}
```

Pero `docker run --rm -i` es más simple y directo.