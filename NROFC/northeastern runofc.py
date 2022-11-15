# Importando pygame, time e random
import pygame
import time
import random
import sys

# Iniciando pygame e declarando variáveis
pygame.init()
colorg = (119, 118, 110)
gray = (87,87,87)
brown = (235,118,0)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (30, 144, 255)
orange = (255, 128, 0)
bright_orange = (255, 188, 64)
bright_red = (255, 105, 97)
bright_green = (178, 255, 102)
bright_blue = (135,206,250)
yellowtxt = (255, 255, 0)
w = 800
h = 600
nickname = ""
recordes = []
player = ""

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Northeastern Run")
clock = pygame.time.Clock()

#variáveis de manipulação de arquivo
arqRecorde = open("recorde.txt", "r")
ultimoRecorde = arqRecorde.read()
arqRecorde.close()

# Importando imagens
car1 = pygame.image.load("car1.png")
terra = pygame.image.load("terra.png")
terra1 = pygame.image.load("terra1.png")
terrac = pygame.image.load("terrac.png")
terra1c = pygame.image.load("terra1c.png")
mato = pygame.image.load("mato.png")
marca = pygame.image.load("marca.png")
listra = pygame.image.load("listra.png")
listra2 = pygame.image.load("listra2.png")
fio = pygame.image.load("fio.png")
tela_menu = pygame.image.load("telamenu.png")
instrucoes = pygame.image.load("instruções.png")
dados = pygame.image.load("dados.png")
ranking = pygame.image.load("ranking.png")
sobre = pygame.image.load("sobre.png")
selecao = pygame.image.load("selecao.png")
pausado = pygame.image.load("pause.png")
burro1 = pygame.image.load("burro1r.png")
burro2 = pygame.image.load("burro2r.png")
burroImage = burro1
burroCurrentImage = 1
car_w = 56
pause = False
tick = 0

# Música menu
def musictheme():
    pygame.mixer.music.load("asabranca.mp3")
    pygame.mixer.music.play(-1)
# Efeito sonoro de Clique dos botões   
def musiclick():
    sound=pygame.mixer.Sound("stapling.wav")
    pygame.mixer.Channel(0).play(sound)
# Efeito sonoro de Falha
def fail():
    pygame.mixer.music.load("fail.wav")
    pygame.mixer.music.play()

"""" 
Carrega os valores contidos no arquivo ranking.txt na lista recordes
no formato [["nome", "pontuacao"], ["nome2", "pontuacao2"], [...], ...]
"""
def loadRecordes():
    # Abrindo arquivo
    arqRanking = open("ranking.txt", "r")

    # Pegando cada linha do arquivo
    dados = arqRanking.readlines()

    # Fechando o arquivo
    arqRanking.close()

    # Lista que armazena recordes
    global recordes

    # Limpa lista
    recordes = []

    for i in dados:
        # Retira \n do fim da linha - resulta em "nome;pontuacao"
        recorde = i.rstrip('\n')

        # Separa a string pelo ; como lista e adiona na lista de recordes - resulta em ["nome", "pontuacao"]
        recordes.append(recorde.split(";"))


"""" 
Converte os valores contidos na lista recordes no formato ["nome;pontuacao\n", "nome2;pontuacao2\n", ...]
escreve os valores convertidos no arquivo ranking.txt
"""
def persistRecordes():
    dados = []
    for indice, i in enumerate(recordes):
        # Verifica se nao esta no ultimo laco
        if indice != 4:
            # Converte a lista ["nome", "pontuacao"] em string com ; entre os indices - "nome;pontuacao"
            # concatena \n no fim da string - "nome;pontuacao\n"
            dados.append(";".join([i[0], str(i[1])]) + "\n")
        else:
            # Faz a mesma coisa que o if exceto pela concatenacao do \n
            dados.append(";".join([i[0], str(i[1])]))

    # Abrindo arquivo
    arqRanking = open("ranking.txt", "w")

    # Escrevendo no arquivo
    arqRanking.writelines(dados)

    # Fechando o arquivo
    arqRanking.close()

