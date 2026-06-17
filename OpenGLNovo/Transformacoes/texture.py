# arquivo texture.py
from OpenGL.GL import *
from PIL import Image

class Texture:
    def __init__(self, filePath):
        # cria a textura e gera seu id
        self.textId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textId) # ativa uma textura a partir do id da textura 

        # parâmetros da textura nos eixos
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # eixo horizontal
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # eixo vertical
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # quando a imagem diminui
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # quando a imagem aumenta

        # carrega a imagem
        image = Image.open(filePath) # abre a imagem a partir do seu path passado
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = image.convert("RGBA")  # gconverte para rgb-a
        img_data = image.tobytes() # converte a imagem para um array de bytes

        # envia para a GPU
        glTexImage2D(
            GL_TEXTURE_2D, # tipo de textura
            0, 
            GL_RGBA, # formato interno usado pela GPU
            image.width, # largura da imagem
            image.height, # altura da imagem
            0, # ira ser sempre 0
            GL_RGBA, # formato dos dados
            GL_UNSIGNED_BYTE, # tipo dos dados
            img_data # pixels da imagem
        )


        glGenerateMipmap(GL_TEXTURE_2D) # cria versões menores da textura

        # desativa
        glBindTexture(GL_TEXTURE_2D, 0) # desativa a textura ativa atual