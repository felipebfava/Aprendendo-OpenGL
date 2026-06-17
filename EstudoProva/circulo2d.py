# Circulo 2d simples com OpenGL e glfw

from OpenGL.GL import *
import glfw
import math


# Variáveis Globais para movimentar o círculo começando da origem (0,0)
# Movimento de transladar
transla_x = 0
transla_y = 0


def init():
    # Seta uma cor de fundo a janela alterando r,g,b,alpha(opacidade)
    glClearColor(1, 1, 1, 1)


def desenhaCirculo2d(raio, segmentos):

    # # Aplicar uma matriz identidade para não acumular as transformações
    # # sem ela o quadrado só para de movimentar caso receba
    # # uma tecla contrária ao movimento que está fazendo
    glLoadIdentity()

    # # Para aplicar movimento na estrutura
    # # Precisa ser antes de definir a estrutura em glBegin()
    glTranslatef(transla_x, transla_y, 0)

    # Função que inicia qualquer estrutura aceita pelo glfw 
    # Estrutura do circulo usaremos varios triangulos
    glBegin(GL_TRIANGLE_FAN)

    # Para definir uma cor a ser usada pela estrutura
    # Alterando r,g,b indo de 0-(0) a 1-(255)
    glColor3f(1, 0, 0) # vermelho

    # Loop para repetir a conexão dos triangulos
    # segmentos + 1 para conectar o último triangulo
    # caso a quantidade de segmentos sejam pares

    # Para cada i na quantidade de segmentos + 1
    for i in range (segmentos + 1):
        # Usaremos o cálculo do raio e dos senos cossenos
        # para pegar o angulo em graus usamos o circulo completo
        # divido pela quantidade de segmentos
        # Como temos 20 segmentos: 360 / 20 = 18°
        # cada segmento terá 18°
        # multiplica i para iterar e ir para o próximo
        angulo_graus = (360/segmentos) * i

        # as funções seno e cosseno da biblioteca math
        # só aceitam o angulo em radianos
        # então precisa converter
        angulo_radianos = math.radians(angulo_graus)

        # Calcula a posição de x e y conforme os valores de cosseno e seno
        # cos(angulo) = cateto adjacente / hipotenusa
        # sin(angulo) = cateto oposto / hipotenusa
        # cos(θ) = x / raio
        # sen(θ) = y / raio
        x = raio * math.cos(angulo_radianos)
        y = raio * math.sin(angulo_radianos)

        # Define os vértices do círculo
        # Alterando a posição em x,y,z
        # Como faremos um círculo 2d usaremos glVertex2f()
        # ainda dentro do for
        glVertex2f(x, y)

    # Determina o Fim da estrutura do Begin
    glEnd()


def render():
    
    # Limpa o buffer de cor da janela
    glClear(GL_COLOR_BUFFER_BIT)

    # Chama a função de desenhar o círculo 2d
    # No nosso caso precisamos passar o raio do circulo e
    # a quantidade de segmentos que ele terá
    # quanto mais segmentos, mais redondo será o círculo
    desenhaCirculo2d(0.1, 20)

    


# Função que pega as teclas apertadas do teclado
def teclado(window, key, scancode, action, mods):
    
    # Variáveis globais precisam ser chamadas
    # caso os seus valores se alterem dentro de funções
    global transla_x, transla_y

    # se a ação for de pressionar (tecla pressionada) faça
    if action == glfw.PRESS:

        # W sobe, S desce, A move para esquerda, D move para direita
        # para subir(+) ou descer(-) precisa alterar o valor de y
        # para a esquerda x diminui(-) e para a direita x aumenta (+)
        if key == glfw.KEY_W: # se esta tecla for W faça
            transla_y += 0.01 # sobe
        
        if key == glfw.KEY_S:
            transla_y -= 0.01 # desce
        
        if key == glfw.KEY_A:
            transla_x -= 0.01 # esquerda
        
        if key == glfw.KEY_D:
            transla_x += 0.01 # direita


def main():
    
    # Iniciar o GLFW
    glfw.init()

    # Criar a Janela
    window = glfw.create_window(800, 600, "Janela Quadrado", None, None)

    # Define como janela principal no contexto
    glfw.make_context_current(window)

    # Define a função que irá captar as entradas do teclado
    glfw.set_key_callback(window, teclado)

    # Chama a função para iniciar
    init()
    
    # Loop para deixar a janela aberta até ser fechada
    while not glfw.window_should_close(window):
        
        # Carrega os eventos de inputs
        glfw.poll_events()

        # Chama a função de renderização - nossa imagem/objeto
        render()

        # Usa buffers para renderização da imagem da janela
        glfw.swap_buffers(window)

if __name__ == "__main__":
    main()