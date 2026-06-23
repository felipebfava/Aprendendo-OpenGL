import random

import glfw
from OpenGL.GL import *
from PIL import Image


# As variaveis de textura começam como None porque o OpenGL so consegue criar
# texturas depois que a janela e o contexto grafico ja existem.
textura_jogador = None
textura_coracao = None
textura_inimigo1 = None
textura_inimigo2 = None
textura_cone = None
textura_barreira = None
textura_pista = None
textura_linha_chegada = None

# dt guarda o tempo entre um frame e outro. Usamos isso para o jogo rodar em
# velocidade parecida mesmo em computadores diferentes.
dt = 0

# Enquanto jogo_ativo for True, o laco principal continua rodando.
jogo_ativo = True

# Essa flag evita imprimir "FIM DA CORRIDA" mais de uma vez.
fim_corrida_impresso = False

# Posicao do jogador em coordenadas normalizadas do OpenGL.
pos_x_jogador = -0.15 # mudei de 0.0
pos_y_jogador = -0.75

# O jogador pode bater cinco vezes. Cada vida sera desenhada como um coracao.
vidas_jogador = 5

# Velocidades principais do jogador e da pista.
velocidade_lateral = 0.7
velocidade_jogador = 0.5
velocidade_base = 1.0
velocidade_maxima = 2.0
velocidade_minima = 0.1
aceleracao = 0.7
desaceleracao = 0.9

# tempo_colisao cria um pequeno intervalo entre batidas para nao perder varios
# coracoes no mesmo contato.
tempo_colisao = 0

# Medidas usadas para desenhar e calcular colisao dos carros.
largura_carro = 0.12
altura_carro = 0.20
margem_colisao = 0.015

# Dados do movimento visual da pista.
velocidade_pista = 0.8
velocidade_troca_faixa = 0.5
offset_faixa = 0
fase_grama = 0.0

# Quatro pistas para carros e obstaculos. Cada valor e o centro de uma pista.
faixas = [
    -0.45,
    -0.15,
     0.15,
     0.45
]

# Tres linhas separam as quatro pistas.
divisorias_faixa = [
    -0.30,
     0.00,
     0.30
]

# Dados de progresso da corrida.
distancia_percorrida = 0
comprimento_corrida = 20
distancia_visivel_chegada = 2.0
mostrar_chegada = False
largura_linha_chegada = 1.2
altura_linha_chegada = 0.16

# Listas de entidades do jogo.
inimigos = []
qtd_inimigos = 2
ultrapassagens = 0
obstaculos = []
qtd_obstaculos = 5


def init():
    # Cor de fundo caso alguma parte da tela nao seja preenchida pela pista.
    glClearColor(0.4, 0.7, 1.0, 1.0)

    # Ativa transparencia para PNGs com fundo transparente.
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def carregar_textura(caminho):
    # Abre a imagem usando Pillow.
    imagem = Image.open(caminho)

    # OpenGL e imagens comuns contam o eixo Y de formas diferentes; por isso
    # viramos a imagem para a textura aparecer na orientacao certa.
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

    # Convertemos para RGBA para manter transparencia quando existir.
    imgData = imagem.convert("RGBA").tobytes()

    # glGenTextures cria um identificador numerico para a textura.
    texId = glGenTextures(1)

    # Tudo que configurarmos agora sera aplicado nessa textura.
    glBindTexture(GL_TEXTURE_2D, texId)

    # GL_REPEAT permite repetir a textura, util para a pista infinita.
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # GL_LINEAR suaviza a textura quando ela e ampliada ou reduzida.
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Envia os pixels da imagem para a memoria da placa de video.
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        imagem.width,
        imagem.height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        imgData
    )

    # Desliga a textura atual para evitar afetar desenhos seguintes sem querer.
    glBindTexture(GL_TEXTURE_2D, 0)

    return texId


def dimensoes_obstaculo(tipo):
    # Esta funcao devolve a AREA DE COLISAO, nao o tamanho visual.
    # A hitbox e menor que a imagem para ignorar partes transparentes.
    if tipo == 0:
        return 0.08, 0.11

    # A barreira precisa ser menor para nao bloquear as quatro faixas durante o
    # sorteio de novas posicoes.
    return 0.15, 0.08


