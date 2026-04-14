import streamlit as st
import pandas as pd
import plotly.express as px

# --- Data Loading ---
# In a standalone Streamlit app, you would load your data directly
# using the file path.
file_path = 'datos/SalidaVentas.xlsx'
df = pd.read_excel(file_path)

# --- Data Cleaning and Aggregation ---
# Ensure 'Order Date' is datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Fill NaN values in 'Discount' with 0
df['Discount'] = df['Discount'].fillna(0)

# Drop rows where 'Postal Code' is NaN
df.dropna(subset=['Postal Code'], inplace=True)

# Drop columns with a high percentage of missing values (if they exist after loading)
columns_to_drop = ['Return Reason', 'Notas devolución', 'Aprobador']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Extract year and month for time-series analysis
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month_name()

# --- Aggregated Data for Dashboard ---
sales_profit_by_year = df.groupby('Order Year')[['Sales', 'Profit']].sum().reset_index()
sales_profit_by_month = df.groupby(['Order Year', 'Order Month'])[['Sales', 'Profit']].sum().reset_index()
sales_profit_by_region = df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()

# --- Streamlit App Layout ---
st.set_page_config(layout='wide', page_title='Dashboard de Ventas de la Empresa')

st.title('📊 Dashboard de Ventas de la Empresa')
st.markdown('Este dashboard interactivo presenta un análisis de las ventas y ganancias de la empresa, desglosado por región y a lo largo del tiempo.')

# --- Key Metrics --- 
st.header('Métricas Clave')

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric(label='Ventas Totales', value=f'${total_sales:,.2f}')
with col2:
    st.metric(label='Ganancia Total', value=f'${total_profit:,.2f}')

# --- Sales and Profit by Region ---
st.header('Ventas y Ganancias por Región')
fig_region = px.bar(sales_profit_by_region, x='Region', y=['Sales', 'Profit'],
                    title='Ventas y Ganancias por Región',
                    barmode='group', height=400)
st.plotly_chart(fig_region, use_container_width=True)

# --- Sales and Profit Over Time (Yearly) ---
st.header('Tendencias Anuales de Ventas y Ganancias')
fig_year = px.line(sales_profit_by_year, x='Order Year', y=['Sales', 'Profit'],
                   title='Ventas y Ganancias Anuales',
                   markers=True, height=400)
st.plotly_chart(fig_year, use_container_width=True)

# --- Sales and Profit Over Time (Monthly) ---
st.header('Tendencias Mensuales de Ventas y Ganancias')

# Add a year filter for monthly data
selected_year = st.selectbox('Selecciona el Año para el Análisis Mensual', sorted(df['Order Year'].unique(), reverse=True))

monthly_data_filtered = sales_profit_by_month[sales_profit_by_month['Order Year'] == selected_year]

# Define a consistent order for months
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']
monthly_data_filtered['Order Month'] = pd.Categorical(monthly_data_filtered['Order Month'], categories=month_order, ordered=True)
monthly_data_filtered = monthly_data_filtered.sort_values('Order Month')

fig_month = px.line(monthly_data_filtered, x='Order Month', y=['Sales', 'Profit'],
                    title=f'Ventas y Ganancias Mensuales para {selected_year}',
                    markers=True, height=400)
st.plotly_chart(fig_month, use_container_width=True)

# --- Raw Data (optional) ---
st.header('Vista Previa de Datos')
st.dataframe(df.head())
