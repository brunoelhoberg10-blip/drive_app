import os
import shutil
import time
import streamlit as st

# -----------------------------
# Configuración de la página
# -----------------------------
st.set_page_config(
    page_title="CloudBox Empresarial",
    page_icon="☁️",
    layout="wide"
)
st.markdown(
    "<h1 style='text-align:center; color:#2E86C1;'>☁️ CloudBox Empresarial</h1>",
    unsafe_allow_html=True
)

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
if "uploader_count" not in st.session_state:
    st.session_state["uploader_count"] = 0
if "reload" not in st.session_state:
    st.session_state["reload"] = False

# -----------------------------
# Manejo de recarga después de acciones
# -----------------------------
if st.session_state["reload"]:
    st.session_state["reload"] = False
    st.experimental_rerun()

# -----------------------------
# Funciones auxiliares
# -----------------------------
def listar(ruta):
    elementos = os.listdir(ruta)
    carpetas = [f for f in elementos if os.path.isdir(os.path.join(ruta, f))]
    archivos = [f for f in elementos if os.path.isfile(os.path.join(ruta, f))]
    return carpetas, archivos

def estilo_archivo(nombre):
    ext = nombre.lower().split(".")[-1]
    if ext in ["xls", "xlsx", "xlsm"]:
        return "🟩 Excel"
    elif ext in ["doc", "docx"]:
        return "🟦 Word"
    elif ext in ["ppt", "pptx"]:
        return "🟧 PowerPoint"
    elif ext in ["png", "jpg", "jpeg", "gif"]:
        return "🖼️ Imagen"
    else:
        return "🟫 Otro"

# -----------------------------
# Controles superiores
# -----------------------------
col1, col2, col3, col4 = st.columns([1,3,2,1])

# Atrás solo si no estamos en la raíz (comparación absoluta)
with col1:
    if os.path.abspath(st.session_state["ruta"]) != os.path.abspath(ROOT_DIR):
        if st.button("⬅️ Atrás"):
            st.session_state["ruta"] = os.path.dirname(st.session_state["ruta"])
            st.session_state["reload"] = True

# Carpeta actual estilo "En línea"
with col2:
    st.markdown(
        f"🟢 **En línea - {os.path.basename(st.session_state['ruta'])}**",
        unsafe_allow_html=True
    )

# Crear carpeta
with col3:
    nueva = st.text_input("📁 Nueva carpeta", key="nueva_carpeta")
    if st.button("➕ Crear carpeta"):
        if nueva:
            nueva_ruta = os.path.join(st.session_state["ruta"], nueva)
            os.makedirs(nueva_ruta, exist_ok=True)
            st.success(f"📂 Carpeta '{nueva}' creada")
            time.sleep(1)
            st.session_state["reload"] = True

# Actualizar
with col4:
    if st.button("🔄 Actualizar"):
        st.success("📌 Página actualizada")
        time.sleep(1)
        st.session_state["reload"] = True

st.divider()

# -----------------------------
# Subir archivos (solo dentro de carpetas)
# -----------------------------
if os.path.abspath(st.session_state["ruta"]) != os.path.abspath(ROOT_DIR):
    st.subheader("⬆️ Subir archivos")
    uploader_key = f"uploader_{st.session_state['uploader_count']}"
    archivos_subir = st.file_uploader(
        "Selecciona archivos", type=None, accept_multiple_files=True, key=uploader_key
    )

    if archivos_subir:
        if not os.path.exists(st.session_state["ruta"]):
            os.makedirs(st.session_state["ruta"])
        
        for archivo in archivos_subir:
            ruta_guardar = os.path.join(st.session_state["ruta"], archivo.name)
            with open(ruta_guardar, "wb") as f:
                f.write(archivo.read())
        st.success(f"✅ {len(archivos_subir)} archivo(s) subido(s) con éxito")
        time.sleep(1)

        st.session_state["uploader_count"] += 1
        st.session_state["reload"] = True

st.divider()

# -----------------------------
# Listar carpetas y archivos
# -----------------------------
st.subheader("📂 Contenido de la carpeta")
carpetas, archivos = listar(st.session_state["ruta"])

# Mostrar solo carpetas si estamos en la raíz
if os.path.abspath(st.session_state["ruta"]) == os.path.abspath(ROOT_DIR):
    archivos = []

# -----------------------------
# Manejo de carpetas con menú
# -----------------------------
for carpeta in carpetas:
    carpeta_path = os.path.join(st.session_state["ruta"], carpeta)
    col1, col2 = st.columns([4,1])

    # Abrir carpeta
    with col1:
        if st.button(f"📁 {carpeta}", key=f"open_{carpeta}"):
            st.session_state["ruta"] = carpeta_path
            st.session_state["reload"] = True

    # Menú de opciones
    with col2:
        accion = st.selectbox(
            "Opciones", ["", "Editar", "Eliminar"], key=f"menu_{carpeta}", index=0
        )

        # Eliminar carpeta con confirmación y 1 segundo de espera
        if accion == "Eliminar":
            confirmar = st.button(f"Confirmar eliminación '{carpeta}'", key=f"confirm_del_{carpeta}")
            if confirmar:
                st.warning(f"🗑️ Eliminando carpeta '{carpeta}' en 1 segundo...")
                time.sleep(1)
                shutil.rmtree(carpeta_path)
                st.success(f"✅ Carpeta '{carpeta}' eliminada")
                st.session_state["reload"] = True

        # Editar carpeta: cambiar nombre con Enter o botón Guardar
        if accion == "Editar":
            nuevo_nombre = st.text_input(
                "Nuevo nombre:", value=carpeta, key=f"edit_{carpeta}"
            )

            if st.session_state.get(f"enter_pressed_{carpeta}", False):
                st.session_state[f"enter_pressed_{carpeta}"] = False
                if nuevo_nombre and nuevo_nombre != carpeta:
                    nueva_ruta = os.path.join(st.session_state["ruta"], nuevo_nombre)
                    time.sleep(1)  # esperar 1 segundo antes de renombrar
                    os.rename(carpeta_path, nueva_ruta)
                    st.success(f"✏️ Carpeta renombrada a '{nuevo_nombre}'")
                    st.session_state["reload"] = True

            if st.button("Guardar", key=f"save_{carpeta}"):
                st.session_state[f"enter_pressed_{carpeta}"] = True

# -----------------------------
# Manejo de archivos (solo dentro de carpetas)
# -----------------------------
for archivo in archivos:
    ruta_archivo = os.path.join(st.session_state["ruta"], archivo)
    col1, col2, col3 = st.columns([4,1,1])
    with col1:
        st.markdown(f"{estilo_archivo(archivo)} **{archivo}**")
    with col2:
        with open(ruta_archivo, "rb") as f:
            st.download_button("⬇️ Descargar", f, file_name=archivo, key=f"down_{archivo}")
    with col3:
        if st.button("🗑️", key=f"del_file_{archivo}"):
            os.remove(ruta_archivo)
            st.success(f"🗑️ Archivo '{archivo}' eliminado")
            time.sleep(1)
            st.session_state["reload"] = True

    # Vista previa
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
