import glfw
from OpenGL.GL import *

# está certa
VELOCIDADE = 0.01

dx = 0
dy = 0

# está certa
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

# está certa
def desenha_quadrado(x, y, tamanho, cor):
    glColor3f(*cor)

    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + tamanho, y)
    glVertex2f(x + tamanho, y + tamanho)
    glVertex2f(x, y + tamanho)
    glEnd()

# está certa
def renderiza(vermelho, azuis, amarelos):
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    desenha_quadrado(vermelho["x"], vermelho["y"], vermelho["tam"], vermelho["cor"])
    desenha_quadrado(azuis[0]["x"], azuis[0]["y"], azuis[0]["tam"], azuis[0]["cor"])
    desenha_quadrado(azuis[1]["x"], azuis[1]["y"], azuis[1]["tam"], azuis[1]["cor"])
    desenha_quadrado(amarelos[0]["x"], amarelos[0]["y"], amarelos[0]["tam"], amarelos[0]["cor"])
    desenha_quadrado(amarelos[1]["x"], amarelos[1]["y"], amarelos[1]["tam"], amarelos[1]["cor"])


# precisa movimentar o quadrado vermelho
# está certa
def movimenta_vermelho(window, vermelho):
    global dx, dy

    # todo loop eu coloco para zero denovo
    # senão a velocidade cresce sempre
    dx = 0
    dy = 0

    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        dx -= VELOCIDADE

    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        dx += VELOCIDADE

    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        dy += VELOCIDADE

    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        dy -= VELOCIDADE
    
    # atualizei os valores, agora preciso passar para o quadrado vermelho
    # x irá variar conforme dx e
    # y irá variar conforme dy
    vermelho["x"] += dx
    vermelho["y"] += dy

    # logo após movimentar o vermelho
    # verifica os limites da tela para ele não escapar
    limites_tela(vermelho)


# função que irá calcular a colisão AABB
# ela receberá 2 quadrados e fará verificações de colisão
# está certa
def colidiu(q1, q2):
    
    # a posição X + o tamanho do quadrado indicam uma borda
    # nesse caso a borda direita de q1
    # somente o valor X indica o início dessa borda

    # se a borda direita do q1 não alcança o início da borda de q2, não houve colisão
    if q1["x"] + q1["tam"] < q2["x"]:
        return False
    
    # se a borda direita de q2 não alcança o início da borda de q1, não houve colisão 
    if q1["x"] > q2["x"] + q2["tam"]:
        return False
    
    # testes para Y - os mesmos usados para X porém agora com Y 
    # se a borda direita do q1 não alcança o início da borda de q2, não houve colisão
    if q1["y"] + q1["tam"] < q2["y"]:
        return False
    
    # se a borda direita de q2 não alcança o início da borda de q1, não houve colisão 
    if q1["y"] > q2["y"] + q2["tam"]:
        return False
    
    # se chegou até aqui houve colisão - as bordas se tocaram
    return True


# precisa detectar colisão do quadrado vermelho com os outros quadrados
# está certa
def colisao(vermelho, azuis, amarelos):
    
    # aqui eu estou pegando cada item da lista dos amarelos
    for amarelo in amarelos:
        
        # vamos passar cada quadrado para uma função que calcula a colisão AABB - Hitbox
        # verificação da colisão se for verdadeira:
        if colidiu(vermelho, amarelo):
            # se for troca a cor do amarelo para verde
            amarelo["cor"] = (0.0, 1.0, 0.0) # cor verde
        else:
            # senão deixa a cor amarela padrão
            amarelo["cor"] = (1.0, 1.0, 0.0) # cor amarela
    
    # aqui eu estou pegando cada item da lista dos azuis
    for azul in azuis:
        # agora precisamos verificar a colisão do vermelho com os azuis
        # além disso, preciso mudar a posição dos azuis (x,y)
        # o que estamos até agora para a posição é dx e dy
        if colidiu(vermelho, azul):
            # então, de forma parecida como movemos o vermelho
            # azul recebe dx em x e dy em y sempre somando
            azul["x"] += dx
            azul["y"] += dy
            
            # como o azul se movimenta junto, chama a função para limitar a tela e ele não sair
            limites_tela(azul)

# precisamos definir os limites para a tela
# eu vou chamar essa função passando o quadrado, para testar se ele saiu ou não da tela
# irei colocar essa função onde quero testar esse limite, como os quadrados azuis e os vermelhos que podem sair da tela
def limites_tela(quadrado):
    
    # faço verificações para X e Y do quadrado
    # para a coordenada -1 é fácil 
    if quadrado["x"] < -1:
        quadrado["x"] = -1
    
    # porém para a coordenada maior que 1, precisamos diminuir o tamanho
    # caso não tenha o tamanho aqui o quadrado passa fora da tela porém até o ponto de ficar invisível para fora da tela
    # para o quadrado aparecer do jeito certo na tela sem passar ela, precisa informar o tamanho dele
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

        # posso chama o limite do vermelho logo após desenhar ele ou quando movimento ele
        # é a mesma coisa no fim das contas
        # limites_tela(vermelho)

        renderiza(vermelho, azuis, amarelos)

        # vamos passar todos os quadrados que vem de inicializa_objetos
        colisao(vermelho, azuis, amarelos)
        
        # esses parâmetros precisam ser passados assim
        glfw.swap_buffers(window)
        glfw.wait_events_timeout(1.0/60.0)

    glfw.terminate()


if __name__ == "__main__":
    main()