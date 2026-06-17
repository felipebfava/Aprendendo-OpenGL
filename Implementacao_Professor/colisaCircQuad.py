import glfw
from OpenGL.GL import *
import math

# posições
largura, altura = 800, 600
deslocamento_x = 0.0


deslocamento_y = 0.0
varia = 0.0001


velocidade = 0.001
mov = 0


# sobre o circulo
tam = 0.2

obstaculos = [(-0.6, 0.3)]
raioObstaculo = 0.25

raioCirculoMaior = 0.2
raioCirculoMenor = 0.1
segmentos = 40


def inicializar():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    

def teclado(window):
    global mov, deslocamento_x, deslocamento_y

    tecla = glfw.get_key

    # if action == glfw.PRESS:
    if tecla(window, glfw.KEY_LEFT) == glfw.PRESS:    
        deslocamento_x -= varia

        for ox, oy in obstaculos:

            if colisaoCirculoQuadrado(deslocamento_x, deslocamento_y, ox, oy, tam, tam):

                deslocamento_x += varia
                pararObjeto()
           
    if tecla(window, glfw.KEY_RIGHT) == glfw.PRESS:   
        deslocamento_x += varia
        
        for ox, oy in obstaculos:

            if colisaoCirculoQuadrado(deslocamento_x, deslocamento_y, ox, oy, tam, tam):

                deslocamento_x -= varia
                pararObjeto()
        
    if tecla(window, glfw.KEY_UP) == glfw.PRESS:
        deslocamento_y += varia

        for ox, oy in obstaculos:

            if colisaoCirculoQuadrado(deslocamento_x, deslocamento_y, ox, oy, tam, tam):

                deslocamento_y -= varia
                pararObjeto()
    
    if tecla(window, glfw.KEY_DOWN) == glfw.PRESS:
        deslocamento_y -= varia

        for ox, oy in obstaculos:

            if colisaoCirculoQuadrado(deslocamento_x, deslocamento_y, ox, oy, tam, tam):

                deslocamento_y += varia
                pararObjeto()


def atualizar():
    global deslocamento_x, deslocamento_y
    deslocamento_x += mov
    if deslocamento_x < -0.95:
        deslocamento_x = -0.95
    if deslocamento_x > 0.95:
        deslocamento_x = 0.95


def desenharCirculo():

    global raioCirculoMenor, segmentos

    glPushMatrix()
    glColor3f(1,1,1)
    glTranslatef(deslocamento_x, deslocamento_y, 0.0)

    # circulo menor
    glBegin(GL_TRIANGLE_FAN)

    for i in range(segmentos + 1):
 
        angGraus = (360/segmentos)*i
        angle = math.radians(angGraus)

        x = raioCirculoMenor * math.cos(angle)
        y = raioCirculoMenor * math.sin(angle)

        glVertex2f(x, y)
    glEnd()   
    
    glPopMatrix()


def desenharObstaculos(x, y):

    glLoadIdentity()

    glColor3f(0, 0, 1)

    glBegin(GL_QUADS)

    glVertex2f(x, y)
    glVertex2f(x + tam, y)
    glVertex2f(x + tam, y + tam)
    glVertex2f(x, y + tam)

    glEnd()


def colisaoCirculoQuadrado(cx, cy, rx, ry, rw, rh):

    global raioCirculoMenor
    
    # ponto MAIS próximo do quadrado
    proximo_x = max(rx, min(cx, rx + rw))
    proximo_y = max(ry, min(cy, ry + rh))
    
    # distância do círculo até esse ponto
    dx = cx - proximo_x
    dy = cy - proximo_y

    # colisão
    return (dx * dx + dy * dy) < (raioCirculoMenor * raioCirculoMenor)
    


def pararObjeto():
    global mov
    mov = 0
    

def main():


    glfw.init()        
    window = glfw.create_window(largura, altura, "Colisao Circulo x Quadrado", None, None)    
    glfw.make_context_current(window)
    # glfw.set_key_callback(window, teclado)
   
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT) 

        teclado(window)
        atualizar()
        desenharCirculo()
        for x,y in obstaculos:
            desenharObstaculos(x,y)
            
        
        # Verifica colisão
        for ox, oy in obstaculos:
            if colisaoCirculoQuadrado(deslocamento_x, deslocamento_y, ox, oy, tam, tam):
                print(f"Colidiu com obstáculo em ({ox}, {oy})")
                # Aqui você pode adicionar lógica para lidar com a colisão

                pararObjeto()
        
        glfw.poll_events()
        glfw.swap_buffers(window)


    glfw.terminate()


if __name__ == "__main__":
    main()

