import pygame #importing pygame library
import time #importing time for cooldowns
from sys import exit #importing specific method to kill code

pygame.init() #starting pygame
left_speed = 10
right_speed = 10
direction = 'r'
direction_y = 'd'
MAXFRAMERATE = 60 #fps cap
MAXGRAVITY = 20 #gravity cap
screen_info = pygame.display.Info()
screen_multiplier = int(screen_info.current_w/320)
playing_level = False

screen_x = 320*screen_multiplier #window width
screen_y = 180*screen_multiplier #window height
tile_size = 10*screen_multiplier #size of tile (for building level)

leftExtreme =  0
rightExtreme = screen_x
current_chunk = [1, 1]#level, chunk
hor_collision_now = False

hor_col_blocks = []
vert_col_blocks = []

#X = wall, G = gem, P = player spawn C = checkpoint, : = chain (cosmetic), S = spring, K = key
#^ = upright spike, V = upside-down spike, > = right-facing spike, < = left-facing spike
l1c1 = [
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXX        :      :     :    XXX',
    'X>         :      :     :      X',  
    'X>   <X    :      :    ^:      X',
    'X>         X     <XXXXXXXX    <X',
    'X>               <X> K <X>    <X',
    'XXXXX>           <X>   <X>    <X',
    '                 <X    <X>    <X',
    '        G   ^    <X    XX>    <X',
    '    XXXXXXXXX    <X   X>        ',
    '   ^X            <X   V        X',
    'XXXXX            <XX       <XXXX',
    'X                <X           VX',
    'X                <X            X',
    'X                <X           ^X',
    'X                <X         XXXX',
    'X^^^^^^^^^^^^^^^^^X^^S^^^^^^XXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']

l1c2 = [
    '                        XXXX    ',
    '                                ',
    '                  XX            ',
    '                  XX            ',
    '                  XX            ',
    '                  XX            ',
    '                   X            ',
    '                  XX            ',
    '                  XX  XX        ',
    'P                 XX  XX       C',
    '               X  XX   XXXXXXXX ',
    '               X  XX  XXXXXXXX  ',
    'X   XX  XXXXXXXX',
    'X   XX  XXXXXXXX',
    'X   XX  XXXXXXXX',
    'X   XX  XXXXXXXX',
    '',
    '',]

l1c3 = [
    '          XX    ',
    '          XX    ',
    '    XX    XX    ',
    '    XX    XX    ',
    '   XXX    XX    ',
    '    XX    XX    ',
    '     X          ',
    '    XX          ',
    '    XX  XX      ',
    'P   XX  XX     C',
    'X   XX  XXXXXXXX',
    'X   XX  XXXXXXXX',
    '                ',
    '                ',
    '                ',
    '                ',]

order = [l1c1, l1c2, l1c3]

with open('GameData/GameData.txt', 'r') as f: #opening GameData file
    coins = int(f.readline()) #extracting coins from file

gems = 0

