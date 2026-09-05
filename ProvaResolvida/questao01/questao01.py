import glfw
from OpenGL.GL import *
import math

# Variáveis globais para armazenar a posição e velocidade das naves
# Transladar nave 1
transla_x_nave1 = 0
transla_y_nave1 = 0

# Rotacionar nave 1
rot_x_nave1 = 0
rot_y_nave1 = 0

# Transladar nave 2
transla_x_nave2 = 0
transla_y_nave2 = 0

# Rotacionar nave 2
rot_x_nave2 = 0
rot_y_nave2 = 0

angulo = 0

# Acelerar Nave
velocidade = 0
vel_max = 0.1
vel_min = 0.01
vel_rotacao = 3.0
aceleracao = 0.01

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0) 

def render(window):
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    # glPushMatrix()

    glTranslatef(transla_x_nave1, transla_y_nave1, 0)
    glRotatef(angulo, 0, 0, 1)
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    # glVertex2f(-0.50, 0.0) # centro
    
    # glVertex2f(-0.50, 0.1) # ponta do triângulo  
    # glVertex2f(-0.55, -0.05) # canto esquerdo  
    # glVertex2f(-0.45, -0.05)  # canto direito

    # Triangulo na origem
    glVertex2f(0.0, 0.1)
    glVertex2f(-0.05, -0.05)
    glVertex2f(0.05, -0.05)
    
    
    glEnd()
    # glPopMatrix()
    
    # glTranslatef(transla_x_nave2, transla_y_nave2, 0)
    # glRotatef(rot_x_nave2, rot_y_nave2, 0)
    
    # glBegin(GL_TRIANGLES)
    # glColor3f(0.0, 0, 1.0) 
    # glVertex2f(0.5, 0.1)     
    # glVertex2f(0.45, -0.05) 
    # glVertex2f(0.55, -0.05)  
    # glEnd()


def atualizarPosicaoNave1():
    global transla_x_nave1, transla_y_nave1
    
    rad = math.radians(angulo + 90)
    transla_x_nave1 += math.cos(rad) * velocidade
    transla_y_nave1 += math.cos(rad) * velocidade


def atualizarPosicaoNave2():
    global transla_x_nave2, transla_y_nave2
    
    rad = math.radians(angulo + 90)
    transla_x_nave2 += math.cos(rad) * velocidade
    transla_y_nave2 += math.cos(rad) * velocidade


def moveNave1(window):
    global transla_x_nave1, transla_y_nave1, rot_x_nave1, rot_y_nave1, angulo, velocidade
    
    keys = glfw.get_key 
    
    if keys(window, glfw.KEY_UP) == glfw.PRESS:
        print("Acelera")
        velocidade = min(velocidade + aceleracao, vel_max)
        # transla_y_nave1 += 0.01
        
    if keys(window, glfw.KEY_DOWN) == glfw.PRESS:
        print("Desacelera")
        # transla_y_nave1 -= 0.01
        velocidade = max(velocidade - aceleracao, -vel_max)
        
    if keys(window, glfw.KEY_LEFT) == glfw.PRESS:
        print("Gira para a esquerda")
        # transla_x_nave1 -= 0.01
        angulo += vel_rotacao

        
    if keys(window, glfw.KEY_RIGHT) == glfw.PRESS:
        print("Gira para a direita")
        # transla_x_nave1 += 0.01
        angulo -= vel_rotacao



def moveNave2(window):
    global transla_x_nave2, transla_y_nave2
    
    keys = glfw.get_key   

    if keys(window, glfw.KEY_W) == glfw.PRESS:
        print("Acelera")
        transla_y_nave2 += 0.01
        
    if keys(window, glfw.KEY_S) == glfw.PRESS:
        print("Desacelera")
        transla_y_nave2 -= 0.01
        
    if keys(window, glfw.KEY_A) == glfw.PRESS:
        print("Gira para a esquerda")
        transla_x_nave2 -= 0.01
        
    if keys(window, glfw.KEY_D) == glfw.PRESS:
        print("Gira para a direita")
        transla_x_nave2 += 0.01
    


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Nave Triangular (OpenGL Legacy)", None, None)
    glfw.make_context_current(window)
    

    init()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()        
        
        moveNave1(window)
        moveNave2(window)
        render(window)
        atualizarPosicaoNave1()
        atualizarPosicaoNave2()

        glfw.swap_buffers(window)
        glfw.wait_events_timeout(1.0/60.0)

    glfw.terminate()

if __name__ == "__main__":
    main()