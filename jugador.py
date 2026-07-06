import pygame
import random

from configuracion import *

def perder_vida(tablero, pos_jugador, pos_inicial, vidas, sonido_daño):
    """
    Resta una vida y devuelve al jugador a la posición inicial.
    """

    sonido_daño.play()

    vidas -= 1

    col, fila = pos_jugador
    tablero[fila][col] = VACIO

    col_i, fila_i = pos_inicial
    tablero[fila_i][col_i] = JUGADOR

    direccion = (0, 0)

    return pos_inicial, vidas, direccion

def cambiar_direccion(keys, direccion_actual):
    """
    Cambia la dirección del jugador.

    Parámetros:
        - keys: Arreglo de teclas presionadas.
        - direccion_actual: La dirección en la que estaba avanzando justo antes de analizar
            si hubo un cambio de dirección.

    Retorna:
        - direccion_actual: La nueva dirección del jugador.
    """

    # Tecla W
    if keys[pygame.K_w]:
        # La tupla nos indica que horizontalmente (columnas) no hará nada (0) y
        # que verticalmente (filas) disminuirá el índice en el tablero (-1).
        return (0, -1)

    # Tecla S
    if keys[pygame.K_s]:
        # En este caso avanzará a través de las filas del tablero.
        return (0, 1)

    # Tecla A
    if keys[pygame.K_a]:
        # Retrocede por las columnas del tablero.
        return (-1, 0)

    # Tecla D
    if keys[pygame.K_d]:
        # Avanza por las columnas del tablero.
        return (1, 0)

    # Si no se presiona ninguna de las teclas anteriores, la dirección
    # será la misma que la anterior.
    return direccion_actual


def avanzar(tablero, pos_jugador,pos_inicial, direccion, manzanas_comidas, sonido_manzana, sonido_daño, vidas):
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
        pos_jugador, vidas, direccion = perder_vida(tablero,pos_jugador,pos_inicial,vidas,sonido_daño)
        if vidas <= 0:
            return "derrota", pos_jugador, manzanas_comidas, vidas, direccion
        return "ok", pos_jugador, manzanas_comidas, vidas, direccion


    # Obtenemos el elemento que se encuentre en el tablero en la nueva posición del jugador.
    pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

        
    if pos_elem == OBSTACULO or pos_elem == ENEMIGO:
        pos_jugador, vidas, direccion = perder_vida(tablero,pos_jugador,pos_inicial,vidas,sonido_daño)
        if vidas <= 0:
            return "derrota", pos_jugador, manzanas_comidas, vidas, direccion
        return "ok", pos_jugador, manzanas_comidas, vidas, direccion

    if pos_elem == MANZANA:
        sonido_manzana.play()
        manzanas_comidas += 1

        # Mover al jugador a la nueva casilla
        tablero[ind_actual_fila][ind_actual_col] = VACIO

        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

        # Si llegamos al objetivo, victoria
        if manzanas_comidas >= MANZANAS_PARA_GANAR:
            return "victoria", (ind_nueva_col, ind_nueva_fila), manzanas_comidas, vidas,direccion
        
            
    # Movimiento normal, si es que no encontramos manzana ni obstáculo.
    tablero[ind_actual_fila][ind_actual_col] = VACIO
    tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

    return "ok", (ind_nueva_col, ind_nueva_fila), manzanas_comidas, vidas,direccion

def obtener_direccion_aleatoria():
        return random.choice([(0,-1), (0, 1), (-1, 0), (1, 0)])

def avanzar_enemigos(tablero,pos_enemigos,pos_jugador,pos_inicial,vidas,sonido_daño):
    for i in range(len(pos_enemigos)):

        pos_enemigo = pos_enemigos[i]
        col, fila = pos_enemigo

        dir_col, dir_fila = obtener_direccion_aleatoria()

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
                pos_jugador, vidas, direccion = perder_vida(tablero,pos_jugador,pos_inicial,vidas,sonido_daño)

                if vidas <= 0:
                    return "derrota", pos_enemigos, pos_jugador, vidas

    return "ok", pos_enemigos, pos_jugador, vidas

  

   
 
