# arquivo figura-05.py
# video referencia https://www.youtube.com/watch?v=KxBjrq2dMQs&t=456s

import glfw
import glm
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np
import os
import ctypes # para utilizar tipos da linguagem C - gambiarra para o python aguentar
from OpenGLNovo.Transformacoes.item import * # estou importando as coisas do arquivo shader que está localizado na mesma pasta
from OpenGLNovo.Transformacoes.texture import * #essa parte temos que adicionar, não sei de onde vem
import math

obj = None
shaderId = 0
textHornet = None
ang = 0
# T = glm.translate(glm.vec3(0.5,0.2,0.0))
# T = glm.mat4(1) # criacao de uma matriz identidade - mat4 é uma matriz 4x4


def init():
    global obj, shaderId, textHornet, T

    T = glm.translate(glm.vec3(0.5,0.2,0.0)) # translacao do objeto

    glClearColor(0.9, 0.9, 0.9, 0) # seta cor de fundo
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    # criando o Shader
    # código fonte dos shaders
    # chamando a classe Shader do arquivo shader.py
    # dica: pode ser usado o os.path para pegar os caminhos absolutos dos arquivos, caso aconteça algum problema com os caminhos
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, '05_vertexShader.glsl'),'r') as file:
        vsSource = file.read() # le o arquivo e retorna uma string

    # ler o arquivo do fragment shader
    with open(os.path.join(here, '05_fragmentShader.glsl'),'r') as file:
        fsSource = file.read() # le o arquivo e retorna uma string

    vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
    shaderId = gls.compileProgram(vsId, fsId)

    # carregando a textura e criando o objeto
    textHornet = Texture(os.path.join(here, 'hornet.png'))
    obj = Item(textHornet.textId)


def render():
    global ang

    glClear(GL_COLOR_BUFFER_BIT)

    ang += math.radians(0.01) # tive que diminuir pois estava muito rapido - configure o valor
    limite_ang = ang % 3 # limite para que o ang não cresça infinitamente até estourar memória

    translacao_x = math.sin(ang)/2 # função seno sempre vai de -1 até 1
    T = glm.translate(glm.vec3(translacao_x, 0, 0))

    # rotacao em x
    rotacao_x = glm.vec3(1,0,0) # sempre passando um vetor de 3 dimensoes
    rotacao_y = glm.vec3(0,0,1) # sempre passando um vetor de 3 dimensoes
    rotacao_xy = glm.vec3(0,0,1) # rotaciona sentido anti-horario
    R = glm.rotate(glm.mat4(1), # começa com uma matriz identidade sem transformação ou uma já usada
                   ang, # define o angulo de rotacao - nesse caso da func render é a velocidade
                   rotacao_xy) # tipo de rotacao
    
    # escalar = glm.vec3(limite_ang, limite_ang, 0)
    # S = glm.scale(T, # começa com uma matriz identidade sem transformação ou uma já usada
    #               escalar)

    
    M = T * R #* S

    glUseProgram(shaderId)
    obj.render(shaderId, modelMatrix=glm.value_ptr(M)) # transforma o objeto mat4 para array de float

    # desativando o shader
    glUseProgram(0)


def keyboard(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:  glfw.set_window_should_close(window, True)

def main():
    glfw.init()
    window = glfw.create_window(500, 500, "Minha Janela", None, None)
    glfw.make_context_current(window)
    init()
    glfw.set_key_callback(window, keyboard)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__" :
    main()
