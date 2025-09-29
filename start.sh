#!/bin/bash
# Script para iniciar y gestionar los servicios Agro API + MCP

set -e

COLOR_RESET='\033[0m'
COLOR_GREEN='\033[0;32m'
COLOR_BLUE='\033[0;34m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'

echo -e "${COLOR_BLUE}"
echo "╔══════════════════════════════════════╗"
echo "║   Agro API + MCP Server Manager      ║"
echo "║   UTN Course - Docker Setup          ║"
echo "╚══════════════════════════════════════╝"
echo -e "${COLOR_RESET}"

function show_menu() {
    echo ""
    echo -e "${COLOR_GREEN}Opciones disponibles:${COLOR_RESET}"
    echo "  1) Iniciar servicios (API + MCP)"
    echo "  2) Detener servicios"
    echo "  3) Ver logs"
    echo "  4) Poblar base de datos"
    echo "  5) Estado de servicios"
    echo "  6) Reconstruir imágenes"
    echo "  7) Limpiar todo (incluye BD)"
    echo "  8) Abrir Swagger UI"
    echo "  9) Salir"
    echo ""
}

function start_services() {
    echo -e "${COLOR_YELLOW}⚡ Iniciando servicios...${COLOR_RESET}"
    docker-compose up -d
    echo -e "${COLOR_GREEN}✅ Servicios iniciados${COLOR_RESET}"
    echo ""
    echo "API REST disponible en: http://localhost:8000"
    echo "Swagger UI: http://localhost:8000/docs"
}

function stop_services() {
    echo -e "${COLOR_YELLOW}🛑 Deteniendo servicios...${COLOR_RESET}"
    docker-compose down
    echo -e "${COLOR_GREEN}✅ Servicios detenidos${COLOR_RESET}"
}

function show_logs() {
    echo -e "${COLOR_YELLOW}📋 Mostrando logs (Ctrl+C para salir)...${COLOR_RESET}"
    docker-compose logs -f
}

function seed_database() {
    echo -e "${COLOR_YELLOW}🌱 Poblando base de datos...${COLOR_RESET}"
    docker-compose exec agro-api python seed_data.py
    echo -e "${COLOR_GREEN}✅ Base de datos poblada${COLOR_RESET}"
}

function show_status() {
    echo -e "${COLOR_YELLOW}📊 Estado de servicios:${COLOR_RESET}"
    docker-compose ps
}

function rebuild_images() {
    echo -e "${COLOR_YELLOW}🔨 Reconstruyendo imágenes...${COLOR_RESET}"
    docker-compose build --no-cache
    echo -e "${COLOR_GREEN}✅ Imágenes reconstruidas${COLOR_RESET}"
}

function clean_all() {
    echo -e "${COLOR_RED}⚠️  ADVERTENCIA: Esto eliminará todos los datos${COLOR_RESET}"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${COLOR_YELLOW}🗑️  Limpiando todo...${COLOR_RESET}"
        docker-compose down -v
        rm -rf server-api/data/
        echo -e "${COLOR_GREEN}✅ Todo limpio${COLOR_RESET}"
    else
        echo -e "${COLOR_BLUE}Operación cancelada${COLOR_RESET}"
    fi
}

function open_swagger() {
    echo -e "${COLOR_YELLOW}🌐 Abriendo Swagger UI...${COLOR_RESET}"
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8000/docs
    elif command -v open &> /dev/null; then
        open http://localhost:8000/docs
    else
        echo "Abrir manualmente: http://localhost:8000/docs"
    fi
}

# Menú principal
while true; do
    show_menu
    read -p "Selecciona una opción [1-9]: " option

    case $option in
        1) start_services ;;
        2) stop_services ;;
        3) show_logs ;;
        4) seed_database ;;
        5) show_status ;;
        6) rebuild_images ;;
        7) clean_all ;;
        8) open_swagger ;;
        9)
            echo -e "${COLOR_BLUE}👋 ¡Hasta luego!${COLOR_RESET}"
            exit 0
            ;;
        *)
            echo -e "${COLOR_RED}❌ Opción inválida${COLOR_RESET}"
            ;;
    esac
done