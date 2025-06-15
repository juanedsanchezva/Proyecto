import pygame
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
})

usuario_actual = "Juan Sanchez".replace(" ", "_").lower()

def obtener_monedas(usuario_id):
    try:
        ref = db.reference(f'users/{usuario_id}')
        datos = ref.get()
        if datos and 'monedas' in datos:
            return datos['monedas']
        else:
            return 0
    except Exception as e:
        print(f"Error al obtener monedas: {e}")
        return 0
 

def registrar_compra(nombre_usuario, producto):
    ref = db.reference(f"usuarios/{nombre_usuario}/compras")
    nueva_compra = {
        "item": producto["nombre"],
        "precio": producto["precio"]
    }
    ref.push(nueva_compra)




#Inicializar Pygame 
pygame.init()
ANCHO = 300
ALTO = 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TIENDA_V1")
reloj = pygame.time.Clock()
fondo = pygame.image.load("pixil-frame-02 (2).png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
fuente = pygame.font.Font("DePixelHalbfett.ttf", 15)
fuente_saldo = pygame.font.Font("DePixelHalbfett.ttf", 11)

productos = [
    {"nombre": "Velocidad+", "precio": 100},
    {"nombre": "Escudo", "precio": 80},
    {"nombre": "Multiplicador XP", "precio": 100}
]


#Función para dibujar botones y texto
def dibujar_tienda(pos_mouse=None, click=False):
    pantalla.blit(fondo, (0, 0))
    y = 100
    botones.clear()

    # Mostrar saldo
    saldo_text = fuente_saldo.render(f"Monedas: {saldo_jugador}", True, (255, 255, 0))
    pantalla.blit(saldo_text, (90, 15))

    # Mostrar mensaje si está activo
    if mensaje:
        msg_text = fuente.render(mensaje, True, (255, 255, 255))
        msg_rect = msg_text.get_rect(center=(ANCHO // 2, ALTO - 40))
        pantalla.blit(msg_text, msg_rect)

    for producto in productos:
        texto = fuente.render(f"{producto['nombre']} -> ${producto['precio']}", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(ANCHO // 2, y))
        pantalla.blit(texto, texto_rect)

        btn_ancho, btn_alto = 120, 40
        btn_x = (ANCHO - btn_ancho) // 2
        btn_y = y + 30
        btn_rect = pygame.Rect(btn_x, btn_y, btn_ancho, btn_alto)
        botones.append((btn_rect, producto))

        if pos_mouse and btn_rect.collidepoint(pos_mouse):
            color = (100, 250, 100) if not click else (50, 150, 50)
        else:
            color = (8, 113, 18)

        pygame.draw.rect(pantalla, color, btn_rect, border_radius=8)
        btn_texto = fuente.render("Comprar", True, (0, 0, 0))
        btn_texto_rect = btn_texto.get_rect(center=btn_rect.center)
        pantalla.blit(btn_texto, btn_texto_rect)

        y += 100

    pygame.display.flip()




#Bucle principal 
usuario_actual = "Juan Sanchez" 
saldo_jugador = obtener_monedas(usuario_actual)
botones = []              # lista de botones
mensaje = ""              # mensaje temporal (compra o error)
mensaje_timer = 0         # duración del mensaje (en frames)
corriendo = True          # bandera para el bucle principal





while corriendo:
    pos_mouse = pygame.mouse.get_pos()
    click = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            click = True
            for btn_rect, producto in botones:
                if btn_rect.collidepoint(pos_mouse):
                  if saldo_jugador >= producto["precio"]:
                     saldo_jugador -= producto["precio"]
                     #Actualiza monedas en Firebase
                     db.reference(f'users/{usuario_actual}').update({"monedas": saldo_jugador})
                     #Guarda la compra en la base de datos
                     db.reference(f'usuarios/{usuario_actual}/compras').push({
                      "item": producto["nombre"],
                      "precio": producto["precio"]
                                           })
                     mensaje = f"Compraste {producto['nombre']}!"
                     mensaje_timer = 120
                     
    #Temporizador para mensaje
    if mensaje_timer > 0:
        mensaje_timer -= 1
    else:
        mensaje = ""

    dibujar_tienda(pos_mouse, click)
    reloj.tick(60)
    



pygame.quit()