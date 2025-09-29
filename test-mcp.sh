#!/bin/bash
# Script para probar el servidor MCP

set -e

COLOR_RESET='\033[0m'
COLOR_GREEN='\033[0;32m'
COLOR_BLUE='\033[0;34m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'

echo -e "${COLOR_BLUE}"
echo "╔══════════════════════════════════════╗"
echo "║     Agro MCP Server - Test Tool      ║"
echo "╚══════════════════════════════════════╝"
echo -e "${COLOR_RESET}"
echo ""

# Verificar que la imagen existe
echo -e "${COLOR_YELLOW}🔍 Verificando imagen Docker...${COLOR_RESET}"
if docker images | grep -q "agro-mcp"; then
    echo -e "${COLOR_GREEN}✅ Imagen agro-mcp encontrada${COLOR_RESET}"
else
    echo -e "${COLOR_RED}❌ Imagen agro-mcp no encontrada${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}Construyendo imagen...${COLOR_RESET}"
    docker build -t agro-mcp:latest -f server-mcp/Dockerfile server-mcp/
    echo -e "${COLOR_GREEN}✅ Imagen construida${COLOR_RESET}"
fi

# Verificar base de datos
echo ""
echo -e "${COLOR_YELLOW}🔍 Verificando base de datos...${COLOR_RESET}"
if [ -f "server-api/data/agro_api.db" ]; then
    echo -e "${COLOR_GREEN}✅ Base de datos encontrada${COLOR_RESET}"
else
    echo -e "${COLOR_RED}❌ Base de datos no encontrada${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}Necesitas crear la base de datos primero:${COLOR_RESET}"
    echo "  docker-compose up -d agro-api"
    echo "  docker-compose exec agro-api python seed_data.py"
    exit 1
fi

# Probar el servidor MCP
echo ""
echo -e "${COLOR_YELLOW}🧪 Probando servidor MCP...${COLOR_RESET}"
echo -e "${COLOR_BLUE}Enviando comando: tools/list${COLOR_RESET}"
echo ""

# Crear request JSON-RPC
REQUEST='{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Ejecutar y capturar respuesta
RESPONSE=$(echo "$REQUEST" | docker run --rm -i \
  -v "$(pwd)/server-api/data:/app/data" \
  agro-mcp:latest 2>&1 | head -20)

# Verificar respuesta
if echo "$RESPONSE" | grep -q "list_farmers"; then
    echo -e "${COLOR_GREEN}✅ Servidor MCP funcionando correctamente${COLOR_RESET}"
    echo ""
    echo -e "${COLOR_BLUE}Herramientas detectadas:${COLOR_RESET}"
    echo "$RESPONSE" | grep -o '"name":"[^"]*"' | sed 's/"name":"//;s/"$//' | head -15 | nl
else
    echo -e "${COLOR_RED}❌ Error al comunicarse con el servidor${COLOR_RESET}"
    echo ""
    echo -e "${COLOR_YELLOW}Respuesta del servidor:${COLOR_RESET}"
    echo "$RESPONSE"
    exit 1
fi

echo ""
echo -e "${COLOR_GREEN}╔══════════════════════════════════════╗${COLOR_RESET}"
echo -e "${COLOR_GREEN}║       ✅ Test completado exitosamente ║${COLOR_RESET}"
echo -e "${COLOR_GREEN}╚══════════════════════════════════════╝${COLOR_RESET}"
echo ""
echo -e "${COLOR_YELLOW}📝 Siguiente paso:${COLOR_RESET}"
echo "   Configurar Claude Desktop con:"
echo ""
echo -e "${COLOR_BLUE}   ~/.config/Claude/claude_desktop_config.json${COLOR_RESET}"
echo ""
echo "   Ver: MCP_SETUP.md para instrucciones completas"
echo ""