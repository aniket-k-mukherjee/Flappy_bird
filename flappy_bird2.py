import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,650))
    screen.blit(floor_surface, (floor_x_pos+650, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    random_pipe_distance = random.choice(pipe_distance)
    bottom_pipe = pipe_surface.get_rect(midtop = (650, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (650, random_pipe_pos - random_pipe_distance))
    return bottom_pipe,top_pipe

def moves_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5  #moves the pipes to the left
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 750:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False,True)
            screen.blit(flip_pipe, pipe)

#COLLISION
def collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 650:
        return False

    return True

#BIRD ROTATION
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_mov * 3,1)
    return new_bird

#ANIMATION FUNCTION
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

#SCORES
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (325,80))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 255))
        score_rect = score_surface.get_rect(center=(325, 110))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 24, 0))
        high_score_rect = high_score_surface.get_rect(center=(325, 600))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#calling modules in pygame
#pygame.mixer.pre_init(frequency= 44100, size= 16, channels= 1, buffer= 512)
pygame.init()
screen = pygame.display.set_mode((650, 750))  #displaying screen
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',35)

#Game variables
gravity = 0.25
bird_mov = 0
score = 0
high_score = 0

#backgroud image
bg_surface = pygame.image.load('assets/background-day.png')
bg_surface = pygame.transform.scale(bg_surface, (650,750))

#FLOOR IMAGE
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface,(650, 100))
floor_x_pos = 0

#BIRD
# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center = (100,375))

#BIRD ANIMATION
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,375))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


#PIPES
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []  #empty pipe list
SPAWNPIPE = pygame.USEREVENT      #triggered by a timer
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_height = [300,400,500]
pipe_distance = [200,210,220]

#deciding game activation
game_active = True

game_over_surface = pygame.transform.scale(pygame.image.load('assets/message.png').convert_alpha(), (325,375))
game_over_rect = game_over_surface.get_rect(center = (325, 375))

#SOUNDS
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)

while True:
    for event in pygame.event.get():

        #QUITTING
        if event.type == pygame.QUIT:
            pygame.quit()     #exits out of the while loop
            sys.exit()

        #KEY SPACE UP AND DOWN CONTROL
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active :
                bird_mov = 0
                bird_mov = -6
                flap_sound.play()

            # RESTARTING THE GAME
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,375)
                bird_mov = 0
                score = 0
                death_sound.play()

        #CREATING PIPES
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        #ANIMATION BIRDFLAP
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0,0))

    if game_active == True:
       #bird
        bird_mov += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_mov
        screen.blit(rotated_bird, bird_rect)
        game_active = collision(pipe_list)

        #Pipes
        pipe_list = moves_pipe(pipe_list)
        draw_pipes(pipe_list)

        #Score
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -650:
        floor_x_pos = 0


    clock.tick(80)
    pygame.display.update()


