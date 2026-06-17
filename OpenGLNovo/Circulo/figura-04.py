# arquivo figura-01.py
# video referencia https://www.youtube.com/watch?v=HdK784X2xzw&list=PLvat2X-KHJNaWMdOfPJ7OIsNkHfoZXd1f&index=10

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np
import ctypes # para utilizar tipos da linguagem C - gambiarra para o python aguentar
from OpenGLNovo.Circulo.circle import * # estou importando as coisas do arquivo shader que está localizado na mesma pasta
# from shader import * # estou importando as coisas do arquivo shader que está localizado na mesma pasta

obj = None
shaderId = 0
def init():
    global shaderId, obj
    
    obj = Circle(nDivisao=64, raio=0.5) # chama o construtor da classe Circle
    
    glClearColor(1, 1, 1, 1) # seta cor de fundo
    glLineWidth(3)

    # criar os arquivos de shader
    # código fonte dos shaders
    # ler o arquivo do vertex shader
    with open('04_vertexShader.glsl','r') as file:
        vsSource = file.read() # le o arquivo e retorna uma string

    # ler o arquivo do fragment shader
    with open('04_fragmentShader.glsl','r') as file:
        fsSource = file.read() # le o arquivo e retorna uma string

    vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
    shaderId = gls.compileProgram(vsId, fsId)



def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shaderId)
    obj.render(shaderId)
    glUseProgram(0)
   

def keyboard(window, key, scancode, action, mods):
    
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:  glfw.set_window_should_close(window, True)


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
