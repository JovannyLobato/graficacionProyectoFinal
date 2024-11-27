import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math

# Configuración inicial
# Inicializar Pygame y OpenGL
pygame.init()
glutInit()
pygame.display.set_mode((800, 800), DOUBLEBUF | OPENGL | NOFRAME)
gluPerspective(45, (800 / 800), 0.1, 70.0)  # Proyección en perspectiva
glTranslatef(0.0, 0.0, -7)
pygame.display.set_caption("Proyecto Final, Escena navidenia")


# codigo para la camara y configuracion de la vista
def configurarVista():
    glMatrixMode(GL_PROJECTION)    # Cambia a la matriz de proyección
    glLoadIdentity()               # Resetea la matriz
    gluPerspective(45,(800/800),0.1,70.0)
    glMatrixMode(GL_MODELVIEW)     # Cambia a la matriz de modelado
configurarVista()

# Número de copos de nieve
NUM_copos = 400
copos = []  

# Inicializa los copos de nieve en posiciones aleatorias
def initcopos():
    global copos
    copos = [
        [random.uniform(-1, 1), random.uniform(0, 2)] for _ in range(NUM_copos)
    ]

# Dibuja un copo de nieve como un cuadrado
def drawcopo(x, y):
    size = 0.005  # Tamaño del copo 
    glBegin(GL_QUADS)
    glVertex2f(x - size, y - size)  
    glVertex2f(x + size, y - size)  
    glVertex2f(x + size, y + size)  
    glVertex2f(x - size, y + size)  
    glEnd()

# Actualiza la posición de los copos de nieve
def updatecopos():
    global copos
    for copo in copos:
        copo[1] -= 0.01  # Los copos caen hacia abajo
        if copo[1] < -1:  # Si un copo llega al fondo, reaparece arriba
            copo[1] = 1
            copo[0] = random.uniform(-1, 1)

# Dibuja la escena completa
def drawScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Color blanco para los copos
    for copo in copos:
        drawcopo(copo[0], copo[1])
    pygame.display.flip()


# Variables de la cámara
angulo_horizontal = 0.0
angulo_vertical = 0.0  
#distancia al origen (radio de la orbita)
radio = 10.0  
# velocidad de rotación
speed = 2.0  
# velocidad de zoom con E y Q
zoom_speed = 0.2  

def manejarInput():
    """controla la rotación y el zoom segun la entrada del usuario."""
    global angulo_horizontal, angulo_vertical, radio

    keys = pygame.key.get_pressed()

    #rotación horizontal con A/D
    if keys[K_a]:
        angulo_horizontal -= speed
    if keys[K_d]:
        angulo_horizontal += speed

    #rotacion vertical con W/S (limitada entre -89 y 89 grados)
    if keys[K_w] and angulo_vertical < 89:
        angulo_vertical += speed
    if keys[K_s] and angulo_vertical > -89:
        angulo_vertical -= speed

    #zoom in/out con E/Q
    if keys[K_e] and radio > 2:  #limitar el acercamiento mínimo
        radio -= zoom_speed
    if keys[K_q] and radio < 50:  #limitar el alejamiento máximo
        radio += zoom_speed

def actualizarCamara():
    """Actualiza la posición de la camara usando coordenadas esfericas."""
    angulo_h_rad = math.radians(angulo_horizontal)
    angulo_v_rad = math.radians(angulo_vertical)

    #coordenadas esfericas
    cam_x = radio * math.cos(angulo_v_rad) * math.sin(angulo_h_rad)
    cam_y = radio * math.sin(angulo_v_rad)
    cam_z = radio * math.cos(angulo_v_rad) * math.cos(angulo_h_rad)

    #configurar la vista con gluLookAt
    glLoadIdentity()
    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

glEnable(GL_DEPTH_TEST)



#Pueden usar este metodo para cargar las texturas que quieran (llaman al metodo antes del ciclo principal)
def cargar_textura(ruta):
    # Carga la imagen de la textura
    imagen = pygame.image.load(ruta)
    textura = pygame.image.tostring(imagen, "RGB", True)
    ancho, alto = imagen.get_width(), imagen.get_height()

    # Crea un identificador de textura en OpenGL
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ancho, alto, 0, GL_RGB, GL_UNSIGNED_BYTE, textura)
    
    # Configura los parámetros de textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return tex_id

