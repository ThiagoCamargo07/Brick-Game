import pygame

# Inicializar
pygame.init()

tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")

tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)
tamanho_jogador = 120
jogador = pygame.Rect(0, 750, tamanho_jogador, 15)

qtde_blocos_linhas = 8
qtde_linhas_blocos = 5
qtde_total_blocos = qtde_blocos_linhas * qtde_linhas_blocos

def criar_blocos(qtde_blocos_linhas, qtde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / 8 - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10
    
    blocos = []
    # Criar os blocos
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linhas):
            # Criar o bloco
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco, altura_bloco)
            # Adicionar o bloco na lista de blocos 
            blocos.append(bloco)
    return blocos

cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0)
}

fim_jogo = False
pontuacao = 0
movimento_bola = [7, -7]
bola_em_movimento = False  # Flag para verificar se a bola foi movida pela barra
pontuacao_na_vez = False  # Flag para garantir que só contamos uma pontuação por vez

# Desenhar as coisas na tela 
def desenhar_inicio_jogo():
    tela.fill(cores["preta"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)

# Criar as funções do jogo
def movimentar_jogador(evento):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_RIGHT:
            if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
                jogador.x += 10  # Aumentar a velocidade da barra
        if evento.key == pygame.K_LEFT:
            if jogador.x > 0:
                jogador.x -= 10  # Aumentar a velocidade da barra

def movimentar_bola(bola, blocos):
    global pontuacao, bola_em_movimento, pontuacao_na_vez
    movimento = movimento_bola
    bola.x += movimento[0]
    bola.y += movimento[1]
    
    # Verificar colisões com as bordas
    if bola.x <= 0 or bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = -movimento[0]
    if bola.y <= 0:
        movimento[1] = -movimento[1]
    
    # Verificar colisão com o jogador (barra)
    if jogador.colliderect(bola):
        movimento[1] = -movimento[1]
        bola_em_movimento = True  # Agora a bola estará em movimento após a colisão com a barra

    # Verificar colisão com os blocos (alvo)
    for bloco in blocos[:]:
        if bloco.colliderect(bola) and bola_em_movimento and not pontuacao_na_vez:
            blocos.remove(bloco)
            movimento[1] = -movimento[1]
            pontuacao += 1  # Pontuação só conta se a bola passar pela barra primeiro
            pontuacao_na_vez = True  # A pontuação foi contada para esta vez, não contar novamente até a próxima vez
            break  # Para evitar múltiplas colisões no mesmo quadro

    # A bola pode tocar o chão, mas não reiniciar ou terminar o jogo
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        bola.y = tamanho_tela[1] - tamanho_bola  # Coloca a bola no chão, sem reiniciar
        movimento[1] = -movimento[1]  # Faz a bola quicar para cima

    return movimento

def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", 1, cores["amarela"])
    tela.blit(texto, (0, 780))

    # Verificar se venceu
    return pontuacao >= qtde_total_blocos

blocos = criar_blocos(qtde_blocos_linhas, qtde_linhas_blocos)

# Loop principal
while not fim_jogo:
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)

    # Atualiza a pontuação
    fim_jogo = atualizar_pontuacao(pontuacao)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True
        movimentar_jogador(evento)

    # Chama a função movimentar_bola
    movimento_bola = movimentar_bola(bola, blocos)

    # Se a bola não está mais em movimento ou foi tocada, resetar a flag para a próxima rodada
    if bola_em_movimento and pontuacao_na_vez:
        pontuacao_na_vez = False  # Preparar para a próxima rodada de colisões

    pygame.display.flip()

    pygame.time.wait(1)

# Finaliza o Pygame
pygame.quit()
