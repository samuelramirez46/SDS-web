import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


# ============================================================
# 1. CONFIGURACIÓN GENERAL
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
# 2. MÉTODO 1: CIFRADO CÉSAR
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
# 3. MÉTODO 2: SUSTITUCIÓN MONOALFABÉTICA
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
# 4. MÉTODO 3: TRANSPOSICIÓN
# ============================================================

def cifrado_transposicion(texto, columnas):

    if columnas < 1:
        raise ValueError(
            "La cantidad de columnas debe ser mayor que cero."
        )

    resultado = ""

    for columna in range(columnas):
        resultado += texto[columna::columnas]

    return resultado


def descifrado_transposicion(texto, columnas):

    if columnas < 1:
        raise ValueError(
            "La cantidad de columnas debe ser mayor que cero."
        )

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
# 5. MÉTODO 4: CIFRADO COMBINADO
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
# 6. APLICACIÓN PRINCIPAL SDS
# ============================================================

class AplicacionSDS:

    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title(
            "SDS | Sistema de Cifrado y Descifrado"
        )

        self.ventana.geometry("1150x760")
        self.ventana.minsize(900, 650)
        self.ventana.configure(bg=FONDO)

        self.menu_botones = {}

        self.entrada_texto = None
        self.salida_texto = None

        self.entrada_cesar = None
        self.entrada_columnas = None

        self.scroll_activo = False

        self.configurar_estilos()
        self.crear_interfaz()
        self.mostrar_inicio()

    # ========================================================
    # 7. ESTILOS
    # ========================================================

    def configurar_estilos(self):

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TEntry",
            padding=9,
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Vertical.TScrollbar",
            background="#CBD5E1",
            troughcolor=FONDO,
            borderwidth=0,
            arrowsize=14
        )

    # ========================================================
    # 8. ESTRUCTURA DE LA VENTANA
    # ========================================================

    def crear_interfaz(self):

        # Menú lateral
        self.menu = tk.Frame(
            self.ventana,
            bg=AZUL_OSCURO,
            width=250
        )

        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)

        # Nombre SDS
        tk.Label(
            self.menu,
            text="SDS",
            font=("Segoe UI", 29, "bold"),
            bg=AZUL_OSCURO,
            fg=BLANCO
        ).pack(anchor="w", padx=22, pady=(30, 3))

        tk.Label(
            self.menu,
            text="SISTEMA DE CRIPTOGRAFÍA",
            font=("Segoe UI", 8, "bold"),
            bg=AZUL_OSCURO,
            fg="#94A3B8"
        ).pack(anchor="w", padx=23, pady=(0, 25))

        tk.Frame(
            self.menu,
            bg="#334155",
            height=1
        ).pack(fill="x", padx=18, pady=(0, 18))

        tk.Label(
            self.menu,
            text="MENÚ PRINCIPAL",
            font=("Segoe UI", 9, "bold"),
            bg=AZUL_OSCURO,
            fg="#94A3B8"
        ).pack(anchor="w", padx=22, pady=(0, 12))

        opciones = [
            ("inicio", "⌂    Inicio"),
            ("cesar", "01   Cifrado César"),
            ("sustitucion", "02   Sustitución"),
            ("transposicion", "03   Transposición"),
            ("combinado", "04   Cifrado combinado"),
            ("codigo", "05   Código utilizado")
        ]

        for clave, nombre in opciones:

            boton = tk.Button(
                self.menu,
                text=nombre,
                command=lambda c=clave: self.navegar(c),
                font=("Segoe UI", 10, "bold"),
                bg=AZUL_OSCURO,
                fg="#CBD5E1",
                activebackground=AZUL,
                activeforeground=BLANCO,
                relief="flat",
                bd=0,
                anchor="w",
                padx=18,
                pady=15,
                cursor="hand2"
            )

            boton.pack(fill="x", padx=10, pady=3)

            self.menu_botones[clave] = boton

        # Información inferior
        tk.Frame(
            self.menu,
            bg="#334155",
            height=1
        ).pack(side="bottom", fill="x", padx=18, pady=(0, 15))

        tk.Label(
            self.menu,
            text="PROYECTO ACADÉMICO\n\n"
                 "SDS\n"
                 "Matemáticas\n"
                 "Programación\n"
                 "Criptografía básica",
            font=("Segoe UI", 9),
            bg=AZUL_OSCURO,
            fg="#94A3B8",
            justify="left"
        ).pack(side="bottom", anchor="w", padx=22, pady=(0, 25))

        # Área principal
        self.contenido = tk.Frame(
            self.ventana,
            bg=FONDO
        )

        self.contenido.pack(
            side="right",
            fill="both",
            expand=True
        )

    # ========================================================
    # 9. NAVEGACIÓN
    # ========================================================

    def navegar(self, pagina):

        if pagina == "inicio":
            self.mostrar_inicio()
        elif pagina == "codigo":
            self.mostrar_codigo()
        else:
            self.mostrar_cifrado(pagina)

    def activar_menu(self, pagina):

        for clave, boton in self.menu_botones.items():

            if clave == pagina:
                boton.configure(
                    bg=AZUL,
                    fg=BLANCO
                )
            else:
                boton.configure(
                    bg=AZUL_OSCURO,
                    fg="#CBD5E1"
                )

    def limpiar_contenido(self):

        if self.scroll_activo:

            self.ventana.unbind_all("<MouseWheel>")
            self.ventana.unbind_all("<Button-4>")
            self.ventana.unbind_all("<Button-5>")

            self.scroll_activo = False

        for widget in self.contenido.winfo_children():
            widget.destroy()

    # ========================================================
    # 10. ELEMENTOS VISUALES
    # ========================================================

    def etiqueta(
        self,
        parent,
        texto,
        size=11,
        negrita=False,
        color=TEXTO,
        fondo=BLANCO
    ):

        return tk.Label(
            parent,
            text=texto,
            font=(
                "Segoe UI",
                size,
                "bold" if negrita else "normal"
            ),
            bg=fondo,
            fg=color
        )

    def crear_boton(self, parent, texto, color, comando):

        return tk.Button(
            parent,
            text=texto,
            command=comando,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg=BLANCO,
            activebackground=color,
            activeforeground=BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=12
        )

    # ========================================================
    # 11. ÁREAS DE TEXTO CON BARRA VERTICAL
    # ========================================================

    def crear_area_texto(self, parent, altura=7):

        marco = tk.Frame(
            parent,
            bg=BORDE,
            padx=1,
            pady=1
        )

        area = tk.Text(
            marco,
            height=altura,
            font=("Consolas", 11),
            bg="#F8FAFC",
            fg=TEXTO,
            insertbackground=AZUL,
            relief="flat",
            wrap="word",
            padx=12,
            pady=12,
            undo=True
        )

        barra = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=area.yview,
            style="Vertical.TScrollbar"
        )

        area.configure(
            yscrollcommand=barra.set
        )

        area.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        return marco, area

    # ========================================================
    # 12. ENCABEZADOS
    # ========================================================

    def crear_encabezado(self, titulo, descripcion):

        encabezado = tk.Frame(
            self.contenido,
            bg=BLANCO,
            padx=30,
            pady=23
        )

        encabezado.pack(fill="x")

        self.etiqueta(
            encabezado,
            titulo,
            19,
            True
        ).pack(anchor="w")

        self.etiqueta(
            encabezado,
            descripcion,
            10,
            False,
            GRIS
        ).pack(anchor="w", pady=(5, 0))

    # ========================================================
    # 13. PANTALLA DE INICIO
    # ========================================================

    def mostrar_inicio(self):

        self.limpiar_contenido()
        self.activar_menu("inicio")

        self.crear_encabezado(
            "BIENVENIDO A SDS",
            "Inicio / Información general de la aplicación"
        )

        zona = tk.Frame(
            self.contenido,
            bg=FONDO
        )

        zona.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        canvas = tk.Canvas(
            zona,
            bg=FONDO,
            highlightthickness=0
        )

        barra = ttk.Scrollbar(
            zona,
            orient="vertical",
            command=canvas.yview,
            style="Vertical.TScrollbar"
        )

        canvas.configure(
            yscrollcommand=barra.set
        )

        barra.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        interior = tk.Frame(
            canvas,
            bg=FONDO
        )

        ventana_canvas = canvas.create_window(
            (0, 0),
            window=interior,
            anchor="nw"
        )

        def actualizar_region(event):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        def ajustar_ancho(event):

            canvas.itemconfigure(
                ventana_canvas,
                width=event.width
            )

        interior.bind("<Configure>", actualizar_region)
        canvas.bind("<Configure>", ajustar_ancho)

        # Bienvenida
        bienvenida = tk.Frame(
            interior,
            bg=AZUL_OSCURO,
            padx=30,
            pady=35
        )

        bienvenida.pack(fill="x", pady=(0, 18))

        tk.Label(
            bienvenida,
            text="¡BIENVENIDO A SDS!",
            font=("Segoe UI", 25, "bold"),
            bg=AZUL_OSCURO,
            fg=BLANCO
        ).pack(anchor="w")

        tk.Label(
            bienvenida,
            text="Descubre cómo las matemáticas permiten proteger "
                 "y transformar la información.",
            font=("Segoe UI", 11),
            bg=AZUL_OSCURO,
            fg="#CBD5E1",
            wraplength=750,
            justify="left"
        ).pack(anchor="w", pady=(10, 0))

        # Información
        self.tarjeta(
            interior,
            "¿QUÉ ES SDS?",
            "SDS es una aplicación educativa diseñada para comprender "
            "los fundamentos de la criptografía. Permite escribir mensajes, "
            "convertirlos en textos codificados y recuperar su contenido "
            "original mediante diferentes procedimientos matemáticos "
            "y de programación."
        )

        self.tarjeta(
            interior,
            "¿CÓMO FUNCIONA LA APLICACIÓN?",
            "1. Selecciona un método en el menú ubicado a la izquierda.\n\n"
            "2. Escribe el mensaje que deseas cifrar o descifrar.\n\n"
            "3. Introduce las claves solicitadas por el método elegido.\n\n"
            "4. Presiona CIFRAR para transformar el mensaje.\n\n"
            "5. Para recuperar el texto original, coloca el mensaje "
            "codificado en el espacio de entrada y presiona DESCIFRAR.\n\n"
            "6. Presiona BORRAR para limpiar los dos espacios y comenzar "
            "una nueva operación."
        )

        self.tarjeta(
            interior,
            "MÉTODOS DE CIFRADO DISPONIBLES",
            "01. CIFRADO CÉSAR\n"
            "Desplaza las letras del alfabeto según una clave numérica.\n\n"
            "02. SUSTITUCIÓN MONOALFABÉTICA\n"
            "Reemplaza cada letra por su equivalente en el alfabeto invertido.\n\n"
            "03. TRANSPOSICIÓN\n"
            "Modifica el orden de los caracteres utilizando columnas.\n\n"
            "04. CIFRADO COMBINADO\n"
            "Aplica consecutivamente los tres métodos anteriores."
        )

        self.tarjeta(
            interior,
            "RECOMENDACIONES IMPORTANTES",
            "• Utiliza las mismas claves al cifrar y descifrar.\n\n"
            "• En César, recuerda el desplazamiento numérico utilizado.\n\n"
            "• En transposición, conserva la cantidad de columnas.\n\n"
            "• Introduce el mensaje codificado completo al descifrar.\n\n"
            "• Esta aplicación tiene fines educativos y no debe utilizarse "
            "como sistema de protección de información confidencial."
        )

        tk.Label(
            interior,
            text="SDS | MATEMÁTICAS, PROGRAMACIÓN Y CRIPTOGRAFÍA",
            font=("Segoe UI", 9, "bold"),
            bg=FONDO,
            fg=GRIS
        ).pack(pady=20)

        # Desplazamiento de la pantalla de inicio
        def desplazar(event):

            if event.num == 4:
                canvas.yview_scroll(-1, "units")

            elif event.num == 5:
                canvas.yview_scroll(1, "units")

            else:
                canvas.yview_scroll(
                    int(-event.delta / 120),
                    "units"
                )

        self.ventana.bind_all("<MouseWheel>", desplazar)
        self.ventana.bind_all("<Button-4>", desplazar)
        self.ventana.bind_all("<Button-5>", desplazar)

        self.scroll_activo = True

    def tarjeta(self, parent, titulo, descripcion):

        tarjeta = tk.Frame(
            parent,
            bg=BLANCO,
            padx=25,
            pady=22
        )

        tarjeta.pack(fill="x", pady=(0, 15))

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            bg=BLANCO,
            fg=AZUL
        ).pack(anchor="w", pady=(0, 12))

        tk.Label(
            tarjeta,
            text=descripcion,
            font=("Segoe UI", 10),
            bg=BLANCO,
            fg=TEXTO,
            justify="left",
            anchor="w",
            wraplength=780
        ).pack(fill="x", anchor="w")


    # ========================================================
    # 14. PESTAÑA: CÓDIGO UTILIZADO
    # ========================================================

    def mostrar_codigo(self):

        self.limpiar_contenido()
        self.activar_menu("codigo")

        self.crear_encabezado(
            "CÓDIGO UTILIZADO",
            "Información del desarrollo y código fuente completo de SDS"
        )

        cuerpo = tk.Frame(
            self.contenido,
            bg=FONDO,
            padx=25,
            pady=20
        )
        cuerpo.pack(fill="both", expand=True)

        # Descripción del proyecto
        descripcion = tk.Frame(
            cuerpo,
            bg=BLANCO,
            padx=22,
            pady=18
        )
        descripcion.pack(fill="x", pady=(0, 16))

        tk.Label(
            descripcion,
            text="¿QUÉ CÓDIGO UTILIZAMOS Y PARA QUÉ SIRVE?",
            font=("Segoe UI", 12, "bold"),
            bg=BLANCO,
            fg=AZUL
        ).pack(anchor="w", pady=(0, 9))

        texto_descripcion = (
            "Este es el código fuente que utilizamos para desarrollar "
            "la aplicación SDS (Sistema de Cifrado y Descifrado). "
            "Fue programado en Python utilizando la biblioteca Tkinter "
            "para construir la interfaz gráfica.\n\n"
            "Su función es permitir que el usuario escriba mensajes, "
            "los cifre y posteriormente los descifre mediante cuatro "
            "métodos: cifrado César, sustitución monoalfabética, "
            "transposición y cifrado combinado. El programa también "
            "valida las claves ingresadas, muestra los resultados y "
            "permite borrar los textos para realizar nuevas operaciones.\n\n"
            "El código que aparece en el siguiente recuadro corresponde "
            "al archivo Python que está ejecutándose. Puedes desplazarte "
            "hacia arriba y hacia abajo con la barra lateral para revisar "
            "todas sus líneas. También puedes seleccionar y copiar el texto."
        )

        tk.Label(
            descripcion,
            text=texto_descripcion,
            font=("Segoe UI", 10),
            bg=BLANCO,
            fg=TEXTO,
            justify="left",
            anchor="w",
            wraplength=850
        ).pack(fill="x")

        # Panel que contiene el código completo
        panel_codigo = tk.Frame(
            cuerpo,
            bg=BLANCO,
            padx=15,
            pady=15
        )
        panel_codigo.pack(fill="both", expand=True)

        tk.Label(
            panel_codigo,
            text="CÓDIGO FUENTE COMPLETO",
            font=("Segoe UI", 11, "bold"),
            bg=BLANCO,
            fg=TEXTO
        ).pack(anchor="w", pady=(0, 10))

        marco_editor = tk.Frame(
            panel_codigo,
            bg=BORDE,
            padx=1,
            pady=1
        )
        marco_editor.pack(fill="both", expand=True)

        area_codigo = tk.Text(
            marco_editor,
            font=("Consolas", 9),
            bg="#0F172A",
            fg="#E2E8F0",
            insertbackground=BLANCO,
            selectbackground=AZUL,
            selectforeground=BLANCO,
            relief="flat",
            wrap="none",
            padx=14,
            pady=12,
            undo=False
        )

        barra_vertical = ttk.Scrollbar(
            marco_editor,
            orient="vertical",
            command=area_codigo.yview,
            style="Vertical.TScrollbar"
        )

        barra_horizontal = ttk.Scrollbar(
            marco_editor,
            orient="horizontal",
            command=area_codigo.xview,
            style="Horizontal.TScrollbar"
        )

        area_codigo.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        area_codigo.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        marco_editor.grid_rowconfigure(0, weight=1)
        marco_editor.grid_columnconfigure(0, weight=1)

        try:
            ruta_codigo = Path(__file__).resolve()
            codigo_completo = ruta_codigo.read_text(encoding="utf-8")
        except (OSError, NameError):
            codigo_completo = (
                "No fue posible leer automáticamente el archivo fuente.\\n"
                "Guarda y ejecuta esta aplicación desde un archivo .py "
                "para mostrar aquí su código completo."
            )

        area_codigo.insert("1.0", codigo_completo)
        area_codigo.configure(state="disabled")


    # ========================================================
    # 15. PANTALLAS DE LOS CUATRO CIFRADOS
    # ========================================================

    def mostrar_cifrado(self, metodo):

        self.limpiar_contenido()
        self.activar_menu(metodo)

        informacion = {

            "cesar": (
                "CIFRADO CÉSAR",
                "Desplazamiento de letras mediante una clave numérica."
            ),

            "sustitucion": (
                "SUSTITUCIÓN MONOALFABÉTICA",
                "Transformación mediante un alfabeto invertido."
            ),

            "transposicion": (
                "CIFRADO POR TRANSPOSICIÓN",
                "Reorganización de los caracteres mediante columnas."
            ),

            "combinado": (
                "CIFRADO COMBINADO",
                "Aplicación consecutiva de los tres métodos."
            )
        }

        titulo, descripcion = informacion[metodo]

        self.crear_encabezado(
            titulo,
            descripcion
        )

        cuerpo = tk.Frame(
            self.contenido,
            bg=FONDO,
            padx=30,
            pady=22
        )

        cuerpo.pack(
            fill="both",
            expand=True
        )

        # Panel de claves
        panel_claves = tk.Frame(
            cuerpo,
            bg=BLANCO,
            padx=20,
            pady=17
        )

        panel_claves.pack(
            fill="x",
            pady=(0, 18)
        )

        self.entrada_cesar = None
        self.entrada_columnas = None

        if metodo in ("cesar", "combinado"):

            tk.Label(
                panel_claves,
                text="CLAVE CÉSAR",
                font=("Segoe UI", 9, "bold"),
                bg=BLANCO,
                fg=TEXTO
            ).pack(side="left", padx=(0, 10))

            self.entrada_cesar = ttk.Entry(
                panel_claves,
                width=10
            )

            self.entrada_cesar.insert(0, "3")

            self.entrada_cesar.pack(
                side="left",
                padx=(0, 25)
            )

        if metodo in ("transposicion", "combinado"):

            tk.Label(
                panel_claves,
                text="CANTIDAD DE COLUMNAS",
                font=("Segoe UI", 9, "bold"),
                bg=BLANCO,
                fg=TEXTO
            ).pack(side="left", padx=(0, 10))

            self.entrada_columnas = ttk.Entry(
                panel_claves,
                width=10
            )

            self.entrada_columnas.insert(0, "3")

            self.entrada_columnas.pack(
                side="left"
            )

        if metodo == "sustitucion":

            tk.Label(
                panel_claves,
                text="Este método no necesita claves numéricas.",
                font=("Segoe UI", 10),
                bg=BLANCO,
                fg=GRIS
            ).pack(anchor="w")

        # Mensaje de entrada
        self.etiqueta(
            cuerpo,
            "MENSAJE DE ENTRADA",
            11,
            True,
            TEXTO,
            FONDO
        ).pack(anchor="w", pady=(0, 8))

        marco_entrada, self.entrada_texto = self.crear_area_texto(
            cuerpo,
            7
        )

        marco_entrada.pack(
            fill="both",
            expand=True,
            pady=(0, 15)
        )

        # Tres botones
        panel_botones = tk.Frame(
            cuerpo,
            bg=FONDO
        )

        panel_botones.pack(
            fill="x",
            pady=(0, 15)
        )

        self.crear_boton(
            panel_botones,
            "🔒  CIFRAR",
            AZUL,
            lambda: self.procesar(metodo, "cifrar")
        ).pack(side="left", padx=(0, 10))

        self.crear_boton(
            panel_botones,
            "🔓  DESCIFRAR",
            VERDE,
            lambda: self.procesar(metodo, "descifrar")
        ).pack(side="left", padx=10)

        self.crear_boton(
            panel_botones,
            "✕  BORRAR",
            ROJO,
            self.borrar
        ).pack(side="right")

        # Resultado
        self.etiqueta(
            cuerpo,
            "RESULTADO DEL PROCESO",
            11,
            True,
            TEXTO,
            FONDO
        ).pack(anchor="w", pady=(0, 8))

        marco_salida, self.salida_texto = self.crear_area_texto(
            cuerpo,
            7
        )

        marco_salida.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # 16. VALIDACIÓN DE CLAVES
    # ========================================================

    def obtener_claves(self):

        clave_cesar = 0
        columnas = 1

        if self.entrada_cesar is not None:

            valor = self.entrada_cesar.get().strip()

            if not valor:
                raise ValueError(
                    "Debes introducir la clave César."
                )

            try:
                clave_cesar = int(valor)

            except ValueError:
                raise ValueError(
                    "La clave César debe ser un número entero."
                )

        if self.entrada_columnas is not None:

            valor = self.entrada_columnas.get().strip()

            if not valor:
                raise ValueError(
                    "Debes introducir la cantidad de columnas."
                )

            try:
                columnas = int(valor)

            except ValueError:
                raise ValueError(
                    "La cantidad de columnas debe ser un número entero."
                )

            if columnas < 1:
                raise ValueError(
                    "La cantidad de columnas debe ser mayor que cero."
                )

        return clave_cesar, columnas

    # ========================================================
    # 17. PROCESAR CIFRADO Y DESCIFRADO
    # ========================================================

    def procesar(self, metodo, operacion):

        texto = self.entrada_texto.get(
            "1.0",
            "end-1c"
        )

        if not texto.strip():

            messagebox.showwarning(
                "Mensaje vacío",
                "Escribe un mensaje antes de continuar."
            )

            return

        try:

            clave, columnas = self.obtener_claves()

            if metodo == "cesar":

                if operacion == "cifrar":
                    resultado = cifrado_cesar(texto, clave)

                else:
                    resultado = cifrado_cesar(texto, -clave)

            elif metodo == "sustitucion":

                if operacion == "cifrar":
                    resultado = cifrado_sustitucion(texto)

                else:
                    resultado = descifrado_sustitucion(texto)

            elif metodo == "transposicion":

                if operacion == "cifrar":

                    resultado = cifrado_transposicion(
                        texto,
                        columnas
                    )

                else:

                    resultado = descifrado_transposicion(
                        texto,
                        columnas
                    )

            elif metodo == "combinado":

                if operacion == "cifrar":

                    resultado = cifrar_combinado(
                        texto,
                        clave,
                        columnas
                    )

                else:

                    resultado = descifrar_combinado(
                        texto,
                        clave,
                        columnas
                    )

            # Mostrar resultado
            self.salida_texto.delete(
                "1.0",
                tk.END
            )

            self.salida_texto.insert(
                "1.0",
                resultado
            )

        except ValueError as error:

            messagebox.showerror(
                "Error de operación",
                str(error)
            )

    # ========================================================
    # 18. BORRAR MENSAJES
    # ========================================================

    def borrar(self):

        self.entrada_texto.delete(
            "1.0",
            tk.END
        )

        self.salida_texto.delete(
            "1.0",
            tk.END
        )


# ============================================================
# 19. EJECUTAR APLICACIÓN
# ============================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    # Crear e iniciar la aplicación SDS
    aplicacion = AplicacionSDS(ventana)

    # Mantener abierta la ventana principal
    ventana.mainloop()
