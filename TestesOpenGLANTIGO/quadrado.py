from OpenGL.GL import *
import glfw


# tela trabalha no range 0 a 1
# P e Q são pontos que ficam exatamente no meio das retas/vetores, P fica na reta AB, Q fica na reta PC e R fica na reta CD

# criação de tuplas
# seta os pontos do quadrado/vértices pA, pB, pC e pD
pA = (0.5, 0.5, 1, 0, 0) # primeiro vértice/ponto do quadrado -> x, y, r, g, b
pB = (-0.5, 0.5, 0, 1, 0) # segundo ponto do quadrado -> x, y, r, g, b
pC = (-0.5, -0.5, 0, 0, 1) # terceiro ponto do quadrado -> x, y, r, g, b

pD = (0.5, -0.5, 0.25, 0.25, 0.25) # quarto ponto do quadrado

# pP e pQ são pontos que ficam no meio das retas/vetores
pP = (0.5, 0) # ponto que fica no meio da reta A-B
pQ = (0.5, -0.5) # ponto que fica no meio da reta C-P


def init():
    glClearColor(1, 1, 1, 1) # seta cor de fundo


def render():
    glClear(GL_COLOR_BUFFER_BIT)

    # alterar o tamanho do ponto, altera o espaçamento de preenchimento das cores
    # entre 4 e 6 nenhum vértice fica apagado ou achatado.
    glPointSize(6)

    glBegin(GL_POINTS)

    alpha = 0.0 # escalar que vai percorer a reta AB
    while alpha <= 1.0:

        # vai calcular o ponto P na reta AB
        Px = alpha*pB[0] + pA[0]*(1-alpha)
        Py = alpha*pB[1] + pA[1]*(1-alpha)
        
        # a cor rgb varia conforme alpha -> A*(1-alpha)
        rP = alpha*pB[2] + pA[2]*(1-alpha)
        gP = alpha*pB[3] + pA[3]*(1-alpha)
        bP = alpha*pB[4] + pA[4]*(1-alpha)

        glColor3f(rP, gP, bP)
        glVertex2f(Px, Py)

        beta = 0.0 # escalar que vai percorrer a reta PC
        while beta <= 1.0:

            # vai calcular o ponto Q na reta PC
            Qx = beta*alpha*pB[0] + beta*pA[0]*(1-alpha) + pC[0]*(1-beta)
            Qy = beta*alpha*pB[1] + beta*pA[1]*(1-alpha) + pC[1]*(1-beta)
            
            # vai calcular o ponto C na reta PC
            # Qx = beta*Px + pC[0]*(1-beta)
            # Qy = beta*Py + pC[1]*(1-beta)
            
            # setando as cores
            # variando conforme beta -> C*(1-beta)
            rQ = beta*rP + pC[2]*(1-beta)
            gQ = beta*gP + pC[3]*(1-beta)
            bQ = beta*bP + pC[4]*(1-beta)
            
            # cor da reta PC
            glColor3f(rQ, gQ, bQ)
            glVertex2f(Qx, Qy)

            delta = 0.0
            while delta <= 1.0:

                # vai calcular o ponto Q na reta PC
                Dx = beta*alpha*pB[0] + beta*pA[0]*(1-alpha) + pC[0]*(1-beta)
                Dy = beta*alpha*pB[1] + beta*pA[1]*(1-alpha) + pC[1]*(1-beta)
                
                # vai calcular o ponto C na reta PC
                # Qx = beta*Px + pC[0]*(1-beta)
                # Qy = beta*Py + pC[1]*(1-beta)
                
                # setando as cores
                # variando conforme beta -> C*(1-beta)
                rD = beta*rP + pC[2]*(1-beta)
                gD = beta*gP + pC[3]*(1-beta)
                bD = beta*bP + pC[4]*(1-beta)
                
                # cor da reta PC
                glColor3f(rD, gD, bD)
                glVertex2f(Dx, Dy)

            beta += 0.01
        alpha += 0.01
    glEnd()
            


    # vai pintar uma linha de x ponto 0.5,-1 até x ponto 0.5,0
    # enquanto x=0.5 >= -1
    # while y >= pC[1]:
        
        # cor do ponto B
        #r,g,b = pB[2], pB[3], pB[4]
        # glColor3f(r, g, b)

        # glVertex2f(pC[0],y)
        # y -= 0.01


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Minha Janela", None, None)
    glfw.make_context_current(window)
   
    init()


    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()    


        glfw.swap_buffers(window)
    glfw.terminate()




if __name__ == "__main__" :
    main()