def draw_pino(textura1,textura2):
    #dibuja pino
    ty=-1
    sx=1.5
    #dibuja conos para aparentar 1 pino
    for i in range(4):
        quadric = gluNewQuadric()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura1) #pone la textura
        gluQuadricTexture(quadric,True)
        
        glPushMatrix()
        glColor3f(0,1,0)
        glTranslatef(0,ty,0)
        glRotatef(90,-1,0,0)
        glScalef(sx,1,0.5)
        gluCylinder(quadric, 1.0, 0.0, 2.0, 50, 10)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
        ty+=0.5
        sx-=0.25

    #Dibuja tronco
    quadric = gluNewQuadric()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura2)
    gluQuadricTexture(quadric,True)
    
    glPushMatrix()
    glColor3f(0.5,0.25,0)
    glTranslatef(0,-1.75,0)
    glRotatef(90,-1,0,0)
    glScalef(0.35,0.5,0.5)
    gluCylinder(quadric, 1.0, 1.0, 2.0, 50, 10)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    #dibuja esferas
    vi_x=-0.85
    vi_y=-1

    es_x=vi_x
    es_y=vi_y

    nEsferas=6
    for i in range(4):
        for j in range(nEsferas):
            cuadrica = gluNewQuadric()
            glPushMatrix()
            glColor3f(1,0,0)#definir color
            glTranslatef(es_x,es_y,0.9)
            gluSphere(cuadrica, 0.1, 20, 20)#dibuja la esfera
            gluDeleteQuadric(cuadrica)
            glPopMatrix()

            es_x+=0.3
            es_y+=0.1

        vi_x+=0.2
        vi_y+=0.6
    
        es_x=vi_x
        es_y=vi_y

        nEsferas-=1

    vi_x=-0.85
    vi_y=-1

    es_x=vi_x
    es_y=vi_y

    nEsferas=6
    for i in range(4):
        for j in range(nEsferas):
            cuadrica = gluNewQuadric()
            glPushMatrix()
            glColor3f(1,1,0)#definir color
            glTranslatef(es_x,es_y,-0.9)
            gluSphere(cuadrica, 0.1, 20, 20)#dibuja la esfera
            gluDeleteQuadric(cuadrica)
            glPopMatrix()

            es_x+=0.3
            es_y+=0.1

        vi_x+=0.2
        vi_y+=0.6
    
        es_x=vi_x
        es_y=vi_y

        nEsferas-=1

    vi_z=-0.85
    vi_y=-1

    es_z=vi_z
    es_y=vi_y

    nEsferas=6
    for i in range(4):
        for j in range(nEsferas):
            cuadrica = gluNewQuadric()
            glPushMatrix()
            glColor3f(0,1,1)#definir color
            glTranslatef(1,es_y,es_z)
            gluSphere(cuadrica, 0.1, 20, 20)#dibuja la esfera
            gluDeleteQuadric(cuadrica)
            glPopMatrix()

            es_z+=0.3
            es_y+=0.1

        vi_z+=0.2
        vi_y+=0.6
    
        es_z=vi_z
        es_y=vi_y

        nEsferas-=1
        
    vi_z=-0.85
    vi_y=-1

    es_z=vi_z
    es_y=vi_y

    nEsferas=6
    for i in range(4):
        for j in range(nEsferas):
            cuadrica = gluNewQuadric()
            glPushMatrix()
            glColor3f(1,0,1)#definir color
            glTranslatef(-1,es_y,es_z)
            gluSphere(cuadrica, 0.1, 20, 20)#dibuja la esfera
            gluDeleteQuadric(cuadrica)
            glPopMatrix()

            es_z+=0.3
            es_y+=0.1

        vi_z+=0.2
        vi_y+=0.6
    
        es_z=vi_z
        es_y=vi_y

        nEsferas-=1

    


# Configuración de OpenGL

""" 
 # esto lo tuve que cambiar
glEnable(GL_DEPTH_TEST)
glClearColor(0.1, 0.1, 0.1, 1)
gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
"""
#Aqui ponen la textura
texturaHojas = cargar_textura('hojas.jpg')
texturaTronco = cargar_textura('madera.PNG')




# Variables de control
running = True
initcopos()
# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_p:
            running = False

    manejarInput()
    actualizarCamara()
    
    # Renderizado
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    updatecopos()
    draw_pino(texturaHojas,texturaTronco)
    drawScene()

    pygame.display.flip()
    pygame.time.wait(10)

# Finalización
pygame.quit()
