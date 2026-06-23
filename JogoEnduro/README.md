### Apresentação

Projeto avaliativo destinado a disciplina de Computação Gráfica do Instituto Federal Catarinense Campus Videira --- IFC Videira.

O projeto consistiu dos alunos escolherem um jogo, animação, etc. Utilizando um ambiente 2D, 2.5, 3D ou qualquer outro que fosse implementado utilizando as bibliotecas e técnicas aprendidas em sala de aula, como OpenGL, GLFW ou GLUT.


### Sobre o jogo TopGEz

Este projeto é uma recriação simples inspirada em jogos como Enduro, Top Gear e Out Run.

A ideia principal não foi criar um jogo 3D ou 2.5D. O jogo usa uma visão 2D com uma vista aérea, pista reta de quatro faixas para o jogador, inimigos e obstáculos. A movimentação do jogador é de maneira horizontal.

Foi utilizado texturas gratuítas e modificadas a mão para melhorar a apresentação visual.

## Objetivo do jogo

O jogador controla um carro verde e precisa chegar ao final da corrida, atravessando a faixa quadriculada, desviando de carros vermelhos, carros policiais e obstáculos.

Quando o jogador ultrapassa a linha de chegada, o jogo imprime `FIM DA CORRIDA`.

O jogador começa a partida com 5 vidas, representadas pelos corações vermelhos no canto superior esquerdo da tela. Após cada batida, seja nos obstáculos ou carros inimigos, perde 1 de vida / coração. Quando não restar mais nenhum coração, o jogo termina, imprimindo `GAME OVER` no terminal. Caso fique por um tempo determinado atrás de obstáculos ou inimigos, a quantidade de corações continuará decrescendo. Então, sempre desvie deles quando for possível.

Durante a corrida aparecem:

- inimigos --- carros vermelhos e carros policiais;
- cones;
- barreiras;
- pista texturizada --- altera entre pista com grama e pista com deserto;
- linha de chegada;
- corações que representam as vidas do jogador.


## Tecnologias usadas

- Editor Visual Studio Code
- Python
- Ambiente Virtual Python
- GLFW
- PyOpenGL
- Pillow, para carregar imagens e transformá-las em texturas
- Random, para a geração de números aleatórios

## Como jogar

Use as setas do teclado:

- Seta para esquerda: move o carro para a esquerda
- Seta para direita: move o carro para a direita
- Seta para cima: acelera o carro e faz a pista vir mais rapido
- Seta para baixo: desacelera o carro. Porém não para completamente.

## Ambiente do jogo

A pista possui quatro pistas. Eles são representados por quatro posições centrais no eixo X.

As texturas da pista ficam na pasta `texturas`:

- `asfalto_com_grama_4_pistas.png`
- `asfalto_deserto_4_pistas.png`

Ao iniciar o jogo, uma dessas pistas é escolhida aleatoriamente. A textura se repete verticalmente para criar a sensação de movimento contínuo.

## Texturas

O jogo usa imagens para representar os principais elementos:

- jogador: `carroVerde1.png`
- inimigos: `carroVermelho1.png` e `carroPolicia1.png`
- cone: `cone.png`
- barreira: `barreiraAmarela.png`
- coração: `coracaoCheio.png`
- linha de chegada: `linhaChegada.jpg`

As texturas sao aplicadas com `glTexCoord2f(...)` antes dos vértices desenhados com `glVertex2f(...)`.

## Colisão

A colisão foi implementada como quadrado x quadrado, seguindo a mesma ideia dos exemplos vistos em aula.

Mesmo quando o objeto visual tem formato diferente por causa da textura, a colisão usa uma área simples baseada em `GL_QUADS`.

O código usa:

- largura;
- altura;
- posição X;
- posição Y.

Assim, inimigos, obstáculos e jogador não atravessam uns aos outros. Uma função calcula a posição livre na pista para que seja gerado adequadamente, sem um objeto ocupar a mesma posição que outro. Carros inimigos, tentam desviar dos obstáculos assim como o jogador.

## Etapas de desenvolvimento

1. Criação da janela com GLFW.
2. Definição das variáveis globais do jogo.
3. Desenho inicial da pista com primitivas simples.
4. Criação das quatro faixas da pista.
5. Adição do carro do jogador.
6. Adição dos carros inimigos.
7. Adição dos obstáculos.
8. Implementação do movimento da pista.
9. Implementação da colisão quadrado x quadrado.
10. Criação das vidas do jogador baseada em corações.
11. Aplicação de texturas nos carros, obstáculos, pista e chegada.
12. Implementação da linha de chegada se movendo até o jogador ultrapassar.
13. Ajustes adequados nos tamanhos dos objetos.
14. Comentários extras no código para melhores explicações.

## Organização do código

O arquivo principal do jogo é `Enduro.py`.

Algumas funcoes importantes:

- `carregar_textura`: carrega uma imagem e cria uma textura no OpenGL.
- `desenhar_quad_texturizado`: desenha um quadrado com textura.
- `desenharEstrada`: desenha a estrada base e aplica a textura da pista.
- `desenharLinhaChegada`: desenha a chegada e sua textura.
- `colisaoQuadradoQuadrado`: verifica colisão entre dois objetos desenhados como `GL_QUADS`.
- `posicaoLivre`: verifica se um inimigo ou obstáculo pode ocupar uma posição.
- `atualizarInimigos`: movimenta os inimigos e tenta desviar quando necessário.
- `atualizarObstaculos`: movimenta os obstáculos.
- `entrada`: lê os comandos do teclado.
- `render`: organiza a ordem de desenho na tela.

## Observações

A escolha do nome ocorreu da junção dos termos Top Gear, Enduro e criatividade.