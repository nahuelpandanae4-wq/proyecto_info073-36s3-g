import os
import pygame

from configuracion import *

def dibujar_panel ( screen, vidas = 3) :

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
    titulo = fuente1 . render (" SNAKE ", True , " white ")
    screen . blit ( titulo , (x , 30) )

    for i in range (vidas):
        if i == 0:
            pygame.draw.circle(screen, "red",(screen.get_width() - 200, 400), radio)
        if i == 1:
            pygame.draw.circle(screen, "red",(screen.get_width() - 120, 400), radio)
        if i == 2:
            pygame.draw.circle(screen, "red",(screen.get_width() - 40, 400), radio)
        

def refrescar_tablero(screen,tablero,tiempo_texto= "01=00", manzanas=0, total=3, vidas = 3):
    """
    Dibuja el estado actual del tablero en la pantalla.

    Parámetros:
        - screen: La pantalla sobre la cual estamos dibujando.
        - tablero: El tablero con sus posiciones actuales.
    """
    
    # Rellena la pantalla con el color gris, básicamente pintando
    # por encima de lo que estaba anteriormente.
    screen.fill("gray30")
    

    # definicion de disenos de elementos de tablero
    wall = pygame.image.load("imagenes/elementos/cajas.png").convert_alpha ()
    manzanas= pygame.image.load("imagenes/elementos/tuercas.png").convert_alpha ()
    
    alto_elem = LADO_TABLERO / FILAS
    ancho_elem = LADO_TABLERO / COLUMNAS
    radio = ancho_elem / 2


    wall = pygame.transform.scale(wall, (ancho_elem, alto_elem))
    manzanas = pygame.transform.scale(manzanas, (ancho_elem, alto_elem))

    fondo = pygame.image.load("imagenes/fondo/fondo.jpg").convert()
    fondo = pygame.transform.scale(fondo,(LADO_TABLERO, LADO_TABLERO))
    screen.blit(fondo, (0, 0))

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
                screen.blit(wall , [pos_x , pos_y])
            elif tablero[i][j] == JUGADOR:
                # Dibuja un círculo en la posición (pos_x + radio, pos_y + radio) 
                pygame.draw.circle(screen, "green", (pos_x + radio, pos_y + radio), radio)
                # de tamaño (ancho_elem, alto_elem) y color negro.
            elif tablero[i][j] == MANZANA:
               screen.blit(manzanas, [pos_x, pos_y])


            # Estamos recorriendo los píxeles de la pantalla, por lo que
            # debemos sumar el ancho y altura en pixeles de cada elemento que
            # ya hayamos recorrido para avanzar al siguiente.
            pos_x += ancho_elem
        pos_y += alto_elem

    dibujar_panel ( screen , vidas)
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
    # Crear fuente (tamaño 36)
    fuente = pygame.font.Font(None, 36)
    
    # Color rojo si faltan menos de 10 segundos, blanco si no
    color = "red" if tiempo_restante <= 10 else "white"

    # Crear el texto
    texto = fuente.render(f"Tiempo: {tiempo_restante}s", True, color)
    
    # Dibujarlo en la esquina superior derecha (con un poco de margen)
    screen.blit(texto, (screen.get_width() - 200, 50))
    
    # Actualizar la pantalla
    pygame.display.flip()
