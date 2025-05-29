import streamlit as st
from model import Model
from io import BytesIO
import base64
from PIL import Image



# Inicializar el modelo
model = Model()

# Título y estilo básico
st.set_page_config(page_title="Generador SVG", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎨 Generador de Imágenes SVG</h1>", unsafe_allow_html=True)

# Campo de entrada de texto
description = st.text_area("Escribe una descripción de la imagen que deseas generar:")

# Botón para generar imagen
if st.button("✨ Generar Imagen"):
    if description.strip() == "":
        st.warning("Por favor, ingresa una descripción.")
    else:
        with st.spinner("Generando imagen..."):
            
            #Generar el SVG usando el modelo
            svg_code = model.predict(description,True)

            # Mostrar el SVG
            st.markdown(f'<div style="text-align:center">{svg_code}</div>', unsafe_allow_html=True)
            
            # Botón de descarga
            b64 = base64.b64encode(svg_code.encode()).decode()
            href = f'<a href="data:image/svg+xml;base64,{b64}" download="imagen.svg">📥 Descargar SVG</a>'
            st.markdown(href, unsafe_allow_html=True)



