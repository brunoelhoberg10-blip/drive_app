import os
import streamlit as st

# Carpeta raíz donde se guardan los archivos (en la nube de Streamlit será temporal)
ROOT_DIR = "mis_archivos"

# Crear carpeta raíz si no existe
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)

# Función para listar archivos y carpetas
def listar_archivos(ruta):
    elementos = os.listdir(ruta)
    archivos = [f for f in elementos if os.path.isfile(os.path.join(ruta, f))]
    carpetas = [f for f in elementos if os.path.isdir(os.path.join(ruta, f))]
    return carpetas, archivos

# Interfaz
st.title("📂 Mi Google Drive Casero")

# Navegación entre carpetas
if "ruta" not in st.session_state:
    st.session_state["ruta"] = ROOT_DIR

st.write(f"📍 Estás en: `{st.session_state['ruta']}`")

carpetas, archivos = listar_archivos(st.session_state["ruta"])

# Mostrar carpetas
st.subheader("📁 Carpetas")
for carpeta in carpetas:
    if st.button(f"📂 {carpeta}"):
        st.session_state["ruta"] = os.path.join(st.session_state["ruta"], carpeta)
        st.rerun()

# Subir archivos
st.subheader("⬆️ Subir archivo")
archivo = st.file_uploader("Elige un archivo", type=None)
if archivo:
    ruta_guardar = os.path.join(st.session_state["ruta"], archivo.name)
    with open(ruta_guardar, "wb") as f:
        f.write(archivo.getbuffer())
    st.success(f"Archivo **{archivo.name}** subido con éxito ✅")
    st.rerun()

# Crear nueva carpeta
st.subheader("📂 Crear carpeta")
nueva_carpeta = st.text_input("Nombre de la carpeta:")
if st.button("Crear carpeta"):
    if nueva_carpeta:
        os.makedirs(os.path.join(st.session_state["ruta"], nueva_carpeta), exist_ok=True)
        st.success(f"Carpeta **{nueva_carpeta}** creada ✅")
        st.rerun()

# Listar archivos
st.subheader("📄 Archivos en esta carpeta")
for archivo in archivos:
    col1, col2 = st.columns([3, 1])
    col1.write(archivo)
    if col2.button("🗑️ Eliminar", key=archivo):
        os.remove(os.path.join(st.session_state["ruta"], archivo))
        st.warning(f"Archivo **{archivo}** eliminado ❌")
        st.rerun()

# Botón para volver atrás
if st.session_state["ruta"] != ROOT_DIR:
    if st.button("⬅️ Volver"):
        st.session_state["ruta"] = os.path.dirname(st.session_state["ruta"])
        st.rerun()