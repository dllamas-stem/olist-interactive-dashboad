# python 3.11

import streamlit as st

pages = {
    "Presentación" : [
        st.Page("pages/introduction.py", title="Introducción")
    ],
    "Apartados obligatorios" : [
        st.Page("pages/customers.py", title="Clasificación de clientes por estado"),
        st.Page("pages/orders.py", title="Número de pedidos por ciudad"),
        st.Page("pages/late_orders.py", title="Número de pedidos con retraso por ciudad"),
        st.Page("pages/reviews.py", title="Número de reviews")
    ],
    "Apartados extra" : [
    ]
}

pg = st.navigation(pages)
pg.run()