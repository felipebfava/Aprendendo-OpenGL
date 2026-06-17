import glfw
from OpenGL.GL import *
import math
import random

pos_x = 0.0
pos_y = 0.0
angulo = 0.0
velocidade = 0.0
vel_rotacao = 3.0
vel_max = 0.02
aceleracao = 0.0005

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0) 

num_estrelas = 400
estrelas = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(num_estrelas)]

    
def render(window):
    glClear(GL_COLOR_BUFFER_BIT)

    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 0.6)
    for x,y in estrelas:
        glVertex2f(x, y)
    glEnd()
    

    glLoadIdentity()
    glTranslatef(pos_x, pos_y, 0.0) 
    glRotatef(angulo, 0.0, 0.0, 1.0)     

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0) 
    glVertex2f(0.0, 0.1)     
    glVertex2f(-0.05, -0.05) 
    glVertex2f(0.05, -0.05)  
    glEnd()

    keys = glfw.get_key        

    if keys(window, glfw.KEY_UP) == glfw.PRESS and velocidade > 0:
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.5, 0.0) 
        glVertex2f(0.0, -0.05)   
        glVertex2f(-0.03, -0.08) 
        glVertex2f(0.03, -0.08)  
        glEnd()

def atualizarPosicao():
    global pos_x, pos_y
    rad = math.radians(angulo + 90)
    pos_x += math.cos(rad) * velocidade
    pos_y += math.sin(rad) * velocidade

def limitarBordas():
    global pos_x, pos_y
    if pos_x > 1.0: pos_x = -1.0
    if pos_x < -1.0: pos_x = 1.0
    if pos_y > 1.0: pos_y = -1.0
    if pos_y < -1.0: pos_y = 1.0  

#OPÇÃO USANDO POLL DE TECLAS
def processarEntrada(window):
    global angulo, velocidade
    keys = glfw.get_key        
    if keys(window, glfw.KEY_LEFT) == glfw.PRESS:
        angulo += vel_rotacao  
    if keys(window, glfw.KEY_RIGHT) == glfw.PRESS:
        angulo -= vel_rotacao  
    if keys(window, glfw.KEY_UP) == glfw.PRESS:
        velocidade = min(velocidade + aceleracao, vel_max)  
    if keys(window, glfw.KEY_DOWN) == glfw.PRESS:
        velocidade = max(velocidade - aceleracao, 0)


def main():
    global angulo, velocidade
    glfw.init()
    window = glfw.create_window(800, 600, "Nave Triangular (OpenGL Legacy)", None, None)
    glfw.make_context_current(window)
    
    glfw.swap_interval(0)
    init()
    while not glfw.window_should_close(window):
        glfw.poll_events()        
        
        processarEntrada(window)
        render(window)
        atualizarPosicao()  
        limitarBordas()

        glfw.swap_buffers(window)
        glfw.wait_events_timeout(1.0/60.0)

    glfw.terminate()

if __name__ == "__main__":
    main()