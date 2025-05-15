import streamlit as st

st.title("Análisis de Datos del E-commerce Olist")

st.markdown("""
Este proyecto consiste en el análisis del dataset de Olist, un e-commerce brasileño.
Se estudian aspectos como el comportamiento del cliente, tiempos de entrega, productos más vendidos, y más,
para encontrar patrones valiosos y mejorar la toma de decisiones del negocio.
""")

st.header("Participantes del Proyecto")

participantes = [
    {"nombre": "Marcos Ballesteros", "imagen": "../resources/images/marcos.png"},
    {"nombre": "Daniel Llamas", "imagen": "../resources/images/llamas.png"},
    {"nombre": "Carlos Muñoz", "imagen": "../resources/images/carlos.jpg"}
]

for p in participantes:
    cols = st.columns([1, 4]) 
    with cols[0]:
        st.image(p["imagen"], width=100)
    with cols[1]:
        st.subheader(p["nombre"])
