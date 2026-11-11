import streamlit as st
from pathlib import Path

# ============================================================
# SDS | Adaptación web del programa original de escritorio
# ============================================================

ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
ALFABETO_INV = ALFABETO[::-1]

FONDO = "#F1F5F9"
BLANCO = "#FFFFFF"
AZUL_OSCURO = "#14213D"
AZUL = "#2563EB"
VERDE = "#059669"
ROJO = "#DC2626"
TEXTO = "#1E293B"
GRIS = "#64748B"
BORDE = "#E2E8F0"

# ============================================================
# MÉTODO 1: CIFRADO CÉSAR (misma lógica del código original)
# ============================================================

def cifrado_cesar(texto, clave):
    resultado = ""
    for caracter in texto:
        letra = caracter.upper()
        if letra in ALFABETO:
            posicion = ALFABETO.index(letra)
            nueva_posicion = (posicion + clave) % len(ALFABETO)
            nueva_letra = ALFABETO[nueva_posicion]
            if caracter.islower():
                nueva_letra = nueva_letra.lower()
            resultado += nueva_letra
        else:
            resultado += caracter
    return resultado

# ============================================================
# MÉTODO 2: SUSTITUCIÓN MONOALFABÉTICA
# ============================================================

def cifrado_sustitucion(texto):
    resultado = ""
    for caracter in texto:
        letra = caracter.upper()
        if letra in ALFABETO:
            posicion = ALFABETO.index(letra)
            nueva_letra = ALFABETO_INV[posicion]
            if caracter.islower():
                nueva_letra = nueva_letra.lower()
            resultado += nueva_letra
        else:
            resultado += caracter
    return resultado

def descifrado_sustitucion(texto):
    # El alfabeto invertido es su propia operación inversa.
    return cifrado_sustitucion(texto)

# ============================================================
# MÉTODO 3: TRANSPOSICIÓN
# ============================================================

def cifrado_transposicion(texto, columnas):
    if columnas < 1:
        raise ValueError("La cantidad de columnas debe ser mayor que cero.")
    resultado = ""
    for columna in range(columnas):
        resultado += texto[columna::columnas]
    return resultado

def descifrado_transposicion(texto, columnas):
    if columnas < 1:
        raise ValueError("La cantidad de columnas debe ser mayor que cero.")
    longitud = len(texto)
    if longitud == 0:
        return ""
    filas = (longitud + columnas - 1) // columnas
    sobrantes = longitud % columnas
    longitudes = [
        filas if sobrantes == 0 or columna < sobrantes
        else filas - 1
        for columna in range(columnas)
    ]
    partes = []
    inicio = 0
    for cantidad in longitudes:
        partes.append(texto[inicio:inicio + cantidad])
        inicio += cantidad
    resultado = ""
    for fila in range(filas):
        for columna in range(columnas):
            if fila < len(partes[columna]):
                resultado += partes[columna][fila]
    return resultado

# ============================================================
# MÉTODO 4: CIFRADO COMBINADO
# ============================================================

def cifrar_combinado(texto, clave, columnas):
    paso1 = cifrado_cesar(texto, clave)
    paso2 = cifrado_sustitucion(paso1)
    paso3 = cifrado_transposicion(paso2, columnas)
    return paso3

def descifrar_combinado(texto, clave, columnas):
    paso1 = descifrado_transposicion(texto, columnas)
    paso2 = descifrado_sustitucion(paso1)
    paso3 = cifrado_cesar(paso2, -clave)
    return paso3

# ============================================================
# CONFIGURACIÓN VISUAL
# ============================================================

