from OpenGL.GL import *
import glfw
import math
import random

from PIL import Image


# todas as texturas estarão no caminho: texturas/carroXX
textura_carro_principal = None
# será uma pasta onde tem várias imagens / sprites de carros
# com os arquivos numerados de 01 a 10 
textura_outros_carros = None

# lembrando que a textura será móvel irá mudar dinamicamente
textura_fundo = None

# caso for colocar outros obstaculos
textura_barrica = None

x = 0.0         # pos x do carro
y = 0.0         # pos y do carro
angulo = 0.0    # angulo de rotacao do carro
dt = 0.0        # delta time

velocidade = 0.0
vel_rotacao = 20
vel_max = 2
aceleracao = 1


def init():
    glClearColor(0.0, 0.0, 0.0, 0) # cor de fundo
    glEnable(GL_TEXTURE_2D) # ativa texturas 2d

    # recomendado para trabalhar com texturas em png e jpg
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


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

# como o fundo não terá somente a textura de fundo é preciso desenhar ele
def desenhaFundo():

    glPushMatrix()

    glBindTexture(GL_TEXTURE_2D, textura_fundo)

    glColor3f(1, 1, 1)

    glBegin(GL_QUADS)

    # inferior esquerdo
    glTexCoord2f(0, 0)
    glVertex2f(-1, -1)

    # inferior direito
    glTexCoord2f(1, 0)
    glVertex2f(1, -1)

    # superior direito
    glTexCoord2f(1, 1)
    glVertex2f(1, 1)

    # superior esquerdo
    glTexCoord2f(0, 1)
    glVertex2f(-1, 1)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)

    glPopMatrix()


def desenhaCarro():
    # usando GL_QUADS
    # assim como o jogo top gear
    # o carro estará no centro embaixo da tela
    pass


# função que irá criar a pista que será gerada assim como o jogo top gear.
def desenhaPista():
    pass


# função que irá movimentar a pista
def movimentaPista():
    pass


# função que irá verificar colisão do carro principal x outros carros
# colisão quadrado x quadrado
def verificarColisaoCarro():
    pass


# função de renderização que chama as demais funções em ordem
def render():
    #DESENHO
    desenhaFundo()
    desenhaCarro()
    desenhaPista()
   
    #MOVIMENTO
    movimentaPista()

    #COLISAO
    verificarColisaoCarro()


# função para limitar bordas
# o carro principal não deve sair da tela e não voltar
def limitarBordas(x, y):
    if(x > 1.0): x = -1.0
    if(x < -1.0): x = 1.0
    if(y > 1.0): y = -1.0
    if(y < -1.0): y = 1.0
    return x, y


# função que atualiza a posição constantemente do carro principal
def atualizarPosicao():
    global x, y, dt

    convert = math.radians(angulo + 90)
    x += math.cos(convert) * velocidade * dt
    y += math.sin(convert) * velocidade * dt

    x, y = limitarBordas(x, y)


# função que irá pegar a entrada de comandos pelo teclado e realizar alguma ação
# a maioria será reutilizada do jogo da nave
def entradaTeclado(window):
    global angulo, velocidade, dt

    teclas = glfw.get_key

    ## MOVER
    if teclas(window, glfw.KEY_UP) == glfw.PRESS:
       
        velocidade = min(velocidade + aceleracao *dt, vel_max)
   
    if teclas(window, glfw.KEY_DOWN) == glfw.PRESS:
       
        velocidade = max(velocidade - aceleracao * dt, -vel_max)        


   ## ROTACIONAR
    if teclas(window, glfw.KEY_RIGHT) == glfw.PRESS: # para direita
        angulo -= vel_rotacao * dt
   
    if teclas(window, glfw.KEY_LEFT) == glfw.PRESS: # para esquerda
        angulo += vel_rotacao * dt


def main():
    global dt, textura_carro_principal, textura_outros_carros
    global textura_fundo, textura_barricada

    glfw.init()

    window = glfw.create_window(600, 600, "Jogo Top Gear 2d", None, None)
    glfw.make_context_current(window)
   
    init()

    # textura_carro_principal = carregar_textura("texturas/carroPrincipal.png")
    # textura_outros_carros = carregar_textura("texturas/carroXX.png")
    # textura_fundo = carregar_textura("texturas/fundoPista.jpg")
    # textura_barricada = carregar_textura("texturas/barricada.png")

    temp_inicial = glfw.get_time()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        temp_final = glfw.get_time()
        dt = temp_final - temp_inicial
        temp_inicial = temp_final

        glfw.poll_events()

        entradaTeclado(window)
        atualizarPosicao()
        render()
       
        glfw.swap_buffers(window)

    glfw.terminate()
   

if __name__ == "__main__" :
    main()