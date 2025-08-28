import os
import shutil
import time
import streamlit as st

# Carpeta raíz
BASE_DIR = "cloudbox"
os.makedirs(BASE_DIR, exist_ok=True)

# Inicializar estado de la ruta actual
if "current_path" not in st.session_state:
    st.session_state.current_path = BASE_DIR

# Función para mostrar ícono según tipo de archivo
def get_file_icon(filename):
    ext = filename.lower()
    if ext.endswith((".xls", ".xlsx")):
        return "🟢 Excel"
    elif ext.endswith((".doc", ".docx")):
        return "🔵 Word"
    elif ext.endswith((".ppt", ".pptx")):
        return "🟠 PowerPoint"
    elif ext.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        return "🖼️ Imagen"
    else:
        return "🟤 Archivo"

# Función para eliminar carpeta y contenido
def eliminar_carpeta(carpeta):
    if os.path.exists(carpeta):
        try:
            shutil.rmtree(carpeta)  # elimina carpeta con todo adentro
            return True
        except Exception as e:
            st.error(f"Error al eliminar carpeta: {e}")
            return False
    return False

# Encabezado ruta actual
st.markdown(f"### 🟢 En línea - `{os.path.basename(st.session_state.current_path)}``")

# Botón volver (solo si no estamos en la raíz)
if st.session_state.current_path != BASE_DIR:
    if st.button("⬅️ Volver"):
        st.session_state.current_path = os.path.dirname(st.session_state.current_path)
        st.rerun()

# Crear nueva carpeta
st.subheader("📂 Crear nueva carpeta")
with st.form("crear_carpeta"):
    nueva_carpeta = st.text_input("Nombre de la nueva carpeta:")
    crear_btn = st.form_submit_button("➕ Crear")
    if crear_btn and nueva_carpeta.strip():
        nueva_ruta = os.path.join(st.session_state.current_path, nueva_carpeta.strip())
        if not os.path.exists(nueva_ruta):
            os.makedirs(nueva_ruta)
            st.success(f"✅ Carpeta '{nueva_carpeta}' creada")
            st.rerun()
        else:
            st.warning("⚠️ Ya existe una carpeta con ese nombre.")

# Listar carpetas y archivos en la ruta actual
items = os.listdir(st.session_state.current_path)
folders = [f for f in items if os.path.isdir(os.path.join(st.session_state.current_path, f))]
files = [f for f in items if os.path.isfile(os.path.join(st.session_state.current_path, f))]

# Mostrar carpetas
st.subheader("📁 Carpetas")
if folders:
    for carpeta in folders:
        ruta_carpeta = os.path.join(st.session_state.current_path, carpeta)
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            if st.button(f"📂 {carpeta}", key=f"abrir_{carpeta}"):
                st.session_state.current_path = ruta_carpeta
                st.rerun()
        with col2:
            nuevo_nombre = st.text_input(f"✏️ Renombrar {carpeta}", value=carpeta, key=f"rename_{carpeta}")
            if nuevo_nombre != carpeta:
                try:
                    nuevo_ruta = os.path.join(st.session_state.current_path, nuevo_nombre)
                    os.rename(ruta_carpeta, nuevo_ruta)
                    st.info(f"✏️ Renombrando carpeta '{carpeta}' → '{nuevo_nombre}' en 1 segundo...")
                    time.sleep(1)
                    st.success(f"✅ Carpeta renombrada a '{nuevo_nombre}'")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al renombrar: {e}")
        with col3:
            if st.button(f"🗑️ Eliminar {carpeta}", key=f"eliminar_{carpeta}"):
                st.warning(f"🗑️ Eliminando carpeta '{carpeta}' en 1 segundo...")
                time.sleep(1)
                if eliminar_carpeta(ruta_carpeta):
                    st.success(f"✅ Carpeta '{carpeta}' eliminada")
                    st.rerun()
else:
    st.write("📭 No hay carpetas en esta ubicación.")

# Mostrar archivos
st.subheader("📄 Archivos")
if files:
    for archivo in files:
        ruta_archivo = os.path.join(st.session_state.current_path, archivo)
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"{get_file_icon(archivo)} {archivo}")
        with col2:
            if st.button(f"🗑️ Eliminar {archivo}", key=f"del_file_{archivo}"):
                os.remove(ruta_archivo)
                st.success(f"✅ Archivo '{archivo}' eliminado")
                st.rerun()
else:
    st.write("📭 No hay archivos en esta ubicación.")
