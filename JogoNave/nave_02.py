
from OpenGL.GL import *
import glfw
import math
import random


x = 0.0
y = 0.0
angulo = 0.0

velocidade = 0.0
vel_rotacao = 6.0
vel_max = 0.0003
aceleracao = 0.00005


num_estrelas = 400
estrelas = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(num_estrelas)]

def init():
    glClearColor(0.0, 0.0, 0.0, 0)

def desenhaEstrelas():
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 0.6)
    for x,y in estrelas:
        glVertex2f(x, y)
    glEnd()

def desenhaNave():
    glLoadIdentity()

    glPushMatrix()

    glTranslatef(x, y, 0)
    glRotatef(angulo, 0.0, 0.0, 1.0) # angulo, x, y, z

    glBegin(GL_TRIANGLES)
    glColor3f(0.5,0.7,0)

    glVertex2f(0.1, 0.0) # ponta da navinha
    glVertex2f(-0.05, -0.05)
    glVertex2f(-0.05, 0.05)
   
    glEnd()
   
    glPopMatrix()


def render():
    desenhaEstrelas()
    desenhaNave()

def atualizarPosicao():
    global x, y
    convert = math.radians(angulo)
    x += math.cos(convert) * velocidade
    y += math.sin(convert) * velocidade


def limitarBordas():
    global x, y
    if(x > 1.0): x = -1.0
    if(x < -1.0): x = 1.0
    if(y > 1.0): y = -1.0
    if(y < -1.0): y = 1.0


def teclado(window, key, scancode, action, mods):
    global x, y, angulo, velocidade

    if action == glfw.PRESS or action == glfw.REPEAT:

        ## MOVER PARA FRENTE
        if key == glfw.KEY_UP:
           
            velocidade = min(velocidade + aceleracao, vel_max)
        
        if key == glfw.KEY_DOWN:
           
            velocidade = max(velocidade - aceleracao, -vel_max)        

        ## ROTACIONAR
        if key == glfw.KEY_RIGHT: # para direita
            angulo -= vel_rotacao

        if key == glfw.KEY_LEFT: # para esquerda
            angulo += vel_rotacao


def main():
    glfw.init()
    window = glfw.create_window(600, 600, "Minha Navinha 02", None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, teclado)

    init()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        atualizarPosicao()
        limitarBordas()
        render()
       
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__" :
    main()
