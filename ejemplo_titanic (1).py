import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px  # <--- IMPORTANTE: Nueva librería para el 3D

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
    div = st.slider('Número de bins:', 0, 20, 10)
    
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
fig, ax = plt.subplots(1, 3, figsize=(15, 3))

# Gráfico 1: Histograma
ax[0].hist(df_filtrado["Age"], bins=div, color="skyblue", edgecolor="black")
ax[0].set_xlabel("Edad")
ax[0].set_ylabel("Frecuencia")
ax[0].set_title("Histograma de edades")

# Gráfico 2: Distribución Total
cant_hombres = len(df_filtrado[df_filtrado["Sexo"] == "Hombre"])
cant_mujeres = len(df_filtrado[df_filtrado["Sexo"] == "Mujer"])
ax[1].bar(["Masculino", "Femenino"], [cant_hombres, cant_mujeres], color="red")
ax[1].set_xlabel("Sexo")
ax[1].set_ylabel("Cantidad")
ax[1].set_title('Distribución Total')

# Gráfico 3: Sobrevivientes
sob_male = len(df_filtrado[(df_filtrado["Sex"] == "Hombre") & (df_filtrado["Sobrevivió"] == 1)])
sob_female = len(df_filtrado[(df_filtrado["Sex"] == "Mujer") & (df_filtrado["Sobrevivió"] == 1)])
ax[2].bar(["Masculino", "Femenino"], [sob_male, sob_female], color="gold")
ax[2].set_xlabel("Sexo")
ax[2].set_title('Sobrevivientes por Sexo')

plt.tight_layout()
st.pyplot(fig)

# --- NUEVO: GRÁFICO 3D INTERACTIVO (PLOTLY) ---
st.write("---")
st.write("### 🧊 Explorador 3D: Edad vs Tarifa vs Clase")

# Convertimos Survived a string para que el color sea discreto (Categoría) y no continuo
df_plot = df_filtrado.copy()
df_plot["Survived"] = df_plot["Survived"].map({0: "No sobrevivió", 1: "Sobrevivió"})

# Creamos el gráfico 3D
fig_3d = px.scatter_3d(
    df_plot, 
    x='Edad',           # Eje X: Edad
    y='Tarifa',          # Eje Y: Precio del ticket
    z='Clase',        # Eje Z: Clase (Altura)
    color='Sobrevivió',  # Color: Si sobrevivió o no
    symbol='Sexo',      # Símbolo: Hombre o Mujer (Círculo o Diamante)
    opacity=0.7,       # Transparencia para ver los puntos de atrás
    color_discrete_map={"Sobrevivió": "green", "No sobrevivió": "red"} # Colores personalizados
)

# Ajustamos el tamaño inicial para que se vea bien en pantalla completa
fig_3d.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=500)

# Mostramos el gráfico
st.plotly_chart(fig_3d, use_container_width=True)

# --- TABLA ---
with st.expander("📂 Ver datos detallados"):
    st.table(df_filtrado.head())
