import pygame, math
import random
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    K_r,
    QUIT,
)

pygame.init()

clock = pygame.time.Clock()
fade_counter = 0
# CREATE A GAME WINDOW
HEIGHT = 652
WIDTH = 1150
FPS = 60
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Flappy Bird")

# TIMER
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 100)

# BACKGROUND
backg = pygame.image.load("birdbackg.jpg").convert()
backg_width = backg.get_width()

# PLAY BUTTON
play = pygame.image.load('play.png')

# SONG
lobbysong = pygame.mixer.music.load('Naruto - Afternoon of Konoha.mp3')
pygame.mixer.music.set_volume(0.2)


# MOUSE CURSOR
new_cursor = pygame.image.load("cursor.png").convert_alpha()
new_cursor = pygame.transform.scale(new_cursor, (int(WIDTH/49), int(HEIGHT/31)))

pygame.mouse.set_visible(False)

class buttons():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.alpha = 0  # Alpha value for fading effect

    def draw(self):
        global start
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                start = True
    
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
    
    def fade_in(self):
        if self.alpha < 255:
            self.alpha += 0.1  # Increase alpha value gradually
            self.image.set_alpha(self.alpha)
            SCREEN.blit(self.image, (self.rect.x, self.rect.y))

        

        

#LOGO
logoa = pygame.image.load("Flappy_Logo.png")
logo = pygame.transform.scale(logoa, ((logoa.get_rect().width) / 8.3, 120))

# FLAPPY
flappy_idle = [
    pygame.image.load("flappyup.png").convert_alpha(),
    pygame.image.load('flappymid.png').convert_alpha(),
    pygame.image.load('flappydown2.png').convert_alpha(),
    pygame.image.load('flappymid.png').convert_alpha()
]
width_up = pygame.image.load("flappyup.png").get_rect().width
height_up = pygame.image.load("flappyup.png").get_rect().height
idlecount = 0
imagedef = flappy_idle[idlecount]
# FLAPPY MASKS
image = pygame.transform.scale(imagedef, (width_up / 6, height_up / 6))
imagemask = pygame.mask.from_surface(image)

# PIPE
pipe = pygame.image.load("2.png")
prebody = pygame.image.load("pipe.png")
pipe_width = pygame.image.load("2.png").get_rect().width
pipe_height = pygame.image.load("2.png").get_rect().height
body = pygame.transform.scale(prebody, (pipe_width / 4.27, pipe_height))
prebody = pygame.transform.flip(body, True, False)
bodypost = pygame.transform.scale(prebody, (pipe_width / 4.225, pipe_height))
bodytwo = pygame.transform.flip(bodypost, True, False)
pipedown = pygame.transform.scale(pipe, (pipe_width / 4, 107))
pipeuphalf = pygame.transform.rotate(pipe, 180)
pipeup = pygame.transform.scale(pipeuphalf, (pipe_width / 4, pipe_height / 4))
pipeup = pygame.transform.flip(pipeup, True, False)
piperect = pipeup.get_rect()
retry = pygame.image.load('retry.png').convert_alpha()
retry_alpha = 0
retry.set_alpha(255)


# PIPE MASKS
pipemask = pygame.mask.from_surface(pipeup)
pipemask2 = pygame.mask.from_surface(pipedown)
bodymask = pygame.mask.from_surface(body)
body2mask = pygame.mask.from_surface(bodytwo)

# TEXT FONT
text_font = pygame.font.Font("botsmatic.ttf", 80)
text_font2 = pygame.font.Font("botsmatic.ttf", 35)
scorefont = pygame.font.Font('04B_19__.ttf', 60)
scorefont2 = pygame.font.Font('04B_19__.ttf', 48)

#FLOOR
flo = pygame.image.load('birdbackfloor.jpg')
floor = pygame.transform.scale(flo, ((flo.get_rect().width) * 1.7, 62) )

