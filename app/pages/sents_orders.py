import streamlit as st
import pandas as pd
import plotly.express as px

df_orders = pd.read_csv('../resources/clean_data/clean_orders.csv', encoding='utf-8')
df_customers = pd.read_csv('../resources/clean_data/orders_by_customer.csv', encoding='utf-8')

df_orders_with_state = pd.merge(
    df_orders,
    df_customers[['customer_id', 'customer_state']],
    on='customer_id',
    how='left'
)

df_sent = df_orders_with_state[df_orders_with_state['order_delivered_carrier_date'].notna()]

stats = []

for state in df_sent['customer_state'].dropna().unique():
    df_state = df_sent[df_sent['customer_state'] == state]

    total_sent_state = df_state.shape[0]
    df_state_not_delivered = df_state[df_state['order_delivered_customer_date'].isna()]
    undelivered_count_state = df_state_not_delivered.shape[0]
    undelivered_percentage_state = (undelivered_count_state / total_sent_state) * 100 if total_sent_state > 0 else 0

    stats.append({
        'state': state,
        'total_sent': total_sent_state,
        'undelivered': undelivered_count_state,
        'undelivered_percentage': undelivered_percentage_state
    })

df_stats = pd.DataFrame(stats)
df_stats = df_stats.sort_values('total_sent', ascending=False).head(10)

st.title("Análisis de Entregas por Estado")
st.markdown("""
Se muestran los estados con más pedidos **enviados**, cuántos de ellos **no han sido entregados**, 
y el **porcentaje de no entregas** sobre el total de pedidos enviados.
""")

st.dataframe(df_stats)

st.subheader("Total de pedidos enviados por estado")
fig_total_sent = px.bar(
    df_stats,
    x='state',
    y='total_sent',
    title="Total de Pedidos Enviados por Estado",
    color_discrete_sequence=['blue'],
    labels={'state': 'Estado', 'total_sent': 'Pedidos Enviados'}
)
st.plotly_chart(fig_total_sent, use_container_width=True)

st.subheader("Pedidos enviados pero no entregados")
fig_undelivered = px.bar(
    df_stats,
    x='state',
    y='undelivered',
    title="Pedidos No Entregados por Estado",
    color_discrete_sequence=['red'],
    labels={'state': 'Estado', 'undelivered': 'No Entregados'}
)
st.plotly_chart(fig_undelivered, use_container_width=True)

st.subheader("Porcentaje de pedidos no entregados sobre enviados (Top 10)")
fig_pie = px.pie(
    df_stats,
    names='state',
    values='undelivered_percentage',
    title='Porcentaje de Pedidos No Entregados por Estado',
    hole=0.3,
)
fig_pie.update_traces(textinfo='label+percent')
st.plotly_chart(fig_pie, use_container_width=True)