def zerar():
    data = ["-;0\n"] * 5
    # Abrindo arquivo
    arqRanking = open("ranking.txt", "w")
    # Escrevendo no arquivo
    arqRanking.writelines(data)
    # Fechando o arquivo
    arqRanking.close()
    # Abrindo arquivo
    arqRecorde = open('recorde.txt', 'w')
    # Escrevendo no arquivo
    arqRecorde.write(("0"))
    # Fechando o arquivo
    arqRecorde.close()
    atualizaUltRecorde()
    screen_ranking()
    
# Função menu
def menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        screen.blit(tela_menu, (0, 0))
        button("Jogar", 150, 520, 100, 50, green, bright_green, "play")
        button("Sair", 550, 520, 100, 50, red, bright_red, "quit")
        button("Instruções", 300, 520, 200, 50, blue, bright_blue, "intro")
        button("Ranking", 300, 0, 200, 50, orange, bright_orange, "ranking")
        pygame.display.update()
        clock.tick(50)


# Função pause(burro)
def pausedb():
    pygame.mixer.music.pause()
    global pause

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    musiclick()
                    pygame.mixer.music.unpause()
                    unpaused()
        screen.blit(pausado, (0, 0))
        button("Continue", 150, 450, 150, 50, green, bright_green, "unpause")
        button("Restart", 350, 450, 150, 50, blue, bright_blue, "playb")
        button("Menu Principal", 550, 450, 200, 50, red, bright_red, "menu1")
        pygame.display.update()
        clock.tick(30)

    # Função botões


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                musiclick()
                screenselect()
            elif action == "ranking":
                musiclick()
                screen_ranking()
            elif action == "playc":
                musiclick()
                contagem()
            elif action == "playb":
                musiclick()
                contagemb()
            elif action == "quit":
                musiclick()
                pygame.quit()
                quit()
                sys.exit()
            elif action == "intro":
                musiclick()
                introduction()
            elif action == "menu":
                musiclick()
                menu()
            elif action == "menu1":
                musiclick()
                musictheme()
                menu()
            elif action == "about":
                musiclick()
                sobreinfo()
            elif action == "pause":
                musiclick()
                paused()
            elif action == "pauseb":
                musiclick()
                pausedb()
            elif action == "unpause":
                musiclick()
                unpaused()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textsurf, textrect)


# Função instruções
def introduction():
    introduction = True
    while introduction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
               if event.key==pygame.K_ESCAPE:
                   musiclick()
                   menu()
        screen.blit(instrucoes, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 80)
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        mediumtext = pygame.font.Font('freesansbold.ttf', 40)
        stextSurf, stextRect = text_objects("SETA ESQUERDA : Vira à esquerda", smalltext)
        stextRect.center = ((380), (400))
        hTextSurf, hTextRect = text_objects("SETA DIREITA : Vira à direita", smalltext)
        hTextRect.center = ((380), (450))
        atextSurf, atextRect = text_objects("Z : Acelera", smalltext)
        atextRect.center = ((380), (500))
        rtextSurf, rtextRect = text_objects("X : Desacelera ", smalltext)
        rtextRect.center = ((380), (550))
        ptextSurf, ptextRect = text_objects("P : Pause  ", smalltext)
        ptextRect.center = ((380), (350))
        screen.blit(stextSurf, stextRect)
        screen.blit(hTextSurf, hTextRect)
        screen.blit(atextSurf, atextRect)
        screen.blit(rtextSurf, rtextRect)
        screen.blit(ptextSurf, ptextRect)
        button("Voltar", 600, 450, 100, 50, blue, bright_blue, "menu")
        button("Sobre", 100, 450, 100, 50, green, bright_green, "about")
        pygame.display.update()
        clock.tick(30)


# Função pause
def paused():
    pygame.mixer.music.pause()
    global pause

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    musiclick()
                    pygame.mixer.music.unpause()
                    unpaused()
        screen.blit(pausado, (0, 0))
        button("Continue", 150, 450, 150, 50, green, bright_green, "unpause")
        button("Restart", 350, 450, 150, 50, blue, bright_blue, "playc")
        button("Menu Principal", 550, 450, 200, 50, red, bright_red, "menu1")
        pygame.display.update()
        clock.tick(30)

