# tpcuanti3

import sqlite3
import streamlit as st
import pandas as pd

st.image("./1000048660 (1) (1).png")

# Código CSS para cambiar el estilo del título, subtítulo y fondo
page_style = """
<style>
    /* Cambia el color de fondo de la página */
    .stApp {
        background-color: #1f93f9;
    }

    /* Estilo para el título */
    h1 {
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Estilo para el subtítulo */
    h2 {
        color: white;
        font-size: 1.5em;
        font-weight: normal;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    /* Cambia el estilo de los botones */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 8px;
    }
    
    /* Cambia el color al pasar el mouse por encima */
    div.stButton > button:hover {
        background-color: #45a049;
    }
</style>
"""

# Aplica el CSS con st.markdown
st.markdown(page_style, unsafe_allow_html=True)

# Función para crear la tabla si no existe (incluyendo columna para el archivo PDF)
def create_table():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            author TEXT NOT NULL,
            pdf BLOB
        )
    ''')
    conn.commit()
    conn.close()

# Llamar a la función para crear la tabla antes de hacer cualquier otra operación
create_table()

# Función para agregar proyectos (incluyendo el archivo PDF)
def add_project(title, description, author, pdf_file):
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO projects (title, description, author, pdf)
        VALUES (?, ?, ?, ?)
    ''', (title, description, author, pdf_file))
    conn.commit()
    conn.close()

# Función para obtener todos los proyectos
def get_projects():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('SELECT title, description, author, pdf FROM projects')
    projects = c.fetchall()
    conn.close()
    return projects

# Interfaz de Streamlit
st.title('Plataforma para la Gestión y Publicación de proyectos comunitarios y solidarios')

# Formulario para subir proyectos
st.header('Subí tu proyecto para facilitar su visibilización y la gestión de voluntarios')
title = st.text_input('Título')
description = st.text_area('Descripción')
author = st.text_input('Autor')
pdf_file = st.file_uploader("Sube el archivo PDF del proyecto (opcional)", type=["pdf"])

if st.button('Subir'):
    if title and description and author:
        # Leer el archivo PDF si existe
        pdf_data = pdf_file.read() if pdf_file is not None else None
        add_project(title, description, author, pdf_data)
        st.success('Proyecto subido con éxito')
    else:
        st.error('Por favor, completa todos los campos')

# Mostrar proyectos
st.header('Ver Proyectos')
projects = get_projects()

for project in projects:
    st.subheader(project[0])
    st.write(f"**Descripción:** {project[1]}")
    st.write(f"**Autor:** {project[2]}")
    if project[3]:  # Si hay un archivo PDF
        st.download_button("Descargar PDF", data=project[3], file_name="proyecto.pdf", mime="application/pdf")
