import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE PÁGINA (Esto le da el título a la pestaña del navegador)
st.set_page_config(
    page_title="Titanic App de Cris",
    page_icon="🚢",
    layout="wide"
)

# Carga el archivo CSV
df = pd.read_csv("database_titanic.csv")

# Título principal
st.write("""
# 🚢 La mejor app interactiva ¡Hecha por Cris!
## Análisis visual del Titanic
""")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Slider de Bins (Lo que ya tenías)
    div = st.slider('Número de bins:', 0, 20, 10)    
    st.write("---")
    
    # NUEVO: Filtro por Clase
    st.write("Filtrar por Clase de Pasajero:")
    opcion_clase = st.multiselect(
        "Selecciona las clases:",
        options=[1, 2, 3],
        default=[1, 2, 3] # Por defecto todas seleccionadas
    )
    
    st.write("---")
    # Botón divertido
    if st.button("¡Presiona aquí!"):
        st.balloons()

# Filtrar el DataFrame según la selección del usuario
df_filtrado = df[df["Pclass"].isin(opcion_clase)]

# --- LAYOUT DE MÉTRICAS (KPIs) ---
# Usamos columnas para mostrar números grandes
col1, col2, col3 = st.columns(3)
total_pasajeros = len(df_filtrado)
total_sobrevivientes = len(df_filtrado[df_filtrado["Survived"] == 1])
# Calcular porcentaje evitando división por cero
pct_supervivencia = (total_sobrevivientes / total_pasajeros * 100) if total_pasajeros > 0 else 0

col1.metric("Total Pasajeros", total_pasajeros)
col2.metric("Sobrevivientes", total_sobrevivientes)
col3.metric("Tasa de Supervivencia", f"{pct_supervivencia:.1f}%")
# Slider para controlar la frecuencia
frecuencia = st.slider('Frecuencia', min_value=0.1, max_value=5.0, value=1.0, step=0.1)
st.write("---")

# --- PESTAÑAS PARA LOS GRÁFICOS (TABS) ---
# Esto organiza mucho mejor tu visualización
tab1, tab2, tab3 = st.tabs(["🎂 Edades", "👫 Distribución por Sexo", "🟢 Sobrevivientes"])

with tab1:
    st.header("Histograma de Edades")
    # Creamos figura solo para este gráfico
    fig1, ax1 = plt.subplots()
    ax1.hist(df_filtrado["Age"], bins=div, color="skyblue", edgecolor="black")
    ax1.set_xlabel("Edad")
    ax1.set_ylabel("Frecuencia")
    st.pyplot(fig1)

with tab2:
    st.header("Total Hombres y Mujeres")
    # Cálculo dinámico basado en el filtro
    cant_male = len(df_filtrado[df_filtrado["Sex"] == "male"])
    cant_female = len(df_filtrado[df_filtrado["Sex"] == "female"])
    
    fig2, ax2 = plt.subplots()
    ax2.bar(["Masculino", "Femenino"], [cant_male, cant_female], color="red")
    ax2.set_ylabel("Cantidad")
    st.pyplot(fig2)

with tab3:
    st.header("¿Quiénes sobrevivieron más?")
    # Lógica para sobrevivientes
    sob_male = len(df_filtrado[(df_filtrado["Sex"] == "male") & (df_filtrado["Survived"] == 1)])
    sob_female = len(df_filtrado[(df_filtrado["Sex"] == "female") & (df_filtrado["Survived"] == 1)])
    
    fig3, ax3 = plt.subplots()
    ax3.bar(["Masculino", "Femenino"], [sob_male, sob_female], color="gold") # Cambié a gold para que se vea mejor
    ax3.set_ylabel("Cantidad Sobrevivientes")
    st.pyplot(fig3)

# --- DATA EXPANDER ---
# Ocultamos la tabla para que no ocupe espacio visual innecesario
st.write("---")
with st.expander("📂 Ver datos detallados (Click para desplegar)"):
    st.write("Estos son los primeros 10 registros de tu selección:")
    st.table(df_filtrado.head(10))