# SOUND EFFECTS
jump_effect = pygame.mixer.Sound("jumpsound.mp3")
jump_effect.set_volume(0.5)
fall_effect = pygame.mixer.Sound('falleffect.mp3')
fall_effect.set_volume(0.5)
wind_effect = pygame.mixer.Sound("wind.mp3")
wind_effect.set_volume(0.7)
score_effect = pygame.mixer.Sound("scoresound.mp3")
score_effect.set_volume(0.5)

# COORDINATES
originy = 326
originx = 450
fx = 150
fy = 50
flappyx = (WIDTH / 2) - fx
flappyy = (HEIGHT / 2) - fy

idleframe = 3

velocity = 0
angle = 0

# DEFINE GAME VARIABLES
tiles = math.ceil(WIDTH / backg_width) + 1
bgscroll = 0
scroll = 0
floor_scroll = 0
floor_scroll_speed = 5  # Adjust this value to change the floor scroll speed

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image_up = pipeup
        self.image_down = pipedown
        self.rect_up = self.image_up.get_rect()
        self.rect_down = self.image_down.get_rect()
        self.rect_up.x = x
        self.rect_down.x = x
        self.rect_up.y = HEIGHT - 272
        self.random_y = random.randint(-360, -30)
        self.rect_down.y = self.random_y + pipe_gap
        self.body = body
        self.body2 = bodytwo
        self.image_down = pygame.transform.scale(self.image_down, (self.rect_down.width, self.rect_down.height * 2))

        self.speed = 5
        self.passed = False  # New attribute to track if the bird has passed this pipe

    def move(self):     
        if not collision:
            self.rect_up.x -= self.speed
            self.rect_down.x -= self.speed
            self.update_masks()

    def draw(self, screen):
        SCREEN.blit(self.image_up, (self.rect_up.x, self.rect_down.y + 360))
        SCREEN.blit(self.image_down, (self.rect_down.x, self.rect_down.y))
        SCREEN.blit(self.body, (self.rect_down.x + 3, self.rect_down.y - pipe_height + 3))
        
        self.body2_x = self.rect_up.x + 2.3  # Center of pipeup
        self.body2_y = self.rect_down.y + 500 # Position it just below pipeup
        
        SCREEN.blit(self.body2, (self.body2_x, self.body2_y))

    def update_masks(self):
        global pipemask, pipemask2, bodymask
        pipemask = pygame.mask.from_surface(self.image_up)
        pipemask2 = pygame.mask.from_surface(self.image_down)
        bodymask = pygame.mask.from_surface(self.body)

def reset_game():
    global flappyy, flappyx, scrolling, angle, keyevents, jumpplayed, reset, velocity, falling, tilepass, collision, collided, textplayed, score, retry_alpha, collision_flash
    collision_flash = False
    flappyy = originy
    flappyx = originx
    scrolling = True
    angle = 0
    keyevents = True
    jumpplayed = False
    falling = False
    reset = True
    collision = False
    velocity = 0
    tilepass = False
    collided = False
    textplayed = True
    retry_alpha = 0 
    score = 0
    reset_pipes()

    # Reset pipe masks
    global pipemask, pipemask2, bodymask
    pipemask = pygame.mask.from_surface(pipeup)
    pipemask2 = pygame.mask.from_surface(pipedown)
    bodymask = pygame.mask.from_surface(body)
    fall_effect.stop()

def enforce_border():
    global flappyx, flappyy, velocity
    if flappyy >= HEIGHT - 100:
        flappyy = HEIGHT - 100
        SCREEN.blit(flappy_idle[1], (flappyx, HEIGHT - 100))
    elif flappyy <= 0:
        flappyy = 0
        velocity = -1
        SCREEN.blit(flappy_idle[1], (flappyx, flappyy))

def text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x,y))

def reset_pipes():
    global pipes
    pipes = []
    new_pipe = Pipe(WIDTH)
    pipes.append(new_pipe)

