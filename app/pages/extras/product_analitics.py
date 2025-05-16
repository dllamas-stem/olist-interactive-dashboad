import streamlit as st
import pandas as pd
import plotly.express as px

df_order_items = pd.read_csv('resources/clean_data/clean_order_items.csv', encoding='utf-8')
df_order_reviews = pd.read_csv('resources/clean_data/clean_order_reviews_review_comments_no_null.csv', encoding='utf-8')
df_products = pd.read_csv('resources/clean_data/clean_products_with_translations.csv', encoding='utf-8')

df_reviews_products = pd.merge(
    df_order_items[['order_id', 'product_id']],
    df_order_reviews[['order_id', 'review_score']],
    on='order_id',
    how='inner'
)

product_review_stats = df_reviews_products.groupby('product_id').agg(
    avg_score=('review_score', 'mean'),
    num_reviews=('review_score', 'count')
).reset_index()

product_review_stats_filtered = product_review_stats[product_review_stats['num_reviews'] >= 100]

df_full = pd.merge(
    product_review_stats_filtered,
    df_products[['product_id', 'product_category_name_english']],
    on='product_id',
    how='left'
)

best_product_named = df_full.sort_values('avg_score', ascending=False).iloc[0]
worst_product_named = df_full.sort_values('avg_score', ascending=True).iloc[0]

st.title("Análisis de Productos Mejor y Peor Valorados")

st.markdown("Se muestran los productos con **mejor** y **peor** puntuación promedio en reviews, considerando solo aquellos con al menos 100 reseñas.")
col1, col2 = st.columns(2)
with col1: 
    st.subheader("Producto mejor valorado")
    st.markdown(f"**ID:** `{best_product_named['product_id']}`")
    st.markdown(f"**Categoría:** `{best_product_named['product_category_name_english']}`")
    st.markdown(f"**Puntuación media:** `{best_product_named['avg_score']:.2f}`")
    st.markdown(f"**Número de reseñas:** `{int(best_product_named['num_reviews'])}`")
    
with col2:
    st.subheader("Producto peor valorado")
    st.markdown(f"**ID:** `{worst_product_named['product_id']}`")
    st.markdown(f"**Categoría:** `{worst_product_named['product_category_name_english']}`")
    st.markdown(f"**Puntuación media:** `{worst_product_named['avg_score']:.2f}`")
    st.markdown(f"**Número de reseñas:** `{int(worst_product_named['num_reviews'])}`")

st.subheader("Gráfica comparativa entre el mejero y el peor valorado")
comparison_df = pd.DataFrame([
    {
        'Tipo': 'Mejor producto',
        'product_id': best_product_named['product_id'],
        'Categoría': best_product_named['product_category_name_english'],
        'Puntuación promedio': best_product_named['avg_score']
    },
    {
        'Tipo': 'Peor producto',
        'product_id': worst_product_named['product_id'],
        'Categoría': worst_product_named['product_category_name_english'],
        'Puntuación promedio': worst_product_named['avg_score']
    }
])

fig = px.bar(
    comparison_df,
    x='Tipo',
    y='Puntuación promedio',
    color='Tipo',
    text='Puntuación promedio',
    color_discrete_sequence=['#2ca02c', '#d62728'], 
    hover_data=['product_id', 'Categoría']
)
fig.update_layout(yaxis_range=[0, 5])
st.plotly_chart(fig, use_container_width=True)
