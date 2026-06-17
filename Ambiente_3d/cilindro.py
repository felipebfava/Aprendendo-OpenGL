import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, pi
from PIL import Image


# texturas
textura_cilindro = None
textura_topo = None
textura_corpo = None
textura_base = None

# Para a Janela
width, height = 800, 600

# Para a rotação
rot_x = 0
rot_y = 0

mouse_pressionado = False

ultimo_x = 0
ultimo_y = 0

# Para a Translação
pos_x = 0
pos_y = 0


def init():
    glfw.init()
    window = glfw.create_window(width,height, "Cilindro 3D", None, None)    
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    # Configuração do pipeline gráfico
    glMatrixMode(GL_PROJECTION) #seleciona matriz projeção
    glLoadIdentity()
    #define a projeção perspectiva
    #configura campo de visão e proporção, ponto mais próximo e ponto mais distante
    gluPerspective(45, width / height, 0.1, 100.0)
    #volta para a matriz de modelo
    glMatrixMode(GL_MODELVIEW)
    #garante que objetos mais distantes não sejam desenhados sobre objetos mais próximos
    glEnable(GL_DEPTH_TEST)

    # texturas
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    return window


def carregar_textura(caminho):

    imagem = Image.open(caminho)
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

    imgData = imagem.convert("RGBA").tobytes()

    texId = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texId)


    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)


    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        imagem.width,
        imagem.height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        imgData
    )

    glBindTexture(GL_TEXTURE_2D, 0)

    return texId


def desenharCilindro():
    raio = 1.0
    altura = 2.0
    segmentos = 20
    

    # Topo - Tampa superior
    # GL_TRIANGLE_FAN
    # glColor3f(1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, textura_topo)
    glBegin(GL_TRIANGLE_FAN)
    
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0, 0, altura) # centro

    for i in range(segmentos, -1, -1):
        angulo = 2 * pi * i / segmentos
        u = 0.5 + 0.5*cos(angulo)
        v = 0.5 + 0.5*sin(angulo)

        glTexCoord2f(u, v)
        glVertex3f(raio * cos(angulo),  raio * sin(angulo), altura)


    glEnd()


    # Base - Tampa Inferior
    # GL_TRIANGLE_FAN
    # glColor3f(0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, textura_base)
    glBegin(GL_TRIANGLE_FAN)

    glTexCoord2f(0.5, 0.5)
    glVertex3f(0, 0, 0)

    for i in range(segmentos + 1):
        angulo = 2 * pi * i / segmentos

        u = 0.5 + 0.5*cos(angulo)
        v = 0.5 + 0.5*sin(angulo)

        glTexCoord2f(u, v)
        glVertex3f(raio * cos(angulo),  raio * sin(angulo), 0)


    glEnd()


    # Corpo - Lado
    # GL_TRIANGLES
    glBindTexture(GL_TEXTURE_2D, textura_corpo)
    glBegin(GL_TRIANGLES)
   
    for i in range(segmentos):
        a1 = 2*pi*i/segmentos
        a2 = 2*pi*(i+1)/segmentos

        # percorrem a textura horizontalmente
        u1 = i / segmentos
        u2 = (i + 1) / segmentos


        x1 = raio*cos(a1)
        y1 = raio*sin(a1)


        x2 = raio*cos(a2)
        y2 = raio*sin(a2)


        # triângulo 1
        glTexCoord2f(u1, 0)
        glVertex3f(x1, y1, 0)

        glTexCoord2f(u2, 0)
        glVertex3f(x2, y2, 0)

        glTexCoord2f(u1, 1)
        glVertex3f(x1, y1, altura)


        # triângulo 2
        glTexCoord2f(u2, 0)
        glVertex3f(x2, y2, 0)

        glTexCoord2f(u2, 1)
        glVertex3f(x2, y2, altura)

        glTexCoord2f(u1, 1)
        glVertex3f(x1, y1, altura)
   
    glEnd()


def movimentaCilindro(window, button, action, mods):
    global mouse_pressionado, ultimo_x, ultimo_y

    if button == glfw.MOUSE_BUTTON_LEFT:
    
        if action == glfw.PRESS:
            mouse_pressionado = True

            # posicao do mouse
            ultimo_x, ultimo_y = glfw.get_cursor_pos(window)

        elif action == glfw.RELEASE:
            mouse_pressionado = False

def moveMouse(window, posx, posy):
    global ultimo_x, ultimo_y, rot_x, rot_y, mouse_pressionado # rotação
    global pos_x, pos_y # translação

    if mouse_pressionado:
        dx = posx - ultimo_x
        dy = posy - ultimo_y

        rot_x += dx * 0.3
        rot_y += dy * 0.3

        pos_x += dx * 0.001
        pos_y += dy * 0.001
    
    ultimo_x = posx
    ultimo_y = posy


def main():
    global textura_cilindro # somente uma textura
    global textura_topo, textura_corpo, textura_base

    window = init()

    glfw.set_mouse_button_callback(window, movimentaCilindro)
    glfw.set_cursor_pos_callback(window, moveMouse)

    # textura_cilindro = carregar_textura("texturas/pedras_01.jpg")

    textura_topo = carregar_textura("texturas/madeira_01.jpg")
    textura_corpo = carregar_textura("texturas/metal_01.jpg")
    textura_base = carregar_textura("texturas/pedras_01.jpg")

    # precisa mexer com luz

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
       
        glLoadIdentity()
       
        gluLookAt(
            0, 5, 6,   # x, y, z da câmera
            0, 0, 1,   # centro do cilindro
            0, 0, 1    # eixo vertical
        )
       
        # glTranslatef(0.0, 0.0, -1.0)
        # glRotatef(30, 1, 0, 0)  # inclina para baixo
        # glRotatef(30, 0, 1, 0)  # gira para o lado
       
        glTranslatef(pos_x, pos_y, 0)

        glRotatef(rot_x, 0, -1, 0)
        glRotatef(rot_y, -1, 0, 0)

        desenharCilindro()
       
        glfw.swap_buffers(window)
        glfw.poll_events()


    glfw.terminate()




if __name__ == "__main__" :
    main()

