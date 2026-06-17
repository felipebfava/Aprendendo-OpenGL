import glfw
from OpenGL.GL import *
from PIL import Image #pillow


def init():
    glClearColor(0.2, 0.2, 0.2, 1.0)
    # habilita texturas
    glEnable(GL_TEXTURE_2D)

def carregar_textura(caminho):
    # abre a imagem e inverte verticalmente para corrigir a orientação
    imagem = Image.open(caminho)
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

    # converte a imagem para RGBA e obtém os dados em bytes
    imgData = imagem.convert("RGBA").tobytes()

    # gera um ID para a textura e vincula a textura
    # o parametro 1 indica que queremos gerar 1 textura, a função retorna um array com os IDs gerados
    texId = glGenTextures(1)
    # ativa a textura 2D e vincula o ID gerado
    glBindTexture(GL_TEXTURE_2D, texId)


    # Configurações da textura
    # GL_REPEAT para repetir a textura quando as coordenadas de textura estão fora do intervalo [0, 1]
    # GL_TEXTURE_WRAP_S para o eixo horizontal (S) e GL_TEXTURE_WRAP_T para o eixo vertical (T) 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Configurações de filtragem
    # GL_LINEAR para suavizar a textura quando ampliada ou reduzida
    # GL_NEAREST para um efeito pixelado
    # GL_TEXTURE_MIN_FILTER e GL_TEXTURE_MAG_FILTER são usados quando a resolução da textura é diferente da resolução do objeto na tela 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Envia imagem para GPU
    glTexImage2D(
        GL_TEXTURE_2D,    # alvo da textura
        0,                # nível de detalhe (0 para a imagem original)
        GL_RGBA,          # formato interno da textura
        imagem.width,     # largura da imagem
        imagem.height,    # altura da imagem
        0,                # borda (código legado, deve ser 0)
        GL_RGBA,          # formato dos dados da imagem a ser enviada
        GL_UNSIGNED_BYTE, # tipo dos dados
        imgData           # ponteiro para os dados
    )
    # Após criada, a textura pode ser desativada, e ativada apenas quando for usada para desenhar
    glBindTexture(GL_TEXTURE_2D, 0)

    return texId


def desenhar_quadrado(textura):
    glBindTexture(GL_TEXTURE_2D, textura)

    glBegin(GL_QUADS)

    # canto inferior esquerdo
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-0.8, -0.8)

    # canto inferior direito
    glTexCoord2f(1.0, 0.0)
    glVertex2f(0.8, -0.8)



    # canto superior direito
    glTexCoord2f(1.0, 1.0)
    glVertex2f(0.8, 0.8)

    # canto superior esquerdo
    glTexCoord2f(0.0, 1.0)
    glVertex2f(-0.8, 0.8)

    glEnd()


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Textura 2D", None, None)
    glfw.make_context_current(window)

    init()

    textura = carregar_textura("naveAzulSemFundo.png")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        desenhar_quadrado(textura)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

main()