pipes = []
pipe_gap = 200  # Gap between the upper and lower pipes
pipe_spacing = 250  # Space between consecutive pairs of pipes

# Add initial pair of pipes
new_pipe = Pipe(WIDTH + 100)
pipes.append(new_pipe)

# RUN TILL QUIT
running = True
scrolling = True
falling = False
keyevents = True
jumpplayed = False
windplayed = False
reset = True
tilepass = False
ready = False
collision = False
firstpipe = False
collided = False
first = True
textplayed = False
start = False
textscroll = 0
textpos = WIDTH/2 - 250
textpos2 = WIDTH/2 - 400
mplayed = False
collision_flash = False
score = 0
start_button = buttons(WIDTH/2 - 50, HEIGHT/2 - 10, play, 0.24)
retry_button = buttons(500, 380, retry, 0.2)
while running:
    keys = pygame.key.get_pressed()
    clock.tick(30)
    enforce_border()
    pos = pygame.mouse.get_pos()
    text_surface = scorefont.render(str(score), False, (0, 0, 0))
    text_surface2 = scorefont2.render(str(score), False, (250, 250, 250))

    
    if not scrolling:
        if retry_button.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    reset_game()


    # SCROLLING
    for i in range(0, tiles):
        SCREEN.blit(backg, (i * backg_width + bgscroll, 0))
        SCREEN.blit(backg, (i * backg_width + bgscroll, 0))
        
    if falling:
        for pipe in pipes:
            pipe.move()
            pipe.update_masks()

    pipes = [pipe for pipe in pipes if pipe.rect_up.right > 0]
    if pipes[-1].rect_up.x < WIDTH - pipe_spacing:
        new_pipe = Pipe(WIDTH)
        pipes.append(new_pipe)

    for pipe in pipes:
        pipe.draw(SCREEN)

    if falling:
        tilepass = True

    # SCROLL BACKG
    if scrolling and reset:
        bgscroll -= 3.5
        floor_scroll -= floor_scroll_speed
        if tilepass:
            scroll -= 5
    # RESET SCROLL
    if abs(bgscroll) > backg_width:
        bgscroll = 0
    if abs(scroll) > backg_width + 400 + pipe_width:
        scroll = 0
    if abs(floor_scroll) > backg_width:
        floor_scroll = 0

    if falling and reset:
        velocity += 1.5
        flappyy += velocity 
        angle = max(-70, angle - 3)

    if idlecount == len(flappy_idle):
        idlecount = 0

    image = flappy_idle[idlecount]
    image = pygame.transform.scale(image, (width_up / 6, height_up / 6))
    imagemask = pygame.mask.from_surface(image)

    collided = False
    for pipe in pipes:
        if imagemask.overlap(pipemask, (pipe.rect_up.x - flappyx, pipe.rect_down.y + 375 - flappyy)):
            collided = True
            break
        if imagemask.overlap(pipemask2, (pipe.rect_down.x - flappyx, pipe.rect_down.y - flappyy)):
            collided = True
            break
        if imagemask.overlap(bodymask, (pipe.rect_down.x - flappyx, pipe.rect_down.y - flappyy - pipe_height + 3)):
            collided = True
            break
        if imagemask.overlap(body2mask, (pipe.body2_x - flappyx, pipe.body2_y - flappyy)):
            collided = True
        if not pipe.passed and flappyx > pipe.rect_up.x + pipe.rect_up.width:
            pipe.passed = True
            score += 1
            score_effect.play()
            
            

    # EVENT HANDLER
    for event in pygame.event.get():
        if event.type == KEYDOWN and reset:
    
            if event.key == K_SPACE and scrolling  and start and fade_counter > WIDTH + 500:
                first = False
                jump_effect.play()
                falling = True
                angle = 40
                flappyy -= 6
                velocity = -15
                ready = True
            if event.key == pygame.K_r and not scrolling:
                reset_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and scrolling  and start and fade_counter > WIDTH + 500:
                first = False
                jump_effect.play()
                falling = True
                angle = 40
                flappyy -= 6
                velocity = -15
                ready = True
            
        if event.type == pygame.QUIT:
            running = False
        if event.type == timer_event:
            idlecount += 1
        # ESCAPE EVENT      
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if keyevents and reset:   
            # KEYS AND HEIGHT
            if flappyy >= HEIGHT - 85:
                flappyx = (WIDTH / 2) - 150
                flappyy = HEIGHT - 84

    # FALL FUNCTION                    
    if flappyy >= HEIGHT - 110 and not jumpplayed and reset:
        fall_effect.play(0)
        jumpplayed = True

    if flappyy >= HEIGHT - 110 and reset:
        collision = True
        flappyx = (WIDTH / 2) - 150
        flappyy = HEIGHT - 110
        scrolling = False
        angle = -3
        image = pygame.transform.scale(flappy_idle[3], (width_up / 6, height_up / 6))
        image = pygame.transform.rotate(image, 300)
        if not collision_flash:
            SCREEN.fill((255, 255, 255))
            collision_flash = True

    if collision:
        if retry_button.draw():
                reset_game()
                collision = False

    if reset:
        rotated_image = pygame.transform.rotate(image, angle)
    
    if not falling and collision:
        retry_alpha = min(retry_alpha + 5, 255)  # Increase alpha value, maxing at 255
        retry.set_alpha(retry_alpha)
        retry_button.fade_in()
        

    if start and fade_counter > WIDTH and not textplayed:
        if not ready:
            text("get ready", text_font, (0,0,0), textpos , 80)
            text("press space or left click to jump", text_font2, (0,0,0), textpos2 + textscroll , 200)
        if ready and textpos2 > - 600 and not collision:
            textscroll -= 5
            text("get ready", text_font, (0,0,0), textpos + textscroll , 80)
            text("press space or left click to jump", text_font2, (0,0,0), textpos2 + textscroll , 200)

        if collision:
            text("get ready", text_font, (0,0,0), textpos + textscroll , 80)
            text("press space or left click to jump", text_font2, (0,0,0), textpos2 + textscroll , 200)

    if mplayed == False:
        pygame.mixer.music.play()
    
    if running:
        mplayed = True
    if start:
        pygame.mixer.music.set_volume(0.08)

    if collided and not collision:
        scrolling = False
        collision = True
        jumpplayed = True
        velocity = 0
        fall_effect.play(0)
        image = pygame.transform.scale(flappy_idle[3], (width_up / 6, height_up / 6))
        image = pygame.transform.rotate(image, 300)
        SCREEN.fill((255, 255, 255))
        collision_flash = True

    if first and not falling and not start:
        SCREEN.blit(logo, (330, 100))
        SCREEN.blit(rotated_image, (800, 130))
        start_button.draw()
    
    
    for i in range(0, tiles):
        SCREEN.blit(floor, (i * backg_width + floor_scroll, HEIGHT - 62))
        pygame.draw.line(SCREEN, (65, 65, 65), (0, HEIGHT - 62.5), (WIDTH, HEIGHT - 62.5), 2)

    if start:
        if windplayed == False:
            wind_effect.play()
            windplayed = True
        if fade_counter > WIDTH:
            SCREEN.blit(text_surface, (WIDTH/2, 50))
            SCREEN.blit(text_surface2, (WIDTH/2 + 4, 56))
            SCREEN.blit(rotated_image, (flappyx, flappyy))
        if fade_counter < WIDTH*2:
            fade_counter += 70
            pygame.draw.rect(SCREEN, (0,0,0), ((0-WIDTH) + fade_counter, 0, fade_counter, HEIGHT))

    SCREEN.blit(new_cursor, pos)
    
    pygame.display.update()

pygame.quit()