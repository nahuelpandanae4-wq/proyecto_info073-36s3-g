import pygame

from configuracion import *
from tablero import reiniciar
from jugador import cambiar_direccion, avanzar
from interfaz import (
    refrescar_tablero,
    mostrar_pantalla,
    mostrar_temporizador,
)


def main():
    pygame.init()

    # Establecemos la resolución de la pantalla.
    screen = pygame . display . set_mode (( ANCHO_VENTANA , ALTO_VENTANA ) )
    
    # Establecemos el título de la ventana.
    pygame.display.set_caption("Juego Básico")

    running = True

    estado = ESTADO_INICIO
    tablero = []
    pos_jugador = (0, 0)
    direccion = (0, 0)
    tiempo_ultimo_mov = 0
    manzanas_comidas = 0
    vidas = 3
    # TEMPORIZADOR - Variable para rastrear cuándo comenzó el juego
    tiempo_inicio_juego = 0
    
    # TEMPORIZADOR - Clock para controlar la velocidad de actualización
    clock = pygame.time.Clock()

    mostrar_pantalla(screen, PANTALLA_INICIO)

    sonido_manzana = pygame.mixer.Sound("sonidos/interacciones/manzana.wav")

    pygame.mixer.music.load("sonidos/principal/durante_juego.mp3")
    pygame.mixer.music.play(-1)


    # Este es el bucle principal del juego, todo lo que sucede en el juego
    # está aquí.
    while running:
        # Se analizan los eventos del bucle actual.
        # TEMPORIZADOR - Limitar a 60 FPS (60 veces por segundo)
        clock.tick(60)
        
        for evento in pygame.event.get():
            # Si es que se quiere cerrar la ventana.
            if evento.type == pygame.QUIT:
                running = False

            # Si es que se presiona alguna tecla.
            if evento.type == pygame.KEYDOWN:
                if estado == ESTADO_INICIO:
                    if evento.key == pygame.K_SPACE:
                        tablero, pos_jugador, pos_inicial, vidas = reiniciar()
                        direccion = (0, 0)
                        # Obtiene tiempo en milisegundos
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        tiempo_inicio_juego = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        manzanas_comidas = 0
                        refrescar_tablero(screen, tablero, "01:00", 0, MANZANAS_PARA_GANAR)
                        tiempo_inicio = pygame.time.get_ticks() #Reinicia tiempo a 1 minuto
                    elif evento.key == pygame.K_i:
                        estado = ESTADO_INSTRUCCIONES
                        mostrar_pantalla(screen, PANTALLA_INSTRUCCIONES)

                elif estado == ESTADO_INSTRUCCIONES:
                    estado = ESTADO_INICIO
                    mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado in (ESTADO_DERROTA, ESTADO_VICTORIA):
                    if evento.key == pygame.K_r:
                        tablero, pos_jugador, pos_inicial, vidas = reiniciar()
                        direccion = (0, 0)
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        tiempo_inicio_juego = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        manzanas_comidas = 0
                        refrescar_tablero(screen, tablero, "01:00", 0, MANZANAS_PARA_GANAR)

                    if evento.key == pygame.K_ESCAPE:
                        estado = ESTADO_INICIO
                        mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado == ESTADO_JUGANDO:
                    direccion = cambiar_direccion(pygame.key.get_pressed(), direccion)

        if estado == ESTADO_JUGANDO:
            tiempo_actual = pygame.time.get_ticks()  # En milisegundos

            tiempo_transcurrido = (tiempo_actual - tiempo_inicio_juego) // 1000  # Convertir a segundos
            tiempo_restante = TIEMPO_LIMITE - tiempo_transcurrido
            

            if tiempo_restante <= 0:
                estado = ESTADO_DERROTA
                mostrar_pantalla(screen, PANTALLA_DERROTA)

            # La variable RETRASO hace que si no han pasado esa cantidad de ticks,
            # entonces no se avanzará en el tablero.
            elif direccion != (0, 0) and tiempo_actual - tiempo_ultimo_mov >= RETRASO:
                resultado, pos_jugador, manzanas_comidas, vidas, direccion = avanzar(tablero, pos_jugador, pos_inicial, direccion, manzanas_comidas, sonido_manzana,vidas)
                if resultado == "derrota":
                    estado = ESTADO_DERROTA
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
                elif resultado == "victoria":
                    estado = ESTADO_VICTORIA
                    mostrar_pantalla(screen, PANTALLA_VICTORIA)
                else:
                    tiempo_ultimo_mov = tiempo_actual
                    refrescar_tablero(screen, tablero, manzanas_comidas, MANZANAS_PARA_GANAR)
                    mostrar_temporizador(screen, tiempo_restante)
            else:
                 mostrar_temporizador(screen, tiempo_restante)


    pygame.quit()


if __name__ == "__main__":
    main()