def dimensoes_visuais_obstaculo(tipo):
    # Esta funcao devolve o tamanho que sera desenhado na tela.
    # Ele pode ser maior que a colisao porque a textura tem desenho e bordas.
    if tipo == 0:
        return 0.32, 0.36 # cone esse tamanho está bom

    return 0.80, 0.56 # barreira esse tamanho está bom


def colisaoQuadradoQuadrado(x1, y1, largura1, altura1, x2, y2, largura2, altura2):
    # Esta e a mesma ideia do exemplo de colisao quadrado x quadrado.
    # A diferenca e que nossos objetos guardam a posicao pelo CENTRO.
    # Por isso, primeiro transformamos o centro no canto inferior esquerdo.

    # Canto inferior esquerdo do primeiro quadrado/quad.
    esquerda1 = x1 - largura1 / 2
    baixo1 = y1 - altura1 / 2

    # Canto inferior esquerdo do segundo quadrado/quad.
    esquerda2 = x2 - largura2 / 2
    baixo2 = y2 - altura2 / 2

    # Agora usamos a mesma logica do exemplo:
    # x < outro_x + tamanho e x + tamanho > outro_x.
    return (
        esquerda1 < esquerda2 + largura2 and
        esquerda1 + largura1 > esquerda2 and
        baixo1 < baixo2 + altura2 and
        baixo1 + altura1 > baixo2
    )


def colide_com_jogador(x, y, largura, altura):
    # Reaproveita a colisao quadrado x quadrado comparando qualquer objeto com
    # o carro controlado pelo jogador.
    return colisaoQuadradoQuadrado(
        x,
        y,
        largura,
        altura,
        pos_x_jogador,
        pos_y_jogador,
        largura_carro + margem_colisao,
        altura_carro + margem_colisao
    )


def posicaoLivre(
    x,
    y,
    largura=largura_carro,
    altura=altura_carro,
    ignorar_inimigo=None,
    ignorar_obstaculo=None,
    verificar_jogador=False
):
    # Se for pedido, tambem consideramos o jogador como barreira.
    if verificar_jogador and colide_com_jogador(x, y, largura, altura):
        return False

    # Testa a posicao contra todos os inimigos.
    for inimigo in inimigos:
        # ignorar_inimigo permite testar a proxima posicao de um inimigo sem ele
        # colidir consigo mesmo.
        if inimigo is ignorar_inimigo:
            continue

        if colisaoQuadradoQuadrado(
            x,
            y,
            largura,
            altura,
            inimigo[0],
            inimigo[1],
            largura_carro + margem_colisao,
            altura_carro + margem_colisao
        ):
            return False

    # Testa a posicao contra todos os obstaculos.
    for obstaculo in obstaculos:
        # ignorar_obstaculo tem o mesmo papel do ignorar_inimigo.
        if obstaculo is ignorar_obstaculo:
            continue

        largura_obstaculo, altura_obstaculo = dimensoes_obstaculo(obstaculo[2])

        if colisaoQuadradoQuadrado(
            x,
            y,
            largura,
            altura,
            obstaculo[0],
            obstaculo[1],
            largura_obstaculo + margem_colisao,
            altura_obstaculo + margem_colisao
        ):
            return False

    return True


def sortearPosicaoLivre(y_minimo, y_maximo, tentativas=120):
    # Tenta varias posicoes aleatorias ate encontrar uma pista e uma altura
    # livres para criar inimigo ou obstaculo.
    for _ in range(tentativas):
        x = random.choice(faixas)
        y = random.uniform(y_minimo, y_maximo)

        if posicaoLivre(x, y):
            return x, y

    # Se a tela estiver cheia, colocamos o objeto mais longe para reduzir a
    # chance de nascer sobre outro objeto.
    return random.choice(faixas), y_maximo + 0.8


def indice_faixa_mais_proxima(x):
    # Comecamos assumindo que a primeira faixa e a mais perto.
    melhor_indice = 0
    menor_distancia = abs(x - faixas[0])

    # Comparamos com as outras faixas uma por uma, de forma mais legivel.
    for indice in range(1, len(faixas)):
        distancia = abs(x - faixas[indice])

        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_indice = indice

    return melhor_indice


