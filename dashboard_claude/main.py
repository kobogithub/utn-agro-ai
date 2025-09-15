import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Commodities Agrícolas",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🌾 Dashboard de Análisis de Commodities Agrícolas")
st.markdown("Análisis de tendencias históricas de precios de commodities utilizando Yahoo Finance")

# Sidebar para configuración
st.sidebar.header("⚙️ Configuración")

# Definición de commodities agrícolas predefinidos
DEFAULT_COMMODITIES = {
    'Soja': 'ZS=F',      # Soybean Futures - CBOT
    'Maíz': 'ZC=F',     # Corn Futures - CBOT
    'Trigo': 'ZW=F',    # Wheat Futures - CBOT
    'Algodón': 'CT=F',  # Cotton Futures
    'Azúcar': 'SB=F',   # Sugar Futures
    'Café': 'KC=F',     # Coffee Futures
    'Cacao': 'CC=F',    # Cocoa Futures
    'Arroz': 'ZR=F',    # Rice Futures
    'Avena': 'ZO=F',    # Oats Futures
    'Aceite de Soja': 'ZL=F'  # Soybean Oil Futures
}

# Selector de período de análisis
st.sidebar.subheader("📅 Período de Análisis")
periodo_options = {
    "1 mes": "1mo",
    "3 meses": "3mo",
    "6 meses": "6mo",
    "1 año": "1y",
    "2 años": "2y",
    "5 años": "5y",
    "10 años": "10y",
    "Máximo": "max"
}

periodo_seleccionado = st.sidebar.selectbox(
    "Selecciona el período:",
    options=list(periodo_options.keys()),
    index=3  # Por defecto 1 año
)

# Selector de commodities
st.sidebar.subheader("🌾 Selección de Commodities")

# Opción para usar commodities predefinidos o personalizados
modo_seleccion = st.sidebar.radio(
    "Modo de selección:",
    ["Commodities Predefinidos", "Códigos Personalizados"]
)

commodities_seleccionados = {}

if modo_seleccion == "Commodities Predefinidos":
    # Multiselect para commodities predefinidos
    nombres_seleccionados = st.sidebar.multiselect(
        "Selecciona commodities:",
        options=list(DEFAULT_COMMODITIES.keys()),
        default=["Soja", "Maíz", "Trigo"]
    )

    commodities_seleccionados = {
        nombre: DEFAULT_COMMODITIES[nombre]
        for nombre in nombres_seleccionados
    }

else:
    # Entrada manual de códigos
    st.sidebar.markdown("**Ingresa códigos de Yahoo Finance (uno por línea):**")
    st.sidebar.markdown("Formato: Nombre,Código (ej: Soja,ZS=F)")

    codigos_input = st.sidebar.text_area(
        "Códigos personalizados:",
        value="Soja,ZS=F\nMaíz,ZC=F\nTrigo,ZW=F",
        height=100
    )

    # Procesar códigos ingresados
    if codigos_input.strip():
        for linea in codigos_input.strip().split('\n'):
            if ',' in linea:
                nombre, codigo = linea.split(',', 1)
                commodities_seleccionados[nombre.strip()] = codigo.strip()

# Función para obtener datos históricos
@st.cache_data(ttl=3600)  # Cache por 1 hora
def obtener_datos_historicos(simbolo, periodo):
    """
    Obtiene datos históricos de Yahoo Finance para un símbolo específico
    """
    try:
        ticker = yf.Ticker(simbolo)
        hist = ticker.history(period=periodo)

        if hist.empty:
            return None

        # Devolver solo precios de cierre
        return hist['Close']
    except Exception as e:
        st.error(f"Error obteniendo datos para {simbolo}: {str(e)}")
        return None

# Función para calcular estadísticas
def calcular_estadisticas(datos):
    """
    Calcula estadísticas básicas de los datos
    """
    if datos is None or datos.empty:
        return None

    return {
        'precio_actual': datos.iloc[-1],
        'precio_inicial': datos.iloc[0],
        'variacion_total': ((datos.iloc[-1] / datos.iloc[0]) - 1) * 100,
        'precio_maximo': datos.max(),
        'precio_minimo': datos.min(),
        'precio_promedio': datos.mean(),
        'volatilidad': datos.pct_change().std() * 100
    }

# Función principal de análisis
def ejecutar_analisis():
    """
    Ejecuta el análisis de tendencias para los commodities seleccionados
    """
    if not commodities_seleccionados:
        st.warning("⚠️ Por favor selecciona al menos un commodity para analizar.")
        return

    periodo = periodo_options[periodo_seleccionado]

    # Contenedor para mostrar progreso
    progress_bar = st.progress(0)
    status_text = st.empty()

    datos_historicos = {}
    estadisticas = {}

    # Obtener datos para cada commodity
    total_commodities = len(commodities_seleccionados)

    for i, (nombre, simbolo) in enumerate(commodities_seleccionados.items()):
        status_text.text(f"Obteniendo datos para {nombre} ({simbolo})...")
        progress_bar.progress((i + 1) / total_commodities)

        datos = obtener_datos_historicos(simbolo, periodo)

        if datos is not None and not datos.empty:
            datos_historicos[nombre] = datos
            estadisticas[nombre] = calcular_estadisticas(datos)

    # Limpiar indicadores de progreso
    progress_bar.empty()
    status_text.empty()

    if not datos_historicos:
        st.error("❌ No se pudieron obtener datos para ningún commodity seleccionado.")
        return

    # Mostrar resultados
    mostrar_resultados(datos_historicos, estadisticas, periodo_seleccionado)

