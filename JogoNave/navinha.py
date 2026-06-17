
from OpenGL.GL import *
import glfw
import math
import random

from PIL import Image


jogo_ativo = True

textura_nave = None
textura_projetil = None
textura_fundo = None
textura_chamas = None
textura_meteoritos = None

x = 0.0
y = 0.0
angulo = 0.0
dt = 0.0


velocidade = 0.0
vel_rotacao = 150
vel_max = 1
aceleracao = 0.5


num_misseis = 40
misseis = []
velocidade_missel = 1.5


num_estrelas = 400
estrelas = [(random.uniform(-1, 1), #x
             random.uniform(-1, 1)) #y
            for _ in range(num_estrelas)]


meteoritos = []

num_meteoritos = 12
velocidade_meteorito = 0.4


def init():
    glClearColor(0.0, 0.0, 0.0, 0)
    glEnable(GL_TEXTURE_2D)

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


def desenhaEstrelas():

    # glLoadIdentity()
    glPushMatrix()
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 0.6)
    for x,y in estrelas:
        glVertex2f(x, y)
    glEnd()
    glPopMatrix()


def movimentaEstrelas():
    global estrelas

    # se a nave estiver parada, não move estrelas
    if velocidade == 0:
        return
   
    convert = math.radians(angulo + 90)

    novas_estrelas = []

    for ex, ey in estrelas:

        # movimento contrário ao da nave
        ex -= math.cos(convert) * velocidade * dt
        ey -= math.sin(convert) * velocidade * dt

        ex, ey = limitarBordas(ex, ey)

        novas_estrelas.append((ex, ey))

    estrelas = novas_estrelas


def criaMeteoritos():
    global meteoritos
    
    lado = random.randint(0, 3)

    raio = random.uniform(0.02, 0.08)

    # cria meteorito nas bordas
    # topo -> desce
    if lado == 0:
        mx = random.uniform(-1, 1)
        my = 1.1

        tipo_movimento = random.randint(0, 1)

        # movimento reto
        if tipo_movimento == 0:
            vx = -1
            vy = 0

        # movimento diagonal
        else:
            vx = -1

            # diagonal para cima ou para baixo
            vy = random.choice([-0.5, 0.5])

    # baixo -> sobe
    elif lado == 1:
        mx = random.uniform(-1, 1)
        my = -1.1

        tipo_movimento = random.randint(0, 1)

        # reto
        if tipo_movimento == 0:
            vx = 0
            vy = 1

        # diagonal
        else:
            vx = random.choice([-0.5, 0.5])
            vy = 1

    # esquerda -> direita
    elif lado == 2:
        mx = -1.1
        my = random.uniform(-1, 1)

        tipo_movimento = random.randint(0, 1)

        # reto
        if tipo_movimento == 0:
            vx = 1
            vy = 0

        # diagonal
        else:
            vx = 1
            vy = random.choice([-0.5, 0.5])

    # direita -> esquerda
    else:
        mx = 1.1
        my = random.uniform(-1, 1)

        tipo_movimento = random.randint(0, 1)

        # movimento reto
        if tipo_movimento == 0:
            vx = -1
            vy = 0

        # movimento diagonal
        else:
            vx = -1

            # diagonal para cima ou para baixo
            vy = random.choice([-0.5, 0.5])

    meteoritos.append([mx, my, raio, vx, vy])


def desenhaMeteoritos():
    global meteoritos

    novos_meteoritos = []

    for mx, my, raio, vx, vy in meteoritos:

        # movimento reto
        mx += vx * velocidade_meteorito * dt
        my += vy * velocidade_meteorito * dt

        # se saiu da tela, reaparece (sempre fora da tela)
        if mx > 1.2:
            mx = -1.2

        if mx < -1.2:
            mx = 1.2

        if my > 1.2:
            my = -1.2

        if my < -1.2:
            my = 1.2
      
        novos_meteoritos.append([mx, my, raio, vx, vy])

        # desenha meteoro
        glPushMatrix()
        glTranslatef(mx, my, 0)

        glBindTexture(GL_TEXTURE_2D, textura_meteoritos)

        glColor3f(0.5, 0.3, 0.2)

        glBegin(GL_QUADS)

        glTexCoord2f(0, 0)
        glVertex2f(-raio, -raio)

        glTexCoord2f(1, 0)
        glVertex2f( raio, -raio)

        glTexCoord2f(1, 1)
        glVertex2f( raio,  raio)

        glTexCoord2f(0, 1)
        glVertex2f(-raio,  raio)

        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)

        glPopMatrix()

    meteoritos = novos_meteoritos


