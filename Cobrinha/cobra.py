import pygame
import random
import time

# --- 1. Configurações Iniciais ---
pygame.init()

# Define as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (50, 153, 213)

# Define as dimensões da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo da Cobrinha")

# Define o tamanho dos blocos
tamanho_bloco = 20

# Define a velocidade do jogo
relogio = pygame.time.Clock()
velocidade_cobra = 15

# --- 2. Funções do Jogo ---
def desenhar_cobra(tamanho_bloco, lista_cobra):
    """Desenha cada bloco da cobra na tela."""
    for x in lista_cobra:
        pygame.draw.rect(tela, VERDE, [x[0], x[1], tamanho_bloco, tamanho_bloco])

def mostrar_pontuacao(pontuacao):
    """Exibe a pontuação atual na tela."""
    fonte = pygame.font.SysFont("Arial", 35)
    texto = fonte.render("Pontos: " + str(pontuacao), True, BRANCO)
    tela.blit(texto, [10, 10])

def mensagem_final(msg, cor):
    """Exibe uma mensagem na tela, como 'Game Over'."""
    fonte = pygame.font.SysFont("Arial", 50)
    texto = fonte.render(msg, True, cor)
    texto_rect = texto.get_rect(center=(largura_tela // 2, altura_tela // 2))
    tela.blit(texto, texto_rect)

# --- 3. Loop Principal do Jogo ---
def loop_jogo():
    """Contém toda a lógica do jogo."""
    jogo_acabou = False
    perdeu_o_jogo = False

    # Posição inicial da cobra
    pos_x = largura_tela / 2
    pos_y = altura_tela / 2

    # Mudança de posição (velocidade)
    muda_x = 0
    muda_y = 0

    # Corpo da cobra
    lista_cobra = []
    tamanho_cobra = 1

    # Posição inicial da comida
    comida_x = round(random.randrange(0, largura_tela - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
    comida_y = round(random.randrange(0, altura_tela - tamanho_bloco) / tamanho_bloco) * tamanho_bloco

    while not jogo_acabou:
        while perdeu_o_jogo:
            tela.fill(PRETO)
            mensagem_final("Você Perdeu! Pontos: " + str(tamanho_cobra - 1), VERMELHO)
            
            # Mensagem de instruções para jogar novamente ou sair
            fonte_pequena = pygame.font.SysFont("Arial", 25)
            texto_instrucao = fonte_pequena.render("Pressione 'C' para Jogar de Novo ou 'Q' para Sair", True, BRANCO)
            texto_rect = texto_instrucao.get_rect(center=(largura_tela // 2, altura_tela // 2 + 50))
            tela.blit(texto_instrucao, texto_rect)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        jogo_acabou = True
                        perdeu_o_jogo = False
                    if event.key == pygame.K_c:
                        loop_jogo() # Reinicia o jogo
                if event.type == pygame.QUIT:
                    jogo_acabou = True
                    perdeu_o_jogo = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogo_acabou = True
            
            # Movimento da cobra
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and muda_x == 0:
                    muda_x = -tamanho_bloco
                    muda_y = 0
                elif event.key == pygame.K_RIGHT and muda_x == 0:
                    muda_x = tamanho_bloco
                    muda_y = 0
                elif event.key == pygame.K_UP and muda_y == 0:
                    muda_y = -tamanho_bloco
                    muda_x = 0
                elif event.key == pygame.K_DOWN and muda_y == 0:
                    muda_y = tamanho_bloco
                    muda_x = 0

        # Verifica se a cobra bateu nas bordas
        if pos_x >= largura_tela or pos_x < 0 or pos_y >= altura_tela or pos_y < 0:
            perdeu_o_jogo = True

        # Atualiza a posição da cobra
        pos_x += muda_x
        pos_y += muda_y
        
        # Limpa a tela
        tela.fill(PRETO)
        
        # Desenha a comida
        pygame.draw.rect(tela, VERMELHO, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])
        
        # Adiciona a cabeça da cobra à lista
        cabeca_cobra = []
        cabeca_cobra.append(pos_x)
        cabeca_cobra.append(pos_y)
        lista_cobra.append(cabeca_cobra)

        # Mantém o tamanho da cobra
        if len(lista_cobra) > tamanho_cobra:
            del lista_cobra[0]

        # Verifica se a cobra bateu no próprio corpo
        for x in lista_cobra[:-1]:
            if x == cabeca_cobra:
                perdeu_o_jogo = True

        desenhar_cobra(tamanho_bloco, lista_cobra)
        mostrar_pontuacao(tamanho_cobra - 1)

        pygame.display.update()

        # Verifica se a cobra comeu a comida
        if pos_x == comida_x and pos_y == comida_y:
            comida_x = round(random.randrange(0, largura_tela - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
            comida_y = round(random.randrange(0, altura_tela - tamanho_bloco) / tamanho_bloco) * tamanho_bloco
            tamanho_cobra += 1

        relogio.tick(velocidade_cobra)

    pygame.quit()
    quit()

# --- 4. Inicia o Jogo ---
loop_jogo()