def mostrar_resultados(datos_historicos, estadisticas, periodo):
    """
    Muestra los resultados del análisis
    """
    st.success(f"✅ Datos obtenidos exitosamente para {len(datos_historicos)} commodities")

    # Tabs para organizar la información
    tab1, tab2, tab3 = st.tabs(["📊 Gráficos de Tendencias", "📈 Estadísticas", "📋 Datos Detallados"])

    with tab1:
        mostrar_graficos(datos_historicos)

    with tab2:
        mostrar_estadisticas(estadisticas)

    with tab3:
        mostrar_datos_detallados(datos_historicos)

def mostrar_graficos(datos_historicos):
    """
    Muestra gráficos interactivos de las tendencias
    """
    st.subheader("📊 Tendencias Históricas de Precios")

    # Gráfico combinado con Plotly
    fig = go.Figure()

    colores = px.colors.qualitative.Set1[:len(datos_historicos)]

    for i, (nombre, datos) in enumerate(datos_historicos.items()):
        fig.add_trace(go.Scatter(
            x=datos.index,
            y=datos.values,
            mode='lines',
            name=nombre,
            line=dict(color=colores[i], width=2),
            hovertemplate=f'<b>{nombre}</b><br>' +
                         'Fecha: %{x}<br>' +
                         'Precio: $%{y:.2f}<br>' +
                         '<extra></extra>'
        ))

    fig.update_layout(
        title="Evolución de Precios de Commodities Agrícolas",
        xaxis_title="Fecha",
        yaxis_title="Precio (USD)",
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Gráficos individuales en grid
    if len(datos_historicos) > 1:
        st.subheader("📈 Análisis Individual por Commodity")

        cols = st.columns(2)

        for i, (nombre, datos) in enumerate(datos_historicos.items()):
            with cols[i % 2]:
                fig_individual = go.Figure()

                fig_individual.add_trace(go.Scatter(
                    x=datos.index,
                    y=datos.values,
                    mode='lines',
                    name=nombre,
                    line=dict(color=colores[i], width=3),
                    fill='tonexty' if i == 0 else None,
                    fillcolor=f'rgba({colores[i][4:-1]}, 0.1)'
                ))

                fig_individual.update_layout(
                    title=f"Tendencia de {nombre}",
                    xaxis_title="Fecha",
                    yaxis_title="Precio (USD)",
                    height=400,
                    showlegend=False
                )

                st.plotly_chart(fig_individual, use_container_width=True)

def mostrar_estadisticas(estadisticas):
    """
    Muestra estadísticas calculadas
    """
    st.subheader("📈 Estadísticas de Mercado")

    # Crear métricas en columnas
    num_cols = min(len(estadisticas), 3)
    cols = st.columns(num_cols)

    for i, (nombre, stats) in enumerate(estadisticas.items()):
        with cols[i % num_cols]:
            st.metric(
                label=f"💰 {nombre}",
                value=f"${stats['precio_actual']:.2f}",
                delta=f"{stats['variacion_total']:.2f}%"
            )

    # Tabla detallada de estadísticas
    st.subheader("📊 Resumen Estadístico Detallado")

    df_stats = pd.DataFrame(estadisticas).T
    df_stats.columns = [
        'Precio Actual',
        'Precio Inicial',
        'Variación Total (%)',
        'Precio Máximo',
        'Precio Mínimo',
        'Precio Promedio',
        'Volatilidad (%)'
    ]

    # Formatear valores para mejor visualización
    df_display = df_stats.copy()
    for col in ['Precio Actual', 'Precio Inicial', 'Precio Máximo', 'Precio Mínimo', 'Precio Promedio']:
        df_display[col] = df_display[col].apply(lambda x: f"${x:.2f}")

    for col in ['Variación Total (%)', 'Volatilidad (%)']:
        df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}%")

    st.dataframe(df_display, use_container_width=True)

def mostrar_datos_detallados(datos_historicos):
    """
    Muestra datos históricos en formato tabular
    """
    st.subheader("📋 Datos Históricos Detallados")

    # Combinar todos los datos en un DataFrame
    df_combinado = pd.DataFrame(datos_historicos)

    # Mostrar información del dataset
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📅 Registros Totales", len(df_combinado))
    with col2:
        st.metric("🌾 Commodities", len(df_combinado.columns))
    with col3:
        st.metric("📊 Período", f"{df_combinado.index[0].strftime('%Y-%m-%d')} a {df_combinado.index[-1].strftime('%Y-%m-%d')}")

    # Tabla interactiva
    st.dataframe(
        df_combinado.round(2),
        use_container_width=True,
        height=400
    )

    # Opción para descargar datos
    csv = df_combinado.to_csv()
    st.download_button(
        label="📥 Descargar datos como CSV",
        data=csv,
        file_name=f"commodities_historicos_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Sección principal
st.markdown("---")

if st.button("🚀 Ejecutar Análisis", type="primary", use_container_width=True):
    ejecutar_analisis()

# Información adicional en el sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Información")
st.sidebar.markdown("""
**Códigos de Commodities Comunes:**
- ZS=F: Soja
- ZC=F: Maíz
- ZW=F: Trigo
- CT=F: Algodón
- SB=F: Azúcar
- KC=F: Café
- CC=F: Cacao

**Fuente de Datos:** Yahoo Finance
""")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🌾 Dashboard de Commodities Agrícolas | Desarrollado con Streamlit | Datos de Yahoo Finance</p>
    </div>
    """,
    unsafe_allow_html=True
)