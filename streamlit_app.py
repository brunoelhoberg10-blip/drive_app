import os
import shutil
import streamlit as st

# -----------------------------
# Configuración
# -----------------------------
st.set_page_config(page_title="CloudBox Empresarial", page_icon="☁️", layout="wide")
st.markdown("<h1 style='text-align:center; color:#2E86C1;'>☁️ CloudBox Empresarial</h1>", unsafe_allow_html=True)

# -----------------------------
# Carpeta raíz
# -----------------------------
ROOT_DIR = "cloudbox"
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)

# -----------------------------
# Estado de sesión
# -----------------------------
if "ruta" not in st.session_state:
    st.session_state["ruta"] = ROOT_DIR
if "actualizado" not in st.session_state:
    st.session_state["actualizado"] = False

# -----------------------------
# Funciones auxiliares
# -----------------------------
def listar(ruta):
    elementos = os.listdir(ruta)
    carpetas = [f for f in elementos if os.path.isdir(os.path.join(ruta, f))]
    archivos = [f for f in elementos if os.path.isfile(os.path.join(ruta, f))]
    return carpetas, archivos

# -----------------------------
# Controles superiores
# -----------------------------
col1, col2, col3, col4 = st.columns([1,3,2,1])

# Atrás
with col1:
    if st.session_state["ruta"] != ROOT_DIR:
        if st.button("⬅️ Atrás"):
            st.session_state["ruta"] = os.path.dirname(st.session_state["ruta"])

# Carpeta actual
with col2:
    st.markdown(f"📂 **Carpeta actual:** `{st.session_state['ruta']}`")

# Crear carpeta
with col3:
    nueva = st.text_input("📁 Nueva carpeta", key="nueva_carpeta")
    if st.button("➕ Crear carpeta"):
        if nueva:
            nueva_ruta = os.path.join(st.session_state["ruta"], nueva)
            os.makedirs(nueva_ruta, exist_ok=True)
            st.success(f"📂 Carpeta '{nueva}' creada")

import time

# Actualizar
with col4:
    if st.button("🔄 Actualizar"):
        placeholder = st.empty()  # Contenedor temporal
        placeholder.success("📌 Página actualizada")
        time.sleep(2)  # Esperar 2 segundos
        placeholder.empty()  # Borrar el mensaje
        st.session_state["actualizado"] = True


if st.session_state["actualizado"]:
    st.success("📌 Página actualizada")
    st.session_state["actualizado"] = False

st.divider()

# -----------------------------
# Subir archivos múltiples
# -----------------------------
st.subheader("⬆️ Subir archivos")
archivos_subir = st.file_uploader("Selecciona archivos", type=None, accept_multiple_files=True)
if archivos_subir:
    for archivo in archivos_subir:
        ruta_guardar = os.path.join(st.session_state["ruta"], archivo.name)
        with open(ruta_guardar, "wb") as f:
            f.write(archivo.read())
    st.success(f"✅ {len(archivos_subir)} archivo(s) subido(s) con éxito")

st.divider()

# -----------------------------
# Listar carpetas y archivos
# -----------------------------
st.subheader("📂 Contenido de la carpeta")
carpetas, archivos = listar(st.session_state["ruta"])

# Carpetas
for carpeta in carpetas:
    carpeta_path = os.path.join(st.session_state["ruta"], carpeta)
    col1, col2, col3 = st.columns([4,1,1])

    # Abrir carpeta
    if col1.button(f"📁 {carpeta}", key=f"open_{carpeta}"):
        st.session_state["ruta"] = carpeta_path
        st.experimental_rerun = False  # Solo para asegurar que Streamlit rerenderiza automáticamente

    # Editar carpeta
    nuevo_nombre = col2.text_input("", key=f"edit_{carpeta}", value=carpeta)
    if col2.button("✏️", key=f"save_{carpeta}"):
        if nuevo_nombre and nuevo_nombre != carpeta:
            nueva_ruta = os.path.join(st.session_state["ruta"], nuevo_nombre)
            os.rename(carpeta_path, nueva_ruta)
            st.success(f"✏️ Carpeta renombrada a '{nuevo_nombre}'")
            # Actualizar lista de carpetas
            carpetas, _ = listar(st.session_state["ruta"])

    # Eliminar carpeta
    if col3.button("🗑️", key=f"del_{carpeta}"):
        shutil.rmtree(carpeta_path)
        st.success(f"🗑️ Carpeta '{carpeta}' eliminada")
        # Actualizar lista de carpetas
        carpetas, _ = listar(st.session_state["ruta"])

# Archivos
for archivo in archivos:
    ruta_archivo = os.path.join(st.session_state["ruta"], archivo)
    col1, col2, col3 = st.columns([4,1,1])
    
    with col1:
        st.markdown(f"📄 **{archivo}**")

    # Descargar
    with col2:
        with open(ruta_archivo, "rb") as f:
            st.download_button("⬇️ Descargar", f, file_name=archivo, key=f"down_{archivo}")

    # Eliminar archivo
    with col3:
        if st.button("🗑️", key=f"del_file_{archivo}"):
            os.remove(ruta_archivo)
            st.success(f"🗑️ Archivo '{archivo}' eliminado")
            archivos = listar(st.session_state["ruta"])[1]  # Actualizar lista de archivos

    # Vista previa universal
    ext = archivo.lower().split(".")[-1]
    if ext in ["png", "jpg", "jpeg", "gif"]:
        st.image(ruta_archivo, use_column_width=True)
    elif ext == "pdf":
        st.write("📖 Vista previa PDF (abrir en visor externo o descargar):")
        with open(ruta_archivo, "rb") as f:
            st.download_button("📂 Abrir PDF", f, file_name=archivo, key=f"view_{archivo}")
    elif ext in ["txt", "csv", "md"]:
        with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f:
            contenido = f.read()
        st.text_area("📜 Contenido:", contenido, height=200, key=f"text_{archivo}")
    else:
        st.info("🛈 Vista previa solo disponible para imágenes, PDF y textos. Usa el botón 'Descargar' para abrir este archivo.")
