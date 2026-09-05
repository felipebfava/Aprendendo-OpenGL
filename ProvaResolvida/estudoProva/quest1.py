import glfw
from OpenGL.GL import *
import math

# Precisa transladar e rotacionar as duas naves com controles diferentes

# Variáveis Globais
aceleracao = 0.001
vel_max = 0.1

# Nave 1
transla_x_nave1 = 0
transla_y_nave1 = 0

# velocidade principal da nave começa zerada
velocidade_nave1 = 0
vel_rotacao_nave1 = 3

angulo_nave1 = 0

# Nave 2
transla_x_nave2 = 0
transla_y_nave2 = 0

velocidade_nave2 = 0
vel_rotacao_nave2 = 3

angulo_nave2 = 0

# está certo
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

# está certo
def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    # translada a nave com base na origem
    glTranslatef(transla_x_nave1, transla_y_nave1, 0)
    
    # translado até o centro da nave1 - verde
    glTranslatef(-0.5, 0.0, 0.0) # centro da nave

    # aplico rotação nela no eixo Z
    glRotatef(angulo_nave1, 0, 0, 1)
    
    # após aplicar a rotação, translada para a origem novamente
    glTranslatef(+0.5, 0.0, 0.0) # volta a origem

    # glPointSize(10)
    # glBegin(GL_POINTS)
    # glColor3f(1.0, 1.0, 1.0)
    # glVertex2f(-0.5, 0.0) # centro da nave 1 - verde
    # glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    
    glVertex2f(-0.50, 0.1) # ponta do triângulo  
    glVertex2f(-0.55, -0.05) # canto esquerdo  
    glVertex2f(-0.45, -0.05)  # canto direito
    
    glEnd()


    glLoadIdentity()

    # translada a nave com base na origem
    glTranslatef(transla_x_nave2, transla_y_nave2, 0)
    
    # translado até o centro da nave1 - verde
    glTranslatef(0.5, 0.0, 0.0) # centro da nave

    # aplico rotação nela
    glRotatef(angulo_nave2, 0, 0, 1)

    # mesma coisa, preciso voltar na origem
    glTranslatef(-0.5, 0.0, 0.0)

    # glPointSize(10)
    # glBegin(GL_POINTS)
    # glColor3f(1.0, 1.0, 1.0)
    # glVertex2f(0.5, 0.0) # centro da nave 2 - azul
    # glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0, 1.0) 
    glVertex2f(0.5, 0.1)     
    glVertex2f(0.45, -0.05) 
    glVertex2f(0.55, -0.05)
    glEnd()
    

# Precisamos atualizar a posição das naves conforme seno para y e cosseno para x

# está certo - porém precisa chamar essas funções na main
def atualizar_pos_nave1():
    global transla_x_nave1, transla_y_nave1

    angulo_rad = math.radians(angulo_nave1 + 90)
    transla_x_nave1 += math.cos(angulo_rad) * velocidade_nave1
    transla_y_nave1 += math.sin(angulo_rad) * velocidade_nave1


# está certo
def atualizar_pos_nave2():
    global transla_x_nave2, transla_y_nave2

    angulo_rad = math.radians(angulo_nave2 + 90)
    transla_x_nave2 += math.cos(angulo_rad) * velocidade_nave2
    transla_y_nave2 += math.sin(angulo_rad) * velocidade_nave2


# está certo
def moveNave1(window):

    global velocidade_nave1, vel_rotacao_nave1, angulo_nave1

    keys = glfw.get_key

    if keys(window, glfw.KEY_UP) == glfw.PRESS:
        print("Acelera")
        # velocidade sobe conforme a aceleração
        velocidade_nave1 += aceleracao

        # controle para quando chegar num máximo
        if velocidade_nave1 > vel_max:
            velocidade_nave1 = vel_max
    
    if keys(window, glfw.KEY_DOWN) == glfw.PRESS:
        print("Desacelera")
        # mesma lógica de acelerar
        velocidade_nave1 -= aceleracao

        if velocidade_nave1 < -vel_max:
            velocidade_nave1 = -vel_max
    
    if keys(window, glfw.KEY_LEFT) == glfw.PRESS:
        print("Gira para a esquerda")
        # precisa alterar o angulo. Pois faz a nave girar
        angulo_nave1 += vel_rotacao_nave1

    if keys(window, glfw.KEY_RIGHT) == glfw.PRESS:
        print("Gira para a direita")
        # mesma lógica de rotacionar para a esquerda
        angulo_nave1 -= vel_rotacao_nave1
        

# está certo
def moveNave2(window):

    global vel_rotacao_nave2, velocidade_nave2, angulo_nave2

    keys = glfw.get_key   

    if keys(window, glfw.KEY_W) == glfw.PRESS:
        print("Acelera")

        velocidade_nave2 += aceleracao

        # controle para quando chegar num máximo
        if velocidade_nave2 > vel_max:
            velocidade_nave2 = vel_max
    
    if keys(window, glfw.KEY_S) == glfw.PRESS:
        print("Desacelera")

        velocidade_nave2 -= aceleracao

        if velocidade_nave2 < -vel_max:
            velocidade_nave2 = -vel_max
    
    if keys(window, glfw.KEY_A) == glfw.PRESS:
        print("Gira para a esquerda")
        angulo_nave2 += vel_rotacao_nave2

    if keys(window, glfw.KEY_D) == glfw.PRESS:
        print("Gira para a direita")
        angulo_nave2 -= vel_rotacao_nave2


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Nave Triangular (OpenGL Legacy)", None, None)
    glfw.make_context_current(window)
    
    init()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()        
        
        moveNave1(window)
        moveNave2(window)

        atualizar_pos_nave1()
        atualizar_pos_nave2()

        render()

        glfw.swap_buffers(window)
        glfw.wait_events_timeout(1.0/60.0)

    glfw.terminate()

if __name__ == "__main__":
    main()