# arquivo figura-01.py
# video referencia https://www.youtube.com/watch?v=ouH4X9g_aLI

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np
import ctypes # para utilizar tipos da linguagem C - gambiarra para o python aguentar

# posicao em x e y + rgb
vertices = [
    [-0.8, -0.8, 1,0,0],
    [0.0, -0.8, 1,1,0],
    [-0.4, 0.0, 1,0,1],
    [0.0, -0.8, 1,1,0],
    [0.8, -0.8, 0,1,0],
    [0.4, 0.0, 0,1,1],
    [-0.4, 0.0, 1,0,1],
    [0.4, 0.0, 0,1,1],
    [0.0, 0.8, 0,0,1]
]
# 9(vertices) x 5(numeros) = 45 x 4bytes (float) = 180 bytes

qtdVertices = len(vertices) #sempre pega o tamanho de vertices
vaoId = 0
shaderId = 0

def init():
    glClearColor(1, 1, 1, 1) # seta cor de fundo

    # precisa declarar que vai usar a variável global setada fora da função e não precisa criar uma nova
    global vertices, vaoId, shaderId

    # normalização de dados do array vertices
    vertices = np.array(vertices, np.dtype(np.float32)) # 4 bytes ou 32 bits
    # 18 x 4 = 72 bytes

    # Precisa criar o Vertex Array Object - antes do VBO
    # é um objeto que incorpora/encapsula o VBO e os atributos num único objeto
    vaoId = glGenVertexArrays(1) # qtd que será criado
    # tornar o VAO ativo
    glBindVertexArray(vaoId)

    # criar o Vertex Buffer Object
    vboId = glGenBuffers(1)
    # tornar o VBO ativo
    glBindBuffer(GL_ARRAY_BUFFER, vboId)
    # enviar os dados para o VBO
    glBufferData(GL_ARRAY_BUFFER, # tipo de buffer - o mesmo usado na função BindBuffer
                 vertices.nbytes, # tamanho do buffer - passo exatamente a quantidade de bytes de vertices para o buffer, 18valores x 8bytes = 144bytes (72 para 4bytes)
                 vertices, # os dados em si, array vertices
                 GL_STATIC_DRAW) # uso do buffer
   
    # opções de uso do buffer
    # GL_STATIC_DRAW
    # GL_DYNAMIC_DRAW
    # GL_STATIC_READ

    # Só enviar os dados o OpenGL não saberá o que fazer com eles, então vc descreve
    # para os vertices dos triangulos - figura
    glVertexAttribPointer(0, #index - código do atributo (posição) - vc define
                          2, #size - qtd de valores do atributo - qtd de coordenadas
                          GL_FLOAT, #type - tipo de dados/valores do atributo
                          GL_FALSE, #normalized - se os valores devem ser normalizados entre 0 a 1 ou -1 a 1
                          5*4, #stride - espaçamento/qtd em bytes entre os atributos/coordenadas - 2 coordenadas floats (2*4 bytes)
                          ctypes.c_void_p(0)) #defino onde o vertice começa (inicio(0 bytes), meio ou fim), precisa apontar o local na memória - ponteiro para void em C
    
    # para a cor dos triangulos
    glVertexAttribPointer(1, #index - código do atributo (cor) - vc define
                          3, #size - qtd de valores do atributo - qtd de coordenadas
                          GL_FLOAT, #type - tipo de dados/valores do atributo
                          GL_FALSE, #normalized - se os valores devem ser normalizados entre 0 a 1 ou -1 a 1
                          5*4, #stride - espaçamento/qtd em bytes entre os atributos/coordenadas - 2 coordenadas floats (2*4 bytes)
                          ctypes.c_void_p(2*4)) #defino onde o vertice começa (inicio(2valores(float) x 4bytes (tam do float) = 8), meio ou fim), precisa apontar o local na memória - ponteiro para void em C
    

    # Tornar a config do atributo posicao ativa
    glEnableVertexAttribArray(0) # o index do atributo

    # Tornar a config do atributo cor ativa
    glEnableVertexAttribArray(1) # o index do atributo

    # desativar o VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # desativar o VAO
    glBindVertexArray(0)

    # Precisamos configurar as cores ao desenho no OpenGL moderno 3.0 com shaders
    # criar os arquivos de shader

    # código fonte dos shaders
    # ler o arquivo do vertex shader
    with open('01_vertexShader.glsl','r') as file:
        vsSource = file.read() # le o arquivo e retorna uma string

    # ler o arquivo do fragment shader
    with open('01_fragmentShader.glsl','r') as file:
        fsSource = file.read() # le o arquivo e retorna uma string


    vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)

    # vsId = glCreateShader(GL_VERTEX_SHADER) # criar o objeto vertex shader
    # glShaderSource(vsId, vsSource) # enviar o codigo fonte do vertex shader para esse objeto
    # glCompileShader(vsId) # compilar o vertex shader
    # if not glGetShaderiv(vsId, GL_COMPILE_STATUS): # verificar por erros no vertex shader
    #     vsInfo = glGetShaderInfoLog(vsId)
    #     print('Erro de compilação no vertex shader')
    #     print(vsInfo)

    fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
    
    # fsId = glCreateShader(GL_FRAGMENT_SHADER) # criar o objeto fragment shader
    # glShaderSource(fsId, fsSource) # enviar o codigo fonte do fragment shader para esse objeto
    # glCompileShader(fsId) # compilar o fragment shader   
    # if not glGetShaderiv(fsId, GL_COMPILE_STATUS): # verificar por erros no fragment shader
    #     fsInfo = glGetShaderInfoLog(fsId)
    #     print('Erro de compilação no fragment shader')
    #     print(fsInfo)

    shaderId = gls.compileProgram(vsId, fsId)

    # # vai ter que unir o vertex shader com o fragment shader
    # shaderId = glCreateProgram() # criar o shader program - par de shaders que estarão juntos na mesma pipeline
    # glAttachShader(shaderId, vsId)
    # glAttachShader(shaderId, fsId)
    # glLinkProgram(shaderId) # unindo os arquivos compilador do vertex e fragment shaders




def render():
    glClear(GL_COLOR_BUFFER_BIT)

    # ativando o shader
    glUseProgram(shaderId)

    # vou usar o objeto VAO, então ativa ele
    glBindVertexArray(vaoId)

    #glDraw é usado para desenhos que não tem indices - EBO
    glDrawArrays(GL_TRIANGLES, #o que vai desenhar
                 0, #indice de qual vertice (do array) vai começar a desenhar
                 qtdVertices) # qtd de vertices que vc quer desenhar
    glBindVertexArray(0)

    # desativando o shader
    glUseProgram(0)
   


def main():
    glfw.init()
    window = glfw.create_window(500, 500, "Minha Janela", None, None)
    glfw.make_context_current(window)

    init()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()


        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__" :
    main()
