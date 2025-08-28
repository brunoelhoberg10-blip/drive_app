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
if "accion" not in st.session_state:
    st.session_state["accion"] = None
if "target" not in st.session_state:
    st.session_state["target"] = None
if "actualizado" not in st.session_state:
    st.session_state["actualizado"] = False
if "refresh_request" not in st.session_state:
    st.session_state["refresh_request"] = False

# -----------------------------
# Funciones
# -----------------------------
def listar(ruta):
    elementos = os.listdir(ruta)
    carpetas = [f for f in elementos if os.path.isdir(os.path.join(ruta, f))]
    archivos = [f for f in elementos if os.path.isfile(os.path.join(ruta, f))]
    return carpetas, archivos

def ir_atras():
    if st.session_state["ruta"] != ROOT_DIR:
        st.session_state["ruta"] = os.path.dirname(st.session_state["ruta"])
        st.experimental_rerun()

def refrescar():
    st.session_state["actualizado"] = True
    st.session_state["refresh_request"] = True

# Refresh seguro
if st.session_state["refresh_request"]:
    st.session_state["refresh_request"] = False
    st.experimental_rerun()

# -----------------------------
# Controles superiores
# -----------------------------
col1, col2, col3, col4 = st.columns([1,3,2,1])

# Botón Atrás
with col1:
    if st.session_state["ruta"] != ROOT_DIR:
        if st.button("⬅️ Atrás"):
            ir_atras()

# Carpeta actual
with col2:
    st.markdown(f"📂 **Carpeta actual:** `{st.session_state['ruta']}`")

# Crear carpeta nueva
with col3:
    nueva = st.text_input("📁 Nueva carpeta", key="nueva_carpeta")
    if st.button("➕ Crear carpeta"):
        if nueva:
            nueva_ruta = os.path.join(st.session_state["ruta"], nueva)
            os.makedirs(nueva_ruta, exist_ok=True)
            st.success(f"✅ Carpeta '{nueva}' creada")
            st.experimental_rerun()

# Botón actualizar
with col4:
    if st.button("🔄 Actualizar"):
        refrescar()

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
    st.experimental_rerun()

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

    # Navegar
    if col1.button(f"📁 {carpeta}", key=f"open_{carpeta}"):
        st.session_state["accion"] = "abrir_carpeta"
        st.session_state["target"] = carpeta_path

    # Editar
    nuevo_nombre = col2.text_input("", key=f"edit_{carpeta}", value=carpeta)
    if col2.button("✏️", key=f"save_{carpeta}"):
        st.session_state["accion"] = "renombrar_carpeta"
        st.session_state["target"] = (carpeta_path, nuevo_nombre)

    # Eliminar
    if col3.button("🗑️", key=f"del_{carpeta}"):
        st.session_state["accion"] = "eliminar_carpeta"
        st.session_state["target"] = carpeta_path

# Archivos
for archivo in archivos:
    ruta_archivo = os.path.join(st.session_state["ruta"], archivo)
    col1, col2, col3 = st.columns([4,1,1])
    
    with col1:
        st.markdown(f"📄 **{archivo}**")

    with col2:
        with open(ruta_archivo, "rb") as f:
            st.download_button("⬇️ Descargar", f, file_name=archivo, key=f"down_{archivo}")

    with col3:
        if st.button("🗑️", key=f"del_file_{archivo}"):
            st.session_state["accion"] = "eliminar_archivo"
            st.session_state["target"] = ruta_archivo

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

# -----------------------------
# Ejecutar acción fuera de bucles (seguro)
# -----------------------------
if st.session_state["accion"]:
    if st.session_state["accion"] == "abrir_carpeta":
        st.session_state["ruta"] = st.session_state["target"]
    elif st.session_state["accion"] == "renombrar_carpeta":
        carpeta_path, nuevo_nombre = st.session_state["target"]
        nueva_ruta = os.path.join(st.session_state["ruta"], nuevo_nombre)
        os.rename(carpeta_path, nueva_ruta)
    elif st.session_state["accion"] == "eliminar_carpeta":
        shutil.rmtree(st.session_state["target"])
    elif st.session_state["accion"] == "eliminar_archivo":
        os.remove(st.session_state["target"])

    # Limpiar estado y recargar
    st.session_state["accion"] = None
    st.session_state["target"] = None
    st.experimental_rerun()