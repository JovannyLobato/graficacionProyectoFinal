from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from PIL import Image as Image
import numpy
from numpy import asarray
import pygame
from pygame.locals import *


def read_texture(filename):
    img = Image.open(filename)
    img_data=numpy.asarray(img)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                    GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                    GL_NEAREST)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 img.size[0], img.size[1],0,
                 GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID

pygame.init()
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode(
    (screen_width, screen_height),
    DOUBLEBUF | OPENGL)
pygame.display.set_caption('Muñeco de nieve')
done = False

white = pygame.Color(255, 255, 255)

gluPerspective(60, (screen_width/screen_height), 0.1, 50.0)
glTranslatef(0, 0, -15)    

glPushMatrix()
glEnable(GL_DEPTH_TEST)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


glEnable(GL_LIGHTING)

glLight(GL_LIGHT0, GL_POSITION, (6, 1.5 , 5, 1))
glLightfv(GL_LIGHT0, GL_AMBIENT, (2.0, 2.0 ,2.0,1))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1,1,1))
glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (-1, 0, -1))
glLight(GL_LIGHT0, GL_SPOT_CUTOFF, 80)
glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 0.5)

glEnable(GL_LIGHT0)

BLACK = (0, 0, 0)
fogColor = (1.0, 1.0, 1.0, 0.8)  # fog color
FogMode=True
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    if FogMode==True:
        fogMode = GL_EXP2 # Other nodes: 
        glFogi (GL_FOG_MODE, fogMode)
        glFogfv (GL_FOG_COLOR, fogColor)
        glFogf (GL_FOG_DENSITY, 0.021)
        glHint (GL_FOG_HINT, GL_NICEST)
        glFogf (GL_FOG_START, -1.0)
        glFogf (GL_FOG_END, 5.0)
        glEnable(GL_FOG)  # Enable fog

##
    if False:
        glBegin(GL_QUADS)
        glColor3f(0,0,1)
        glMaterial
        glNormal(0,0,1)
        glVertex3f(-10,10,-10)
        glVertex3f(10,10,-10)
        glVertex3f(10,-10,-10)
        glVertex3f(-10,-10,-10)
        glEnd()
        
    #  Textured sphere
    #glPushMatrix()
    glTranslatef(0,-5,0)
    #glRotatef(90,1,0,0)  #to correct jpeg issues in my Mac
    tex = read_texture('nieve.jpg')
    qobj = gluNewQuadric()
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)
    gluSphere(qobj, 3, 25, 25)
    gluDeleteQuadric(qobj)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    #glTranslatef(0,0,-0.05)
    #glRotatef(0.5,0,1,0)

    glPushMatrix()
    glTranslatef(0,-1,0)
    #glRotatef(90,1,0,0)  #to correct jpeg issues in my Mac
    tex = read_texture('nieve.jpg')
    qobj = gluNewQuadric()
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)
    gluSphere(qobj, 2.5, 20, 20)
    gluDeleteQuadric(qobj)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0,2,0)
    #glRotatef(90,1,0,0)  #to correct jpeg issues in my Mac
    tex = read_texture('negro.jpg')
    qobj = gluNewQuadric()
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)
    gluSphere(qobj, 2, 7, 6)
    gluDeleteQuadric(qobj)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0,-2,0)
    #glRotatef(90,1,0,0)  #to correct jpeg issues in my Mac
    tex = read_texture('bufanda.jpg')
    qobj = gluNewQuadric()
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)
    gluSphere(qobj, 2.5, 10, 10)
    gluDeleteQuadric(qobj)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    pygame.draw.circle(screen,BLACK,(422,253),20)

    
    pygame.display.flip()
    pygame.time.wait(1)
    
    
pygame.quit()

