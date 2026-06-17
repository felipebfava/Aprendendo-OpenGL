# Quadrado 3d simples com OpenGL e glfw

from OpenGL.GL import *
import glfw
from OpenGL.GLU import *
from PIL import Image

# Variáveis Globais para movimentar o quadrado começando da origem (0,0)
# Movimento de transladar
transla_x = 0
transla_y = 0

# Variáveis Globais para texturas
textura_quadrado = None


def init():

    # Iniciar o GLFW
    glfw.init()

    # Criar a Janela
    window = glfw.create_window(800, 600, "Janela Quadrado 3D", None, None)

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


def render():

    # Para aplicar alguma textura, precisa definir antes do glBegin()
    # Além disso precisamos usar glTexCoord2f()
    # para definir os pontos de onde aplicar a textura
    glBindTexture(GL_TEXTURE_2D, textura_quadrado)

    # Função que inicia qualquer estrutura aceita pelo glfw 
    # Estrutura do quadrado
    glBegin(GL_QUADS)
 
    # Define os vértices / cantos do quadrado
    # Por ser 3d é necessário desenhar as 6 faces do quadrado e depois liga-las
    # Como faremos um quadrado 3d usaremos glVertex3f()

    # Frente
    # Para definir uma cor a ser usada pela estrutura
    # Alterando r,g,b indo de 0-(0) a 1-(255)
    # glColor3f(1,0,0)

    # glTexCoord2f usa o sistema de coordenadas UV
    # sendo o (0,0) o canto inferior esquerdo e
    # (1,1) o canto superior direito em X
    glTexCoord2f(0,0)
    glVertex3f(-0.25,-0.25, 0.25)

    glTexCoord2f(0,1)
    glVertex3f(-0.25, 0.25, 0.25)

    glTexCoord2f(1,1)
    glVertex3f( 0.25, 0.25, 0.25)

    glTexCoord2f(1,0)
    glVertex3f( 0.25,-0.25, 0.25)

    # Trás
    # glColor3f(0,1,0)

    glVertex3f(-0.25,-0.25,-0.25)
    glVertex3f(-0.25, 0.25,-0.25)
    glVertex3f( 0.25, 0.25,-0.25)
    glVertex3f( 0.25,-0.25,-0.25)

    # Esquerda
    # glColor3f(0,0,1)

    glVertex3f(-0.25,-0.25,-0.25)
    glVertex3f(-0.25,-0.25, 0.25)
    glVertex3f(-0.25, 0.25, 0.25)
    glVertex3f(-0.25, 0.25,-0.25)

    # Direita
    # glColor3f(1,1,0)

    glVertex3f(0.25,-0.25,-0.25)
    glVertex3f(0.25,-0.25, 0.25)
    glVertex3f(0.25, 0.25, 0.25)
    glVertex3f(0.25, 0.25,-0.25)

    # Topo
    # glColor3f(1,0,1)

    glVertex3f(-0.25,0.25,-0.25)
    glVertex3f(-0.25,0.25, 0.25)
    glVertex3f( 0.25,0.25, 0.25)
    glVertex3f( 0.25,0.25,-0.25)

    # Base
    # glColor3f(0,1,1)

    glVertex3f(-0.25,-0.25,-0.25)
    glVertex3f(-0.25,-0.25, 0.25)
    glVertex3f( 0.25,-0.25, 0.25)
    glVertex3f( 0.25,-0.25,-0.25)

    # Determina o Fim da estrutura do Begin
    glEnd()


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
    global textura_quadrado

    # Criar a Janela chamando a função para iniciar
    window = init()

    # Define a função que irá captar as entradas do teclado
    glfw.set_key_callback(window, teclado)

    # Define uma textura para o quadrado:
    textura_quadrado = carregar_textura("texturas/madeira_01.jpg")

    # Loop para deixar a janela aberta até ser fechada
    while not glfw.window_should_close(window):
        # Limpa o buffer de cor da janela e da profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Aplicar uma matriz identidade para não acumular as transformações
        # sem ela o quadrado só para de movimentar caso receba
        # uma tecla contrária ao movimento que está fazendo
        glLoadIdentity()

        # Para aplicar movimento na estrutura
        # Precisa ser antes de definir a estrutura em glBegin()
        glTranslatef(transla_x, transla_y, -2)
        # glRotatef(30, 1, 0, 0)
        # glRotatef(30, 0, 1, 0)
        
        # E ajustar a câmera, ou onde estaremos olhando
        gluLookAt(
            1, 1, 1,   # x,y,z - posição da câmera
            0, 0, 0,   # x,y,z - para onde a câmera olha
            0, 1, 0    # x,y,z - qual direção é "cima" para a câmera
        )

        # Chama a função de renderização - nossa imagem/objeto
        render()    

        # Usa buffers para renderização da imagem da janela
        glfw.swap_buffers(window)
        # Carrega os eventos de inputs
        glfw.poll_events()

if __name__ == "__main__":
    main()