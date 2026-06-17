import glfw
from OpenGL.GL import *
import numpy as np

#tupla
vertices = (
    (-0.2, -0.2),
    (0.2, -0.2),
    (0.0, 0.2)
)

def init():
    glClearColor(0, 0, 0, 1)
   
def translacao(v, tx, ty):
    novo = []
    for x, y in v:
        novo.append([x+tx, y+ty])
    return novo


def rotacao(v, angulo):
    theta = np.radians(angulo) # precisa ser transformado em radianos para a função cosseno e seno usarem
    cos, sin = np.cos(theta), np.sin(theta)

    matriz_rotacao = np.array((
        (cos, -sin),
        (sin, cos)
        ))
    
    # rota = matriz_rotacao * v
    # return rota

    # preciso fazer a transposta da matriz_rotacao pois temos vertice sendo uma matriz 3x2 e matriz_rotacao uma matriz 2x2
    # vai ficar algo desse tipo por baixo dos panos (algo do tipo)
    # a transposta de uma matriz é, a primeira linha se tornará a primeira coluna, assim por diante
    #  [x1, y1]
    #  [x2, y2]
    #  [x3, y3]
    #      x
    #  [cos, sin]
    #  [-sin, cos]
    # = [x', y']

    # v não aceita a transposta, então para dar certo, faço a transposta da matriz_rotacao

    return np.dot(v, matriz_rotacao.T) # .T significa a operação transposta


def escala(v, escalar):
    novo = []
    for x, y in v:
        novo.append([x*escalar, y*escalar])
    return novo

# cisalhamento horizontal ocorrerá quando houver variação em x
# cisalhamento vertical ocorrerá quando houver variação em y

# usando a mesma ideia das funções de escala() e translação()
def cisalhamento_01(v, shx, shy):
    novo = []

    for x, y in v:
        novo.append([x+shx*y, y+shy*x])

    return novo

# outra forma de ser feito usando a mesma ideia da função rotação()
def cisalhamento_02(v, shx, shy):

    matriz_cisalhamento = np.array((
        (1, shx),
        (shy, 1)
        ))

    return np.dot(v, matriz_cisalhamento.T) # .T significa a operação transposta


def reflexao(v):
    # será a matriz_reflexao que definirá o tipo de reflexão que irá acontecer
    # representa reflexão no eixo x - inverte sinal de y
    # matriz_reflexao = np.array((
    #   (1, 0),
    #   (0, -1)
    # ))

    # representa reflexão no eixo y - inverte sinal de x
    # matriz_reflexao = np.array((
    #   (-1, 0),
    #   (0, 1)
    # ))
    
    # representa reflexão na origem - inverte sinal de x e y
    # matriz_reflexao = np.array((
    #   (-1, 0),
    #   (0, 1)
    # ))

    # representa reflexão na reta y=x - troca valores de x e y entre si
    # matriz_reflexao = np.array((
    #   (-1, 0),
    #   (0, 1)
    # ))

    matriz_reflexao = np.array((
        (0, 1),
        (1, 0)
    ))

    return np.dot(v, matriz_reflexao.T) # .T significa a operação transposta

def render(v):    
    glBegin(GL_TRIANGLES)
    for x, y in v:
        glVertex2f(x,y)                    
    glEnd()
   

def main():
    glfw.init() #inicializa biblioteca glfw
    window = glfw.create_window(800, 600, "Matrizes de Transformação", None, None)
    glfw.make_context_current(window) #cria o contexto


    init()
    global vertices # para trabalhar com o vetor localmente
    v = np.array(vertices) # transforma em um vetor numpy deixa + facil

    ## -- # Transformações # -- ##
    # v = translacao(vertices, 0, 0.5) # passa os pontos e os numeros para variacao em x e y
    # v = rotacao(vertices, 30) # passa os pontos e o angulo
    # v = escala(vertices, 2) # passa os pontos e o numero escalar que vai multiplicar
    # v = cisalhamento_01(vertices, 0.1, 0) # passa os pontos e os numeros para variacao em x e y - cisalhamento horizontal
    # v = cisalhamento_02(vertices, 0, 0.3) # passa os pontos e os numeros para variacao em x e y - cisalhamento vertical
    v = reflexao(vertices) # passa somente os pontos


    glClear(GL_COLOR_BUFFER_BIT)

    while not glfw.window_should_close(window): #roda enquanto não fecha a janela
        glfw.poll_events() #captura eventos
        glColor3f(1,0,0) # cor do triangulo original é vermelho
        render(vertices) # renderiza/exibe a figura geometrica original
        
        glColor3f(0,0,1) # cor do triangulo modificado é azul
        render(v) # renderiza/exibe a figura geometrica apos alguma transformação
        glfw.swap_buffers(window)
    glfw.terminate()
   
if __name__ == "__main__":
    main()
