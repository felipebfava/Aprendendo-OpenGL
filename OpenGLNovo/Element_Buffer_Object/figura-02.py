# arquivo figura-01.py
# video referencia https://www.youtube.com/watch?v=ouH4X9g_aLI

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np
import ctypes # para utilizar tipos da linguagem C - gambiarra para o python aguentar

# posicao em x e y + rgb
# faça no geogebra e coloque os pontos para cá
vertices = [
    [-0.8, -0.8, 1,0,0],    #v0 - vertice 0
    [0.0, -0.8, 1,1,0],     #v1
    [0.8, -0.8, 0,1,0],     #v2
    [-0.4, 0.0, 1,0,1],     #v3
    [0.4, 0.0, 0,1,1],      #v4
    [0.0, 0.8, 0,0,1]       #v5
]
# 9(vertices) x 5(numeros) = 45 x 4bytes (float) = 180 bytes

# otimização do OpenGL, diminuir vertices que apresentam valores. Porém o OpenGL não saberá mais qual figura (face) desenhar
# solução, fazer um array (vetor) contendo uma lista de indices indicando quais são os vertices para conectar cada face

#buffer de indices - Element Buffer Object - EBO
faces = [
    [0,1,3], # face inferior esquerda
    [1,2,4], # face inferior direita
    [3,4,5],  # face superior
    [1,3,4] # conectando a face do triangulo do meio
]

qtdVertices = len(vertices) #sempre pega o tamanho de vertices
qtdFaces = len(faces)
vaoId = 0
shaderId = 0

def init():
    glClearColor(1, 1, 1, 1) # seta cor de fundo

    global vertices, faces, vaoId, shaderId

    # normalização de dados do array vertices
    vertices = np.array(vertices, dtype=np.float32)

    # criar o Vertex Array Object - antes do VBO
    vaoId = glGenVertexArrays(1) # qtd que será criado
    # tornar o VAO ativo
    glBindVertexArray(vaoId)

    # criar o Vertex Buffer Object
    vboId = glGenBuffers(1)
    # tornar o VBO ativo
    glBindBuffer(GL_ARRAY_BUFFER, vboId)
    # enviar os dados para o VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) 
   
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(0)) # para os vertices dos triangulos - figura
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(2*4)) # para a cor dos triangulos
    
    glEnableVertexAttribArray(0) # atributo posicao
    glEnableVertexAttribArray(1) # atributo cor


    faces = np.array(faces, dtype=np.uint32) # normalização de dados do array faces

    # criar o Element Buffer Object - EBO
    eboId = glGenBuffers(1)
    
    # tornar o EBO ativo
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eboId)
    
    # enviar os dados para o EBO
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)


    # desativar o VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # desativar o VAO
    glBindVertexArray(0)

    # Precisamos configurar as cores ao desenho no OpenGL moderno 3.0 com shaders
    # criar os arquivos de shader

    # código fonte dos shaders
    # ler o arquivo do vertex shader
    with open('02_vertexShader.glsl','r') as file:
        vsSource = file.read() # le o arquivo e retorna uma string

    # ler o arquivo do fragment shader
    with open('02_fragmentShader.glsl','r') as file:
        fsSource = file.read() # le o arquivo e retorna uma string

    vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
    shaderId = gls.compileProgram(vsId, fsId)



def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shaderId)
    glBindVertexArray(vaoId)

    # glDrawArrays(GL_TRIANGLES, # o que vai desenhar - primitiva
    #              0, #indice de qual vertice (do array) vai começar a desenhar
    #              qtdVertices) # qtd de vertices que vc quer desenhar
    
    # configurando o desenho baseado no que tem no EBO
    glDrawElements(GL_TRIANGLES, # o que vai desenhar - primitiva
                   3 * qtdFaces, # qtd de faces (indices) que vai desenhar
                   GL_UNSIGNED_INT, # tipo de dados que estão sendo usados nos indices
                   None) #indice do EBO de qual vertice (do array) vai começar a desenhar - tamanho em bytes
    
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