def faixas_vizinhas_livres(x, y, largura, altura, ignorar_inimigo=None):
    # Primeiro descobrimos em qual faixa o objeto esta.
    indice_atual = indice_faixa_mais_proxima(x)

    # Depois criamos uma lista com as faixas vizinhas possiveis.
    candidatos = []

    if indice_atual > 0:
        candidatos.append(faixas[indice_atual - 1])

    if indice_atual < len(faixas) - 1:
        candidatos.append(faixas[indice_atual + 1])

    # Embaralhar evita que todos os inimigos sempre prefiram o mesmo lado.
    random.shuffle(candidatos)

    # A primeira faixa vizinha livre vira a faixa escolhida.
    for faixa in candidatos:
        if posicaoLivre(
            faixa,
            y,
            largura,
            altura,
            ignorar_inimigo=ignorar_inimigo,
            verificar_jogador=True
        ):
            return faixa

    # None significa que nao existe desvio livre neste momento.
    return None


def criarInimigo():
    # Sorteia uma posicao inicial sem sobrepor objetos.
    x, y = sortearPosicaoLivre(1.2, 4.0)

    # Cada inimigo tem uma pequena variacao de velocidade.
    velocidade = random.uniform(velocidade_pista * 0.7, velocidade_pista * 1.3)

    # tempo_decisao controla de quanto em quanto tempo ele pensa em trocar faixa.
    tempo_decisao = random.uniform(2, 6)

    # tipo_textura alterna entre o carro vermelho e o carro de policia.
    tipo_textura = random.randint(0, 1)

    inimigos.append([
        x,               # 0 - posicao X
        y,               # 1 - posicao Y
        False,           # 2 - esta mudando de faixa?
        x,               # 3 - destino X da troca de faixa
        tempo_decisao,   # 4 - tempo ate decidir de novo
        velocidade,      # 5 - velocidade propria
        tipo_textura     # 6 - qual textura usar
    ])


def criarObstaculo():
    # Obstaculos tambem nascem em posicoes livres.
    x, y = sortearPosicaoLivre(1.2, 4.0)

    # tipo 0 e cone, tipo 1 e barreira.
    tipo = random.randint(0, 1)

    obstaculos.append([
        x,               # 0 - posicao X
        y,               # 1 - posicao Y
        tipo             # 2 - tipo visual e tipo de hitbox
    ])


def preparar_textura(textura):
    # Liga o uso de textura para o proximo desenho.
    glEnable(GL_TEXTURE_2D)

    # Escolhe qual textura sera usada.
    glBindTexture(GL_TEXTURE_2D, textura)

    # Branco preserva as cores originais da imagem.
    glColor3f(1, 1, 1)


def finalizar_textura():
    # Desvincula a textura atual.
    glBindTexture(GL_TEXTURE_2D, 0)

    # Desliga texturas para os desenhos coloridos comuns.
    glDisable(GL_TEXTURE_2D)


def desenhar_quad_texturizado(x, y, largura, altura, textura, cor_fallback):
    # Move temporariamente a origem para o centro do objeto.
    glPushMatrix()
    glTranslatef(x, y, 0)

    if textura:
        preparar_textura(textura)
    else:
        glDisable(GL_TEXTURE_2D)
        glColor3f(cor_fallback[0], cor_fallback[1], cor_fallback[2])

    # Cada glTexCoord2f informa qual ponto da imagem acompanha o vertice.
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(-largura / 2, -altura / 2)
    glTexCoord2f(1, 0)
    glVertex2f( largura / 2, -altura / 2)
    glTexCoord2f(1, 1)
    glVertex2f( largura / 2,  altura / 2)
    glTexCoord2f(0, 1)
    glVertex2f(-largura / 2,  altura / 2)
    glEnd()

    if textura:
        finalizar_textura()

    # Volta a origem para onde estava antes do glTranslatef.
    glPopMatrix()