st.set_page_config(
    page_title="SDS | Sistema de Cifrado y Descifrado",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"""
<style>
    .stApp {{ background: {FONDO}; color: {TEXTO}; }}
    [data-testid="stSidebar"] {{ background: {AZUL_OSCURO}; }}
    [data-testid="stSidebar"] * {{ color: {BLANCO} !important; }}
    .sds-brand {{ color: {BLANCO}; font-size: 2.2rem; font-weight: 800;
                  margin: 0 0 .1rem 0; }}
    .sds-subbrand {{ color: #94A3B8; font-size: .68rem; font-weight: 700;
                     letter-spacing: .08em; }}
    .sds-project {{ color: #94A3B8; font-size: .82rem; line-height: 1.7; }}
    .sds-header {{ background: {BLANCO}; padding: 1.15rem 1.5rem;
                   border: 1px solid {BORDE}; border-radius: 12px;
                   margin-bottom: 1.25rem; }}
    .sds-header h2 {{ color: {AZUL_OSCURO}; margin: 0; font-size: 1.35rem; }}
    .sds-header p {{ color: {GRIS}; margin: .25rem 0 0 0; }}
    .sds-welcome {{ background: {AZUL_OSCURO}; padding: 2rem;
                    border-radius: 12px; color: white; margin-bottom: 1rem; }}
    .sds-welcome h1 {{ color: white; margin: 0; }}
    .sds-welcome p {{ color: #CBD5E1; margin-bottom: 0; }}
    .sds-card {{ background: white; border: 1px solid {BORDE};
                 border-radius: 12px; padding: 1.25rem 1.4rem;
                 margin-bottom: 1rem; }}
    .sds-card h3 {{ color: {AZUL}; font-size: 1rem; margin-top: 0; }}
    div.stButton > button {{ border-radius: 8px; font-weight: 700; }}
    div[data-testid="stTextArea"] textarea {{
        background: #F8FAFC; color: {TEXTO}; font-family: Consolas, monospace;
    }}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# MENÚ LATERAL / NAVEGACIÓN (equivalente al menú Tkinter)
# ============================================================

with st.sidebar:
    st.markdown('<div class="sds-brand">SDS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sds-subbrand">SISTEMA DE CRIPTOGRAFÍA</div>', unsafe_allow_html=True)
    st.divider()
    st.caption("MENÚ PRINCIPAL")
    pagina = st.radio(
        "Navegación",
        ["⌂  Inicio", "01  Cifrado César", "02  Sustitución",
         "03  Transposición", "04  Cifrado combinado", "05  Código utilizado"],
        label_visibility="collapsed",
        key="sds_pagina",
    )
    st.divider()
    st.markdown(
        '<div class="sds-project"><b>PROYECTO ACADÉMICO</b><br><br>'
        'SDS<br>Matemáticas<br>Programación<br>Criptografía básica</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# PANTALLA DE INICIO
# ============================================================

if pagina == "⌂  Inicio":
    st.markdown("""
    <div class="sds-header">
      <h2>BIENVENIDO A SDS</h2>
      <p>Inicio / Información general de la aplicación</p>
    </div>
    <div class="sds-welcome">
      <h1>¡BIENVENIDO A SDS!</h1>
      <p>Descubre cómo las matemáticas permiten proteger y transformar la información.</p>
    </div>
    """, unsafe_allow_html=True)

    tarjetas = [
        ("¿QUÉ ES SDS?",
         "SDS es una aplicación educativa diseñada para comprender los fundamentos de la criptografía. "
         "Permite escribir mensajes, convertirlos en textos codificados y recuperar su contenido original "
         "mediante diferentes procedimientos matemáticos y de programación."),
        ("¿CÓMO FUNCIONA LA APLICACIÓN?",
         "1. Selecciona un método en el menú ubicado a la izquierda.\n\n"
         "2. Escribe el mensaje que deseas cifrar o descifrar.\n\n"
         "3. Introduce las claves solicitadas por el método elegido.\n\n"
         "4. Presiona CIFRAR para transformar el mensaje.\n\n"
         "5. Para recuperar el texto original, coloca el mensaje codificado en el espacio de entrada y presiona DESCIFRAR.\n\n"
         "6. Presiona BORRAR para limpiar los dos espacios y comenzar una nueva operación."),
        ("MÉTODOS DE CIFRADO DISPONIBLES",
         "01. CIFRADO CÉSAR\nDesplaza las letras del alfabeto según una clave numérica.\n\n"
         "02. SUSTITUCIÓN MONOALFABÉTICA\nReemplaza cada letra por su equivalente en el alfabeto invertido.\n\n"
         "03. TRANSPOSICIÓN\nModifica el orden de los caracteres utilizando columnas.\n\n"
         "04. CIFRADO COMBINADO\nAplica consecutivamente los tres métodos anteriores."),
        ("RECOMENDACIONES IMPORTANTES",
         "• Utiliza las mismas claves al cifrar y descifrar.\n\n"
         "• En César, recuerda el desplazamiento numérico utilizado.\n\n"
         "• En transposición, conserva la cantidad de columnas.\n\n"
         "• Introduce el mensaje codificado completo al descifrar.\n\n"
         "• Esta aplicación tiene fines educativos y no debe utilizarse como sistema de protección de información confidencial."),
    ]
    for titulo, contenido in tarjetas:
        st.markdown(
            f'<div class="sds-card"><h3>{titulo}</h3><div style="white-space:pre-line;color:{TEXTO}">{contenido}</div></div>',
            unsafe_allow_html=True,
        )
    st.caption("SDS | MATEMÁTICAS, PROGRAMACIÓN Y CRIPTOGRAFÍA")

# ============================================================
# PANTALLA: CÓDIGO UTILIZADO
# ============================================================

elif pagina == "05  Código utilizado":
    st.markdown("""
    <div class="sds-header">
      <h2>CÓDIGO UTILIZADO</h2>
      <p>Información del desarrollo y código fuente completo de SDS</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sds-card"><h3>¿QUÉ CÓDIGO UTILIZAMOS Y PARA QUÉ SIRVE?</h3>'
                'Este es el código fuente que utilizamos para desarrollar la aplicación SDS '
                '(Sistema de Cifrado y Descifrado). Fue programado originalmente en Python '
                'utilizando la biblioteca Tkinter para construir la interfaz gráfica.<br><br>'
                'Su función es permitir que el usuario escriba mensajes, los cifre y posteriormente '
                'los descifre mediante cuatro métodos: cifrado César, sustitución monoalfabética, '
                'transposición y cifrado combinado. El programa también valida las claves ingresadas, '
                'muestra los resultados y permite borrar los textos para realizar nuevas operaciones.'
                '</div>', unsafe_allow_html=True)

    source_file = Path(__file__).with_name("codigo_fuente_sds.py")
    st.markdown("### CÓDIGO FUENTE COMPLETO")
    if source_file.exists():
        source = source_file.read_text(encoding="utf-8")
        st.code(source, language="python", line_numbers=True)
        st.download_button(
            "Descargar código fuente original",
            data=source,
            file_name="SDS_completo_con_pestana_codigo.py",
            mime="text/x-python",
        )
    else:
        st.error("No se encontró el archivo del código fuente original en el proyecto publicado.")

