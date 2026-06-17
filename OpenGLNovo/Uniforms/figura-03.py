# arquivo figura-01.py
# video referencia https://www.youtube.com/watch?v=KxBjrq2dMQs&t=456s

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np
import ctypes # para utilizar tipos da linguagem C - gambiarra para o python aguentar
from OpenGLNovo.Uniforms.shader import * # estou importando as coisas do arquivo shader que está localizado na mesma pasta

vertices = [
    [-0.8, -0.8],     #v0
    [ 0.8, -0.8],     #v1
    [ 0.8, 0.8],      #v2
    [-0.8, 0.8]       #v2
]

faces = [
    [0,1,2],
    [0,2,3]
]

colors = [
    [1,0,0], # vermelho
    [0,1,0], # verde
    [0,0,1], # azul
    [1,1,0], # amarelo
    [1,0,1], # magenta
    [0,1,1], # ciano
]

colorActive = 0

qtdVertices = len(vertices) #sempre pega o tamanho de vertices
qtdFaces = len(faces)
vaoId = 0
myShader = None

def init():
    glClearColor(1, 1, 1, 1) # seta cor de fundo

    global vertices, faces, vaoId, myShader

    # normalização de dados do array vertices
    vertices = np.array(vertices, dtype=np.float32)

    # criando o VAO
    vaoId = glGenVertexArrays(1)            
    glBindVertexArray(vaoId)                # tornar o VAO ativo
    
    # criando o VBO
    vboId = glGenBuffers(1)                 
    glBindBuffer(GL_ARRAY_BUFFER, vboId)    # tornar o VBO ativo
    
    # enviar os dados para o VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) 
   
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2*4, ctypes.c_void_p(0)) # para os vertices dos triangulos - figura
    
    glEnableVertexAttribArray(0) # atributo posicao



    # criando o EBO
    faces = np.array(faces, dtype=np.uint32) # normalização de dados do array faces
    eboId = glGenBuffers(1)                            
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eboId)        # tornar o EBO ativo

    # enviar os dados para o EBO
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)


    glBindBuffer(GL_ARRAY_BUFFER, 0)        # desativar o VBO
    glBindVertexArray(0)                    # desativar o VAO

    # criando o Shader
    # código fonte dos shaders
    # chamando a classe Shader do arquivo shader.py
    # dica: pode ser usado o os.path para pegar os caminhos absolutos dos arquivos, caso aconteça algum problema com os caminhos
    myShader = Shader('03_vertexShader.glsl', '03_fragmentShader.glsl')



def render():
    glClear(GL_COLOR_BUFFER_BIT)

    # glUseProgram(shaderId)  # substituido pelo método
    myShader.bind() # chamando o método criado na classe Shader
    glBindVertexArray(vaoId)

    #OpenGL com GLSL versões antigas - antes da 4.6.0
    # color_loc = glGetUniformLocation(shaderId, 'color') # vai achar onde está a variável uniform color do fragmentShader
    # glUniform3f(color_loc, 0,1,0)
    # glUniform3f(0, 0,1,0) # o primeiro 0 se refere ao id do location do fragmentShader

    # chamando o método da classe Shader que substitui o glUniform3f
    myShader.setUniformv('color', colors[colorActive])

    # configurando o desenho baseado no que tem no EBO
    glDrawElements(GL_TRIANGLES, # o que vai desenhar - primitiva
                   3 * qtdFaces, # qtd de faces (indices) que vai desenhar
                   GL_UNSIGNED_INT, # tipo de dados que estão sendo usados nos indices
                   None) #indice do EBO de qual vertice (do array) vai começar a desenhar - tamanho em bytes
    
    glBindVertexArray(0)

    # desativando o shader
    # glUseProgram(0)
    myShader.unbind()
   
# window - ponteiro para a janela que recebeu o evento (a ativa)
# key - código da tecla pressionada ou liberada - GLFW_KEY_A ou GLFW_KEY_ESCAPE
# scancode - código da tecla físico (varia com tipo de teclado)
# action - indica o que aconteceu com a tecla - GLFW_PRESS (pressionada), GLFW_RELEASE (liberada), GLFW_REPEAT (está sendo segurada)
# mods - flag que indica qual identificar está ativo - GLFW_MOD_SHIFT, GLFW_MOD_CONTROL ou GLFW_MOD_ALT
def keyboard(window, key, scancode, action, mods):
    global colorActive
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:  glfw.set_window_should_close(window, True)
        if key == glfw.KEY_SPACE: colorActive = (colorActive + 1) % len(colors) # a varial colorActive vai ficar girando entre 0,1,2,3,4,5 - tamanho do vetor colors

def main():
    glfw.init()
    window = glfw.create_window(500, 500, "Minha Janela", None, None)
    glfw.make_context_current(window)

    glfw.set_key_callback(window, keyboard)

    init()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()


        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__" :
    main()
