import pygame, sys, time, random
from pygame import display
from pygame.locals import *
import math

# configurar pygame
pygame.init()
relojPrincipal = pygame.time.Clock()

gameRunning = True

# configurar la ventana
ANCHOVENTANA = 500
ALTOVENTANA = 500
superficieVentana = pygame.display.set_mode((ANCHOVENTANA, ALTOVENTANA), 0, 32)
pygame.display.set_caption('Sprites y Sonido')

# configurar los colores
NEGRO = (0, 0, 0)

# configurar la estructura de bloque de datos
jugador = pygame.Rect(300, 100, 40, 40)

#Estados juego
jugando = False

pacmanArriba = pygame.image.load('PacmanArriba.png')
pacmanAbajo = pygame.image.load('PacmanAbajo.png')
pacmanDerecha = pygame.image.load('PacmanDerecha.png')
pacmanIzquierda = pygame.image.load('PacmanIzq.png')

#Fantasmita
enemy = pygame.Rect(100, 100, 10, 40)
fantasmitaAuto= pygame.image.load('fantasmita-izquierda.png')

enemy2 = pygame.Rect(50, 100, 10, 40)
fantasmitaTop= pygame.image.load('fantasmita-izquierda.png')

enemy3 = pygame.Rect(75, 100, 10, 40)
fantasmitaBottom = pygame.image.load('fantasmita-izquierda.png')

# Fantasmita configurar variables del teclado
VELOCIDADMOVIMIENTOENEMY = 3

#imagenEstiradaJugador = pygame.transform.scale(imagenJugador, (40, 40))
imagenComida = pygame.image.load('cereza.png')
comidas = []

puntaje = 0

for i in range(20):
    comidas.append(pygame.Rect(random.randint(0, ANCHOVENTANA - 20), random.randint(0, ALTOVENTANA - 20), 20, 20))

contadorComida = 0
NUEVACOMIDA = 100

# configurar variables del teclado
moverseIzquierda = False
moverseDerecha = False
moverseArriba = False
moverseAbajo = False
lastState = "moverseDerecha"

VELOCIDADMOVIMIENTO = 5

# configurar música
sonidoRecolección = pygame.mixer.Sound('recolección.wav')
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1, 0.0)
músicaSonando = True

level = 0

# Pantalla de inicio
pantallaInicio = pygame.image.load('Start.jpg')
fondo = pygame.image.load('background.jpg')

