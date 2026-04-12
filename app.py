import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title('Aplicación Streamlit con DataFrame y Gráfica de Línea')

st.header('DataFrame de Ejemplo')

# Crear un DataFrame de ejemplo
data = {
    'Fecha': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='D')),
    'Valor_A': np.random.rand(100).cumsum() * 100,
    'Valor_B': np.random.rand(100).cumsum() * 50
}
df = pd.DataFrame(data)

# Mostrar el DataFrame
st.dataframe(df)

st.header('Gráfica de Línea de Valor_A vs. Fecha')

# Crear una gráfica de línea
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Fecha'], df['Valor_A'], label='Valor A', color='skyblue')
ax.plot(df['Fecha'], df['Valor_B'], label='Valor B', color='salmon')
ax.set_xlabel('Fecha')
ax.set_ylabel('Valor')
ax.set_title('Tendencia de Valores a lo largo del tiempo')
ax.legend()
ax.grid(True)
st.pyplot(fig)