# ============================================================
# PANTALLAS DE LOS CUATRO CIFRADOS
# ============================================================

else:
    paginas = {
        "01  Cifrado César": (
            "CIFRADO CÉSAR",
            "Desplazamiento de letras mediante una clave numérica.",
            "cesar",
        ),
        "02  Sustitución": (
            "SUSTITUCIÓN MONOALFABÉTICA",
            "Transformación mediante un alfabeto invertido.",
            "sustitucion",
        ),
        "03  Transposición": (
            "CIFRADO POR TRANSPOSICIÓN",
            "Reorganización de los caracteres mediante columnas.",
            "transposicion",
        ),
        "04  Cifrado combinado": (
            "CIFRADO COMBINADO",
            "Aplicación consecutiva de los tres métodos.",
            "combinado",
        ),
    }
    titulo, descripcion, metodo = paginas[pagina]
    st.markdown(
        f'<div class="sds-header"><h2>{titulo}</h2><p>{descripcion}</p></div>',
        unsafe_allow_html=True,
    )

    clave_cesar = 3
    columnas = 3

    if metodo in ("cesar", "combinado"):
        st.markdown("**CLAVE CÉSAR**")
        clave_cesar = st.number_input(
            "Clave César", value=3, step=1, key=f"clave_cesar_{metodo}",
            label_visibility="collapsed",
        )
    if metodo in ("transposicion", "combinado"):
        st.markdown("**CANTIDAD DE COLUMNAS**")
        columnas = st.number_input(
            "Cantidad de columnas", min_value=1, value=3, step=1,
            key=f"columnas_{metodo}", label_visibility="collapsed",
        )
    if metodo == "sustitucion":
        st.info("Este método no necesita claves numéricas.")

    input_key = f"entrada_{metodo}"
    output_key = f"salida_{metodo}"
    if input_key not in st.session_state:
        st.session_state[input_key] = ""
    if output_key not in st.session_state:
        st.session_state[output_key] = ""

    # Streamlit ejecuta este callback antes de volver a crear los widgets.
    # Así se pueden limpiar sus valores sin modificar claves después de instanciarlos.
    def limpiar_campos(clave_entrada, clave_salida):
        st.session_state[clave_entrada] = ""
        st.session_state[clave_salida] = ""

    st.markdown("**MENSAJE DE ENTRADA**")
    st.text_area(
        "Mensaje de entrada",
        key=input_key,
        height=180,
        label_visibility="collapsed",
        placeholder="Escribe aquí el mensaje que deseas cifrar o descifrar...",
    )

    col_cifrar, col_descifrar, col_borrar = st.columns([1, 1, 1])
    with col_cifrar:
        cifrar = st.button("🔒  CIFRAR", type="primary", use_container_width=True)
    with col_descifrar:
        descifrar = st.button("🔓  DESCIFRAR", use_container_width=True)
    with col_borrar:
        st.button(
            "✕  BORRAR",
            use_container_width=True,
            on_click=limpiar_campos,
            args=(input_key, output_key),
        )

    if cifrar or descifrar:
        texto = st.session_state[input_key]
        if not texto.strip():
            st.warning("Escribe un mensaje antes de continuar.")
        else:
            try:
                if metodo in ("cesar", "combinado"):
                    clave = int(clave_cesar)
                else:
                    clave = 0
                if metodo in ("transposicion", "combinado"):
                    cantidad_columnas = int(columnas)
                    if cantidad_columnas < 1:
                        raise ValueError("La cantidad de columnas debe ser mayor que cero.")
                else:
                    cantidad_columnas = 1

                if metodo == "cesar":
                    resultado = cifrado_cesar(texto, clave if cifrar else -clave)
                elif metodo == "sustitucion":
                    resultado = cifrado_sustitucion(texto) if cifrar else descifrado_sustitucion(texto)
                elif metodo == "transposicion":
                    resultado = (
                        cifrado_transposicion(texto, cantidad_columnas)
                        if cifrar else descifrado_transposicion(texto, cantidad_columnas)
                    )
                else:
                    resultado = (
                        cifrar_combinado(texto, clave, cantidad_columnas)
                        if cifrar else descifrar_combinado(texto, clave, cantidad_columnas)
                    )
                st.session_state[output_key] = resultado
            except ValueError as error:
                st.error(str(error))

    st.markdown("**RESULTADO DEL PROCESO**")
    st.text_area(
        "Resultado del proceso",
        key=output_key,
        height=180,
        label_visibility="collapsed",
        disabled=True,
    )
    if st.session_state[output_key]:
        st.download_button(
            "Descargar resultado",
            data=st.session_state[output_key],
            file_name="resultado_sds.txt",
            mime="text/plain",
        )

st.markdown("---")
st.markdown(
    f'<p style="text-align:center;color:{GRIS};font-size:.85rem">'
    'SDS | SISTEMA DE CIFRADO Y DESCIFRADO</p>',
    unsafe_allow_html=True,
)