while True:
    # comprobar si se ha disparado el evento QUIT (salir)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

        if level == 0:
            superficieVentana.blit(pantallaInicio, pygame.Rect(0, 0, ANCHOVENTANA, ALTOVENTANA))
            pygame.display.update()

            if evento.type == KEYDOWN:
                if evento.key == K_SPACE: level = 1

        elif level == 1:
            if evento.type == KEYDOWN and gameRunning:
                # cambiar las variables del teclado
                if evento.key == K_LEFT or evento.key == ord('a'):
                    moverseDerecha = False
                    moverseIzquierda = True
                
                if evento.key == K_RIGHT or evento.key == ord('d'):
                    moverseIzquierda = False
                    moverseDerecha = True
                
                if evento.key == K_UP or evento.key == ord('w'):
                    moverseAbajo = False
                    moverseArriba = True
                
                if evento.key == K_DOWN or evento.key == ord('s'):
                    moverseArriba = False
                    moverseAbajo = True
                
            if evento.type == KEYUP:
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key == K_LEFT or evento.key == ord('a'):
                    moverseIzquierda = False
                
                if evento.key == K_RIGHT or evento.key == ord('d'):
                    moverseDerecha = False
                
                if evento.key == K_UP or evento.key == ord('w'):
                    moverseArriba = False
                   
                if evento.key == K_DOWN or evento.key == ord('s'):
                    moverseAbajo = False
                    
                if evento.key == ord('x'):
                    jugador.top = random.randint(0, ALTOVENTANA - jugador.height)
                    jugador.left = random.randint(0, ANCHOVENTANA - jugador.width)
                if evento.key == ord('m'):
                    if músicaSonando:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    músicaSonando = not músicaSonando

            if evento.type == MOUSEBUTTONUP:
                comidas.append(pygame.Rect(evento.pos[0] - 10, evento.pos[1] - 10, 20, 20))

    if level == 1:
        superficieVentana.fill(NEGRO)

        superficieVentana.blit(fondo, pygame.Rect(0, 0, ANCHOVENTANA, ALTOVENTANA))
        
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Puntaje: ' + str(puntaje), True, (255,255,255), (0, 0, 0))
        superficieVentana.blit(text, pygame.Rect(30, 30, 100, 25))

        contadorComida += 1
        if contadorComida >= NUEVACOMIDA:
            # agregar nueva comida
            contadorComida = 0
            comidas.append(pygame.Rect(random.randint(0, ANCHOVENTANA - 20), random.randint(0, ALTOVENTANA - 20), 20, 20))
        # mover el jugador
        if moverseAbajo and jugador.bottom < ALTOVENTANA:
            jugador.top += VELOCIDADMOVIMIENTO
            superficieVentana.blit(pacmanAbajo, jugador)
            lastState = "moverseAbajo"
        elif moverseArriba and jugador.top > 0:
            jugador.top -= VELOCIDADMOVIMIENTO
            superficieVentana.blit(pacmanArriba, jugador)
            lastState = "moverseArriba"
        elif moverseIzquierda and jugador.left > 0:
            jugador.left -= VELOCIDADMOVIMIENTO
            superficieVentana.blit(pacmanIzquierda, jugador)
            lastState = "moverseIzquierda"
        elif moverseDerecha and jugador.right < ANCHOVENTANA:
            jugador.right += VELOCIDADMOVIMIENTO
            superficieVentana.blit(pacmanDerecha, jugador)
            lastState = "moverseDerecha"
        else:
            if lastState == "moverseDerecha": superficieVentana.blit(pacmanDerecha, jugador)
            if lastState == "moverseIzquierda": superficieVentana.blit(pacmanIzquierda, jugador)
            if lastState == "moverseAbajo": superficieVentana.blit(pacmanAbajo, jugador)
            if lastState == "moverseArriba": superficieVentana.blit(pacmanArriba, jugador)

        #GHOST AUTO--------------------------------------------
        dx = jugador.x - enemy.x
        dy = jugador.y - enemy.y

        dist = math.hypot(dx, dy)
        dx, dy = dx / (dist + 0.1) , dy / (dist+0.1)   # Normalize.
        
        # Acercar al jugador
        enemy.x += dx * VELOCIDADMOVIMIENTOENEMY
        enemy.y += dy * VELOCIDADMOVIMIENTOENEMY

        superficieVentana.blit(fantasmitaAuto, enemy)
        


        if jugador.colliderect(enemy): #or enemy2 or enemy3):
            comidas = []
            gameRunning = False
            font = pygame.font.Font('freesansbold.ttf', 72)
            text = font.render('Perdiste :(', True, (255,255,255), (0, 0, 0))
            superficieVentana.blit(text, pygame.Rect(60, (ALTOVENTANA/2)-50, 100, 50))

        # comprobar si el jugador ha intersectado alguno de los cuadrados de comida
        for comida in comidas[:]:
            if jugador.colliderect(comida):
                comidas.remove(comida)
                jugador = pygame.Rect(jugador.left, jugador.top, jugador.width + 2, jugador.height + 2)
                #imagenEstiradaJugador = pygame.transform.scale(imagenJugador, (jugador.width, jugador.height))
                puntaje = puntaje + 1
                if músicaSonando:
                    sonidoRecolección.play()

        if puntaje >= 10:
            comidas = []
            gameRunning = False

            font = pygame.font.Font('freesansbold.ttf', 72)
            text = font.render('GANASTE!', True, (255,255,255), (0, 0, 0))
            superficieVentana.blit(text, pygame.Rect(60, (ALTOVENTANA/2)-50, 100, 50))

        # dibujar la comida
        for comida in comidas:
            superficieVentana.blit(imagenComida, comida)

    # dibujar la ventana sobre la pantalla
    relojPrincipal.tick(40)
    pygame.display.update()