def desenhaNave(window):

    # se a nave colidiu com algum meteorito, a nave não é desenhada
    if not jogo_ativo:
        return

    glBindTexture(GL_TEXTURE_2D, textura_nave)

    teclas = glfw.get_key

    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glRotatef(angulo, 0.0, 0.0, 1.0) # angulo, x, y, z
   
    # Nave
    glColor4f(1, 1, 1, 1)

    # Nave
    glBegin(GL_QUADS)
   
    # inferior esquerdo
    glTexCoord2f(0, 0)
    glVertex2f(-0.07, -0.07)

    # inferior direito
    glTexCoord2f(1, 0)
    glVertex2f(0.07, -0.07)
   
    # superior direito
    glTexCoord2f(1, 1)
    glVertex2f(0.07, 0.07)

    # superior esquerdo
    glTexCoord2f(0, 1)
    glVertex2f(-0.07, 0.07)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
   
    # Propulsão
    if teclas(window, glfw.KEY_UP) == glfw.PRESS and velocidade > 0:
        glBindTexture(GL_TEXTURE_2D, textura_chamas)

        glColor4f(1, 1, 1, 1)

        glBegin(GL_QUADS)

        # inferior esquerdo
        glTexCoord2f(0, 0)
        glVertex2f(-0.03, -0.13)

        # inferior direito
        glTexCoord2f(1, 0)
        glVertex2f(0.03, -0.13)

        # superior direito
        glTexCoord2f(1, 1)
        glVertex2f(0.03, -0.04)

        # superior esquerdo
        glTexCoord2f(0, 1)
        glVertex2f(-0.03, -0.04)

        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
   
    glPopMatrix()


def desenhaMisseis():
    global misseis

    novos_misseis = []
   
    for missel in misseis:
       
        x, y, direcao = missel

        x += math.cos(direcao) * velocidade_missel * dt
        y += math.sin(direcao) * velocidade_missel * dt


        if -1.0 <= x <= 1.0 and -1.0 <= y <= 1.0:
            novos_misseis.append([x, y, direcao])

        
        glPushMatrix()

        glTranslatef(x, y, 0.0)

        glBindTexture(GL_TEXTURE_2D, textura_projetil)

        glColor3f(1, 1, 1)

        glBegin(GL_QUADS)

        # inferior esquerdo
        glTexCoord2f(0, 0)
        glVertex2f(-0.02, -0.02)

        # inferior direito
        glTexCoord2f(1, 0)
        glVertex2f(0.02, -0.02)

        # superior direito
        glTexCoord2f(1, 1)
        glVertex2f(0.02, 0.02)

        # superior esquerdo
        glTexCoord2f(0, 1)
        glVertex2f(-0.02, 0.02)

        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)

        glPopMatrix()
   
    misseis = novos_misseis


def tecladoAtirar(window, key, scancode, action, mods):
# def tecladoAtirar(window):
    global misseis
   
    teclas = glfw.get_key
   
    if teclas(window, glfw.KEY_SPACE) and action == glfw.PRESS:

        # limite da quantidade de tiros
        if len(misseis) < 10:
            direcao = math.radians(angulo + 90)
        
            misseis.append([x, y, direcao])


def render(window):
    #DESENHO
    desenhaFundo()
    desenhaEstrelas()
    desenhaNave(window)
    desenhaMisseis()
    desenhaMeteoritos()
   
    #MOVIMENTO
    movimentaEstrelas()

    #COLISAO
    verificarColisaoNave()
    verificarColisaoMisseis()


