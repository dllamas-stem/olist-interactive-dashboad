import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

resource= 'resources/clean_data/clean_orders.csv'
df_orders_original = pd.read_csv(resource, encoding='utf-8')
df_orders = df_orders_original.copy()
df_orders.name = 'orders'

resource= 'resources/clean_data/clean_orders_by_customer.csv'
df_customers_original = pd.read_csv(resource, encoding='utf-8')
df_customers = df_customers_original.copy()
df_customers.name = 'customers'

resource= 'resources/clean_data/clean_order_reviews_review_comments_no_null.csv'
df_order_reviews_original = pd.read_csv(resource, encoding='utf-8')
df_order_reviews = df_order_reviews_original.copy()
df_order_reviews.name = 'order_reviews'

df_orders_customers = pd.merge(
    df_orders,
    df_customers[['customer_id', 'customer_state']],
    on='customer_id',
    how='left'
)

df_reviews_full = pd.merge(
    df_orders_customers,
    df_order_reviews[['order_id', 'review_score']],
    on='order_id',
    how='inner'
)

df_reviews_full['is_late'] = pd.to_datetime(df_reviews_full['order_delivered_customer_date']) > pd.to_datetime(df_reviews_full['order_estimated_delivery_date'])

reviews_all = df_reviews_full.copy()
reviews_on_time = df_reviews_full[~df_reviews_full['is_late']]

reviews_grouped = reviews_all.groupby('customer_state').agg(
    total_reviews=('review_score', 'count')
)

score_grouped = reviews_on_time.groupby('customer_state').agg(
    avg_score=('review_score', 'mean')
)

result_reviews = pd.merge(reviews_grouped, score_grouped, on='customer_state')
result_reviews = result_reviews.sort_values('total_reviews', ascending=False)

st.title("Análisis de Reseñas por Estado")
st.write("Este análisis muestra el número de reseñas por estado y el puntaje promedio de reseñas para entregas a tiempo.")

pretty_result_reviews = result_reviews.copy()
columns_map = {
    'total_reviews': 'Reviews totales',
    'avg_score': 'Nota media'
}
pretty_result_reviews.index.names = ['Estado']
pretty_result_reviews.rename(columns=columns_map, inplace=True)
st.dataframe(pretty_result_reviews.head(10))

st.subheader("Número total de reseñas por estado")
fig_reviews = px.bar(
    result_reviews.head(10),
    x=result_reviews.head(10).index,
    y='total_reviews',
    labels={'x': 'Estado', 'total_reviews': 'Total de Reseñas'},
    title="Top 10 Estados por Cantidad de Reseñas",
    color='total_reviews',
)
st.plotly_chart(fig_reviews, use_container_width=True)

st.subheader("Puntaje promedio de reseñas (entregas a tiempo)")
fig_scores = px.bar(
    result_reviews.head(10),
    x=result_reviews.head(10).index,
    y='avg_score',
    labels={'x': 'Estado', 'avg_score': 'Puntaje Promedio'},
    title="Top 10 Estados por Puntaje Promedio de Reseñas (Entregas a Tiempo)",
)
fig_scores.update_yaxes(range=[0, 5])
st.plotly_chart(fig_scores, use_container_width=True)