# Função despause
def unpaused():
    global pause
    pause = False
    


# Função de tela de contagem
def contagem_tela():
    font = pygame.font.SysFont(None, 30)
    x = (w * 0.47)
    y = (h * 0.8)
    screen.blit(terra, (0, 0))
    screen.blit(terra, (0, 200))
    screen.blit(terra, (0, 400))
    screen.blit(terra1, (700, 0))
    screen.blit(terra1, (700, 200))
    screen.blit(terra1, (700, 400))
    screen.blit(listra, (380, 100))
    screen.blit(listra, (380, 200))
    screen.blit(listra, (380, 300))
    screen.blit(listra, (380, 400))
    screen.blit(listra, (380, 100))
    screen.blit(listra, (380, 500))
    screen.blit(listra, (380, 0))
    screen.blit(listra, (380, 600))
    screen.blit(fio, (120, 200))
    screen.blit(fio, (120, 0))
    screen.blit(fio, (120, 100))
    screen.blit(fio, (680, 100))
    screen.blit(fio, (680, 0))
    screen.blit(fio, (680, 200))
    screen.blit(car1, (x, y))
    textRecord = font.render((" Recorde: " + str(ultimoRecorde)), False, yellowtxt)
    text = font.render(" Desviou: 0", False, yellowtxt)
    score = font.render(" Pontos: 0", False, yellowtxt)
    screen.blit(textRecord, (0, 70))
    screen.blit(text, (0, 50))
    screen.blit(score, (0, 30))
    button("Pause", 650, 0, 150, 50, blue, bright_blue, "pause")


