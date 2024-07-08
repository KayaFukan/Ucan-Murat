# Import module 
import random 
import sys 
import pygame 
from pygame.locals import *
from button import Button
  
# All the Game Variables 
window_width = 288
window_height = 500
  
# set height and width of window 
window = pygame.display.set_mode((window_width, window_height)) 
elevation = window_height * 0.8
game_images = {} 
framepersecond = 32
icon = pygame.image.load('Dosyalar\\icon.ico')
pipeimage = 'Dosyalar\\firat boru.png'
background_image = 'Dosyalar\\background-day.png'
birdplayer_images = ['Dosyalar\\murat 1.2.png', 'Dosyalar\\murat 1.3.png']
sealevel_image = 'Dosyalar\\basee.png'
flap_sound = 'Dosyalar\\ah.wav'
die_sound = 'Dosyalar\\bi degmeyin ya.wav'
pygame.display.set_icon(icon)
max_score = open("Dosyalar\\score.txt","r")
max_score = int(max_score.readline())

def get_font(size):
    return pygame.font.Font("Dosyalar\\font.ttf", size)

def StartMenu():
    color = (0,0,0)
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        window.fill(color)
        
        MENU_TEXT = get_font(25).render("ANA MENU", True, "#d7fcd4")
        MENU_RECT = MENU_TEXT.get_rect(center=(150, 50))
        
        TOTAL_SCORE = get_font(13).render(f"En Yüksek Puan: {max_score}", True, "#b68f40")
        SCORE_RECT = TOTAL_SCORE.get_rect(center=(150, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("Dosyalar/Play Rect.png"), pos=(150, 250), 
                            text_input="OYNA", font=get_font(25), base_color="#d7fcd4", hovering_color="White",scale=(150, 50))
        QUIT_BUTTON = Button(image=pygame.image.load("Dosyalar/Quit Rect.png"), pos=(150, 350), 
                            text_input="ÇIK", font=get_font(25), base_color="#d7fcd4", hovering_color="White",scale=(150, 50))

        window.blit(MENU_TEXT, MENU_RECT)
        window.blit(TOTAL_SCORE, SCORE_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    flappygame()
                    return
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                flappygame()
                return
        pygame.display.update()
        


def flappygame(): 
    global max_score
    your_score = 0
    horizontal = int(window_width/5) 
    vertical = int((window_height - game_images['flappybird'][0].get_height())/2)
    ground = 0
    mytempheight = 100
  
    # Generating two pipes for blitting on window 
    first_pipe = createPipe() 
    second_pipe = createPipe() 
  
    # List containing lower pipes 
    down_pipes = [ 
        {'x': window_width+300-mytempheight, 
         'y': first_pipe[1]['y']}, 
        {'x': window_width+300-mytempheight+(window_width/2), 
         'y': second_pipe[1]['y']}, 
    ] 
  
    # List Containing upper pipes 
    up_pipes = [ 
        {'x': window_width+300-mytempheight, 
         'y': first_pipe[0]['y']}, 
        {'x': window_width+200-mytempheight+(window_width/2), 
         'y': second_pipe[0]['y']}, 
    ] 
  
    # pipe velocity along x 
    pipeVelX = -4
  
    # bird velocity 
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1
  
    bird_flap_velocity = -8
    bird_flapped = False
    bird_animation_index = 0

    while True: 
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit() 
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                #adding a sound
                pygame.mixer.Sound(flap_sound).play()
                if vertical > 0: 
                    bird_velocity_y = bird_flap_velocity 
                    bird_flapped = True
                    bird_animation_index = (bird_animation_index + 1) % len(game_images['flappybird'])

        # This function will return true 
        # if the flappybird is crashed 
        game_over = isGameOver(horizontal, 
                               vertical, 
                               up_pipes, 
                               down_pipes) 
        if game_over:
            score_screen(your_score)
            return
  
        # check for your_score 
        playerMidPos = horizontal + game_images['flappybird'][0].get_width()/2
        for pipe in up_pipes: 
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4: 
                your_score += 1
                if your_score > max_score:
                    max_score = your_score
                    with open("Dosyalar\\score.txt","w") as f:
                        f.write(str(max_score))  
  
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped: 
            bird_velocity_y += birdAccY 
  
        if bird_flapped: 
            bird_flapped = False
        playerHeight = game_images['flappybird'][0].get_height() 
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

  
        # move pipes to the left 
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes): 
            upperPipe['x'] += pipeVelX 
            lowerPipe['x'] += pipeVelX 
  
        # Add a new pipe when the first is 
        # about to cross the leftmost part of the screen 
        if 0 < up_pipes[0]['x'] < 5: 
            newpipe = createPipe() 
            up_pipes.append(newpipe[0]) 
            down_pipes.append(newpipe[1]) 
  
        # if the pipe is out of the screen, remove it 
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width(): 
            up_pipes.pop(0) 
            down_pipes.pop(0) 
  
        # Lets blit our game images now 
        window.blit(game_images['background'], (0, 0)) 
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes): 
            window.blit(game_images['pipeimage'][0], 
                        (upperPipe['x'], upperPipe['y'])) 
            window.blit(game_images['pipeimage'][1], 
                        (lowerPipe['x'], lowerPipe['y'])) 
  
        window.blit(game_images['sea_level'], (ground, elevation)) 
        window.blit(game_images['flappybird'][bird_animation_index], (horizontal, vertical)) 
  
        # Fetching the digits of score. 
        numbers = [int(x) for x in list(str(your_score))] 
        width = 0
  
        # finding the width of score images from numbers. 
        for num in numbers: 
            width += game_images['scoreimages'][num].get_width() 
        Xoffset = (window_width - width)/1.1
  
        # Blitting the images on the window. 
        for num in numbers: 
            window.blit(game_images['scoreimages'][num], 
                        (Xoffset, window_width*0.02)) 
            Xoffset += game_images['scoreimages'][num].get_width() 
  
        # Refreshing the game window and displaying the score. 
        pygame.display.update() 
        framepersecond_clock.tick(framepersecond) 
    StartMenu()
    
  
