import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Titanic App de Cris",
    layout="wide",
    page_icon="🚢"
)

# Carga de datos
df = pd.read_csv("database_titanic.csv")

# Título
st.write("""
# 🚢 La mejor app interactiva ¡Hecha por Cris!
## Análisis visual del Titanic
""")

# --- SIDEBAR ---
with st.sidebar:
    st.write("# Opciones")
    div = st.slider('Número de bins:', 1, 20, 10)
    
    st.write("---")
    st.write("Filtrar por Clase:")
    opcion_clase = st.multiselect(
        "Clases a mostrar:",
        options=[1, 2, 3],
        default=[1, 2, 3]
    )
    
    st.write("---")
    if st.button("¡Sorpresa!"):
        st.balloons()

# Filtrado de datos
df_filtrado = df[df["Pclass"].isin(opcion_clase)]

# --- MÉTRICAS (KPIs) ---
col1, col2, col3 = st.columns(3)
total_pas = len(df_filtrado)
total_sob = len(df_filtrado[df_filtrado['Survived'] == 1])
pct_sob = (total_sob / total_pas * 100) if total_pas > 0 else 0

col1.metric("Total Pasajeros", total_pas)
col2.metric("Sobrevivientes", total_sob)
col3.metric("Tasa Supervivencia", f"{pct_sob:.1f}%")

st.write("---")

# --- TUS GRÁFICOS ORIGINALES (MATPLOTLIB) ---
st.write("### 📊 Resumen General (Estático)")
fig, ax = plt.subplots(1, 3, figsize=(15
