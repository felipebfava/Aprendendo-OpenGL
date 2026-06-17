
from OpenGL.GL import *
import glfw
import math
import random

velocidade = 0.005
aceleracao = 0
rotacao = 5 # de quanto em quanto vai rodar

tran_x = 0.0
tran_y = 0.0
angulo = 0.0

num_estrelas = 400
estrelas = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(num_estrelas)]

def init():
    glClearColor(0, 0, 0, 0) # seta cor de fundo

def render():
    global aceleracao
   
    glClear(GL_COLOR_BUFFER_BIT)

    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 0.6)
    for x,y in estrelas:
        glVertex2f(x, y)
    glEnd()

    glLoadIdentity()

    glPushMatrix()

    glTranslatef(tran_x, tran_y, 0)
    glRotatef(angulo, 0, 0, 1) # angulo, x, y, z

    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    # glColor3f(0.2, 0.6, 0.9)
    glColor3f(0.5,0.7,0)
    # glColor3f(1, 0, 0)

    glVertex2f(0.1, 0.0) # ponta da navinha
    glVertex2f(-0.1, -0.1)
    glVertex2f(-0.1, 0.1)
   
    glEnd()
   
    glPopMatrix()


def teclado(window, key, scancode, action, mods):
    global velocidade, rotacao, tran_x, tran_y, angulo, aceleracao

    if action == glfw.PRESS or action == glfw.REPEAT:

        ## MOVER PARA FRENTE
        if key == glfw.KEY_UP:
           
            if(aceleracao <= 0.02):
                aceleracao += 0.0001
           
            velocidade += aceleracao
           
            if(velocidade > 0.02):
                velocidade = 0.02
           
            convert = math.radians(angulo)
            tran_x += math.cos(convert) * velocidade
            tran_y += math.sin(convert) * velocidade

            if(tran_x > 1): tran_x = -1
            if(tran_x < -1): tran_x = 1
            if(tran_y > 1): tran_y = -1
            if(tran_y < -1): tran_y = 1           

        if key == glfw.KEY_DOWN:
           
            if(aceleracao > -0.02):
                aceleracao -= 0.0001
           
            if(velocidade < -0.02):
                velocidade = -0.02
           
            convert = math.radians(angulo)
            tran_x -= math.cos(convert) * velocidade
            tran_y -= math.sin(convert) * velocidade

            if(tran_x > 1): tran_x = -1
            if(tran_x < -1): tran_x = 1
            if(tran_y > 1): tran_y = -1
            if(tran_y < -1): tran_y = 1

        ## ROTACIONAR
        if key == glfw.KEY_RIGHT: # para direita
            angulo -= rotacao

        if key == glfw.KEY_LEFT: # para esquerda
            angulo += rotacao
           

def main():
   
    glfw.init()
    window = glfw.create_window(600, 600, "Minha Navinha 01", None, None)
    glfw.make_context_current(window)

    glfw.set_key_callback(window, teclado)    

    init()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__" :
    main()