def isGameOver(horizontal, vertical, up_pipes, down_pipes): 
    # Kuş zemine değerse
    if vertical > elevation - game_images['flappybird'][0].get_height():
        pygame.mixer.Sound(die_sound).play()
        return True
    
    # Kuş ekrandan çıkarsa
    if vertical < 0: 
        pygame.mixer.Sound(die_sound).play()
        return True
    
    if vertical > 333: 
        pygame.mixer.Sound(die_sound).play()
        return True

    for pipe in up_pipes: 
        pipeHeight = game_images['pipeimage'][0].get_height() 
        if(vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()): 
            pygame.mixer.Sound(die_sound).play()
            return True

    for pipe in down_pipes: 
        if(vertical + game_images['flappybird'][0].get_height() > pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()): 
            pygame.mixer.Sound(die_sound).play()
            return True
    return False
  
def score_screen(score):
    while True:
        window.fill((0, 0, 0))
        score_text = get_font(25).render(f"Skorun: {score}", True, "#b68f40")
        score_rect = score_text.get_rect(center=(144, 150))

        RESTART_BUTTON = Button(image=pygame.image.load("Dosyalar/Play Rect.png"), pos=(150, 250), 
                                text_input="YENİDEN BAŞLAT", font=get_font(10), base_color="#d7fcd4", hovering_color="White", scale=(150, 50))
        MENU_BUTTON = Button(image=pygame.image.load("Dosyalar/Quit Rect.png"), pos=(150, 350), 
                             text_input="MENU", font=get_font(25), base_color="#d7fcd4", hovering_color="White", scale=(150, 50))

        QUIT_BUTTON = Button(image=pygame.image.load("Dosyalar/Quit Rect.png"), pos=(150, 450), 
                            text_input="ÇIK", font=get_font(25), base_color="#d7fcd4", hovering_color="White",scale=(150, 50))

        window.blit(score_text, score_rect)

        for button in [RESTART_BUTTON, MENU_BUTTON, QUIT_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESTART_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    flappygame()
                    return
                if MENU_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    StartMenu()
                    return
                if QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                flappygame()
                return
            

        pygame.display.update()


def createPipe(): 
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height() 
    y2 = offset + random.randrange( 0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))   
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset 
    pipe = [ 
        # upper Pipe 
        {'x': pipeX, 'y': -y1}, 
  
        # lower Pipe 
        {'x': pipeX, 'y': y2} 
    ] 
    return pipe 
  
  
# program where the game starts 
if __name__ == "__main__": 
  
    # For initializing modules of pygame library
    pygame.init() 
    
    framepersecond_clock = pygame.time.Clock() 
  
    # Sets the title on top of game window 
    pygame.display.set_caption('Uçan MURAT') 
  
    # Load all the images which we will use in the game 
  
    # images for displaying score 
    game_images['scoreimages'] = ( 
        pygame.image.load('Dosyalar\\0.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\1.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\2.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\3.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\4.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\5.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\6.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\7.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\8.png').convert_alpha(), 
        pygame.image.load('Dosyalar\\9.png').convert_alpha() 
    ) 
    game_images['flappybird'] = [
        pygame.image.load( birdplayer_images[0]).convert_alpha(),
        pygame.image.load(birdplayer_images[1]).convert_alpha()] 
    game_images['sea_level'] = pygame.image.load( 
        sealevel_image).convert_alpha() 
    game_images['background'] = pygame.image.load( 
        background_image).convert_alpha() 
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load( 
        pipeimage).convert_alpha(), 180), pygame.image.load( 
      pipeimage).convert_alpha()) 
    StartMenu()
  
    # Here starts the main game 
  
    while True: 
        StartMenu()
    
        # sets the coordinates of flappy bird 
  
        horizontal = int(window_width/5) 
        vertical = int( 
            (window_height - game_images['flappybird'][0].get_height())/2) 
        ground = 0
        while True: 
            for event in pygame.event.get(): 
  
                # if user clicks on cross button, close the game 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                    pygame.quit() 
                    sys.exit() 
  
                # If the user presses space or 
                # up key, start the game for them 
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                    flappygame() 
  
                # if user doesn't press anykey Nothing happen 
                else: 
                    window.blit(game_images['background'], (0, 0)) 
                    window.blit(game_images['flappybird'][0], 
                                (horizontal, vertical)) 
                    window.blit(game_images['sea_level'], (ground, elevation)) 
                    pygame.display.update() 
                    framepersecond_clock.tick(framepersecond)