from py_compile import main

import glfw
import numpy as np # lembre de instalar o mumpy usando: pip install numpy
from OpenGL.GL import *
import sys

pA = np.array([-0.5, -0.5])
pB = np.array([0.5, -0.5])
pC = np.array([0.0, 0.5])

loop = 500 # aumente esse valor para melhorar a qualidade da imagem, mas cuidado, acima de 500 o começa a ficar lento

def init():
    glClearColor(1, 1, 1, 1)

def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glPointSize(5)
    glBegin(GL_POINTS)
    for alpha in range(0, loop):
        alpha /= loop
        for beta in range(0, loop):
            beta /= loop
            Q = beta * pA * (1 - alpha) + alpha * beta * pB + pC * (1 - beta)
            glColor3f(beta * (1 - alpha), alpha * beta, (1 - beta))
            glVertex2f(Q[0], Q[1])
    glEnd()

def main():
    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800, 600, "Triangulo Interpolação", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    init()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()  