# Função de contagem do carro
def contagem():
    pygame.mixer.music.stop()
    countdown = True
    pygame.mixer.music.load("CR.mp3")
    pygame.mixer.music.play()
    while countdown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        screen.fill(colorg)
        contagem_tela()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("3", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen.fill(colorg)
        contagem_tela()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("2", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen.fill(colorg)
        contagem_tela()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("1", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen.fill(colorg)
        contagem_tela()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("RAI!!!", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen.fill(colorg)
        contagem_tela()
        largetext = pygame.font.Font('freesansbold.ttf', 70)
        TextSurf, TextRect = text_objects("LEVEL 1", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen_loop()


# Função de tela de contagem burro
def contagem_telab():
    font = pygame.font.SysFont(None, 30)
    x = (w * 0.47)
    y = (h * 0.8)
    screen.blit(terra, (0, 0))
    screen.blit(terra, (0, 200))
    screen.blit(terra, (0, 400))
    screen.blit(terra1, (700, 0))
    screen.blit(terra1, (700, 200))
    screen.blit(terra1, (700, 400))
    screen.blit(listra2, (380, 100))
    screen.blit(listra2, (380, 200))
    screen.blit(listra2, (380, 300))
    screen.blit(listra2, (380, 400))
    screen.blit(listra2, (380, 100))
    screen.blit(listra2, (380, 500))
    screen.blit(listra2, (380, 0))
    screen.blit(listra2, (380, 600))
    screen.blit(fio, (120, 200))
    screen.blit(fio, (120, 0))
    screen.blit(fio, (120, 100))
    screen.blit(fio, (680, 100))
    screen.blit(fio, (680, 0))
    screen.blit(fio, (680, 200))
    screen.blit(burro1, (x, y))
    textRecord = font.render((" Recorde: " + str(ultimoRecorde)), False, yellowtxt)
    text = font.render(" Desviou: 0", False, yellowtxt)
    score = font.render(" Pontos: 0", False, yellowtxt)
    screen.blit(textRecord, (0, 70))
    screen.blit(text, (0, 50))
    screen.blit(score, (0, 30))
    button("Pause", 650, 0, 150, 50, blue, bright_blue, "pause")


# Função de contagem do burro
def contagemb():
    pygame.mixer.music.stop()
    countdown = True
    pygame.mixer.music.load("CR.mp3")
    pygame.mixer.music.play()
    while countdown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        screen.fill(gray)
        contagem_telab()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("3", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen.fill(gray)
        contagem_telab()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("2", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen.fill(gray)
        contagem_telab()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("1", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen.fill(gray)
        contagem_telab()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("RAI!!!", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen.fill(gray)
        contagem_telab()
        largetext = pygame.font.Font('freesansbold.ttf', 70)
        TextSurf, TextRect = text_objects("LEVEL 1", largetext)
        TextRect.center = ((w / 2), (h / 2))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        screen_loop_donkey()

# Função de efeito sonoro partida
def music():
    pygame.mixer.music.load("frevom.mp3")
    pygame.mixer.music.play(-1)
    
#Função de efeito sonoro level
def scream():
    sound2=pygame.mixer.Sound("grito.wav")
    pygame.mixer.Channel(0).play(sound2)


# Função dos obstáculos
def obstacle(obs_startx, obs_starty, obs):
    if obs == 0:
        obsimg = pygame.image.load("car2.png")
    elif obs == 1:
        obsimg = pygame.image.load("car3.png")
    elif obs == 2:
        obsimg = pygame.image.load("car4.png")
    elif obs == 3:
        obsimg = pygame.image.load("car5.png")
    elif obs == 4:
        obsimg = pygame.image.load("car6.png")
    elif obs == 5:
        obsimg = pygame.image.load("car7.png")
    elif obs == 6:
        obsimg = pygame.image.load("buraco.png")
    elif obs == 7:
        obsimg = pygame.image.load("camaleao.png")

    screen.blit(obsimg, (obs_startx, obs_starty))


# Função de pontuação
def system_score(passed, score):
    font = pygame.font.SysFont(None, 30)
    textRecord = font.render((" Recorde: " + str(ultimoRecorde)), False, yellowtxt)
    text = font.render(" Desviou: " + str(passed), False, yellowtxt)
    score = font.render(" Pontos: " + str(score), False, yellowtxt)
    screen.blit(textRecord, (0, 70))
    screen.blit(text, (0, 50))
    screen.blit(score, (0, 30))


# Função do objeto texto
def text_objects(text, font):
    textsurface = font.render(text, False, black)
    return textsurface, textsurface.get_rect()


# Função da definição de fonte e posição do texto
def message_display(text):
    largetext = pygame.font.Font("freesansbold.ttf", 70)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((w / 2), (h / 2))
    screen.blit(textsurf, textrect)
    pygame.display.update()
    pygame.mixer.music.stop()
    pygame.mixer.music.load("batida.mp3")
    pygame.mixer.music.play()
    time.sleep(3)
    global player
    player = "carro"


# Função que exibe o texto na tela
def crash(score):
    message_display("Você Barruou!!!")
    atualizaRecorde(score)
    


# Função da definição de fonte e posição do texto(burro)
def message_displayb(text):
    largetext = pygame.font.Font("freesansbold.ttf", 70)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((w / 2), (h / 2))
    screen.blit(textsurf, textrect)
    pygame.display.update()
    pygame.mixer.music.stop()
    pygame.mixer.music.load("burro.mp3")
    pygame.mixer.music.play()
    time.sleep(3)
    global player
    player = "burro"


# Função que exibe o texto na tela (burro)
def crashb(score):
    message_displayb("Você Barruou!!!")
    atualizaRecorde(score)
    

# Função de digitação do nome de usuário
def nomerecorde():
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(285, 200, 140, 32)
    # Cor inativo
    color_inactive = pygame.Color('lightskyblue3')
    # Cor ativo
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    nomerecorde = True

    while nomerecorde:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o ponto do clique esta dentro do retangulo da caixa de texto
                if input_box.collidepoint(event.pos):
                    # Inverte o valor da variavel 'active'
                    active = not active
                else:
                    # Caso o clique esteja fora do retangulo 'desativa' a caixa de texto
                    active = False

                # Muda a cor da caixa de texto dependendo da variavel active
                if active == True:
                    color = color_active
                else:
                    color = color_inactive

            # Teclando
            if event.type == pygame.KEYDOWN:
                # Campo de texto esta ativo
                if active:
                    # Caso tecle enter limpa campo e imprime no terminal
                    if event.key == pygame.K_RETURN:
                        global nickname

                        # Verifica se a variavel esta vazia
                        if len(text):
                            nickname = text
                        else:
                            nickname = "Sem nome"

                        text = ''
                        nomerecorde = False
                    # Caso tecle backspace retira a ultima posicao da string
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    # Caso tecle outra tecla concatena o valor da tecla na string text
                    else:
                        text += event.unicode

        # 'Pinta' a tela com a cor(RGB) passada                
        screen.fill((30, 30, 30))

        txt_mensagem = font.render(text, True, color)

        # max(pega o maior valor) se a largura do texto for maior que 200px seta esse tamanho + 10 
        width = max(200, txt_mensagem.get_width() + 10)
        input_box.w = width

        # Imprime o texto com base na posicao do retangulo
        screen.blit(dados, (0, 0))
        screen.blit(txt_mensagem, (input_box.x + 5, input_box.y + 5))
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        stextSurf, stextRect = text_objects("Após inserir um nome, pressione ENTER para continuar", smalltext)
        stextRect.center = ((400), (450))
        screen.blit(stextSurf, stextRect)

        # Desenha o retangulo na tela.
        pygame.draw.rect(screen, color, input_box, 2)

        # Atualiza os elementos da tela
        pygame.display.flip()
        clock.tick(30)


# Função de digitação do nome de usuário (burro)
def nomerecordeb():
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(285, 200, 140, 32)
    # Cor inativo
    color_inactive = pygame.Color('lightskyblue3')
    # Cor ativo
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    nomerecordeb = True

    while nomerecordeb:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o ponto do clique esta dentro do retangulo da caixa de texto
                if input_box.collidepoint(event.pos):
                    # Inverte o valor da variavel 'active'
                    active = not active
                else:
                    # Caso o clique esteja fora do retangulo 'desativa' a caixa de texto
                    active = False

                # Muda a cor da caixa de texto dependendo da variavel active
                if active == True:
                    color = color_active
                else:
                    color = color_inactive

            # Teclando
            if event.type == pygame.KEYDOWN:
                # Campo de texto esta ativo
                if active:
                    # Caso tecle enter limpa campo e imprime no terminal
                    if event.key == pygame.K_RETURN:
                        global nickname

                        # Verifica se a variavel esta vazia
                        if len(text):
                            nickname = text
                        else:
                            nickname = "Sem nome"

                        text = ''
                        nomerecordeb = False
                    # Caso tecle backspace retira a ultima posicao da string
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    # Caso tecle outra tecla concatena o valor da tecla na string text
                    else:
                        text += event.unicode

        # 'Pinta' a tela com a cor(RGB) passada                
        screen.fill((30, 30, 30))

        txt_mensagem = font.render(text, True, color)

        # max(pega o maior valor) se a largura do texto for maior que 200px seta esse tamanho + 10 
        width = max(200, txt_mensagem.get_width() + 10)
        input_box.w = width

        # Imprime o texto com base na posicao do retangulo
        screen.blit(dados, (0, 0))
        screen.blit(txt_mensagem, (input_box.x + 5, input_box.y + 5))
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        stextSurf, stextRect = text_objects("Após inserir um nome, pressione ENTER para continuar", smalltext)
        stextRect.center = ((400), (450))
        screen.blit(stextSurf, stextRect)

        # Desenha o retangulo na tela.
        pygame.draw.rect(screen, color, input_box, 2)

        # Atualiza os elementos da tela
        pygame.display.flip()
        clock.tick(30)


# Função de ranking
def screen_ranking():
    loadRecordes()
    font = pygame.font.SysFont(None, 50)
    font1 = pygame.font.SysFont(None, 60)
    font2 = pygame.font.SysFont(None, 32)
    while nomerecordeb or nomerecorde:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    musiclick()
                    menu()
                elif event.key ==pygame.K_x:
                    zerar()
                elif event.key ==pygame.K_RETURN:
                    screenselect()                    
        screen.blit(ranking, (0, 0))
        titulo = font1.render(( "TOP 5"), False, black)
        texto = font2.render(("Aperte 'x' se desejar zerar as pontuações"), False,black)
        texto2 = font2.render(("Pressione 'ENTER' para continuar"), False,black)
        textRecord = font.render(( "1º {}".format(recordes[0][0]) + ": " + recordes[0][1]), False, black)
        textRecord2 = font.render(("2º {}".format(recordes[1][0]) + ": " + recordes[1][1]), False, black)
        textRecord3 = font.render(("3º {}".format(recordes[2][0]) + ": " + recordes[2][1]), False, black)
        textRecord4 = font.render(("4º {}".format(recordes[3][0]) + ": " + recordes[3][1]), False, black)
        textRecord5 = font.render(("5º {}".format(recordes[4][0]) + ": " + recordes[4][1]), False, black)
        screen.blit(titulo,(320,120))
        screen.blit(texto,(180,450))
        screen.blit(texto2,(180,500))
        screen.blit(textRecord, (310,200))
        screen.blit(textRecord2, (310,240))
        screen.blit(textRecord3, (310,280))
        screen.blit(textRecord4, (310,320))
        screen.blit(textRecord5, (310,360))
        
        pygame.display.update()


# Função de tela de seleção
def screenselect():
    select = True
    while select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    musiclick()
                    menu()
                elif event.key == pygame.K_c:
                    contagem()
                elif event.key == pygame.K_b:
                    contagemb()

        screen.blit(selecao, (0, 0))
        pygame.display.update()

# Função de tela sobre
def sobreinfo():
    about = True
    while about:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    musiclick()
                    menu()
        screen.blit(sobre, (0, 0))
        pygame.display.update()

def atualizaUltRecorde():
    global ultimoRecorde
    loadRecordes()
    arqRecorde = open('recorde.txt', 'r')
    ultimoRecorde = arqRecorde.read()
    arqRecorde.close()


# Função que atualiza o recorde
def atualizaRecorde(score):
    atualizaUltRecorde()    
    global recordes

    # Percorre cada recorde do ranking
    for indice, recorde in enumerate(recordes):
        # Verifica se o score eh maior que o i-esimo recorde do ranking
        if score > int(recorde[1]):
            if player == "carro":
                pygame.mixer.music.stop()
                fail()
                nomerecorde()
            else:
                pygame.mixer.music.stop()
                fail()
                nomerecordeb()
                

            global nickname
            novoRecorde = [nickname, score]

            # Insere o novo recorde na posicao i - avancando 1 na posicao do atual e dos subsequentes
            recordes.insert(indice, novoRecorde)

            # Remove o ultimo(sexto) recorde da lista
            recordes.pop()

            # Insere a lista atualizada no arquivo
            persistRecordes()

            # Para o laco
            break
    if score > int(ultimoRecorde):
        arqRecorde = open('recorde.txt', 'w')
        arqRecorde.write(str(score))
        arqRecorde.close()
        atualizaUltRecorde()        
    if score==0:
      musictheme()
      screen_ranking()
    else:
      musictheme()
      screen_ranking()
      

# Função background
def background():
    screen.blit(terra, (0, 0))
    screen.blit(terra, (0, 200))
    screen.blit(terra, (0, 400))
    screen.blit(terra1, (700, 0))
    screen.blit(terra1, (700, 200))
    screen.blit(terra1, (700, 400))
    screen.blit(listra, (380, 0))
    screen.blit(listra, (380, 100))
    screen.blit(listra, (380, 200))
    screen.blit(listra, (380, 300))
    screen.blit(listra, (380, 400))
    screen.blit(listra, (380, 500))
    screen.blit(fio, (120, 0))
    screen.blit(fio, (120, 100))
    screen.blit(fio, (120, 200))
    screen.blit(fio, (680, 0))
    screen.blit(fio, (680, 100))
    screen.blit(fio, (680, 200))


# Função da posição do carro na tela
def car(x, y):
    screen.blit(car1, (x, y))


# Função da posição do burro na tela
def donkey(x, y, tick):
    global burroImage
    if tick == 9:
        if burroImage == burro1:
            burroImage = burro2
        else:
            burroImage = burro1

    screen.blit(burroImage, (x, y))

# Função loop do jogo
def screen_loop():
    global pause
    x = (w * 0.47)
    y = (h * 0.8)
    x_vel = 0
    obs_vel = 9
    obs = 0
    y_vel = 0
    obs_startx = random.randrange(200, (w - 200))
    obs_starty = -750
    obs_w = 56
    obs_h = 125
    music()
    passed = 0
    level = 1
    score = 0
    y2 = 7
    fps = 120
    permanecer = True
    while permanecer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    musiclick()
                    paused()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                x_vel = -5
            elif keys[pygame.K_RIGHT]:
                x_vel = 5
            elif keys[pygame.K_z]:
                obs_vel += 2
            elif keys == [pygame.K_x]:
                obs_vel -= 2
            else:
                x_vel = 0
        x += x_vel
        pause = True
        if level%2==0:
            screen.fill(brown)
            # movendo background
            rel_y = y2 % mato.get_rect().w
            screen.blit(mato, (0, rel_y - mato.get_rect().w))
            screen.blit(mato, (700, rel_y - mato.get_rect().w))
            if rel_y < 800:
                screen.blit(mato, (0, rel_y))
                screen.blit(mato, (700, rel_y))
                screen.blit(marca, (200, rel_y))
                screen.blit(marca, (200, rel_y + 100))


            y2 += obs_vel
        
        else:
            screen.fill(colorg)
            # movendo background
            rel_y = y2 % terra.get_rect().w
            screen.blit(terra, (0, rel_y - terra.get_rect().w))
            screen.blit(terra1, (700, rel_y - terra.get_rect().w))
            if rel_y < 800:
                screen.blit(terra, (0, rel_y))
                screen.blit(terra1, (700, rel_y))
                screen.blit(listra, (380, rel_y))
                screen.blit(listra, (380, rel_y + 100))
                screen.blit(listra, (380, rel_y + 200))
                screen.blit(listra, (380, rel_y + 300))
                screen.blit(listra, (380, rel_y + 400))
                screen.blit(listra, (380, rel_y + 500))
                screen.blit(listra, (380, rel_y - 100))
                screen.blit(fio, (120, rel_y - 200))
                screen.blit(fio, (120, rel_y + 20))
                screen.blit(fio, (120, rel_y + 30))
                screen.blit(fio, (680, rel_y - 100))
                screen.blit(fio, (680, rel_y + 20))
                screen.blit(fio, (680, rel_y + 30))

            y2 += obs_vel

        car(x, y)
        system_score(passed, score)
        obs_starty -= (obs_vel / 4)
        obstacle(obs_startx, obs_starty, obs)
        obs_starty += obs_vel

        if x > 680 - car_w or x < 110:
            crash(score)
        if x > w - (car_w + 110) or x < 110:
            crash(score)
        if obs_starty > h:
            obs_starty = 0 - obs_h
            obs_startx = random.randrange(170, (w - 170))
            obs = random.randrange(0, 8)
            passed += 1
            score = passed * 10

            if int(passed) % 10 == 0:
                level += 1
                obs_vel += 2
                largetext = pygame.font.Font("freesansbold.ttf", 70)
                textsurf, textrect = text_objects("LEVEL " + str(level), largetext)
                textrect.center = ((w / 2), (h / 2))
                screen.blit(textsurf, textrect)
                scream()
                pygame.display.update()
                clock.tick(1)

        if y < obs_starty + obs_h:
            if x > obs_startx and x < obs_startx + obs_w or x + car_w > obs_startx and x + car_w < obs_startx + obs_w:
                crash(score)
        button("Pause (P)", 650, 0, 150, 50, blue, bright_blue, "pause")

        pygame.display.update()
        clock.tick(120)


# Função loop do jogo com burro
def screen_loop_donkey():
    global pause
    x = (w * 0.47)
    y = (h * 0.8)
    x_vel = 0
    obs_vel = 9
    obs = 0
    y_vel = 0
    obs_startx = random.randrange(200, (w - 200))
    obs_starty = -750
    obs_w = 56
    obs_h = 125
    music()
    passed = 0
    level = 1
    score = 0
    y2 = 7
    fps = 120
    permanecer = True
    while permanecer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    musiclick()
                    pausedb()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                x_vel = -5
            elif keys[pygame.K_RIGHT]:
                x_vel = 5
            elif keys[pygame.K_z]:
                obs_vel += 2
            elif keys == [pygame.K_x]:
                obs_vel -= 2
            else:
                x_vel = 0
        x += x_vel
        pause = True
        if level%2==0:
            screen.fill(brown)
            # movendo background
            rel_y = y2 % terrac.get_rect().w
            screen.blit(terrac, (0, rel_y - terrac.get_rect().w))
            screen.blit(terra1c, (700, rel_y - terra1c.get_rect().w))
            if rel_y < 800:
                screen.blit(terrac, (0, rel_y))
                screen.blit(terra1c, (700, rel_y))
                screen.blit(marca, (200, rel_y))
                screen.blit(marca, (200, rel_y + 100))


            y2 += obs_vel
        
        else:
            screen.fill(gray)
            # movendo background
            rel_y = y2 % terra.get_rect().w
            screen.blit(terra, (0, rel_y - terra.get_rect().w))
            screen.blit(terra1, (700, rel_y - terra1.get_rect().w))
            if rel_y < 800:
                screen.blit(terra, (0, rel_y))
                screen.blit(terra1, (700, rel_y))
                screen.blit(listra2, (380, rel_y))
                screen.blit(listra2, (380, rel_y + 100))
                screen.blit(listra2, (380, rel_y + 200))
                screen.blit(listra2, (380, rel_y + 300))
                screen.blit(listra2, (380, rel_y + 400))
                screen.blit(listra2, (380, rel_y + 500))
                screen.blit(listra2, (380, rel_y - 100))
                screen.blit(fio, (120, rel_y - 200))
                screen.blit(fio, (120, rel_y + 20))
                screen.blit(fio, (120, rel_y + 30))
                screen.blit(fio, (680, rel_y - 100))
                screen.blit(fio, (680, rel_y + 20))
                screen.blit(fio, (680, rel_y + 30))

            y2 += obs_vel
        global tick
        if tick <= 10:
            tick += 1
        else:
            tick = 0

        donkey(x, y, tick)
        system_score(passed, score)
        obs_starty -= (obs_vel / 4)
        obstacle(obs_startx, obs_starty, obs)
        obs_starty += obs_vel

        if x > 680 - car_w or x < 110:
            crashb(score)
        if x > w - (car_w + 110) or x < 110:
            crashb(score)
        if obs_starty > h:
            obs_starty = 0 - obs_h
            obs_startx = random.randrange(170, (w - 170))
            obs = random.randrange(0, 8)
            passed += 1
            score = passed * 10

            if int(passed) % 10 == 0:
                level += 1
                obs_vel += 2
                largetext = pygame.font.Font("freesansbold.ttf", 70)
                textsurf, textrect = text_objects("LEVEL " + str(level), largetext)
                textrect.center = ((w / 2), (h / 2))
                screen.blit(textsurf, textrect)
                scream()
                pygame.display.update()
                clock.tick(1)
                
                

        if y < obs_starty + obs_h:
            if x > obs_startx and x < obs_startx + obs_w or x + car_w > obs_startx and x + car_w < obs_startx + obs_w:
                crashb(score)
        button("Pause (P)", 650, 0, 150, 50, blue, bright_blue, "pauseb")

        pygame.display.update()
        clock.tick(60)

musictheme()
menu()
screen_loop()
pygame.quit()
quit()
