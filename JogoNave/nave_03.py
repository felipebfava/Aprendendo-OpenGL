
from OpenGL.GL import *
import glfw
import math
import random


x = 0.0
y = 0.0
angulo = 0.0

velocidade = 0.0
vel_rotacao = 0.02
vel_max = 0.0001
aceleracao = 0.00001


num_estrelas = 400
estrelas = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(num_estrelas)]


def init():
    glClearColor(0.0, 0.0, 0.0, 0)


def desenhaEstrelas():

    glLoadIdentity()

    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 0.6)
    for x,y in estrelas:
        glVertex2f(x, y)
    glEnd()


def movimentaEstrelas(window):
    global estrelas
    teclas = glfw.get_key

    if teclas(window, glfw.KEY_UP) == glfw.PRESS and velocidade > 0:
        convert = math.radians(angulo + 90)

        novas_estrelas = []

        for ex, ey in estrelas:
            ex -= math.cos(convert) * velocidade
            ey -= math.sin(convert) * velocidade

            ex, ey = limitarBordas(ex, ey)

            novas_estrelas.append((ex, ey))

        estrelas = novas_estrelas


def desenhaNave():
    glLoadIdentity()

    glTranslatef(x, y, 0)
    glRotatef(angulo, 0.0, 0.0, 1.0) # angulo, x, y, z

    glBegin(GL_TRIANGLES)
    glColor3f(0.36, 0.35, 0.33)

    glVertex2f(0.0, 0.1) # ponta da navinha
    glVertex2f(-0.05, -0.05)
    glVertex2f(0.05, -0.05)
    glEnd()
   

def desenhaPropulsao(window):

    teclas = glfw.get_key

    if teclas(window, glfw.KEY_UP) == glfw.PRESS and velocidade > 0:
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.6, 0.0)
        glVertex2f(0.0, -0.05)   
        glVertex2f(-0.03, -0.08) 
        glVertex2f(0.03, -0.08)  
        glEnd()


def render(window):
    desenhaEstrelas()
    desenhaNave()
    desenhaPropulsao(window)
    # movimentaEstrelas(window)


def atualizarPosicao():
    global x, y

    convert = math.radians(angulo + 90)
    x += math.cos(convert) * velocidade
    y += math.sin(convert) * velocidade

    x, y = limitarBordas(x, y)


def limitarBordas(x, y):
    if(x > 1.0): x = -1.0
    if(x < -1.0): x = 1.0
    if(y > 1.0): y = -1.0
    if(y < -1.0): y = 1.0
    return x, y

## Substituição da Função Teclado
def entradaTeclado(window):
    global angulo, velocidade

    teclas = glfw.get_key

    ## MOVER
    if teclas(window, glfw.KEY_UP) == glfw.PRESS:
        
        velocidade = min(velocidade + aceleracao, vel_max)
    
    if teclas(window, glfw.KEY_DOWN) == glfw.PRESS:
        
        velocidade = max(velocidade - aceleracao, -vel_max)        

    ## ROTACIONAR
    if teclas(window, glfw.KEY_RIGHT) == glfw.PRESS: # para direita
        angulo -= vel_rotacao

    if teclas(window, glfw.KEY_LEFT) == glfw.PRESS: # para esquerda
        angulo += vel_rotacao


def main():
    glfw.init()
    window = glfw.create_window(600, 600, "Minha Navinha 03", None, None)
    glfw.make_context_current(window)
    
    init()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glfw.poll_events()
        entradaTeclado(window)
        atualizarPosicao()
        render(window)
       
        glfw.swap_buffers(window)
        glfw.wait_events_timeout(1)

    glfw.terminate()

if __name__ == "__main__" :
    main()
