import os
import streamlit as st

# --- Configuración de la app ---
st.set_page_config(page_title="CloudBox", page_icon="☁️", layout="wide")
st.markdown("<h1 style='text-align:center; color:#2E86C1;'>☁️ CloudBox Empresarial</h1>", unsafe_allow_html=True)

# --- Carpeta raíz ---
ROOT_DIR = "cloudbox"
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)

# --- Estado de la sesión (navegación de carpetas) ---
if "ruta" not in st.session_state:
    st.session_state["ruta"] = ROOT_DIR

# --- Funciones ---
def listar(ruta):
    elementos = os.listdir(ruta)
    archivos = [f for f in elementos if os.path.isfile(os.path.join(ruta, f))]
    carpetas = [f for f in elementos if os.path.isdir(os.path.join(ruta, f))]
    return carpetas, archivos

def ir_atras():
    if st.session_state["ruta"] != ROOT_DIR:
        st.session_state["ruta"] = os.path.dirname(st.session_state["ruta"])
        st.rerun()

# --- Controles superiores ---
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("⬅️ Atrás"):
        ir_atras()
with col2:
    st.write(f"📂 Carpeta actual: `{st.session_state['ruta']}`")
with col3:
    nueva = st.text_input("📁 Nueva carpeta", "")
    if st.button("➕ Crear") and nueva:
        os.makedirs(os.path.join(st.session_state["ruta"], nueva), exist_ok=True)
        st.success(f"✅ Carpeta '{nueva}' creada")
        st.rerun()

# --- Subir archivos ---
st.divider()
st.subheader("⬆️ Subir archivo")
archivo = st.file_uploader("Selecciona un archivo para subir", type=None)
if archivo:
    ruta_guardar = os.path.join(st.session_state["ruta"], archivo.name)
    with open(ruta_guardar, "wb") as f:
        f.write(archivo.read())
    st.success(f"✅ Archivo '{archivo.name}' subido correctamente")
    st.rerun()

# --- Listar carpetas y archivos ---
st.divider()
st.subheader("📂 Contenido de la carpeta")

carpetas, archivos = listar(st.session_state["ruta"])

# --- Mostrar carpetas ---
for carpeta in carpetas:
    if st.button(f"📁 {carpeta}", key=f"carpeta_{carpeta}"):
        st.session_state["ruta"] = os.path.join(st.session_state["ruta"], carpeta)
        st.rerun()

# --- Mostrar archivos ---
for archivo in archivos:
    ruta_archivo = os.path.join(st.session_state["ruta"], archivo)
    col1, col2, col3 = st.columns([4,1,1])
    with col1:
        st.write(f"📄 {archivo}")
    with col2:
        with open(ruta_archivo, "rb") as f:
            st.download_button("⬇️ Descargar", f, file_name=archivo, key=f"down_{archivo}")
    with col3:
        if st.button("🗑️ Eliminar", key=f"del_{archivo}"):
            os.remove(ruta_archivo)
            st.rerun()

    # --- Vista previa ---
    if archivo.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        st.image(ruta_archivo, use_column_width=True)
    elif archivo.lower().endswith(".pdf"):
        st.write("📖 Vista previa PDF (descarga para abrir en visor externo):")
        with open(ruta_archivo, "rb") as f:
            st.download_button("📂 Abrir PDF", f, file_name=archivo, key=f"view_{archivo}")
    elif archivo.lower().endswith((".txt", ".csv", ".md")):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        st.text_area("📜 Contenido:", contenido, height=200, key=f"text_{archivo}")