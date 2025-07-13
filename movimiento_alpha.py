# movimiento_alpha.py
import pygame
import random
import os
import time

CAMINABLES = [1, 2]

player_pos = [0, 0]
TILE_WIDTH = TILE_HEIGHT = 32
buho_img = None
board = []

estela = []  # Lista de (fila, columna, tiempo_de_creacion)
VIDA_ESTELA_MS = 400  # tiempo de vida en milisegundos (0.4 segundos aprox)

def inicializar_movimiento(tablero, ancho, alto, ruta_imagen_buho="INTERFAZ GRAFICA/Buho test.png"):
    global player_pos, TILE_WIDTH, TILE_HEIGHT, buho_img, board, estela
    board = tablero
    estela = []  # Limpiar rastro

    TILE_HEIGHT = (alto - 50) // 32
    TILE_WIDTH = ancho // 30

    posiciones_validas = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] in CAMINABLES]
    player_pos = list(random.choice(posiciones_validas))

    try:
        buho_img_original = pygame.image.load(ruta_imagen_buho)
        buho_img = pygame.transform.scale(buho_img_original, (int(TILE_WIDTH), int(TILE_HEIGHT)))
    except Exception as e:
        print("Error cargando la imagen del búho:", e)
        buho_img = None

def mover_personaje(direccion):
    global player_pos
    dx, dy = 0, 0
    if direccion == 'w': dx = -1       # ↑ arriba
    elif direccion == 's': dx = 1      # ↓ abajo
    elif direccion == 'a': dy = -1      # → derecha
    elif direccion == 'd': dy = 1     # ← izquierda

    while True:
        nueva_x = player_pos[0] + dx
        nueva_y = player_pos[1] + dy

        if (
            0 <= nueva_x < len(board) and
            0 <= nueva_y < len(board[0]) and
            board[nueva_x][nueva_y] in CAMINABLES
        ):
            # Guardar la posición y el tiempo
            estela.append((player_pos[0], player_pos[1], pygame.time.get_ticks()))
            player_pos[0], player_pos[1] = nueva_x, nueva_y
        else:
            break

def dibujar_personaje(superficie):
    tiempo_actual = pygame.time.get_ticks()
    estela_viva = []

    for fila, col, creado_en in estela:
        tiempo_transcurrido = tiempo_actual - creado_en
        if tiempo_transcurrido < VIDA_ESTELA_MS:
            # Calcular opacidad: más reciente = más visible
            alpha = int(255 * (1 - (tiempo_transcurrido / VIDA_ESTELA_MS)))
            sombra = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
            sombra.fill((255, 255, 0, alpha))  # amarillo transparente
            x = col * TILE_WIDTH
            y = fila * TILE_HEIGHT
            superficie.blit(sombra, (x, y))
            estela_viva.append((fila, col, creado_en))  # conservar
        # si ya expiró, no lo añadimos a la nueva lista

    # Actualizar estela eliminando los pasos viejos
    estela.clear()
    estela.extend(estela_viva)

    # Dibujar al personaje
    x = player_pos[1] * TILE_WIDTH
    y = player_pos[0] * TILE_HEIGHT
    if buho_img:
        superficie.blit(buho_img, (x, y))
    else:
        pygame.draw.rect(superficie, (255, 0, 0), (x, y, TILE_WIDTH, TILE_HEIGHT))