class Character(pygame.sprite.Sprite): #creating a sprite class
    def __init__(self): #defining main character function
        super().__init__() #initializing function
        self.pos_x = 0  #player spawn point x
        self.pos_y = 600 #player spawn point y
        self.is_dashing = False #is the player dashing?
        self.grav_immune = False #is the player immune to gravity?
        self.alive = True
        self.has_key = False
        self.dash_range = 100 #dash distance
        self.time_since_dash = 0 #time in seconds since the last time player dashed
        self.gravity = 0 #current gravity (changes per frame)
        self.state = 0 #0 = on the ground, 1 = in the air,
        self.jumps_since_land = 0 #number of jumps since player state 0
        self.image = pygame.transform.scale(pygame.image.load('Images/Player/player_idle.png'), (round(35*screen_multiplier/3.75), round(32*screen_multiplier/3.75))).convert_alpha() #loading the image for the player
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y)) #assigning a rectangle for the image
    
    def reset_player(self, BoF):
        if BoF == 'f':
            self.rect.x = 0
            self.rect.y = 600
        elif BoF == 'b':
            self.rect.x = 750

    def player_input(self):
        global direction, left_speed, right_speed, direction_y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += right_speed
            direction = 'r'
            if left_speed == 0:
                left_speed = 10
        if keys[pygame.K_a]:
            self.rect.x -= left_speed
            direction = 'l'
            if right_speed == 0:
                right_speed = 10
            if self.rect.x <= 0:
                self.rect.x = 0
                left_speed = 0
        if keys[pygame.K_SPACE] and self.jumps_since_land < 2 and self.gravity > -6:
            self.grav_immune =  False
            self.gravity = -17
            left_speed = 10
            right_speed = 10
            self.jumps_since_land += 1
            direction_y = 'u'
            self.state = 1
        if keys[pygame.K_f] and self.is_dashing == False and direction != None and keys[pygame.K_w] != True and time.time()-self.time_since_dash >= 1:
            self.grav_immune = True
            self.is_dashing = True
            self.time_since_dash = time.time()
            if direction == 'r':
                self.rect.x += self.dash_range
            elif direction == 'l':
                self.rect.x -= self.dash_range
            self.grav_immune = False
            self.is_dashing = False
        elif keys[pygame.K_f] and self.is_dashing == False and keys[pygame.K_w] :
            self.is_dashing = True
            self.time_since_dash = time.time()
            self.gravity = -1*self.dash_range
            self.is_dashing = False
        if self.rect.x > rightExtreme:
            scroll('r')
            self.reset_player('f')
        elif self.rect.x < leftExtreme:
            if current_chunk[1] == 1:
                left_speed = 0
            scroll('l')
            self.reset_player('b')      
            
    def apply_gravity(self):
        global direction_y
        if not self.grav_immune:
            self.gravity += 1
            self.rect.y += self.gravity
        if self.rect.bottom > 175*screen_multiplier:
            self.alive = False
        if self.gravity > MAXGRAVITY:
            self.gravity -= 1
        if self.gravity > 0 and self.rect.bottom < 720 and self.state != 0:
            direction_y = 'd'

    def update(self):
        self.player_input()
        self.apply_gravity()

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Images/Bricks/bricks.png'), (size, size)).convert()
        self.rect = self.image.get_rect(topleft=pos)

class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, size, rotation):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Images/Elements/spikes.png'), size), rotation).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
class Spring(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Images/Elements/spring.png'), (size, size)).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class Chain(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Images/Elements/chain.png'), size).convert_alpha()
        self.image.set_alpha(100)
        self.rect = self.image.get_rect(topleft = pos)

class Gem(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Images/Collectables/gem.png'), (size, size)).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class Key(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Images/Collectables/key.png'), (size, size)).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.u_disable = False
    
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.chains = pygame.sprite.Group()
        self.springs = pygame.sprite.Group()
        self.gems = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'X':
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                elif col == '^' or col == 'V' or col == '>' or col == '<':
                    rot = {'^':0, 'V':180, '>':270, '<':90}
                    y_skew = {'^':screen_multiplier*7, 'V':0, '<':0, '>':0}
                    x_skew = {'^':0, 'V':0, '<':screen_multiplier*7, '>':0}
                    self.spikes.add(Spike((x+x_skew[col],y+y_skew[col]), (tile_size, 3*screen_multiplier), rot[col]))
                elif col == ':':
                    self.chains.add(Chain((x+4*screen_multiplier,y), (2*screen_multiplier, tile_size)))
                elif col == 'S':
                    spring = Spring((x,y), tile_size)
                    self.springs.add(spring)
                elif col == 'G':
                    self.gems.add(Gem((x,y), tile_size))
                elif col == 'K':
                    self.keys.add(Key((x,y), tile_size))
                    
    def remove_item(self, type):
        for row_index, row in enumerate(order[current_chunk[1]-1]):
                for col_index, col in enumerate(row):
                    if col == type:
                        col_with_gem = list(order[current_chunk[1]-1][row_index])
                        col_with_gem[col_index] = ' '
                        new_col = ''
                        for item in col_with_gem:
                            new_col += item
                        order[current_chunk[1]-1][row_index] = new_col

    def check_horizontal_collision(self):
        global left_speed, right_speed, hor_collision_now, hor_col_blocks
        player = character.sprite
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if direction == 'l':
                    player.rect.left = sprite.rect.right
                    left_speed = 0
                    hor_collision_now = True
                if direction == 'r':
                    player.rect.right = sprite.rect.left
                    right_speed = 0
                    hor_collision_now = True
                    
    def check_vertical_collision(self):
        global direction_y, jumps_since_land
        player = character.sprite
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if direction_y == 'd':
                    player.rect.bottom = sprite.rect.top
                    player.gravity = 0
                    player.state = 0
                    player.jumps_since_land = 0
                elif direction_y == 'u':
                    if player.state != 0:
                        player.rect.top = sprite.rect.bottom
                        player.gravity = 0
                        direction_y = 'd'

    def check_spike_collision(self):
        player = character.sprite
        for sprite in self.spikes.sprites():
            if sprite.rect.colliderect(player.rect):
                player.alive = False
                
    def check_spring_collision(self):
        player = character.sprite
        for sprite in self.springs.sprites():
            if sprite.rect.colliderect(player.rect):
                player.gravity = -30
    
    def check_gem_collision(self):
        global gems, order
        player = character.sprite
        for sprite in self.gems.sprites():
            if sprite.rect.colliderect(player.rect):
                gems += 1
                self.gems.remove(sprite)
                sprite.kill()
                self.remove_item('G')

    def check_key_collision(self):
        player = character.sprite
        for sprite in self.keys.sprites():
            if sprite.rect.colliderect(player.rect):
                player.has_key = True
                self.keys.remove(sprite)
                sprite.kill()
                self.remove_item('K')
                



    def run(self):
        self.tiles.draw(self.display_surface)
        self.spikes.draw(self.display_surface)
        self.chains.draw(self.display_surface)
        self.springs.draw(self.display_surface)
        self.gems.draw(self.display_surface)
        self.keys.draw(self.display_surface)
        self.check_vertical_collision()
        self.check_horizontal_collision()
        self.check_spike_collision()
        self.check_spring_collision()
        self.check_gem_collision()
        self.check_key_collision()
 
