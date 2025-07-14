# enemigo_alpha.py
import pygame
import math
from collections import deque


CAMINABLES = [0, 1, 2]

enemigo_pos = [0, 0]
enemigo_img = None
TILE_WIDTH = TILE_HEIGHT = 32
board = []
activo = True  # puede usarse para desactivar el enemigo si se quiere

def inicializar_enemigo(tablero, ancho, alto, pos_inicial=(19, 14), ruta_imagen=r"C:\Users\eduar\OneDrive\Documents\EscapaDeLaUNAL-main\Assets1\Cabra test.png"):
    global enemigo_pos, enemigo_img, TILE_WIDTH, TILE_HEIGHT, board
    board = tablero
    enemigo_pos = list(pos_inicial)

    TILE_HEIGHT = (alto - 50) // 32
    TILE_WIDTH = ancho // 30

    try:
        cabra_original = pygame.image.load(ruta_imagen)
        enemigo_img = pygame.transform.scale(cabra_original, (int(TILE_WIDTH), int(TILE_HEIGHT)))
    except Exception as e:
        print("Error cargando la imagen del enemigo:", e)
        enemigo_img = None



def mover_enemigo(player_pos):
    global enemigo_pos
    if not activo:
        return

    filas = len(board)
    columnas = len(board[0])
    visitado = [[False]*columnas for _ in range(filas)]
    came_from = {}

    cola = deque()
    cola.append(tuple(enemigo_pos))
    visitado[enemigo_pos[0]][enemigo_pos[1]] = True

    encontrado = False

    while cola:
        actual = cola.popleft()
        if actual == player_pos:
            encontrado = True
            break

        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nx = actual[0] + dx
            ny = actual[1] + dy
            if 0 <= nx < filas and 0 <= ny < columnas and not visitado[nx][ny]:
                if board[nx][ny] in CAMINABLES:
                    visitado[nx][ny] = True
                    came_from[(nx, ny)] = actual
                    cola.append((nx, ny))

    if encontrado:
        camino = []
        nodo = player_pos
        while nodo != tuple(enemigo_pos):
            camino.append(nodo)
            nodo = came_from[nodo]
        camino.reverse()

        if camino:
            enemigo_pos[0], enemigo_pos[1] = camino[0]

   
def dibujar_enemigo(superficie):
    x = enemigo_pos[1] * TILE_WIDTH
    y = enemigo_pos[0] * TILE_HEIGHT
    if enemigo_img:
        superficie.blit(enemigo_img, (x, y))
    else:
        pygame.draw.rect(superficie, (255, 0, 255), (x, y, TILE_WIDTH, TILE_HEIGHT))

def get_enemigo_pos():
    return tuple(enemigo_pos)