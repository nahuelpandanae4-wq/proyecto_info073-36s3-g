import os

# Estados
ESTADO_INICIO = "inicio"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_JUGANDO = "jugando"
ESTADO_DERROTA = "derrota"
ESTADO_VICTORIA = "victoria"

PANTALLA_INICIO = "pantalla_inicio.bmp"
PANTALLA_INSTRUCCIONES = "pantalla_instrucciones.bmp"
PANTALLA_VICTORIA = "pantalla_victoria.bmp"
PANTALLA_DERROTA = "pantalla_derrota.bmp"

# Tamano de la ventana (en pixeles )
ANCHO_VENTANA = 1040
ALTO_VENTANA = 800

# El tablero es un cuadrado fijo , independiente de la ventana
LADO_TABLERO = 800

# Lo que sobra a la derecha de la ventana es el ancho del panel
ANCHO_PANEL = ANCHO_VENTANA - LADO_TABLERO


# Tablero
FILAS = 15
COLUMNAS = 15

# variables del tablero
VACIO = 0
OBSTACULO = 1
JUGADOR = 2
MANZANA = 3


MANZANAS_PARA_GANAR = 3


TIEMPO_LIMITE = 60
RETRASO = 200

# crea una ruta a la carpeta de las pantallas
DIR_PANTALLAS = os.path.join(os.path.dirname(__file__),"data","pantallas")

# indica el borde de el tablero
BORDE = (
    [(c, 0) for c in range(COLUMNAS)]
    + [(c, FILAS - 1) for c in range(COLUMNAS)]
    + [(0, f) for f in range(1, FILAS - 1)]
    + [(COLUMNAS - 1, f) for f in range(1, FILAS - 1)]
)