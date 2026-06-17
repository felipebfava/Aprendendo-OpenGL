from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import ctypes
import numpy as np
import math

class Circle:
    def __init__(self, nDivisao=16, raio=1):
        self.vertices = []
        deltaAngle = 2*math.pi/nDivisao # 360° é igual a 2*Pi em radianos - deltaAngle está em radianos agora
        for i in range(nDivisao):
            angle = i*deltaAngle # de quantos em quantos graus vai ter um triangulo
            # usando a ideia de vários triangulos retangulo formam um circulo
            x = raio*math.cos(angle) # determino o tamanho da reta no eixo x
            y = raio*math.sin(angle) # determino o tamanho da reta no eixo y
            self.vertices.append([x, y, 1,0,0])

        self.qtdVertices = len(self.vertices)

        # normalização de dados do array vertices
        self.vertices = np.array(self.vertices, dtype=np.float32)

        # criando o VAO
        self.vaoId = glGenVertexArrays(1)            
        glBindVertexArray(self.vaoId)                # tornar o VAO ativo
        
        # criando o VBO
        vboId = glGenBuffers(1)                 
        glBindBuffer(GL_ARRAY_BUFFER, vboId)    # tornar o VBO ativo
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW) 
        glEnableVertexAttribArray(0) # atributo posicao
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1) # atributo cor
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(2*4))

        glBindBuffer(GL_ARRAY_BUFFER, 0)        # desativar o VBO
        glBindVertexArray(0)                    # desativar o VAO

        # vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
        # fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
        # self.shaderId = gls.compileProgram(vsId, fsId)
    
    def render(self, shaderId):
        glBindVertexArray(self.vaoId) 
        glDrawArrays(GL_LINE_LOOP, 0, self.qtdVertices)
        glBindVertexArray(0)
