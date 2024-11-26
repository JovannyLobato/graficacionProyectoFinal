import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

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

    
# Configuración inicial
pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Dibujo de un Cono con Pygame y PyOpenGL")

# Configuración de OpenGL
glEnable(GL_DEPTH_TEST)
glClearColor(0.1, 0.1, 0.1, 1)
gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

#cargar textura
texturaHojas = cargar_textura('D:\graficacion\proyecto final\hojas.jpg')
texturaTronco = cargar_textura('D:\graficacion\proyecto final\madera.png')

# Variables de control
running = True

# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Renderizado
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_pino(texturaHojas,texturaTronco)
    

    pygame.display.flip()
    pygame.time.wait(10)

# Finalización
pygame.quit()
