import pygame
import random

from configuracion import *

def perder_vida(tablero, pos_jugador, pos_inicial, vidas, sonido_daño, tiene_escudo):
    """
    Resta una vida y devuelve al jugador a la posición inicial.
    """
    if tiene_escudo:
        # Solo se elimina el escudo, sin daño
        return pos_jugador, vidas, (0,0), False

    sonido_daño.play()

    vidas -= 1

    col, fila = pos_jugador
    tablero[fila][col] = VACIO

    col_i, fila_i = pos_inicial
    tablero[fila_i][col_i] = JUGADOR

    direccion = (0, 0)

    return pos_inicial, vidas, direccion

def cambiar_direccion_por_tecla(tecla, direccion_actual):
    if tecla == pygame.K_w:
        return (0, -1)
    if tecla == pygame.K_s:
        return (0, 1)
    if tecla == pygame.K_a:
        return (-1, 0)
    if tecla == pygame.K_d:
        return (1, 0)

    return direccion_actual

def avanzar(tablero, pos_jugador,pos_inicial, direccion, manzanas_comidas, sonido_manzana, sonido_daño, vidas, tiene_escudo):
    """
    Avanza el jugador un paso en la dirección dada.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - pos_jugador: Tupla con la posición actual (índice con
            estructura (columna, fila)) del jugador en el tablero.
        - direccion: Tupla con la dirección en la que está avanzando actualmente el jugador.

    Retorna:
        - (resultado, nueva_pos_jugador): Retorna el resultado que se obtiene
            al avanzar (derrota, victoria o "ok" (no cambia de pantalla)) y la nueva posición del jugador.
    """

    # Obtenemos los componentes "x" e "y" de cada tupla recibida
    # con información de la dirección y posición del jugador.
    dir_col, dir_fila = direccion
    ind_actual_col, ind_actual_fila = (
        pos_jugador  # Tupla (columna, fila) que representa los índices en el tablero.
    )

    # Aplicamos la dirección a la posición del jugador.
    ind_nueva_col = ind_actual_col + dir_col
    ind_nueva_fila = ind_actual_fila + dir_fila

    # Verificamos que no haya choque con el borde del tablero.
    if not (0 <= ind_nueva_col < COLUMNAS and 0 <= ind_nueva_fila < FILAS):
        pos_jugador, vidas, direccion, tiene_escudo = perder_vida(tablero,pos_jugador,pos_inicial,vidas,sonido_daño, tiene_escudo)
        if vidas <= 0:
            return "derrota", pos_jugador, manzanas_comidas, vidas, direccion, tiene_escudo
        return "ok", pos_jugador, manzanas_comidas, vidas, direccion, tiene_escudo


    # Obtenemos el elemento que se encuentre en el tablero en la nueva posición del jugador.
    pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

        
    if pos_elem == OBSTACULO or pos_elem == ENEMIGO:
        pos_jugador, vidas, direccion, tiene_escudo = perder_vida(tablero,pos_jugador,pos_inicial,vidas,sonido_daño, tiene_escudo)
        if vidas <= 0:
            return "derrota", pos_jugador, manzanas_comidas, vidas, direccion, tiene_escudo
        return "ok", pos_jugador, manzanas_comidas, vidas, direccion, tiene_escudo

    if pos_elem == MANZANA:
        sonido_manzana.play()
        manzanas_comidas += 1

        # Mover al jugador a la nueva casilla
        tablero[ind_actual_fila][ind_actual_col] = VACIO

        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

        # Si llegamos al objetivo, victoria
        if manzanas_comidas >= MANZANAS_PARA_GANAR:
            return "victoria", (ind_nueva_col, ind_nueva_fila), manzanas_comidas, vidas,direccion, tiene_escudo

    if pos_elem == ACEITE:
        sonido_manzana.play()  # Usamos el mismo sonido por ahora

        tablero[ind_actual_fila][ind_actual_col] = VACIO

        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

        # Por ahora solo lo recoge, luego agregaremos el escudo
        return "ok", (ind_nueva_col, ind_nueva_fila), manzanas_comidas, vidas, direccion, True
        
            
    # Movimiento normal, si es que no encontramos manzana ni obstáculo.
    tablero[ind_actual_fila][ind_actual_col] = VACIO
    tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

    return "ok", (ind_nueva_col, ind_nueva_fila), manzanas_comidas, vidas,direccion, tiene_escudo

def obtener_direccion_aleatoria(direcciones):
        
        return random.choice(direcciones)

def avanzar_enemigos(tablero,pos_enemigos,pos_jugador,pos_inicial,vidas,sonido_daño, tiene_escudo):
    for i in range(len(pos_enemigos)):

        pos_enemigo = pos_enemigos[i]
        col, fila = pos_enemigo

        direcciones = [(0,-1), (0, 1), (-1, 0), (1, 0)]

        dir_col, dir_fila = obtener_direccion_aleatoria(direcciones)

        nueva_col = col + dir_col
        nueva_fila = fila + dir_fila
        
        if 0 <= nueva_col < COLUMNAS and 0 <= nueva_fila < FILAS:

            # Si la nueva casilla esta vacia, el enemigo se mueve
            if tablero[nueva_fila][nueva_col] == VACIO:
                    tablero[fila][col] = VACIO
                    tablero[nueva_fila][nueva_col] = ENEMIGO
                    pos_enemigos[i] = (nueva_col, nueva_fila)

                    # Si el enemigo pisa a la serpiente, el jugador pierde
            elif tablero[nueva_fila][nueva_col] == JUGADOR:
                pos_jugador, vidas, direccion, tiene_escudo = perder_vida(tablero,pos_jugador,pos_inicial,vidas,sonido_daño, tiene_escudo)

                if vidas <= 0:
                    return "derrota", pos_enemigos, pos_jugador, vidas, tiene_escudo

    return "ok", pos_enemigos, pos_jugador, vidas, tiene_escudo

  

   
 
