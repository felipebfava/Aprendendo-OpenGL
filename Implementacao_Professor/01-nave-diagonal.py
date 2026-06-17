import glfw
from OpenGL.GL import *
import math

x = 0.0
y = 0.0
angulo = 0.0

velocidade = 0.0
vel_rotacao = 3.0
vel_max = 0.02
aceleracao = 0.0005

def desenhaNave():    
    glTranslatef(x, y, 0.0)                
    glRotatef(angulo, 0.0, 0.0, 1.0)
    
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 0)
    glVertex2f(0.0, 0.1)
    glVertex2f(-0.05, -0.1)
    glVertex2f(0.05, -0.1)
    glEnd()
    
def atualizarPosicao():
    global x, y
    rad = math.radians(angulo + 90)
    x += math.cos(rad) * velocidade
    y += math.sin(rad) * velocidade
    
def limitarBordas():
    global x, y
    if x > 1.0: x = -1.0
    if x < -1.0: x = 1.0
    if y > 1.0: y = -1.0
    if y < -1.0: y = 1.0  

def movimenta_nave(window, key, scancode, action, mods):
    global x, y, angulo, velocidade

    if action == glfw.PRESS or action == glfw.REPEAT:

        if key == glfw.KEY_LEFT:
            angulo += vel_rotacao
        elif key == glfw.KEY_RIGHT:
            angulo -= vel_rotacao
        elif key == glfw.KEY_UP:
            velocidade = min(velocidade+aceleracao, vel_max)
        elif key == glfw.KEY_DOWN:
            velocidade = max(velocidade-aceleracao, -vel_max)

def movimenta_nave_hv(window, key, scancode, action, mods):
    global x, y, angulo, velocidade

    if action == glfw.PRESS or action == glfw.REPEAT:

        if key == glfw.KEY_LEFT:
            angulo += vel_rotacao
        elif key == glfw.KEY_RIGHT:
            angulo -= vel_rotacao
        elif key == glfw.KEY_UP:
            velocidade = min(velocidade+aceleracao, vel_max)
        elif key == glfw.KEY_DOWN:
            velocidade = max(velocidade+aceleracao, -vel_max)

def movimenta_nave_quadrada(window, key, scancode, action, mods):
    global x, y

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_LEFT:
            x -= velocidade
        elif key == glfw.KEY_RIGHT:
            x += velocidade
        elif key == glfw.KEY_UP:
            y += velocidade
        elif key == glfw.KEY_DOWN:
            y -= velocidade


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Vetor Direcao", None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, movimenta_nave)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # desenha vetor ANTES da rotação (para acompanhar a nave)
        #desenhaVetor()
        atualizarPosicao()
        limitarBordas()
        desenhaNave()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()