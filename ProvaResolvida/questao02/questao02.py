import glfw
from OpenGL.GL import *

VELOCIDADE = 0.001

dx = 0
dy = 0
    
def inicializa_objetos():

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
    

def colisao():
    
    # posicao do quadrado vermelho
    global dx, dy
    
    vermelho, azuis, amarelos = inicializa_objetos()
    
    posx_azul = abs(azuis[0]["x"]) 
    posy_azul = abs(azuis[0]["y"]) 
    
    
    posx_amarelo = abs(amarelos[0]["x"])
    posy_amarelo = abs(amarelos[0]["y"]) 
    
    if (posx_azul > dx and posy_azul < dy):
        print("Colidiu")
    


def main():

    glfw.init()

    window = glfw.create_window(800, 800,"Questao 1", None, None)
    glfw.make_context_current(window)

    vermelho, azuis, amarelos = inicializa_objetos()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        movimenta_vermelho(window, vermelho)
        renderiza(vermelho, azuis, amarelos)
        
        colisao()
        
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()