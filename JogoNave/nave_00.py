#nave.py

from OpenGL.GL import *
import glfw
import math

velocidade = 0.02
rotacao = 5 # de quanto em quanto vai rodar

tran_x = 0.0
tran_y = 0.0
angulo = 0.0

def init():
    glClearColor(1, 1, 1, 1) # seta cor de fundo


def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    glPushMatrix()

    glTranslatef(tran_x, tran_y, 0)
    glRotatef(angulo, 0, 0, 1) # angulo, x, y, z
    
    glPointSize(10)
    glBegin(GL_POINTS)
    glColor3f(1, 0, 0)
    glVertex2f(0.3, 0.0)

    glEnd()

    glLineWidth(6)
    glBegin(GL_LINE_LOOP)
    # glColor3f(0.2, 0.6, 0.9)
    # glColor3f(0.5,0.7,0)
    glColor3f(1, 0, 0)

    glVertex2f(0.3, 0.0) # ponta da navinha
    glVertex2f(-0.3, -0.3)
    glVertex2f(-0.3, 0.3)
    
    glEnd()
    
    glPopMatrix()


def teclado(window, key, scancode, action, mods):
    global velocidade, rotacao, tran_x, tran_y, angulo


    if action == glfw.PRESS or action == glfw.REPEAT:

        ## MOVER PARA FRENTE
        if key == glfw.KEY_UP: # para cima
            convert = math.radians(angulo)
            tran_x += math.cos(convert) * velocidade
            tran_y += math.sin(convert) * velocidade


        if key == glfw.KEY_DOWN: # para baixo
            convert = math.radians(angulo)
            tran_x -= math.cos(convert) * velocidade
            tran_y -= math.sin(convert) * velocidade

        ## ROTACIONAR
        if key == glfw.KEY_RIGHT: # para direita
            angulo -= rotacao

        if key == glfw.KEY_LEFT: # para esquerda
            angulo += rotacao
            


def main():
    glfw.init()
    window = glfw.create_window(600, 600, "Minha Navinha 00", None, None)
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
