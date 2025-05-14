# python 3.11

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Ejercicio 1

resource= '../resources/clean_data/orders_by_customer.csv'
df_customers_original = pd.read_csv(resource, encoding='utf-8', sep=';')
df_customers = df_customers_original.copy()
df_customers.name = 'customers'

customers_per_state = df_customers['customer_state'].value_counts()

customers_per_city_state = (
    df_customers.groupby(['customer_state', 'customer_city'])
           .size()
           .reset_index(name='num_customers')
           .sort_values(['customer_state', 'num_customers'], ascending=[True, False])
)

df_customers['order_purchase_timestamp'] = pd.to_datetime(df_customers['order_purchase_timestamp'], errors='coerce')

min_date = df_customers['order_purchase_timestamp'].min()
max_date = df_customers['order_purchase_timestamp'].max()

date_range = st.date_input(
    'Selecciona el rango de fechas',
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

df_top_5_estados = df_customers.groupby('customer_state').size().sort_values(ascending=False).head(5)

if isinstance(date_range, tuple) and len(date_range) == 2 and all(date_range):
    start_date, end_date = date_range
    df_filtered = df_customers[
        (df_customers['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
        (df_customers['order_purchase_timestamp'] <= pd.to_datetime(end_date))
    ]

    df_top5 = df_filtered.groupby('customer_state').size().sort_values(ascending=False).head(5)

    st.title('Numero de clientes por estado')
    st.write('Los estados con más clientes')
    st.bar_chart(df_top5, use_container_width=True)
    st.write('Selecciona el estado que deseas ver')
    selected_state = st.selectbox('Selecciona el estado', customers_per_state.index.tolist())
    top_cities = customers_per_city_state[customers_per_city_state['customer_state'] == selected_state].sort_values('num_customers', ascending=False).head(10)

    chart = alt.Chart(top_cities).mark_bar().encode(
        x=alt.X('num_customers:Q', title='Número de Clientes'),
        y=alt.Y('customer_city:N', sort='-x', title='Ciudad'),
        tooltip=['customer_city', 'num_customers']
    ).properties(
        title=f'Top 10 ciudades en {selected_state} con más clientes',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Por favor selecciona ambas fechas para mostrar los datos.")




# Ejercicio 2

resource= '../resources/clean_data/clean_orders.csv'
df_orders_original = pd.read_csv(resource, encoding='utf-8', sep=';')
df_orders = df_orders_original.copy()
df_orders.name = 'orders'

df_orders_top5 = df_orders.merge(df_customers, on='customer_id')
df_orders_top5 = df_orders_top5[df_orders_top5['customer_state'].isin(df_top_5_estados.index.tolist())]

orders_per_city_state = (
    df_orders_top5.groupby(['customer_state', 'customer_city'])
                  .size()
                  .reset_index(name='num_orders')
)

merged = pd.merge(customers_per_city_state, orders_per_city_state,
                  on=['customer_state', 'customer_city'], how='left')


total_orders = merged['num_orders'].sum()

merged['order_pct'] = (merged['num_orders'] / total_orders * 100).round(2)
merged['avg_orders_per_customer'] = (merged['num_orders'] / merged['num_customers']).round(2)

sorted_table = merged.sort_values(['customer_state', 'num_customers'], ascending=[True, False])



top_cities = sorted_table.sort_values('num_orders', ascending=False).head(20)


st.title('Numero de pedidos por ciudad y estado')
st.write('Los 20 ciudades con más pedidos en los 5 estados principales')
fig = px.pie(
    top_cities,
    width=800,
    height=700,
    names='customer_city',
    values='num_orders',
    title='Distribución de pedidos por ciudad y el porcentaje de pedidos que representa',
    hole=0.3 
)

st.plotly_chart(fig, use_container_width=True)
st.write(f'Total de pedidos: {total_orders}')