def desenhar_retangulo_texturizado(x1, y1, x2, y2, textura, tex_y_inicio=0, tex_y_fim=1):
    # Esta funcao desenha usando coordenadas absolutas, boa para pista e chegada.
    preparar_textura(textura)

    glBegin(GL_QUADS)
    glTexCoord2f(0, tex_y_inicio)
    glVertex2f(x1, y1)
    glTexCoord2f(1, tex_y_inicio)
    glVertex2f(x2, y1)
    glTexCoord2f(1, tex_y_fim)
    glVertex2f(x2, y2)
    glTexCoord2f(0, tex_y_fim)
    glVertex2f(x1, y2)
    glEnd()

    finalizar_textura()


def desenharEstradaBase():
    # A base continua existindo para mostrar a ideia geometrica original:
    # primeiro desenhamos grama, asfalto e faixas com primitivas simples.
    altura_grama = 0.20
    inicio = -1.0 - (fase_grama % altura_grama)

    for i in range(12):
        if i % 2 == 0:
            glColor3f(0.08, 0.48, 0.08)
        else:
            glColor3f(0.18, 0.70, 0.16)

        y1 = inicio + i * altura_grama
        y2 = y1 + altura_grama

        glBegin(GL_QUADS)
        glVertex2f(-1, y1)
        glVertex2f(1, y1)
        glVertex2f(1, y2)
        glVertex2f(-1, y2)
        glEnd()

    glColor3f(0.2, 0.2, 0.2)

    glBegin(GL_QUADS)
    glVertex2f(-0.6, -1)
    glVertex2f( 0.6, -1)
    glVertex2f( 0.6,  1)
    glVertex2f(-0.6,  1)
    glEnd()

    glColor3f(1, 1, 1)

    for x in divisorias_faixa:
        y = -1 + offset_faixa

        while y < 1:
            glBegin(GL_QUADS)
            glVertex2f(x - 0.015, y)
            glVertex2f(x + 0.015, y)
            glVertex2f(x + 0.015, y + 0.12)
            glVertex2f(x - 0.015, y + 0.12)
            glEnd()

            y += 0.25


def desenharEstradaTexturizada():
    # A textura da pista cobre a tela inteira. Ela ja contem grama, asfalto e
    # faixas, seguindo o mesmo padrao da base desenhada manualmente.
    if not textura_pista:
        return

    # O offset vertical muda com a pista para dar sensacao de movimento.
    tex_y_inicio = fase_grama
    tex_y_fim = fase_grama + 1

    # A textura repete verticalmente por causa do GL_REPEAT configurado no load.
    desenhar_retangulo_texturizado(
        -1,
        -1,
        1,
        1,
        textura_pista,
        tex_y_inicio,
        tex_y_fim
    )


def desenharEstrada():
    # Mantemos a base e colocamos a textura por cima. Assim a logica original
    # continua visivel no codigo, mas o resultado final fica mais bonito.
    desenharEstradaBase()
    desenharEstradaTexturizada()


def atualizarEstrada():
    global offset_faixa

    # A pista se move mais rapido quando o jogador acelera.
    offset_faixa -= velocidade_pista * velocidade_jogador * dt

    if offset_faixa < -0.25:
        offset_faixa += 0.25


def atualizarCorrida():
    global distancia_percorrida, mostrar_chegada
    global jogo_ativo, fim_corrida_impresso

    # A distancia cresce conforme a velocidade atual do jogador.
    distancia_percorrida += velocidade_jogador * dt

    # A chegada so aparece quando esta perto o bastante para entrar na tela.
    if distancia_percorrida >= comprimento_corrida - distancia_visivel_chegada:
        mostrar_chegada = True

    # A corrida termina apenas depois que a faixa passa pelo jogador.
    if distancia_percorrida >= comprimento_corrida + 0.35 and not fim_corrida_impresso:
        print("FIM DA CORRIDA")
        fim_corrida_impresso = True
        jogo_ativo = False
            


def calcular_y_linha_chegada():
    # Quanto ainda falta para chegar no ponto final da corrida.
    distancia_ate_chegada = comprimento_corrida - distancia_percorrida

    # Quando falta distancia_visivel_chegada, a faixa aparece no topo.
    # Quando falta 0, ela esta na altura do jogador.
    proporcao_do_caminho = distancia_ate_chegada / distancia_visivel_chegada

    # Limitamos a proporcao para nao jogar a faixa longe demais na tela.
    if proporcao_do_caminho < -0.3:
        proporcao_do_caminho = -0.3

    if proporcao_do_caminho > 1:
        proporcao_do_caminho = 1

    # Interpolacao simples entre o jogador e o topo da tela.
    y_no_topo = 1.0
    y_no_jogador = pos_y_jogador
    distancia_visual = y_no_topo - y_no_jogador

    return y_no_jogador + proporcao_do_caminho * distancia_visual


