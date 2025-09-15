# Dashboard de Commodities Agrícolas 🌾

Dashboard interactivo desarrollado con Streamlit para el análisis de tendencias históricas de precios de commodities agrícolas utilizando datos de Yahoo Finance.

## Características

- 📊 **Análisis de Tendencias**: Visualización interactiva de precios históricos
- 🌾 **Commodities Predefinidos**: Soja, Maíz, Trigo, Algodón, Azúcar, Café, etc.
- ⚙️ **Códigos Personalizados**: Posibilidad de agregar cualquier símbolo de Yahoo Finance
- 📈 **Múltiples Períodos**: Desde 1 mes hasta datos históricos máximos
- 📊 **Estadísticas Avanzadas**: Métricas de precio, volatilidad y variaciones
- 💾 **Exportación de Datos**: Descarga de datos en formato CSV

## Instalación

### 1. Clonar y navegar al directorio
```bash
cd dashboard_claude
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno (opcional)
```bash
cp .env.example .env
# Editar .env con tus configuraciones personalizadas
```

### 4. Ejecutar la aplicación
```bash
streamlit run main.py
```

## Uso

### Commodities Predefinidos
La aplicación incluye los siguientes commodities agrícolas:

| Commodity | Símbolo | Mercado |
|-----------|---------|---------|
| Soja | ZS=F | CBOT |
| Maíz | ZC=F | CBOT |
| Trigo | ZW=F | CBOT |
| Algodón | CT=F | ICE |
| Azúcar | SB=F | ICE |
| Café | KC=F | ICE |
| Cacao | CC=F | ICE |
| Arroz | ZR=F | CBOT |
| Avena | ZO=F | CBOT |
| Aceite de Soja | ZL=F | CBOT |

### Códigos Personalizados
También puedes agregar cualquier símbolo disponible en Yahoo Finance:

**Formato**: `Nombre,Símbolo`

**Ejemplos**:
- `Petróleo Crudo,CL=F`
- `Oro,GC=F`
- `Plata,SI=F`
- `Gas Natural,NG=F`

### Períodos de Análisis
- 1 mes, 3 meses, 6 meses
- 1 año, 2 años, 5 años, 10 años
- Máximo (todos los datos disponibles)

## Funcionalidades

### 📊 Gráficos de Tendencias
- Gráfico combinado interactivo con Plotly
- Gráficos individuales por commodity
- Visualización con relleno y colores distintivos

### 📈 Estadísticas
- Precio actual y variación total
- Precios máximo, mínimo y promedio
- Cálculo de volatilidad
- Métricas en tiempo real

### 📋 Datos Detallados
- Tabla completa de datos históricos
- Información del dataset (registros, período)
- Exportación a CSV con timestamp

## Estructura del Proyecto

```
dashboard_claude/
├── main.py              # Aplicación principal de Streamlit
├── requirements.txt     # Dependencias de Python
├── .env.example        # Plantilla de variables de entorno
└── README.md           # Este archivo
```

## Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web
- **yfinance**: API para datos financieros de Yahoo Finance
- **Plotly**: Gráficos interactivos
- **Pandas**: Manipulación de datos
- **Matplotlib/Seaborn**: Visualizaciones adicionales

## Configuración Avanzada

### Variables de Entorno

```env
# Configuración de timeout para yfinance
YFINANCE_TIMEOUT=30
YFINANCE_MAX_RETRIES=3

# Configuración de caché (minutos)
CACHE_TTL=60

# Zona horaria
TIMEZONE=America/Argentina/Buenos_Aires
```

### Cache de Datos

La aplicación utiliza `@st.cache_data` para optimizar las consultas a Yahoo Finance:
- TTL por defecto: 1 hora (3600 segundos)
- Configurable mediante variable de entorno `CACHE_TTL`

## Troubleshooting

### Error: "No se pudieron obtener datos"
- Verificar que el símbolo sea válido en Yahoo Finance
- Comprobar conexión a internet
- Algunos símbolos pueden no tener datos para períodos muy largos

### Error: "Timeout"
- Aumentar el valor de `YFINANCE_TIMEOUT` en .env
- Verificar estabilidad de la conexión

### Rendimiento lento
- Reducir el número de commodities seleccionados
- Usar períodos más cortos para el análisis inicial
- Limpiar caché de Streamlit: `streamlit cache clear`

## Desarrollo

### Agregar nuevos commodities predefinidos
Editar el diccionario `DEFAULT_COMMODITIES` en `main.py`:

```python
DEFAULT_COMMODITIES = {
    'Nuevo Commodity': 'SIMBOLO=F',
    # ... resto de commodities
}
```

### Personalizar gráficos
Los gráficos utilizan Plotly. Puedes modificar las funciones:
- `mostrar_graficos()`: Gráficos principales
- `mostrar_estadisticas()`: Métricas y tablas

## Basado en

Este dashboard está basado en el notebook `04-Automatizacion-Web-Scraping.ipynb` del módulo 3 del curso de LLMs aplicados a la agricultura de la UTN.

## Licencia

Proyecto educativo para la Universidad Tecnológica Nacional (UTN).