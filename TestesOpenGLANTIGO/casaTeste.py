from OpenGL.GL import *
import glfw


def render():
    # define a casa quadrada - cor amarela
    glColor3f(255/255, 255/255, 0/255)
    glBegin(GL_QUADS) # forma de quadrado
    glVertex2f(-0.4, 0.3)
    glVertex2f(0.4, 0.3)
    glVertex2f(0.4, -0.4)
    glVertex2f(-0.4, -0.4)
    glEnd()

    # define a primeira janela (esquerda) retangular - cor amarela com borda mais escura
    glColor3f(255/255, 255/255, 0/255)
    glBegin(GL_QUADS)
    glVertex2f(-0.1, 0.1)
    glVertex2f(0.0, 0.1)
    glVertex2f(0.0, -0.1)
    glVertex2f(-0.1, -0.1)
    glEnd()

    # borda da janela esquerda
    glColor3f(0, 0, 0) # preto
    glLineWidth(5)
    glBegin(GL_LINE_LOOP) # forma de linha
    glVertex2f(-0.1, 0.1)
    glVertex2f(0.0, 0.1)
    glVertex2f(0.0, -0.1)
    glVertex2f(-0.1, -0.1)
    glEnd()
    

    # define a segunda janela (direita) retangular - cor amarela com borda mais escura
    glColor3f(255/255, 255/255, 0/255)
    # glEnable(GL_LINE_SMOOTH) # não mudou nada perceptivel
    # glHint(GL_LINE_SMOOTH_HINT)
    glBegin(GL_QUADS)
    glVertex2f(0.1, 0.1)
    glVertex2f(0.2, 0.1)
    glVertex2f(0.2, -0.1)
    glVertex2f(0.1, -0.1)
    glEnd()

    # borda da janela esquerda
    glColor3f(0, 0, 0) # preto
    glLineWidth(5)
    glBegin(GL_LINE_LOOP)
    glVertex2f(0.1, 0.1)
    glVertex2f(0.2, 0.1)
    glVertex2f(0.2, -0.1)
    glVertex2f(0.1, -0.1)
    glEnd()

    # define o telhado triangular - cor vermelha
    glColor3f(255/255, 0/255, 0/255)
    glBegin(GL_TRIANGLES) # forma de triângulo
    glVertex2f(-0.5, 0.3)
    glVertex2f(0.5, 0.3)
    glVertex2f(0.0, 0.7)
    glEnd()

    # define a porta retangular - cor marrom
    glColor3f(150/255, 75/255, 0/255)
    glBegin(GL_QUADS)
    glVertex2f(-0.3, -0.2)
    glVertex2f(-0.2, -0.2)
    glVertex2f(-0.2, -0.4)
    glVertex2f(-0.3, -0.4)
    glEnd()

    # define um ponto preto na porta
    glEnable(GL_POINT_SMOOTH) # deixa o ponto/pixel com bordas suaves/arredondadas

    glPointSize(8) # define o tamanho do ponto em pixels
    glColor3f(0, 0, 0) # cor preta
    glBegin(GL_POINTS) # forma de ponto
    glVertex2f(-0.21, -0.3)
    glEnd()

    # define o chão verde que fica embaixo da  casa
    glColor3f(0/255, 255/255, 0/255)  # verde
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -0.4)  # canto superior esquerdo do chão (base da casa)
    glVertex2f(1.0, -0.4)   # canto superior direito do chão
    glVertex2f(1.0, -1.0)   # canto inferior direito (parte de baixo da tela)
    glVertex2f(-1.0, -1.0)  # canto inferior esquerdo
    glEnd()
    

def main():
    glfw.init()

    window = glfw.create_window(800, 600, "Casa da Peppa", None, None)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glClearColor(0, 0, 1.0, 1.0)  # azul
        glClear(GL_COLOR_BUFFER_BIT)
        
        render()

        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()