def desenharLinhaChegadaBase(y_centro):
    # Base quadriculada antiga, mantida para demonstrar a construcao manual.
    colunas = 10
    linhas = 2
    largura_quadrado = largura_linha_chegada / colunas
    altura_quadrado = altura_linha_chegada / linhas
    y_inicial = y_centro - altura_linha_chegada / 2

    for linha in range(linhas):
        for coluna in range(colunas):
            if (linha + coluna) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0, 0, 0)

            x1 = -0.6 + coluna * largura_quadrado
            x2 = x1 + largura_quadrado
            y1 = y_inicial + linha * altura_quadrado
            y2 = y1 + altura_quadrado

            glBegin(GL_QUADS)
            glVertex2f(x1, y1)
            glVertex2f(x2, y1)
            glVertex2f(x2, y2)
            glVertex2f(x1, y2)
            glEnd()


def desenharLinhaChegada():
    if not mostrar_chegada:
        return

    # Calcula a altura atual da faixa de chegada.
    y_centro = calcular_y_linha_chegada()

    # Se ela ja saiu muito para baixo, nao precisa desenhar.
    if y_centro < -1.2:
        return

    # Primeiro desenhamos a versao geometrica.
    desenharLinhaChegadaBase(y_centro)

    # Depois colocamos a textura por cima, no mesmo retangulo.
    if textura_linha_chegada:
        desenhar_retangulo_texturizado(
            -0.6,
            y_centro - altura_linha_chegada / 2,
            0.6,
            y_centro + altura_linha_chegada / 2,
            textura_linha_chegada
        )


def atualizarGrama():
    global fase_grama

    # A mesma fase que animava a grama agora tambem anima a textura da pista.
    fase_grama += velocidade_jogador * dt * 0.9


def aplicarColisao():
    global velocidade_jogador, tempo_colisao
    global vidas_jogador, jogo_ativo

    # Se ainda estamos no intervalo de protecao, ignoramos nova colisao.
    if tempo_colisao > 0:
        return

    # A batida reduz a velocidade pela metade.
    velocidade_jogador = max(velocidade_minima, velocidade_jogador / 2)

    # Cada batida remove um coracao.
    vidas_jogador -= 1

    # O cooldown impede perder varias vidas no mesmo contato.
    tempo_colisao = 1.0

    if vidas_jogador <= 0:
        print("GAME OVER")
        jogo_ativo = False


def atualizar_tempo_colisao():
    global tempo_colisao

    # O cooldown diminui com o tempo ate chegar a zero.
    if tempo_colisao > 0:
        tempo_colisao -= dt


def resolver_barreira_jogador(x, y, largura, altura):
    # Se um objeto bate no jogador, ele para antes de atravessar o carro.
    if colide_com_jogador(x, y, largura, altura):
        aplicarColisao()
        y = pos_y_jogador + (altura + altura_carro) / 2 + margem_colisao

    return y


