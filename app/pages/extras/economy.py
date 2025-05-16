import streamlit as st
import pandas as pd
import plotly.express as px

df_orders = pd.read_csv('../resources/clean_data/clean_orders.csv', encoding='utf-8')
df_order_items = pd.read_csv('../resources/clean_data/clean_order_items.csv', encoding='utf-8')
df_order_payments = pd.read_csv('../resources/clean_data/clean_order_payments.csv', encoding='utf-8')

df_orders_items_payments = pd.merge(
    left=df_order_items,
    left_on='order_id',
    right=df_order_payments,
    right_on='order_id',
    how='left'
)

df_orders_full = pd.merge(
    left=df_orders.drop(columns='order_status').drop_duplicates(),
    right=df_orders_items_payments,
    on='order_id'
)

df_products_total_generated = df_orders_items_payments.groupby('product_id').agg(
    times_buyed=('payment_value', 'count'),
    total_generated=('payment_value', 'sum')
).reset_index()

top10_revenue = df_products_total_generated.sort_values(by='total_generated', ascending=False).head(10)

get_total_generated = lambda df, group_by_key, price_key: df.groupby(by=[group_by_key]).agg(
    times_buyed = pd.NamedAgg(column=price_key, aggfunc='count'),
    total_generated = pd.NamedAgg(column=price_key, aggfunc='sum')
).sort_values(by=['total_generated'], ascending=False)

df_orders_full['order_purchase_timestamp'] = pd.to_datetime(df_orders_full['order_purchase_timestamp'])
# filtar por año
df_orders_full['order_purchase_year'] = df_orders_full['order_purchase_timestamp'].dt.year
df_orders_full['order_purchase_month'] = df_orders_full['order_purchase_timestamp'].dt.month
df_orders_full['order_purchase_month_name'] = df_orders_full['order_purchase_timestamp'].dt.month_name()
df_orders_full['order_purchase_day'] = df_orders_full['order_purchase_timestamp'].dt.day

# STREAMLIT
st.title("Análisis de Ingresos y Ventas por Producto")
st.markdown("""
Visualización de los productos con **mayor número de compras** y **mayor generación de ingresos** 
basado en los datos de pedidos, ítems y pagos.
""")

st.subheader("Top 10 Productos con Mayor Ingreso Generado")
fig_revenue = px.bar(
    top10_revenue,
    x='product_id',
    y='total_generated',
    text='total_generated',
    color='total_generated',
    color_continuous_scale='Blues',
    labels={'product_id': 'ID del Producto', 'total_generated': 'Total Generado'},
    title="Top 10 Productos por Ingresos Generados"
)
fig_revenue.update_layout(uniformtext_minsize=8, xaxis_tickangle=-45, height=500)
st.plotly_chart(fig_revenue, use_container_width=True)

st.subheader("Top 20 Productos que mas dinero han generado")
pretty_df_products_total_generated = df_products_total_generated.copy().sort_values(by='total_generated', ascending=False).reset_index(drop=True)
columns_map={
    'product_id': 'ID producto',
    'times_buyed': 'Veces comprado',
    'total_generated': 'Total generado'
}
pretty_df_products_total_generated.rename(columns=columns_map, inplace=True)
st.dataframe(pretty_df_products_total_generated.head(20))

st.title("Análisis de Ingresos por Mes")
st.markdown("Selecciona un año para ver el total generado por mes.")

selected_year = st.selectbox("Selecciona el año", options=[2016, 2017, 2018])

df_filtered = df_orders_full[df_orders_full['order_purchase_year'] == selected_year]

df_monthly_revenue = df_filtered.groupby(['order_purchase_month', 'order_purchase_month_name']).agg(
    total_generated=('payment_value', 'sum')
).reset_index()

df_monthly_revenue = df_monthly_revenue.sort_values(by='order_purchase_month')

fig = px.area(
        df_monthly_revenue,
        x='order_purchase_month_name',
        y='total_generated',
        title=f'Total Generado por Mes en {selected_year}',
        labels={'order_purchase_month_name': 'Mes', 'total_generated': 'Ingresos Generados'},
        color_discrete_sequence=['teal']
    )

fig.update_traces(mode='lines+markers', marker=dict(size=10))
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)