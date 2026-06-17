# arquivo item.py
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import numpy as np

class Item():
    def __init__(self, textId):
        self.textId = textId

        vertices = [
            [-0.25, -0.25,   0.0, 0.0],     
            [ 0.25, -0.25,   1.0, 0.0],     
            [ 0.25, 0.25,    1.0, 1.0],     

            [-0.25, -0.25,   0.0, 0.0],     
            [ 0.25, 0.25,    1.0, 1.0],     
            [-0.25, 0.25,    0.0, 1.0],     
        ]

        self.qtdVertices = len(vertices) #sempre pega o tamanho de vertices
        vertices = np.array(vertices, dtype=np.float32)

        # criando o VAO
        self.vaoId = glGenVertexArrays(1)            
        glBindVertexArray(self.vaoId)                # tornar o VAO ativo
        
        # criando o VBO
        vboId = glGenBuffers(1)                 
        glBindBuffer(GL_ARRAY_BUFFER, vboId)    # tornar o VBO ativo
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) 
        glEnableVertexAttribArray(0) # atributo posicao
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1) # atributo cor
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(2*4))

        glBindBuffer(GL_ARRAY_BUFFER, 0)        # desativar o VBO
        glBindVertexArray(0)                    # desativar o VAO
    
    def render(self, shaderId, modelMatrix):
        glBindVertexArray(self.vaoId)
        glBindTexture(GL_TEXTURE_2D, self.textId)

        modelMatrix_loc = glGetUniformLocation(shaderId, 'modelMatrix')
        # glUniform2fv(shift_loc, 1, modelMatrix) # shift será um vetor/array, 1 significa que vc está enviando somente 1 vetor
        glUniformMatrix4fv(modelMatrix_loc, 1, GL_FALSE, modelMatrix)

        glDrawArrays(GL_TRIANGLES, 0, self.qtdVertices)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
        
