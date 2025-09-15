import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Análisis de Commodities",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Dashboard de Análisis de Tendencias Históricas de Commodities")
st.markdown("Análisis de tendencias basado en datos de Yahoo Finance")

# Función para obtener datos históricos
def obtener_datos_historicos(simbolo, periodo='6mo', intervalo='1d'):
    """
    Obtiene datos históricos de un commodity desde Yahoo Finance
    """
    try:
        ticker = yf.Ticker(simbolo)
        datos = ticker.history(period=periodo, interval=intervalo)
        return datos
    except Exception as e:
        st.error(f"Error obteniendo datos para {simbolo}: {str(e)}")
        return None

# Función para graficar tendencias
def graficar_tendencias(datos_dict, simbolos):
    """
    Crea gráfico de tendencias históricas para múltiples commodities
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    colores = ['blue', 'green', 'red', 'orange', 'purple', 'brown']

    for i, simbolo in enumerate(simbolos):
        if simbolo in datos_dict and datos_dict[simbolo] is not None:
            datos = datos_dict[simbolo]
            if not datos.empty:
                color = colores[i % len(colores)]
                ax.plot(datos.index, datos['Close'],
                       label=simbolo, color=color, linewidth=2)

    ax.set_title('Tendencias Históricas de Commodities', fontsize=14, fontweight='bold')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio (USD)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Rotar etiquetas de fecha
    plt.xticks(rotation=45)

    return fig

# Sidebar para configuración
st.sidebar.header("⚙️ Configuración")

# Input para códigos de commodities
commodities_input = st.sidebar.text_input(
    "Códigos de Commodities (separados por coma)",
    value=os.getenv('DEFAULT_COMMODITIES', 'ZS=F,ZC=F,ZW=F'),
    help="Ejemplos: ZS=F (Soja), ZC=F (Maíz), ZW=F (Trigo), USDARS=X (Dólar)"
)

# Selector de período
periodo = st.sidebar.selectbox(
    "Período de análisis",
    options=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
    index=2,  # 6mo por defecto
    help="Período para el análisis histórico"
)

# Selector de intervalo
intervalo = st.sidebar.selectbox(
    "Intervalo de datos",
    options=['1d', '5d', '1wk', '1mo'],
    index=0,  # 1d por defecto
    help="Frecuencia de los datos históricos"
)

# Botón para actualizar datos
if st.sidebar.button("🔄 Actualizar Datos", type="primary"):
    st.rerun()

# Procesar códigos de commodities
simbolos = [s.strip() for s in commodities_input.split(',') if s.strip()]

# Obtener datos históricos
if simbolos:
    st.header("📈 Análisis de Tendencias Históricas")

    # Mostrar códigos seleccionados
    st.subheader("Commodities seleccionados:")
    cols = st.columns(len(simbolos))
    for i, simbolo in enumerate(simbolos):
        with cols[i]:
            st.code(simbolo)

    # Obtener datos
    with st.spinner("Obteniendo datos históricos..."):
        datos_historicos = {}
        for simbolo in simbolos:
            datos = obtener_datos_historicos(simbolo, periodo, intervalo)
            datos_historicos[simbolo] = datos

    # Verificar si hay datos válidos
    datos_validos = [s for s in simbolos if datos_historicos.get(s) is not None and not datos_historicos[s].empty]

    if datos_validos:
        # Crear gráfico
        fig = graficar_tendencias(datos_historicos, datos_validos)
        st.pyplot(fig)

        # Mostrar estadísticas
        st.header("📊 Estadísticas de los Commodities")

        col1, col2, col3 = st.columns(3)

        for i, simbolo in enumerate(datos_validos):
            datos = datos_historicos[simbolo]

            # Calcular estadísticas
            precio_actual = datos['Close'].iloc[-1]
            precio_max = datos['Close'].max()
            precio_min = datos['Close'].min()
            precio_promedio = datos['Close'].mean()
            variacion = ((precio_actual - datos['Close'].iloc[0]) / datos['Close'].iloc[0]) * 100

            # Mostrar en columnas
            if i % 3 == 0:
                col = col1
            elif i % 3 == 1:
                col = col2
            else:
                col = col3

            with col:
                st.subheader(f"📈 {simbolo}")
                st.metric("Precio Actual", f"${precio_actual:.2f}")
                st.metric("Variación Período", f"{variacion:+.2f}%")
                st.metric("Precio Máximo", f"${precio_max:.2f}")
                st.metric("Precio Mínimo", f"${precio_min:.2f}")
                st.metric("Precio Promedio", f"${precio_promedio:.2f}")

        # Tabla de datos detallados
        st.header("📋 Datos Detallados")

        # Crear tabs para cada commodity
        tabs = st.tabs(datos_validos)

        for i, simbolo in enumerate(datos_validos):
            with tabs[i]:
                datos = datos_historicos[simbolo]
                # Mostrar últimas 10 filas
                st.dataframe(
                    datos.tail(10)[['Open', 'High', 'Low', 'Close', 'Volume']],
                    use_container_width=True
                )

                # Descargar datos
                csv = datos.to_csv().encode('utf-8')
                st.download_button(
                    label=f"📥 Descargar datos de {simbolo}",
                    data=csv,
                    file_name=f'{simbolo}_{periodo}.csv',
                    mime='text/csv'
                )

    else:
        st.warning("No se pudieron obtener datos para ninguno de los códigos de commodities especificados.")
        st.info("Verifique que los códigos sean válidos (ej: ZS=F para Soja, ZC=F para Maíz)")

else:
    st.info("Ingrese los códigos de commodities en la barra lateral para comenzar el análisis.")

# Información adicional
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ Información")

st.sidebar.markdown("""
**Códigos de Commodities comunes:**
- **ZS=F**: Soja (Soybean Futures)
- **ZC=F**: Maíz (Corn Futures)
- **ZW=F**: Trigo (Wheat Futures)
- **CL=F**: Petróleo (Crude Oil)
- **GC=F**: Oro (Gold Futures)
- **USDARS=X**: Dólar vs Peso Argentino

**Fuentes de datos:**
- Yahoo Finance API
- Datos en tiempo real
""")

# Footer
st.markdown("---")
st.markdown("Dashboard creado con Streamlit | Datos proporcionados por Yahoo Finance")
st.markdown(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")