import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

resource= 'resources/clean_data/clean_orders_by_customer.csv'
df_orders_by_customer_original = pd.read_csv(resource, encoding='utf-8')
df_orders_by_customer = df_orders_by_customer_original.copy()
df_orders_by_customer.name = 'orders by customers'

df_top_5_estados = df_orders_by_customer.groupby('customer_state').size().sort_values(ascending=False).head(5)

df_orders_top5 = df_orders_by_customer[df_orders_by_customer['customer_state'].isin(df_top_5_estados.index.tolist())]
orders_per_city_state = (
    df_orders_top5.groupby(['customer_state', 'customer_city'])['order_id']
                  .nunique()
                  .reset_index(name='num_orders')
)

customers_per_city_state = (
    df_orders_by_customer.groupby(['customer_state', 'customer_city'])['customer_unique_id']
            .nunique()
            .reset_index(name='num_customers')
            .sort_values(['customer_state', 'num_customers'], ascending=[True, False])
)


merged = pd.merge(customers_per_city_state, orders_per_city_state,
                  on=['customer_state', 'customer_city'], how='left')

total_orders = merged['num_orders'].sum()

merged['order_pct'] = (merged['num_orders'] / total_orders * 100).round(2).astype(str) + '%'
merged['avg_orders_per_customer'] = (merged['num_orders'] / merged['num_customers']).round(2).astype(str) + '%'

sorted_table = merged.sort_values(['customer_state', 'num_customers'], ascending=[True, False])

top_cities = sorted_table.sort_values('num_orders', ascending=False).head(20)
top_cities['city_label'] = top_cities['customer_city'] + ' (' + top_cities['customer_state'] + ')'

st.title('Numero de pedidos por ciudad')
st.write('Los 20 ciudades con más pedidos en los 5 estados principales')
fig = px.pie(
    top_cities,
    width=900,
    height=700,
    names='city_label',
    values='num_orders',
    title='Distribución de pedidos por ciudad y el porcentaje de pedidos que representa',
    hole=0.3
)
fig.update_traces(text=top_cities['order_pct'], textinfo='text')
st.plotly_chart(fig, use_container_width=True)
st.write(f'Total de pedidos: {total_orders}')

pretty_top_cities = top_cities.copy()
pretty_top_cities.reset_index(inplace=True)
pretty_top_cities.drop(columns=['city_label', 'index'], inplace=True)
columns_map = {
    'customer_state': 'Estado',
    'customer_city': 'Ciudad',
    'num_customers': 'Nº Clientes',
    'num_orders':'Nº Pedidos',
    'order_pct': 'Porcentaje de pedidos',
    'avg_orders_per_customer': 'Media de Pedidos / Cliente',
    }

pretty_top_cities.rename(columns=columns_map, inplace=True)
st.dataframe(pretty_top_cities, use_container_width=True)

st.subheader("\n¿Que te transmite esta informacion?")
st.write("En este gráfico podemos detectar la gran diferencia de pedidos de la primera ciudad respecto a las demás.")
st.write("Principalmente para aumentar las ventas en las demás ciudades, deberían de fijarse y tomar ideas de Sao Paulo y Rio de Janeiro, que son las 2 ciudades con más ventas, en sus campañas de publicidad o como se desenvuelven a nivel logístico.")
st.subheader("\n¿Que acciones como analista de datos crees que deberia de tomar la empresa para mejorar sus ventas?")
st.write("Según los datos, podemos observar que la media de pedidos por cliente es 1, esto se podría mejorar dando descuentos para la segunda compra, puntos acumulativos para obtener un mayor descuento, etc.")
st.write("Otra forma de aumentar las ventas es mejorando la atención al cliente, con esto quiero decir que se podrían atender mejor las malas reseñas y tenerlas en cuenta para poder mejorar esos aspectos.")