class Main_Screen:
    def __init__(self):
         self.frame = pygame.transform.scale(pygame.image.load('Images/Screens/main_screen.png'), (screen_x, screen_y)).convert()
         self.rect = self.frame.get_rect(topleft=(0,0))
         self.font = pygame.font.Font(None, 60)
         self.dead_screen = pygame.Surface((screen_x, screen_y))
         self.dead_screen_rect = self.dead_screen.get_rect()
    
    def display(self):
        screen.blit(self.frame, (0,0))
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_state = pygame.mouse.get_pressed()

        if self.mouse_state[0]:
            if self.mouse_x >= 40*screen_multiplier and self.mouse_x <= 71*screen_multiplier and self.mouse_y >= 52*screen_multiplier and self.mouse_y <= 70*screen_multiplier:
                global playing_level, alive
                playing_level = True
                character.sprite.alive = True
                run_level()
    
    def run_dead(self):
        global playing_level
        playing_level = False
        screen.blit(self.dead_screen, self.dead_screen_rect)
        self.dead_screen.fill('white')
        self.death_label = self.font.render('You Died', False, 'black')
        screen.blit(self.death_label, (100, 100))
        self.display()
        character.sprite.reset_player("f")
    
        
def run_level():
    screen.blit(background_surf, (0,0))
    screen.blit(coin_label, (2,2))
    level = Level(order[current_chunk[1]-1], screen)
    character.draw(screen) 
    level.run()
    level.check_vertical_collision()
    

def scroll(dir):
    if dir == 'r' and current_chunk[1] != len(order):
        current_chunk[1] += 1
        screen.blit(background_surf, (0,0))
        level.run()
    if dir == 'l' and current_chunk[1] != 1:
        current_chunk[1] -= 1
        screen.blit(background_surf, (0,0))
        level.run()

#Setup
screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE) #create a window
pygame.display.set_caption('Magnolia')
clock = pygame.time.Clock() #create a clock the game runs on
level = Level(order[current_chunk[1]-1], screen)
running = True #is the game running?

tile = pygame.sprite.Group()

background_surf = pygame.transform.scale(pygame.image.load('Images/Backgrounds/tundra_bg.png'), (screen_info.current_w, screen_info.current_h)).convert()

character = pygame.sprite.GroupSingle()
character.add(Character())   

basic_font = pygame.font.Font(None, 25)
coin_label = basic_font.render('Coins: '+str(coins), False, 'black')

while running: #the game loop WHOLE GAME INSIDE HERE
    for event in pygame.event.get(): #loops through all events
        if event.type == pygame.QUIT: #is the event exiting the window? 
            pygame.quit()
            exit() 
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

    run_level()
    
    if not playing_level:
        main_frame  = Main_Screen()
        main_frame.display()
   
    if character.sprite.alive == False:
        main_frame.run_dead()
    
    character.update()
    pygame.display.update()
    hor_collision_now = False
    clock.tick(MAXFRAMERATE)
    