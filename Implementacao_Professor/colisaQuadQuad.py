import glfw
from OpenGL.GL import *


# posições
largura, altura = 800, 600
deslocamento_x = 0.0


deslocamento_y = 0.0
varia = 0.05


velocidade = 0.001
mov = 0


# sobre o quadrado
tam = 0.2
quad_x = 0
quad_y = -1
obstaculos = [(-0.6, -0.3), (0.6, 0.4)]


def inicializar():
    glClearColor(0.0, 0.0, 0.0, 1.0)
 


def teclado(window, key, scancode, action, mods):
    global mov, deslocamento_x, deslocamento_y
    if action == glfw.PRESS:
        if key == glfw.KEY_LEFT:    
            deslocamento_x -= varia

            for ox, oy in obstaculos:

                if colisaoQuadradoQuadrado(deslocamento_x, deslocamento_y, ox, oy):

                    deslocamento_x += varia
                    pararObjeto()
           
        elif key == glfw.KEY_RIGHT:    
            deslocamento_x += varia

            for ox, oy in obstaculos:

                if colisaoQuadradoQuadrado(deslocamento_x, deslocamento_y, ox, oy):

                    deslocamento_x -= varia
                    pararObjeto()
           
        elif key == glfw.KEY_UP:
            deslocamento_y += varia

            for ox, oy in obstaculos:

                if colisaoQuadradoQuadrado(deslocamento_x, deslocamento_y, ox, oy):

                    deslocamento_y -= varia
                    pararObjeto()
           
        elif key == glfw.KEY_DOWN:
            deslocamento_y -= varia

            for ox, oy in obstaculos:

                if colisaoQuadradoQuadrado(deslocamento_x, deslocamento_y, ox, oy):

                    deslocamento_y += varia
                    pararObjeto()

                           
    if action == glfw.RELEASE:
        if key == glfw.KEY_LEFT:
            mov = 0
           
        elif key == glfw.KEY_RIGHT:
            mov = 0
           
        elif key == glfw.KEY_UP:
            mov = 0
           
        elif key == glfw.KEY_DOWN:
            mov = 0


def atualizar():
    global deslocamento_x, deslocamento_y
    deslocamento_x += mov
    if deslocamento_x < -0.95:
        deslocamento_x = -0.95
    if deslocamento_x > 0.95:
        deslocamento_x = 0.95


def desenharQuadrado():
    glPushMatrix()
    glColor3f(1,1,1)
    glTranslatef(deslocamento_x, deslocamento_y, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(quad_x, quad_y)
    glVertex2f(quad_x + tam, quad_y)
    glVertex2f(quad_x + tam, quad_y + tam)
    glVertex2f(quad_x, quad_y + tam)    
    glEnd()
    glPopMatrix()


def desenharObstaculos(x,y):
    glLoadIdentity()
    glColor3f(0,0,1)    
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + tam, y)
    glVertex2f(x + tam, y + tam)
    glVertex2f(x, y + tam)
    glEnd()


def colisaoQuadradoQuadrado(dx, dy, ox, oy):
    # ox e oy são as posições dos quadrados
    
    # quadrado principal
    x1 = dx + quad_x
    y1 = dy + quad_y

    # outros quadrados
    x2 = ox
    y2 = oy

    return (
        x1 < x2 + tam and
        x1 + tam > x2 and
        y1 < y2 + tam and
        y1 + tam > y2
        )


def pararObjeto():
    global mov
    mov = 0
    
 
def main():


    glfw.init()        
    window = glfw.create_window(largura, altura, "Colisao Quadrado x Quadrado", None, None)    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, teclado)
   
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        atualizar()
        desenharQuadrado()
        for x,y in obstaculos:
            desenharObstaculos(x,y)
            
        
        # Verifica colisão
        for ox, oy in obstaculos:
            if colisaoQuadradoQuadrado(deslocamento_x, deslocamento_y, ox, oy):
                print(f"Colidiu com obstáculo em ({ox}, {oy})")
                # Aqui você pode adicionar lógica para lidar com a colisão

                pararObjeto()
        
        glfw.swap_buffers(window)
        glfw.poll_events()


    glfw.terminate()


if __name__ == "__main__":
    main()

