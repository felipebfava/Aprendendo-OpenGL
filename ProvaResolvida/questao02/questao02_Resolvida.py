import glfw
from OpenGL.GL import *

VELOCIDADE = 0.01

dx = 0
dy = 0

def inicializa_objetos():
    
    # o tamanho de todos os quadrados é 0.15

    vermelho = {"x": -0.8,"y": -0.8,"tam": 0.15, "cor": (1.0, 0.0, 0.0)}

    azuis = [
        {"x": -0.2, "y": -0.2, "tam": 0.15, "cor": (0.0, 0.0, 1.0)},
        {"x": 0.3, "y": 0.4, "tam": 0.15, "cor": (0.0, 0.0, 1.0)}
    ]

    amarelos = [
        {"x": -0.7, "y": 0.6, "tam": 0.15, "cor": (1.0, 1.0, 0.0)},
        {"x": 0.6, "y": -0.35, "tam": 0.15, "cor": (1.0, 1.0, 0.0)}
    ]

    return vermelho, azuis, amarelos


def desenha_quadrado(x, y, tamanho, cor):
    glColor3f(*cor)

    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + tamanho, y)
    glVertex2f(x + tamanho, y + tamanho)
    glVertex2f(x, y + tamanho)
    glEnd()


def renderiza(vermelho, azuis, amarelos):
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    desenha_quadrado(vermelho["x"], vermelho["y"], vermelho["tam"], vermelho["cor"])
    desenha_quadrado(azuis[0]["x"], azuis[0]["y"], azuis[0]["tam"], azuis[0]["cor"])
    desenha_quadrado(azuis[1]["x"], azuis[1]["y"], azuis[1]["tam"], azuis[1]["cor"])
    desenha_quadrado(amarelos[0]["x"], amarelos[0]["y"], amarelos[0]["tam"], amarelos[0]["cor"])
    desenha_quadrado(amarelos[1]["x"], amarelos[1]["y"], amarelos[1]["tam"], amarelos[1]["cor"])


def movimenta_vermelho(window, vermelho):
    global dx, dy

    dx = 0
    dy = 0

    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        dx = -VELOCIDADE

    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        dx = VELOCIDADE

    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        dy = VELOCIDADE

    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        dy = -VELOCIDADE

    vermelho["x"] += dx
    vermelho["y"] += dy

    print(vermelho["x"], vermelho["y"])


# Tentar fazer uma função mais genérica que consiga resolver
# Que resolva a colisão AABB - Hitbox
def colidiu(q1, q2):

    # eu preciso testar as 4 direções dos quadrados
    # direita, esquerda, cima e baixo

    ## Validação da posição X
    
    # se a distância da pos_x + o tamanho do 1° quadrado
    # for menor que a posição x do 2°, não ocorreu colisão
    if q1["x"] + q1["tam"] < q2["x"]:
        return False
    
    if q1["x"] > q2["x"] + q2["tam"]:
        return False
    
    ## Validação da posição Y
    if q1["y"] + q1["tam"] < q2["y"]:
        return False
    
    if q1["y"] > q2["y"] + q2["tam"]:
        return False

    # se chegou aqui, nenhum teste 'if' foi válido
    # logo, houve colisão    
    return True
    
    


def colisao(vermelho, azuis, amarelos):
    
    global dx, dy

    # dados dos quadrados

    # azuis e amarelos são uma lista de dicionários
    # o vermelho é somente um dicionário

    # 1° quadrado azul
    # pos_quad1_x_azul = azuis[0]["x"]
    # pos_quad1_y_azul = azuis[0]["y"]
    # tam_quad1_azul = azuis[0]["tam"]

    # 2° quadrado azul
    # pos_quad2_x_azul = azuis[1]["x"]
    # pos_quad2_y_azul = azuis[1]["y"]
    # tam_quad2_azul = azuis[1]["tam"]

    # Este loop for tem a mesma função do que eu escrever e extrair as informações da lista de dicionários
    # isto é, melhor percorrer assim, do que acessar todos como eu estava fazendo
    for azul in azuis:
        # Não precisa de todas essas informações
        # pos_x = azul["x"]
        # pos_y = azul["y"]
        # tam = azul["tam"]
        
        # se vermelho e azul colidirem
        # a posição em x recebe dx que é o movimento em x do vermelho
        # a posição em y recebe dy que é o movimento em y do vermelho
        if colidiu(vermelho, azul):
            azul["x"] += dx
            azul["y"] += dy

            limite_tela(azul)
            
    

    # 1° quadrado amarelo
    # pos_quad1_x_amarelo = amarelos[0]["x"]
    # pos_quad1_y_amarelo = amarelos[0]["y"]
    # tam_quad1_amarelo = amarelos[0]["tam"]

    # 2° quadrado amarelo
    # pos_quad1_x_amarelo = amarelos[1]["x"]
    # pos_quad1_y_amarelo = amarelos[1]["y"]
    # tam_quad1_amarelo = amarelos[1]["tam"]

    # Não é necessário passar todas as informações para a função colidiu()
    for amarelo in amarelos:
        # pos_x = amarelos["x"]
        # pos_y = amarelos["y"]
        # tam = amarelos["tam"]
        
        # se colidiu() retornar True a colisão aconteceu então precisa mudar a cor dos amarelos para verde
        # se não aconteceu colisão, deixa a cor amarela
        if colidiu(vermelho, amarelo):
            amarelo["cor"] = (0,1,0) # cor verde
        else:
            amarelo["cor"] = (1,1,0) # cor amarela

    # quadrado vermelho
    # Não precisa - não serão utilizadas desse jeito
    # pos_x_vermelho = vermelho["x"]
    # pos_y_vermelho = vermelho["y"]
    # tam_vermelho = vermelho["tam"]
    

def limite_tela(quadrado):

    if quadrado["x"] < -1:
        quadrado["x"] = -1
    
    if quadrado["x"] > 1 - quadrado["tam"]:
        quadrado["x"] = 1 - quadrado["tam"]
    
    if quadrado["y"] < -1:
        quadrado["y"] = -1
    
    if quadrado["y"] > 1 - quadrado["tam"]:
        quadrado["y"] = 1 - quadrado["tam"]



def main():

    glfw.init()

    window = glfw.create_window(800, 800,"Questao 2", None, None)
    glfw.make_context_current(window)

    vermelho, azuis, amarelos = inicializa_objetos()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        

        movimenta_vermelho(window, vermelho)
        limite_tela(vermelho)

        renderiza(vermelho, azuis, amarelos)
        
        # esses parâmetros precisam ser passados assim
        colisao(vermelho, azuis, amarelos)
        
        glfw.swap_buffers(window)
        glfw.wait_events_timeout(1.0/60.0)

    glfw.terminate()


if __name__ == "__main__":
    main()