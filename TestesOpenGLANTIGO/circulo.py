import glfw
from OpenGL.GL import *
import numpy as np
import math


def draw_circle(radius, segments):
   
    glBegin(GL_TRIANGLE_FAN)    
    for i in range(segments + 1):
        # angle = 2 * math.pi * i / segments
        angGraus = (360/segments)*i
        angle = math.radians(angGraus)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()


def main():
    glfw.init()


    window = glfw.create_window(800, 800, "Circle with OpenGL", None, None)  


    glfw.make_context_current(window)


    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()


        glColor3f(1.0, 0.0, 0.0)
        draw_circle(0.5, 100)


        glfw.swap_buffers(window)
        glfw.poll_events()


    glfw.terminate()


if __name__ == "__main__":
    main()

