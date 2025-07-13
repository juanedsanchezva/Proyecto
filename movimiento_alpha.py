# movimiento_alpha.py
import pygame
import random
import os

CAMINABLES = [1, 2]

player_pos = [0, 0]
TILE_WIDTH = TILE_HEIGHT = 32
buho_img = None
board = []

def inicializar_movimiento(tablero, ancho, alto, ruta_imagen_buho="INTERFAZ GRAFICA/Buho test.png"):
    global player_pos, TILE_WIDTH, TILE_HEIGHT, buho_img, board
    board = tablero

    TILE_HEIGHT = (alto - 50) // 32  # como num1 en draw_board
    TILE_WIDTH = ancho // 30         # como num2 en draw_board

    posiciones_validas = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] in CAMINABLES]
    player_pos = list(random.choice(posiciones_validas))

    try:
        buho_img_original = pygame.image.load(ruta_imagen_buho)
        buho_img = pygame.transform.scale(buho_img_original, (int(TILE_WIDTH), int(TILE_HEIGHT)))
    except Exception as e:
        print("Error cargando la imagen del búho:", e)
        buho_img = None

def mover_personaje(direccion):
    dx, dy = 0, 0
    if direccion == 'w': dx = -1       # ↑ arriba (fila -1)
    elif direccion == 's': dx = 1       # ↓ abajo  (fila +1)
    elif direccion == 'a': dy = -1       # → derecha (columna +1)
    elif direccion == 'd': dy = 1      # ← izquierda (columna -1)

    while True:
        nueva_x = player_pos[0] + dx
        nueva_y = player_pos[1] + dy

        if (
            0 <= nueva_x < len(board) and
            0 <= nueva_y < len(board[0]) and
            board[nueva_x][nueva_y] in CAMINABLES
        ):
            player_pos[0], player_pos[1] = nueva_x, nueva_y
        else:
            break

def dibujar_personaje(superficie):
    x = player_pos[1] * TILE_WIDTH
    y = player_pos[0] * TILE_HEIGHT
    if buho_img:
        superficie.blit(buho_img, (x, y))
    else:
        pygame.draw.rect(superficie, (255, 0, 0), (x, y, TILE_WIDTH, TILE_HEIGHT))