import streamlit as st
import pandas as pd
import plotly.express as px

df_orders = pd.read_csv('resources/clean_data/clean_orders.csv', encoding='utf-8')
df_customers = pd.read_csv('resources/clean_data/clean_orders_by_customer.csv', encoding='utf-8')

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
    undelivered_percentage_state = str(round(((undelivered_count_state / total_sent_state) * 100))) + '%' if total_sent_state > 0 else 0

    stats.append({
        'state': state,
        'total_sent': total_sent_state,
        'undelivered': undelivered_count_state,
        'undelivered_percentage': undelivered_percentage_state
    })

df_stats = pd.DataFrame(stats)
df_stats = df_stats.sort_values('total_sent', ascending=False).head(10).reset_index().drop(columns=['index'])

st.title("Análisis de Entregas por Estado")
st.markdown("""
Se muestran los estados con más pedidos **enviados**, cuántos de ellos **no han sido entregados**, 
y el **porcentaje de no entregas** sobre el total de pedidos enviados.
""")

pretty_df_stats = df_stats.copy()
columns_map = {
    'state': 'Estado',
    'total_sent': 'Pedidos enviados',
    'undelivered': 'Pedidos no entregados',
    'undelivered_percentage': 'Porcentaje pedidos no entregados'
}
pretty_df_stats.rename(columns=columns_map, inplace=True)
st.dataframe(pretty_df_stats, use_container_width=True)

df_stats['delivered'] = df_stats['total_sent'] - df_stats['undelivered']

df_stack = df_stats[['state', 'delivered', 'undelivered']].melt(
    id_vars='state',
    var_name='status',
    value_name='cantidad'
)

df_stack['status'] = df_stack['status'].replace({
    'delivered': 'Entregados',
    'undelivered': 'No Entregados'
})

st.subheader("Pedidos Entregados vs No Entregados por Estado (Top 10)")

fig_stacked = px.bar(
    df_stack,
    x='state',
    y='cantidad',
    color='status',
    title='Pedidos Enviados por Estado (Entregados vs No Entregados)',
    labels={'state': 'Estado', 'cantidad': 'Número de Pedidos'},
    color_discrete_map={'Entregados': 'lime', 'No Entregados': 'red'}
)

fig_stacked.update_layout(barmode='stack', xaxis_tickangle=-45)
st.plotly_chart(fig_stacked, use_container_width=True)

st.subheader("Porcentaje de pedidos no entregados sobre enviados (Top 10)")
fig_pie = px.pie(
    df_stats[['undelivered', 'state']],
    width=900,
    height=700,
    names='state',
    values='undelivered',
    title='Porcentaje de Pedidos No Entregados por Estado',
    hole=0.3,
)
fig_pie.update_traces(textinfo='label+text', text=df_stats['undelivered_percentage'])
st.plotly_chart(fig_pie, use_container_width=True)
