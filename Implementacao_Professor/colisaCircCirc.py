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

            if colisaoCirculoCirculo(deslocamento_x, deslocamento_y, ox, oy):

                deslocamento_x += varia
                pararObjeto()
           
    if tecla(window, glfw.KEY_RIGHT) == glfw.PRESS:   
        deslocamento_x += varia
        
        for ox, oy in obstaculos:

            if colisaoCirculoCirculo(deslocamento_x, deslocamento_y, ox, oy):

                deslocamento_x -= varia
                pararObjeto()
        
    if tecla(window, glfw.KEY_UP) == glfw.PRESS:
        deslocamento_y += varia

        for ox, oy in obstaculos:

            if colisaoCirculoCirculo(deslocamento_x, deslocamento_y, ox, oy):

                deslocamento_y -= varia
                pararObjeto()
    
    if tecla(window, glfw.KEY_DOWN) == glfw.PRESS:
        deslocamento_y -= varia

        for ox, oy in obstaculos:

            if colisaoCirculoCirculo(deslocamento_x, deslocamento_y, ox, oy):

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

    glPushMatrix()
    glTranslatef(x, y, 0)

    glBegin(GL_TRIANGLE_FAN)

    for i in range(segmentos + 1):

        angGraus = (360 / segmentos) * i
        angle = math.radians(angGraus)

        cx = raioObstaculo * math.cos(angle)
        cy = raioObstaculo * math.sin(angle)

        glVertex2f(cx, cy)

    glEnd()
    glPopMatrix()


def colisaoCirculoCirculo(dx, dy, ox, oy):
    # ox e oy são as posições dos quadrados
    
    # quadrado principal
    x1 = dx
    y1 = dy

    # outros quadrados
    x2 = ox
    y2 = oy

    # distância entre centros - pitagoras
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


    # colisão
    return distancia < (raioCirculoMenor + raioObstaculo)


def pararObjeto():
    global mov
    mov = 0
    
 
def main():


    glfw.init()        
    window = glfw.create_window(largura, altura, "Colisao Circulo x Circulo", None, None)    
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
            if colisaoCirculoCirculo(deslocamento_x, deslocamento_y, ox, oy):
                print(f"Colidiu com obstáculo em ({ox}, {oy})")
                # Aqui você pode adicionar lógica para lidar com a colisão

                pararObjeto()
        
        glfw.poll_events()
        glfw.swap_buffers(window)


    glfw.terminate()


if __name__ == "__main__":
    main()

