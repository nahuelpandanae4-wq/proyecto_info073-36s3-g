import os
import pygame

from configuracion import *

def dibujar_panel ( screen,  vidas = 3, manzanas_comidas = 0) :

    alto_elem = LADO_TABLERO / FILAS
    ancho_elem = LADO_TABLERO / COLUMNAS
    radio = ancho_elem / 2

    # Rectangulo del panel : empieza donde termina el tablero
    panel = pygame . Rect ( LADO_TABLERO , 0 , ANCHO_PANEL , ALTO_VENTANA )
    pygame . draw . rect ( screen , " gray15 ", panel )

    # Margen izquierdo del texto dentro del panel
    x = LADO_TABLERO + 24

    # Crear fuente (tamaño 36)
    fuente1 = pygame.font.Font(None, 36)
    
    # Titulo
    titulo = fuente1 . render (" ESCAPE ", True , " white ")
    screen . blit ( titulo , (x , 20) )

    vida = fuente1 . render (" VIDAS:  ", True, " white ")
    screen . blit (vida , (x + 26, 520))

    tuercas = fuente1 . render (" TUERCAS:  ", True , " white ")
    screen . blit (tuercas, ( x + 24, 265))

    imagen_tuerca = pygame.image.load("imagenes/elementos/tuercas.png").convert_alpha()
    imagen_tuerca = pygame.transform.scale(imagen_tuerca, (80, 80))

    imagen_tuerca_gris = imagen_tuerca.copy()
    imagen_tuerca_gris.fill((80, 80, 80, 180), special_flags=pygame.BLEND_RGBA_MULT)

    for i in range(MANZANAS_PARA_GANAR):
        if i < manzanas_comidas:
            screen.blit(imagen_tuerca, (x + i * 60, 300))
        else:
            screen.blit(imagen_tuerca_gris, (x + i * 60, 300))




    for i in range(vidas):
        x = screen.get_width() - 200 + i*80
        vida = pygame.image.load("imagenes/elementos/vida.png").convert_alpha()
        vida = pygame.transform.scale(vida, (ancho_elem, alto_elem))
        screen.blit(vida, (x - ancho_elem/2, 600 - alto_elem/2))

def refrescar_tablero(screen,tablero,tiempo_texto= "01=00", manzanas=3, total=3, vidas = 3):
    """
    Dibuja el estado actual del tablero en la pantalla.

    Parámetros:
        - screen: La pantalla sobre la cual estamos dibujando.
        - tablero: El tablero con sus posiciones actuales.
    """
    
    # Rellena la pantalla con el color gris, básicamente pintando
    # por encima de lo que estaba anteriormente.
    screen.fill("gray30")

    
    alto_elem = LADO_TABLERO / FILAS
    ancho_elem = LADO_TABLERO / COLUMNAS
    radio = ancho_elem / 2

    JUGADOR_IMG = pygame.transform.scale(pygame.image.load("imagenes/elementos/personaje.png").convert_alpha(),(ancho_elem, alto_elem))
    ENEMIGO_IMG =pygame.transform.scale( pygame.image.load("imagenes/elementos/eagle.png").convert_alpha (),(ancho_elem, alto_elem))
    MURO_IMG = pygame.transform.scale(pygame.image.load("imagenes/elementos/cajas.png").convert_alpha (),(ancho_elem, alto_elem))
    TUERCA_IMG = pygame.transform.scale(pygame.image.load("imagenes/elementos/tuercas.png").convert_alpha (),(ancho_elem, alto_elem))
    FONDO_IMG = pygame.transform.scale(pygame.image.load("imagenes/fondo/fondo.jpg").convert_alpha (),(LADO_TABLERO, LADO_TABLERO))

    screen.blit(FONDO_IMG, (0, 0))

    # Podemos calcular el tamaño en pixeles que tendrá cada

    # casilla al dividir tanto la altura de la pantalla (screen.get_height())
    # como el ancho (screen.get_width()) por la cantidad de filas y columnas respectivamente.
    # Por ejemplo en este caso alto_elem sería 800 / 15 = 53.3, lo que nos indica que la
    # altura de cada elemento es de 53.3 píxeles.

    # Como el jugador es un círculo, se necesita el radio.
    

    # Posición en eje "y" en unidad de píxeles.
    pos_y = 0


    for i in range(FILAS):
        # Posición en eje "x" en unidad de píxeles.
        pos_x = 0
        for j in range(COLUMNAS):
            if tablero[i][j] == OBSTACULO:
                # Dibuja un rectángulo en la posición (pos_x, pos_y) y que sea
                screen.blit(MURO_IMG , [pos_x , pos_y])
            elif tablero[i][j] == JUGADOR:

                screen.blit(JUGADOR_IMG, [pos_x, pos_y])
                # de tamaño (ancho_elem, alto_elem) y color negro.
            elif tablero[i][j] == MANZANA:
               screen.blit(TUERCA_IMG, [pos_x, pos_y])
            elif tablero[i][j] == ENEMIGO:
                screen.blit(ENEMIGO_IMG, [pos_x, pos_y])

            # Estamos recorriendo los píxeles de la pantalla, por lo que
            # debemos sumar el ancho y altura en pixeles de cada elemento que
            # ya hayamos recorrido para avanzar al siguiente.
            pos_x += ancho_elem
        pos_y += alto_elem

    dibujar_panel ( screen , vidas, manzanas_comidas = manzanas)
    # Refresca el contenido que se ve en pantalla.

    pygame.display.flip()

def mostrar_pantalla(screen, nombre_archivo):
    """
    Carga una imagen y la muestra escalada a la ventana.

    Parámetros:
        - screen: La pantalla donde colocaremos la imagen.
        - nombre_archivo: El nombre del archivo de la imagen.
    """

    ruta = os.path.join(DIR_PANTALLAS, nombre_archivo)

    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, screen.get_size())

        # Dibujamos la imagen en la pantalla en la coordenada (0, 0).
        screen.blit(imagen, (0, 0))

        # Refrescamos pantalla.
        pygame.display.flip()
    except FileNotFoundError:
        # Fallback de seguridad en caso de que las imágenes no existan aún
        screen.fill("black")
        pygame.display.flip()
        print(f"Advertencia: No se encontró la imagen {ruta}")

def mostrar_temporizador(screen, tiempo_restante):
    """
    Muestra el temporizador en la esquina superior derecha.
    
    Parámetros:
        - screen: La pantalla donde mostrar el temporizador.
        - tiempo_restante: Segundos restantes.
    """

    fondo_temporizador = pygame.Rect(screen.get_width() - 220, 120, 210, 40)
    pygame.draw.rect(screen, "gray15", fondo_temporizador)

    # Crear fuente (tamaño 36)
    fuente = pygame.font.Font(None, 36)
    
    # Color rojo si faltan menos de 10 segundos, blanco si no
    color = "red" if tiempo_restante <= 10 else "white"

    # Crear el texto
    texto = fuente.render(f"Tiempo: {tiempo_restante}s", True, color)
    
    # Dibujarlo en la esquina superior derecha (con un poco de margen)
    screen.blit(texto, (screen.get_width() - 200, 120))
    

    

