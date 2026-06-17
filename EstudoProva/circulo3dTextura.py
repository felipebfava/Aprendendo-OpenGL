# Circulo 3d simples com OpenGL e glfw

from OpenGL.GL import *
import glfw
import math
from OpenGL.GLU import *
from PIL import Image

# Variáveis Globais para movimentar o círculo começando da origem (0,0)
# Movimento de transladar
transla_x = 0
transla_y = 0

# Variáveis Globais para texturas
textura_circulo = None

def init():

    # Iniciar o GLFW
    glfw.init()

    # Criar a Janela
    window = glfw.create_window(800, 600, "Janela Círculo 3D", None, None)

    # Define como janela principal no contexto
    glfw.make_context_current(window)
    
    # Seta uma cor de fundo a janela alterando r,g,b,alpha(opacidade)
    glClearColor(1, 1, 1, 1)

    glViewport(0, 0, 800, 600)

    # Configuração do pipeline gráfico
    glMatrixMode(GL_PROJECTION) #seleciona matriz projeção
    glLoadIdentity() # carrega e seta uma matriz identidade

    # define a perspectiva de projeção
    # configura campo de visão e proporção, ponto mais próximo e ponto mais distante
    # usando a biblioteca GLU
    gluPerspective(
        45, # ângulo do campo de visão da perspectiva
        800 / 600, # tamanhos / proporções da tela mesmas usadas na janela
        0.1, # seta uma perspectiva mínima de renderização
        100.0 # seta uma perspectivaplano máxima de renderização
    )

    # volta para a matriz de modelo
    glMatrixMode(GL_MODELVIEW)


    # Habilita profundidade para estruturas em 3d
    glEnable(GL_DEPTH_TEST)

    # Definindo as texturas
    # ativa o uso de texturas 2d
    glEnable(GL_TEXTURE_2D)
    # ativa a mistura, para combinação de cores
    glEnable(GL_BLEND)
    # ativa a mistura de transparências para combinação de cores
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # retorna toda a estrutura da janela
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


def desenhaCirculo3d(raio, segmentos):

    # Para aplicar alguma textura, precisa definir antes do glBegin()
    # Além disso precisamos usar glTexCoord2f()
    # para definir os pontos de onde aplicar a textura
    glBindTexture(GL_TEXTURE_2D, textura_circulo)

    # Função que inicia qualquer estrutura aceita pelo glfw 
    # Estrutura do circulo usaremos varios triangulos
    glBegin(GL_TRIANGLE_FAN)

    # Para definir uma cor a ser usada pela estrutura
    # Alterando r,g,b indo de 0-(0) a 1-(255)
    # glColor3f(1, 0, 0) # vermelho

    # Define o centro da textura para representar o centro do círculo
    glTexCoord2f(0.5, 0.5)

    # Para desenhar o círculo 3d - Esfera precisamos pegar seu centro
    glVertex3f(0, 0, 0) # centro

    # Loop para repetir a conexão dos triangulos
    # segmentos + 1 para conectar o último triangulo
    # caso a quantidade de segmentos sejam pares

    # Para cada i na quantidade de segmentos + 1
    for i in range (segmentos + 1):
        # Usaremos o cálculo do raio e dos senos cossenos
        # para pegar o angulo em graus usamos o circulo completo
        # divido pela quantidade de segmentos
        # Como temos 20 segmentos: 360 / 20 = 18°
        # cada segmento terá 18°
        # multiplica i para iterar e ir para o próximo
        angulo_graus = (360/segmentos) * i

        # as funções seno e cosseno da biblioteca math
        # só aceitam o angulo em radianos
        # então precisa converter
        angulo_radianos = math.radians(angulo_graus)

        # Calcula a posição de x e y conforme os valores de cosseno e seno
        # cos(angulo) = cateto adjacente / hipotenusa
        # sin(angulo) = cateto oposto / hipotenusa
        # cos(θ) = x / raio
        # sen(θ) = y / raio
        x = raio * math.cos(angulo_radianos)
        y = raio * math.sin(angulo_radianos)

        # Para a textura, precisamos pegar as coordenadas de u e v
        # u e v vão de (0,0) a (1,1)
        u = 0.5 + 0.5 * math.cos(angulo_radianos)
        v = 0.5 + 0.5 * math.sin(angulo_radianos)
        
        # Depois de pegar as coordenadas u e v
        # ligamos elas aos pontos
        glTexCoord2f(u, v)

        # Define os vértices do círculo
        # Alterando a posição em x,y,z
        # Como faremos um círculo 3d usaremos glVertex3f()
        # ainda dentro do for
        glVertex3f(x, y, 0)

    # Determina o Fim da estrutura do Begin
    glEnd()


def render():

    # Chama a função de desenhar o círculo 2d
    # No nosso caso precisamos passar o raio do circulo e
    # a quantidade de segmentos que ele terá
    # quanto mais segmentos, mais redondo será o círculo
    desenhaCirculo3d(0.5, 20)


# Função que pega as teclas apertadas do teclado
def teclado(window, key, scancode, action, mods):
    
    # Variáveis globais precisam ser chamadas
    # caso os seus valores se alterem dentro de funções
    global transla_x, transla_y

    # se a ação for de pressionar (tecla pressionada) faça
    if action == glfw.PRESS:

        # W sobe, S desce, A move para esquerda, D move para direita
        # para subir(+) ou descer(-) precisa alterar o valor de y
        # para a esquerda x diminui(-) e para a direita x aumenta (+)
        if key == glfw.KEY_W: # se esta tecla for W faça
            transla_y += 0.01 # sobe
        
        if key == glfw.KEY_S:
            transla_y -= 0.01 # desce
        
        if key == glfw.KEY_A:
            transla_x -= 0.01 # esquerda
        
        if key == glfw.KEY_D:
            transla_x += 0.01 # direita


def main():
    global textura_circulo

    # Criar a Janela chamando a função para iniciar
    window = init()

    # Define como janela principal no contexto
    glfw.make_context_current(window)

    # Define a função que irá captar as entradas do teclado
    glfw.set_key_callback(window, teclado)

    textura_circulo = carregar_textura("texturas/pedras_02.jpg")

    
    # Loop para deixar a janela aberta até ser fechada
    while not glfw.window_should_close(window):
        # Limpa o buffer de cor da janela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # # Aplicar uma matriz identidade para não acumular as transformações
        # # sem ela o quadrado só para de movimentar caso receba
        # # uma tecla contrária ao movimento que está fazendo
        glLoadIdentity()

        # # Para aplicar movimento na estrutura
        # # Precisa ser antes de definir a estrutura em glBegin()
        glTranslatef(transla_x, transla_y, 0)

        # E ajustar a câmera
        gluLookAt(
            0, 0, 2,   # x,y,z - posição da câmera
            0, 0, 0,   # x,y,z - para onde a câmera olha
            0, 1, 0    # x,y,z - qual direção é "cima" para a câmera
        )

        # Chama a função de renderização - nossa imagem/objeto
        render()

        # Carrega os eventos de inputs
        glfw.poll_events()
        # Usa buffers para renderização da imagem da janela
        glfw.swap_buffers(window)

if __name__ == "__main__":
    main()