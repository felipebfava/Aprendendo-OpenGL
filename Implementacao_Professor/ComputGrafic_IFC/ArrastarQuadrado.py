
import glfw
from OpenGL.GL import *

# tupla de tuplas
pontos = ((-0.25, -0.25),
          (-0.25, 0.25),
          (0.25, 0.25),
          (0.25, -0.25)
)

# para o quadrado começar na origem
transla_x = 0
transla_y = 0

arrasta = False
offset_x = 0
offset_y = 0

def init():
    glClearColor(1,1,1,1)

def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    glPushMatrix()
    glTranslatef(transla_x, transla_y, 0)

    glBegin(GL_QUADS)
    glColor3f(0,1,1)

    for x, y in pontos:
        glVertex2f(x, y)

    glEnd()
    glPopMatrix()

def cliqueMouse(window, button, action, mods):
    global transla_x, transla_y, offset_x, offset_y, arrasta
    
    if button == glfw.MOUSE_BUTTON_LEFT:
        x,y = glfw.get_cursor_pos(window)

        largura, altura = glfw.get_window_size(window)
        x_opengl = (x/ largura) * 2 - 1
        y_opengl = -((y/ altura) * 2 - 1)

        if action == glfw.PRESS:
            # só funciona se o mouse estiver dentro dos limites do quadrado
            if(transla_x - 0.25 <= x_opengl <= transla_x + 0.25 and
               transla_y - 0.25 <= y_opengl <= transla_y + 0.25):
                
                arrasta = True
                offset_x = x_opengl - transla_x
                offset_y = y_opengl - transla_y

        elif action == glfw.RELEASE:
            arrasta = False

def cursor_pos(window, x, y):
    global transla_x, transla_y

    if arrasta:
        largura, altura = glfw.get_window_size(window)
        
        x_opengl = (x/ largura) * 2 - 1
        y_opengl = -((y/ altura) * 2 - 1)

        transla_x = x_opengl - offset_x
        transla_y = y_opengl - offset_y

def main():
    glfw.init()
    window = glfw.create_window(600,600, "Translada Quadrado com Clique", None, None)
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, cliqueMouse)
    glfw.set_cursor_pos_callback(window, cursor_pos)

    init()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
