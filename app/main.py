# python 3.11

import streamlit as st

pages = {
    "Presentación" : [
        st.Page("pages/introduction.py", title="Introducción")
    ],
    "Apartados obligatorios" : [
        st.Page("pages/obligatory/customers.py", title="Clasificación de clientes por estado"),
        st.Page("pages/obligatory/orders.py", title="Número de pedidos por ciudad"),
        st.Page("pages/obligatory/late_orders.py", title="Número de pedidos con retraso por ciudad"),
        st.Page("pages/obligatory/reviews.py", title="Número de reviews")
    ],
    "Apartados extra" : [
        st.Page("pages/extras/sents_orders.py", title="Análisis de pedidos entregados"),
        st.Page("pages/extras/product_analitics.py", title="Análisis de productos"),
        st.Page("pages/extras/sellers.py", title="Análisis de vendedores"),
        st.Page("pages/extras/economy.py", title="Análisis económico")
    ]
}

pg = st.navigation(pages)
pg.run()