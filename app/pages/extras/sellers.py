import streamlit as st
import pandas as pd
import plotly.express as px

df_order_items = pd.read_csv('../resources/clean_data/clean_order_items.csv', encoding='utf-8')
df_order_reviews = pd.read_csv('../resources/clean_data/clean_order_reviews_review_comments_no_null.csv', encoding='utf-8')
df_orders = pd.read_csv('../resources/clean_data/clean_orders.csv', encoding='utf-8')

df_oi_orders = df_order_items.merge(
    df_orders[['order_id', 'order_delivered_customer_date', 'order_estimated_delivery_date']],
    on='order_id'
)

df_oi_orders['total_price'] = df_oi_orders['price'] + df_oi_orders['freight_value']

print(df_oi_orders.columns)

df_oi_orders_reviews = df_oi_orders.merge(
    df_order_reviews[['order_id', 'review_score']],
    on='order_id',
    how='left'
)

df_seller_metrics = df_oi_orders_reviews.groupby('seller_id').agg(
    total_pedidos=('order_id', 'nunique'),
    review_media=('review_score', 'mean'),
    total_generated=('total_price', 'sum')
).reset_index().round(2)

df_seller_metrics.sort_values(by='total_pedidos', ascending=False, inplace=True)

st.title("Desempeño de los Vendedores")
st.markdown("Este gráfico muestra la relación entre el número total de pedidos gestionados por cada vendedor y su puntuación promedio en reseñas.")

pretty_df_seller_metrics = df_seller_metrics.copy().reset_index().drop(columns=['index'])
columns_map = {
    'seller_id': 'ID Vendedor',
    'total_pedidos': 'Nº Pedidos',
    'review_media': 'Valoración media',
    'total_generated': 'Total generado'
}
pretty_df_seller_metrics.rename(columns=columns_map, inplace=True)
st.dataframe(pretty_df_seller_metrics.head(20))

fig = px.scatter(
    df_seller_metrics,
    x='total_pedidos',
    y='review_media',
    hover_name='seller_id',
    size_max=15,
    title="Relación entre Volumen de Pedidos y Puntuación Media por Vendedor",
    labels={
        'total_pedidos': 'Total de Pedidos',
        'review_media': 'Puntuación Media'
    },
    color='review_media',
    color_continuous_scale='RdYlGn'
)

fig.update_layout(height=600, xaxis_type='log', yaxis_range=[0, 5])  

fig2 = px.bar(
    df_seller_metrics.sort_values(by=['total_generated'], ascending=False).head(10),
    x='total_generated',
    y='seller_id',
    orientation='h',
    labels={'total_generated': 'Total generado', 'seller_id': 'ID vendedor'},
    title='Dinero total generado por vendedor'
)
fig2.update_layout(yaxis_title='ID Vendedor', xaxis_title='Dinero total generado', height=500)

st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
