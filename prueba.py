import pygame
import random




ANCHO= 800 #VENTANA
ALTO= 600 #ALTO DE VENTANA
NEGRO = (0,0,0) #FONDO NEGRO
BLANCO = (255,255,255) #BARRA
VERDE = (0, 255, 0) #BARRA Y TEXTO



pygame.init()
pygame.mixer.init()  #SONIDO

VENTANA = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Nave") #TITULO VENTANA   
clock = pygame.time.Clock() #RELOJ FRAME POR SEGUNDO

#añadido 23/05/2023 FUENTE DEL MARCADOR
def dibujar_texto(superficie, texto, tamaño, posicionx, posiciony, color=BLANCO):
    fuente = pygame.font.SysFont("serif", tamaño)
    texto_superficie = fuente.render(texto,True, color)#DEFINICION DEL TEXTO
    texto_rect = texto_superficie.get_rect()
    texto_rect.midtop = (posicionx, posiciony)
    superficie.blit(texto_superficie, texto_rect)

#ESCUDO
def dibujar_escudo_barra(superficie, posicionx, posiciony, porcentaje):
    LARGO_DE_BARRA = 100
    ALTO_DE_BARRA = 10
    LLENAR = (porcentaje / 100) * LARGO_DE_BARRA
    BORDE_BARRA = pygame.Rect(posicionx, posiciony, LARGO_DE_BARRA, ALTO_DE_BARRA)
    LLENAR = pygame.Rect(posicionx, posiciony, LLENAR, ALTO_DE_BARRA)
    pygame.draw.rect(superficie, VERDE, LLENAR)
    pygame.draw.rect(superficie, BLANCO, BORDE_BARRA, 2) 

#CLASE JUGADOR
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() #SUPER CLASS SPRITE
        self.image = pygame.image.load("material/nave/nave1.png") #OJO CARPETA            
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10 
        self.velocidad = 0
        self.escudo = 100

        
    def update(self):
        self.velocidad = 0
        tecla_precionada = pygame.key.get_pressed()#LISTA DE TECLAS PRECIONADA
        if tecla_precionada [pygame.K_LEFT]: #TECLA IZQUIERDA SI FUE PRESIONADA
            self.velocidad = -5
        if tecla_precionada [pygame.K_RIGHT]: #TECLA DERECHA SI FUE PRESIONADA
            self.velocidad = 5
        self.rect.x += self.velocidad
        if self.rect.right > ANCHO: #BORDE DE LA NAVE
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0

    def disparo(self): #BALA
        bala = Bala(self.rect.centerx, self.rect.top)
        grupo_sprites.add(bala)
        grupo_bala.add(bala)
        bala_sonido.play()



#CLASE METEORITO
class Meteorito(pygame.sprite.Sprite): #CLASSE METEORITO
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteoro_imagenes) #OJO CARPETA
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange (ANCHO - self.rect.width) #PARA QUE APAREZCAN EN CUALQUIER LUGAR.
        self.rect.y = random.randrange (-140, -100) #EFECTO DE BAJADA
        self.vel_y = random.randrange (1, 10) #VELOCIDAD ALEOTORIA
        self.vel_x = random.randrange (-5, 5)

    def update(self):
     self.rect.y += self.vel_y
     self.rect.x += self.vel_x
     if self.rect.top > ALTO + 10 or self.rect.left < -40 or self.rect.right > ANCHO + 40:
        self.rect.x = random.randrange (ANCHO - self.rect.width) #PARA QUE APAREZCAN EN CUALQUIER LUGAR.
        self.rect.y = random.randrange (-100, -40) #EFECTO DE BAJADA
        self.vel_y = random.randrange (1, 8) #VELOCIDAD ALEOTORIA

 #CLASE BALA      
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y): #CON LA X, Y, PARA LA POSICIÓN
        super().__init__()
        self.image = pygame.image.load("material/bala/bala.png")#OJO CARPETA
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x #CENTRO DEL OBJETO MAS FACIL
        self.vel_y = -10 #va ir decreceindo cada ves que suba
    
    def update(self):
        self.rect.y += self.vel_y
        if self.rect.bottom < 0: 
            self.kill()

