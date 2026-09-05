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

angulo_nave1 = 0
angulo_nave2 = 0

# Acelerar Nave
velocidade_nave1 = 0
velocidade_nave2 = 0
vel_max = 0.1
vel_min = 0.01
vel_rotacao = 3.0
aceleracao = 0.001

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0) 

def render(window):
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    # glPushMatrix()

    glTranslatef(transla_x_nave1, transla_y_nave1, 0)
    
    glTranslatef(-0.5, 0.0, 0)
    
    glRotatef(angulo_nave1, 0, 0, 1)

    glTranslatef(+0.5, 0.0, 0)
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    # glVertex2f(-0.50, 0.0) # centro
    
    glVertex2f(-0.50, 0.1) # ponta do triângulo  
    glVertex2f(-0.55, -0.05) # canto esquerdo  
    glVertex2f(-0.45, -0.05)  # canto direito
    
    glEnd()

    
    # Para separar da construção da nave anterior
    glLoadIdentity()

    # Ache o centro da nave
    # faça a translação desse jeito que está certo
    # aplique a translação até o centro da nave
    # faça a rotação desse jeito
    # aplique a translação negativa do centro da nave

    glTranslatef(transla_x_nave2, transla_y_nave2, 0)
    
    glTranslatef(0.5, 0, 0)
    
    glRotatef(angulo_nave2, 0, 0, 1)
    
    glTranslatef(-0.5, 0, 0)
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0, 1.0) 
    glVertex2f(0.5, 0.1)     
    glVertex2f(0.45, -0.05) 
    glVertex2f(0.55, -0.05)
    glEnd()


def atualizarRotacaoNave1():
    global transla_x_nave1, transla_y_nave1
    
    rad = math.radians(angulo_nave1 + 90)
    # X sempre trabalha com o cosseno do angulo
    # Y sempre trabalha com o seno do angulo
    transla_x_nave1 += math.cos(rad) * velocidade_nave1
    transla_y_nave1 += math.sin(rad) * velocidade_nave1


def atualizarRotacaoNave2():
    global transla_x_nave2, transla_y_nave2
    
    rad = math.radians(angulo_nave2 + 90)
    # X sempre trabalha com o cosseno do angulo
    # Y sempre trabalha com o seno do angulo
    transla_x_nave2 += math.cos(rad) * velocidade_nave2
    transla_y_nave2 += math.sin(rad) * velocidade_nave2


def moveNave1(window):
    global transla_x_nave1, transla_y_nave1, angulo_nave1, velocidade_nave1
    
    keys = glfw.get_key 
    
    if keys(window, glfw.KEY_UP) == glfw.PRESS:
        print("Acelera")
        # Ao invés de usar essa função difícil de lembrar do max e min das velocidades, faça:
        # velocidade_nave1 = min(velocidade_nave1 + aceleracao, vel_max)

        # Use essa estrutura que é a mesma coisa:
        velocidade_nave1 += aceleracao
        if velocidade_nave1 > vel_max:
            velocidade_nave1 = vel_max
        
    if keys(window, glfw.KEY_DOWN) == glfw.PRESS:
        print("Desacelera")
        # velocidade_nave1 = max(velocidade_nave1 - aceleracao, -vel_max)

        # Use essa estrutura que é a mesma coisa:
        velocidade_nave1 -= aceleracao

        if velocidade_nave1 < -vel_max:
            velocidade_nave1 = -vel_max
        
    if keys(window, glfw.KEY_LEFT) == glfw.PRESS:
        print("Gira para a esquerda")
        angulo_nave1 += vel_rotacao

        
    if keys(window, glfw.KEY_RIGHT) == glfw.PRESS:
        print("Gira para a direita")
        angulo_nave1 -= vel_rotacao



def moveNave2(window):
    global transla_x_nave2, transla_y_nave2, angulo_nave2, velocidade_nave2
    
    keys = glfw.get_key   

    if keys(window, glfw.KEY_W) == glfw.PRESS:
        print("Acelera")
        velocidade_nave2 = min(velocidade_nave2 + aceleracao, vel_max)
        
    if keys(window, glfw.KEY_S) == glfw.PRESS:
        print("Desacelera")
        velocidade_nave2 = max(velocidade_nave2 - aceleracao, -vel_max)
        
    if keys(window, glfw.KEY_A) == glfw.PRESS:
        print("Gira para a esquerda")
        angulo_nave2 += vel_rotacao
        
    if keys(window, glfw.KEY_D) == glfw.PRESS:
        print("Gira para a direita")
        angulo_nave2 -= vel_rotacao
    


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Nave Triangular (OpenGL Legacy)", None, None)
    glfw.make_context_current(window)
    
    init()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()        
        
        moveNave1(window)
        moveNave2(window)
        atualizarRotacaoNave1()
        atualizarRotacaoNave2()
        render(window)

        glfw.swap_buffers(window)
        glfw.wait_events_timeout(1.0/60.0)

    glfw.terminate()

if __name__ == "__main__":
    main()