def atualizarPosicao():
    global x, y, dt

    convert = math.radians(angulo + 90)
    x += math.cos(convert) * velocidade * dt
    y += math.sin(convert) * velocidade * dt

    x, y = limitarBordas(x, y)


def limitarBordas(x, y):
    if(x > 1.0): x = -1.0
    if(x < -1.0): x = 1.0
    if(y > 1.0): y = -1.0
    if(y < -1.0): y = 1.0
    return x, y


def colisaoQuadradoCirculo(qx, qy, tamanho, cx, cy, raio):

    # ponto mais próximo do quadrado
    ponto_x = max(qx, min(cx, qx + tamanho))
    ponto_y = max(qy, min(cy, qy + tamanho))

    # distância do círculo até o ponto
    dx = cx - ponto_x
    dy = cy - ponto_y

    distancia = math.sqrt(dx * dx + dy * dy)

    return distancia < raio

# Colisao Nave x Meteoritos
def verificarColisaoNave():
    global jogo_ativo

    # A nave vai de -0.07 até 0.07
    tamanho_nave = 0.14

    for mx, my, raio, vx, vy in meteoritos:

        if colisaoQuadradoCirculo(
            x - 0.07,
            y - 0.07,
            tamanho_nave,
            mx, # posicao em x do meteorito
            my, # posicao em y do meteorito
            raio # raio do meteorito
        ):

            print("NAVE COLIDIU")
            print("!! JOGO ACABOU !!")

            jogo_ativo = False

            return
            

# Colisao Misseis x Meteoritos
def verificarColisaoMisseis():

    global misseis
    global meteoritos

    # missel que colidir com meteorito vai sumir
    novos_misseis = []

    # faz uma copia para não quebrar o loop
    novos_meteoritos = meteoritos.copy()

    for missil in misseis:

        mx_missil, my_missil, direcao = missil

        # se o missil colidir fica True 
        colidiu = False

        for meteorito in novos_meteoritos:

            mx, my, raio, vx, vy = meteorito

            # Missil é um quadrado
            # Meteorito é um circulo
            if colisaoQuadradoCirculo(
                mx_missil - 0.02,
                my_missil - 0.02,
                0.04,
                mx,
                my,
                raio
            ):

                print("METEORITO ATINGIDO")

                # remove o meteorito que foi atingido pelo missil
                novos_meteoritos.remove(meteorito)

                colidiu = True
                break

        if not colidiu:
            novos_misseis.append(missil)

    misseis = novos_misseis
    meteoritos[:] = novos_meteoritos

    # repõe meteoritos destruídos
    while len(meteoritos) < num_meteoritos:
        criaMeteoritos()


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
    global dt, textura_nave, textura_projetil, textura_fundo, textura_chamas, textura_meteoritos
   
    glfw.init()
    
    for _ in range(num_meteoritos):
        criaMeteoritos()

    window = glfw.create_window(600, 600, "Navinha BateBate que atira em Meteoritos", None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, tecladoAtirar)
   
    init()

    textura_nave = carregar_textura("texturas/naveSemFundo.png")
    textura_projetil = carregar_textura("texturas/projetilSemFundo.png")
    textura_fundo = carregar_textura("texturas/fundoEspaco2.jpg")
    textura_chamas = carregar_textura("texturas/chamaFoguete.png")
    textura_meteoritos = carregar_textura("texturas/meteorito.png")

    temp_inicial = glfw.get_time()

    while not glfw.window_should_close(window):
        if not jogo_ativo:
            # se a nave colidiu em algo e foi "destruida" espera 2 segundos e fecha a janela
            glfw.wait_events_timeout(2)
            glfw.set_window_should_close(window, True)

        glClear(GL_COLOR_BUFFER_BIT)

        temp_final = glfw.get_time()
        dt = temp_final - temp_inicial
        temp_inicial = temp_final

        glfw.poll_events()
        entradaTeclado(window)
        atualizarPosicao()
        # tecladoAtirar(window)
        render(window)
       
        glfw.swap_buffers(window)

    glfw.terminate()
   

if __name__ == "__main__" :
    main()