#CLASE EXPLOSIONES
class Explosiones(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosiones_max[0]#1
        self.rect = self.image.get_rect()
        self.rect.center = center #FALLO OJO!!!
        self.frame = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.frame_velocidad = 50 # velocidad de la explsion

    def update(self):
        ya = pygame.time.get_ticks() #CUANTO TIEMPO A TRAS CURRIDO
        if ya - self.ultima_actualizacion > self.frame_velocidad:
            self.ultima_actualizacion = ya
            self.frame += 1
            if self.frame == len(explosiones_max):
                self.kill()
            else: 
                center = self.rect.center
                self.image = explosiones_max[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#VENTANA DE INICIO Y GAME OVER
def fin_de_ventana():
    dibujar_texto(VENTANA, "NAVE", 65, ANCHO // 2, ALTO // 4,VERDE)
    dibujar_texto(VENTANA, "Instrucciones", 27, ANCHO // 2, ALTO // 2)
    dibujar_texto(VENTANA, "Epacio para disparar", 27, ANCHO // 2, ALTO // 2+30)
    dibujar_texto(VENTANA, "Toca cualquier tecla para comenzar", 27, ANCHO // 2, ALTO // 2+60)
    #dibujar_texto(VENTANA, "Dale play", 20, ANCHO // 2, ALTO * 3/4)
    
    # Cuadro rojo
    cuadro_rect = pygame.Rect(ANCHO // 2 - 60, ALTO * 3 // 4 - 20, 125, 45)
    pygame.draw.rect(VENTANA, (255, 0, 0), cuadro_rect)

    # Texto "Dale play" en blanco dentro del cuadro rojo
    dibujar_texto(VENTANA, "Dale play", 20, ANCHO // 2, ALTO * 3 // 4, BLANCO)
    
    pygame.display.flip()
    espera = True
    while espera:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                espera = False
    
    
    #pygame.display.flip()
    #espera = True
    #while espera:
        #clock.tick(60)
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #pygame.quit()
            #if event.type == pygame.KEYUP:
                #espera = False


#LISTA DE METEOROS ALEOTORIOS IMAGENES
meteoro_imagenes = []
for bam in range (9):
    archivo = "material/meteoritos/meteorito0{}.png".format(bam)
    img = pygame.image.load(archivo)
    meteoro_imagenes.append(img)


#LISTA DE EXPLOSIONES IMAGENES
explosiones_max = []
for bam in range(9):
    archivo = "material/explosion/explosion0{}.png".format(bam)
    img = pygame.image.load(archivo)    
    img_escala = pygame.transform.scale(img, (70,70))
    explosiones_max.append(img_escala)
    


#CARGAR SONIDOS
bala_sonido = pygame.mixer.Sound("material/musica/BALA.ogg")
explosiones_sonido = pygame.mixer.Sound("material/musica/EXPLOSIONES.wav")
pygame.mixer.music.load("material/musica/MUSICAFULL.ogg")
pygame.mixer.music.set_volume(0.2)#controlador de volumen de la musica




 #variable que va llevar la cuenta
pygame.mixer.music.play(loops=-1)#bucle musica infinitamente

#FIN DEL JUEGO----!
fin_del_juego = True
velocidad = True


#BUCLE PRINCIPAL
bucle_inicio =  True
while bucle_inicio:
    if fin_del_juego:

        fin_de_ventana()

        fin_del_juego = False
        grupo_sprites = pygame.sprite.Group() #GP JUGADOR
        grupo_meteorito = pygame.sprite.Group() #GP METEORITO
        grupo_bala = pygame.sprite.Group() #GP BALA

        jugador = Jugador()
        grupo_sprites.add(jugador)
        for i in range(8):
            meteorito = Meteorito()
            grupo_sprites.add(meteorito)
            grupo_meteorito.add(meteorito)


        marcador = 0



    clock.tick(60) #RELOJ FPS POR SG
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bucle_inicio = False

        elif event.type == pygame.KEYDOWN: #DISPARO EN CLASE JUGADOR
            if event.key == pygame.K_SPACE:
                jugador.disparo()
        
    
    grupo_sprites.update()



    #COLISIONES (METERO + BALA)
    disparo = pygame.sprite.groupcollide(grupo_meteorito, grupo_bala, True, True)
    for dispar in disparo:
        marcador +=10
        explosiones_sonido.play() #explision sonido
        explosiones = Explosiones(dispar.rect.center)
        grupo_sprites.add(explosiones)
        meteorito = Meteorito() #bucle meteorito
        grupo_sprites.add(meteorito)
        grupo_meteorito.add(meteorito)

    #COLISIONES  #RUNNING (BUBLE_INICIO)
    golpes = pygame.sprite.spritecollide(jugador, grupo_meteorito, True)
    for golpe in golpes:
        jugador.escudo -= 25
        meteorito = Meteorito() #bucle meteorito
        grupo_sprites.add(meteorito)
        grupo_meteorito.add(meteorito)
        if jugador.escudo <= 0:
            fin_del_juego = True
    


    VENTANA.fill(NEGRO)
    grupo_sprites.draw(VENTANA)

    #MARCADOR *_*
    dibujar_texto(VENTANA, str(marcador), 25, ANCHO // 2, 10)

    #ESCUDO *_*
    dibujar_escudo_barra(VENTANA, 5, 5, jugador.escudo)

    pygame.display.flip()
    
pygame.quit()