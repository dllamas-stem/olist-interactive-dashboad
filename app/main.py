# python 3.11

import streamlit as st

pages = {
    "Presentación" : [
        st.Page("introduction.py", title="Introducción")
    ],
    "Apartados obligatorios" : [
        st.Page("customers.py", title="Clasificación de clientes por estado"),
        st.Page("orders.py", title="Número de pedidos por ciudad"),
        st.Page("late_orders.py", title="Número de pedidos con retraso por ciudad"),
        st.Page("reviews.py", title="Número de reviews")
    ],
    "Apartados extra" : [
    ]
}

pg = st.navigation(pages)
pg.run()