def atualizarInimigos():
    global ultrapassagens

    for inimigo in inimigos:
        x = inimigo[0]
        y = inimigo[1]
        mudando = inimigo[2]
        destino = inimigo[3]
        tempo_decisao = inimigo[4]
        velocidade = inimigo[5]

        # Reduz o tempo ate a proxima decisao de troca de faixa.
        tempo_decisao -= dt

        if not mudando and tempo_decisao <= 0:
            tempo_decisao = random.uniform(2, 6)

            if random.random() < 0.20:
                faixa_livre = faixas_vizinhas_livres(
                    x,
                    y,
                    largura_carro,
                    altura_carro,
                    ignorar_inimigo=inimigo
                )

                if faixa_livre is not None:
                    destino = faixa_livre
                    mudando = True

        # Comecamos a nova posicao lateral igual a atual.
        novo_x = x

        # Se estiver mudando de faixa, aproximamos o X do destino aos poucos.
        if mudando:
            if destino > x:
                novo_x = min(destino, x + velocidade_troca_faixa * dt)
            elif destino < x:
                novo_x = max(destino, x - velocidade_troca_faixa * dt)

            if abs(destino - novo_x) < 0.02:
                novo_x = destino
                mudando = False

        # Movimento vertical: inimigos descem em direcao ao jogador.
        novo_y = y - velocidade * velocidade_jogador * dt

        # Se bater no jogador, para antes de atravessar.
        novo_y = resolver_barreira_jogador(
            novo_x,
            novo_y,
            largura_carro,
            altura_carro
        )

        # Antes de aceitar a nova posicao, verificamos se ela esta livre.
        if not posicaoLivre(
            novo_x,
            novo_y,
            largura_carro,
            altura_carro,
            ignorar_inimigo=inimigo,
            verificar_jogador=True
        ):
            faixa_livre = faixas_vizinhas_livres(
                x,
                y,
                largura_carro,
                altura_carro,
                ignorar_inimigo=inimigo
            )

            if faixa_livre is not None:
                destino = faixa_livre
                mudando = True

            # Se nao existe caminho livre neste frame, o inimigo fica parado.
            novo_x = x
            novo_y = y

        # Quando sai da tela, o inimigo volta para cima em posicao livre.
        if novo_y < -1.3:
            ultrapassagens += 1
            novo_x, novo_y = sortearPosicaoLivre(1.5, 4.0)
            mudando = False
            destino = novo_x
            tempo_decisao = random.uniform(2, 6)
            velocidade = random.uniform(
                velocidade_pista * 0.7,
                velocidade_pista * 1.3
            )
            inimigo[6] = random.randint(0, 1)

        inimigo[0] = novo_x
        inimigo[1] = novo_y
        inimigo[2] = mudando
        inimigo[3] = destino
        inimigo[4] = tempo_decisao
        inimigo[5] = velocidade


def atualizarObstaculos():
    for obstaculo in obstaculos:
        largura, altura = dimensoes_obstaculo(obstaculo[2])

        # Obstaculos descem conforme a velocidade do jogador.
        novo_y = obstaculo[1] - velocidade_jogador * dt

        # Obstaculo tambem nao atravessa o jogador.
        novo_y = resolver_barreira_jogador(obstaculo[0], novo_y, largura, altura)

        if posicaoLivre(
            obstaculo[0],
            novo_y,
            largura,
            altura,
            ignorar_obstaculo=obstaculo,
            verificar_jogador=True
        ):
            obstaculo[1] = novo_y

        # Saiu da tela: volta para cima.
        if obstaculo[1] < -2.0:
            x, y = sortearPosicaoLivre(1.2, 4.0)
            obstaculo[0] = x
            obstaculo[1] = y
            obstaculo[2] = random.randint(0, 1)


def entrada(window):
    global pos_x_jogador, velocidade_jogador

    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        velocidade_jogador += aceleracao * dt
    else:
        if velocidade_jogador > velocidade_base:
            velocidade_jogador -= desaceleracao * dt
        elif velocidade_jogador < velocidade_base:
            velocidade_jogador += (desaceleracao * 0.35) * dt

    # Mantem a velocidade dentro dos limites sem esconder a logica em uma funcao.
    if velocidade_jogador < velocidade_minima:
        velocidade_jogador = velocidade_minima

    if velocidade_jogador > velocidade_maxima:
        velocidade_jogador = velocidade_maxima

    novo_x = pos_x_jogador

    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        novo_x -= velocidade_lateral * dt

    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        novo_x += velocidade_lateral * dt

    # Limites laterais da pista.
    if novo_x < -0.52:
        novo_x = -0.52

    if novo_x > 0.52:
        novo_x = 0.52

    # O jogador so muda para a nova posicao se ela nao estiver ocupada.
    if posicaoLivre(
        novo_x,
        pos_y_jogador,
        largura_carro,
        altura_carro,
        verificar_jogador=False
    ):
        pos_x_jogador = novo_x
    elif abs(novo_x - pos_x_jogador) > 0.001:
        aplicarColisao()


