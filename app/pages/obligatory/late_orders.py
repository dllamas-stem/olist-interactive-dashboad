import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

resource= '../resources/clean_data/clean_orders.csv'
df_orders_original = pd.read_csv(resource, encoding='utf-8')
df_orders = df_orders_original.copy()
df_orders.name = 'orders'

resource= '../resources/clean_data/clean_orders_by_customer.csv'
df_customers_original = pd.read_csv(resource, encoding='utf-8')
df_customers = df_customers_original.copy()
df_customers.name = 'customers'

df_customers['order_purchase_timestamp'] = pd.to_datetime(df_customers['order_purchase_timestamp'], errors='coerce')
df_orders['order_delivered_customer_date'] = pd.to_datetime(df_orders['order_delivered_customer_date'], errors='coerce')
df_orders['order_estimated_delivery_date'] = pd.to_datetime(df_orders['order_estimated_delivery_date'], errors='coerce')

df_delivered = df_orders.dropna(subset=['order_delivered_customer_date', 'order_estimated_delivery_date'])

df_delivered['late_days'] = (df_delivered['order_delivered_customer_date'] - df_delivered['order_estimated_delivery_date']).dt.days


df_late_orders = df_delivered[df_delivered['late_days'] > 0]

df_orders_with_city = pd.merge(df_delivered, df_customers[['customer_id', 'customer_city']], on='customer_id', how='left')

df_late_orders_with_city = pd.merge(df_late_orders, df_customers[['customer_id', 'customer_city']], on='customer_id', how='left')

total_by_city = df_orders_with_city.groupby('customer_city')['order_id'].count().rename('total_orders')

late_by_city = df_late_orders_with_city.groupby('customer_city').agg(
    late_orders=pd.NamedAgg(column='order_id', aggfunc='count'),
    avg_late_days=pd.NamedAgg(column='late_days', aggfunc='mean')
).round()

result = pd.merge(total_by_city, late_by_city, left_index=True, right_index=True)

result['late_percentage'] = (result['late_orders'] / result['total_orders']) * 100

result = result.sort_values(by='late_orders', ascending=False)

top10 = result.sort_values('late_orders', ascending=False).head(10)

st.title("Análisis de Entregas Tardías por Ciudad (Top 10)")

cities = top10.index.tolist()

fig1 = px.bar(
    top10,
    x='late_orders',
    y=top10.index,
    orientation='h',
    text='late_orders',
    labels={'late_orders': 'Órdenes Tardías', 'customer_city': 'Ciudad'},
    title='Cantidad de Entregas Tardías por Ciudad'
)
fig1.update_layout(yaxis_title='Ciudad', xaxis_title='Órdenes Tardías', height=500)

fig2 = px.pie(
    top10,
    names=top10.index,
    values='late_percentage',
    title='Porcentaje de Entregas Tardías sobre el Total por Ciudad',
    labels={'customer_city': 'Ciudad', 'late_percentage': 'Porcentaje (%)'},
)
fig2.update_layout(yaxis_title='Ciudad', xaxis_title='Porcentaje (%)', height=500)

df_sorted_by_avg_late_days = top10.sort_values(by='avg_late_days', ascending=False)
fig3 = px.bar(
    df_sorted_by_avg_late_days,
    x='avg_late_days',
    y=df_sorted_by_avg_late_days.index,
    orientation='h',
    labels={'avg_late_days': 'Días Promedio de Retraso', 'customer_city': 'Ciudad'},
    title='Promedio de Días de Retraso por Ciudad'
)
fig3.update_layout(yaxis_title='Ciudad', xaxis_title='Días de Retraso', height=500)

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)


renamed_columns_map = {
    'total_orders': 'Pedidos',
    'late_orders': 'Entregados con retraso',
    'avg_late_days': 'Media de días de retraso',
    'late_percentage': 'Porcentaje'
}

pretty_result = result.copy()
pretty_result.index.names = ['Ciudad']
pretty_result.rename(columns=renamed_columns_map, inplace=True)
st.dataframe(pretty_result.head(10))