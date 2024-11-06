import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.image("./1000048660 (1) (1).png")

# Código CSS para cambiar el estilo del título, subtítulo, fondo y navegación en la esquina superior izquierda
page_style = """
<style>
    .stApp {
        background-color: #1f93f9;
    }
    h1 {
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    h2 {
        color: white;
        font-size: 1.5em;
        font-weight: normal;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 20px;
    }
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
    div.stButton > button:hover {
        background-color: #45a049;
    }
    .nav {
        position: fixed;
        top: 10px;
        left: 10px;
    }
    .nav button {
        font-size: 1.1em;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        margin: 4px;
        cursor: pointer;
        border-radius: 8px;
    }
    .nav button:hover {
        background-color: #45a049;
    }
</style>
"""

# Aplica el CSS con st.markdown
st.markdown(page_style, unsafe_allow_html=True)

# Función para crear la tabla si no existe (incluyendo columna para la categoría)
def create_table():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            pdf BLOB
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Función para agregar proyectos (incluyendo la categoría y el archivo PDF)
def add_project(title, description, author, category, pdf_file):
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO projects (title, description, author, category, pdf)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, author, category, pdf_file))
    conn.commit()
    conn.close()

# Función para obtener todos los proyectos
def get_projects(category=None):
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    if category:
        c.execute('SELECT title, description, author, category, pdf FROM projects WHERE category = ?', (category,))
    else:
        c.execute('SELECT title, description, author, category, pdf FROM projects')
    projects = c.fetchall()
    conn.close()
    return projects

# Función para obtener el conteo de proyectos por categoría
def get_category_counts():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('SELECT category, COUNT(*) FROM projects GROUP BY category')
    category_counts = dict(c.fetchall())
    conn.close()
    return category_counts

# Navegación entre páginas
st.markdown("<div class='nav'><button onclick='window.location.href = \"#proyectos\"'>Proyectos</button><button onclick='window.location.href = \"#estadisticas\"'>Estadísticas</button></div>", unsafe_allow_html=True)

# Mostrar contenido basado en la navegación
section = st.radio("Ir a:", ["Proyectos", "Estadísticas"], index=0)

if section == "Proyectos":
    # Página de Proyectos
    st.title('Plataforma para la Gestión y Publicación de proyectos comunitarios y solidarios')

    # Formulario para subir proyectos
    st.header('Subí tu proyecto para facilitar su visibilización y la gestión de voluntarios')
    title = st.text_input('Título')
    description = st.text_area('Descripción')
    author = st.text_input('Autor')

    # Selección de categoría
    category = st.selectbox(
        'Selecciona la categoría del proyecto',
        ['Solidario/Comunitario', 'Apoyo Escolar', 'Capacitaciones', 'Recreativo', 'Otro']
    )

    pdf_file = st.file_uploader("Sube el archivo PDF del proyecto (opcional)", type=["pdf"])

    if st.button('Subir'):
        if title and description and author and category:
            # Leer el archivo PDF si existe
            pdf_data = pdf_file.read() if pdf_file is not None else None
            add_project(title, description, author, category, pdf_data)
            st.success('Proyecto subido con éxito')
        else:
            st.error('Por favor, completa todos los campos')

    # Mostrar proyectos
    st.header('Ver Proyectos')

    # Filtro de categoría
    selected_category = st.selectbox(
        "Filtrar por categoría",
        ["Todas"] + ['Solidario/Comunitario', 'Apoyo Escolar', 'Capacitaciones', 'Recreativo', 'Otro']
    )

    projects = get_projects(None if selected_category == "Todas" else selected_category)

    for idx, project in enumerate(projects):
        st.subheader(project[0])
        st.write(f"**Descripción:** {project[1]}")
        st.write(f"**Autor:** {project[2]}")
        st.write(f"**Categoría:** {project[3]}")
        if project[4]:  # Si hay un archivo PDF
            st.download_button(
                f"Descargar PDF - {project[0]}",  # Nombre único para cada botón
                data=project[4],
                file_name=f"{project[0]}.pdf",  # También puedes usar el título del proyecto en el nombre del archivo
                mime="application/pdf"
            )

elif section == "Estadísticas":
    # Página de Estadísticas
    st.title("Estadísticas")

    # Obtener los datos de conteo por categoría
    category_counts = get_category_counts()
    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    # Crear gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(categories, counts, color='skyblue')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Número de Proyectos')
    ax.set_title('Número de proyectos por categoría')
    
    st.pyplot(fig)