def verificarColisoesJogador():
    # Confere se algum inimigo ficou encostado no jogador.
    for inimigo in inimigos:
        if colide_com_jogador(
            inimigo[0],
            inimigo[1],
            largura_carro,
            altura_carro
        ):
            aplicarColisao()
            inimigo[1] = pos_y_jogador + altura_carro + margem_colisao
            return

    # Confere se algum obstaculo ficou encostado no jogador.
    for obstaculo in obstaculos:
        largura, altura = dimensoes_obstaculo(obstaculo[2])

        if colide_com_jogador(obstaculo[0], obstaculo[1], largura, altura):
            aplicarColisao()
            obstaculo[1] = pos_y_jogador + (altura + altura_carro) / 2 + margem_colisao
            return


def desenharCarro(x, y, textura, cor_fallback):
    desenhar_quad_texturizado(
        x,
        y,
        largura_carro,
        altura_carro,
        textura,
        cor_fallback
    )


def desenharObstaculo(x, y, tipo):
    largura, altura = dimensoes_visuais_obstaculo(tipo)

    if tipo == 0:
        textura = textura_cone
    else:
        textura = textura_barreira

    desenhar_quad_texturizado(
        x,
        y,
        largura,
        altura,
        textura,
        (1.0, 0.86, 0.05)
    )


def desenharVidas():
    # Os coracoes ficam no canto superior esquerdo como limite de batidas.
    for i in range(vidas_jogador):
        desenhar_quad_texturizado(
            -0.92 + i * 0.09,
            0.90,
            0.07,
            0.07,
            textura_coracao,
            (1, 0, 0)
        )


def render():
    # Primeiro vem o cenario.
    desenharEstrada()
    desenharLinhaChegada()

    # Depois os obstaculos, inimigos, jogador e interface.
    for obstaculo in obstaculos:
        desenharObstaculo(obstaculo[0], obstaculo[1], obstaculo[2])

    for inimigo in inimigos:
        textura = textura_inimigo1 if inimigo[6] == 0 else textura_inimigo2
        desenharCarro(inimigo[0], inimigo[1], textura, (1, 0, 0))

    desenharCarro(pos_x_jogador, pos_y_jogador, textura_jogador, (0, 0, 1))
    desenharVidas()


def carregar_texturas():
    global textura_jogador, textura_coracao
    global textura_inimigo1, textura_inimigo2
    global textura_cone, textura_barreira
    global textura_pista, textura_linha_chegada

    textura_jogador = carregar_textura("texturas/carroVerde1.png")
    textura_coracao = carregar_textura("texturas/coracaoCheio.png")
    textura_inimigo1 = carregar_textura("texturas/carroVermelho1.png")
    textura_inimigo2 = carregar_textura("texturas/carroPolicia1.png")
    textura_barreira = carregar_textura("texturas/barreiraAmarela.png")
    textura_cone = carregar_textura("texturas/cone.png")
    textura_linha_chegada = carregar_textura("texturas/linhaChegada.jpg")

    # A pista pode nascer com textura de grama ou deserto para variar o cenario.
    if random.randint(0, 1) == 0:
        textura_pista = carregar_textura("texturas/asfalto_com_grama_4_pistas.png")
    else:
        textura_pista = carregar_textura("texturas/asfalto_deserto_4_pistas.png")


def main():
    global dt

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Mini Enduro", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    init()
    carregar_texturas()

    for _ in range(qtd_inimigos):
        criarInimigo()

    for _ in range(qtd_obstaculos):
        criarObstaculo()

    tempo_anterior = glfw.get_time()

    print("\nPara jogar Utilize as Setas do seu Teclado")
    print("Movimento horizontal: Seta para Direita, Seta para Esquerda")
    print("Aceleração: Seta para Cima, Desaceleração: Seta para Baixo\n")
    
    

    while (
        not glfw.window_should_close(window)
        and jogo_ativo
    ):
        glClear(GL_COLOR_BUFFER_BIT)

        tempo_atual = glfw.get_time()
        dt = tempo_atual - tempo_anterior
        tempo_anterior = tempo_atual

        glfw.poll_events()

        entrada(window)
        atualizar_tempo_colisao()
        atualizarEstrada()
        atualizarGrama()
        atualizarCorrida()
        atualizarObstaculos()
        atualizarInimigos()
        verificarColisoesJogador()
        render()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
