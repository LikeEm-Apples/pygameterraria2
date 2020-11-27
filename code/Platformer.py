###########
#TERRARPYA#
###########
import pygame, sys, os, random, noise, json
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')

#main menu ui
buttons = [
    pygame.image.load('title_screen/Join World.png'),
    pygame.image.load('title_screen/Load World.png'),
    pygame.image.load('title_screen/New World.png'),
    pygame.image.load('title_screen/Settings.png'),
    pygame.image.load('title_screen/Credits.png')
]
buttons_pos = [
    (90, 50),
    (90, 79),
    (90, 108),
    (15, 165),
    (157, 165)
]
buttons_press = [
    False,
    False,
    False,
    False,
    False
]
def mouse_pos(WINDOW_SIZE): #returns mouse position relative to game surface
    mos_x, mos_y = pygame.mouse.get_pos()
    x_pos = mos_x / (WINDOW_SIZE[0] / 300)
    y_pos = mos_y / (WINDOW_SIZE[1] / 200)
    return x_pos, y_pos
def menu_main(display, WINDOW_SIZE):
    results = ['none']
    display.fill((146,244,255)) # clear screen by filling it with blue
    #checking if mouse over button
    mos_x, mos_y = mouse_pos(WINDOW_SIZE)
    for button in buttons:
        x_len = button.get_width()
        y_len = button.get_height()
        button_x = buttons_pos[buttons.index(button)][0]
        button_y = buttons_pos[buttons.index(button)][1]
        if mos_x > button_x and (mos_x < button_x + x_len):
            x_inside = True
        else:
            x_inside = False
        if mos_y > button_y and (mos_y <button_y + y_len):
            y_inside = True
        else:
            y_inside = False
        if x_inside and y_inside:
            buttons_press[buttons.index(button)] = True
        else:
            buttons_press[buttons.index(button)] = False
    #draws buttons
    for i in range (5):
        if not buttons_press[i]:
            display.blit(buttons[i], (buttons_pos[i][0],buttons_pos[i][1]))
        else:
            display.blit(pygame.transform.scale(buttons[i], (132,28)), (buttons_pos[i][0],buttons_pos[i][1]))

    for event in pygame.event.get():
        #close game (x button)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #on mouse click
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons_press:
                    if button:
                        results = mainMenuButtonEvent(buttons_press.index(button))

    return results

start_world = False
def mainMenuButtonEvent(button):
    global start_world
    results = ['none']
    if button == 0: #join world
        print('join world')
    elif button == 1: #load world
        print('load world')
    elif button == 2: #new world
        ('new world')
        start_world = True
        # create_world('My World', ())
        # results = ['createWorld', 'My World']
    elif button == 3: #settings
        print('settings')
    elif button == 4: #credits
        print('credits')
    return results

WINDOW_SIZE = (1280,720)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0,0]

CHUNK_SIZE = 16

seed = float(random.random()/10)
# print(seed)


dirt1_img = pygame.image.load('blocks\dirt1.png')
dirt2_img = pygame.image.load('blocks\dirt2.png')
dirt3_img = pygame.image.load('blocks\dirt3.png')
plant_img = pygame.image.load('blocks\plant.png')
grass1_img = pygame.image.load('blocks\grass1.png')
grass2_img = pygame.image.load('blocks\grass2.png')
grass3_img = pygame.image.load('blocks\grass3.png')
sand1_img = pygame.image.load('blocks\sand1.png')
sand2_img = pygame.image.load('blocks\sand2.png')
sand3_img = pygame.image.load('blocks\sand3.png')
stone1_img = pygame.image.load('blocks\stone1.png')
stone2_img = pygame.image.load('blocks\stone2.png')
stone3_img = pygame.image.load('blocks\stone3.png')

def generate_chunk(x,y):
    chunk_data = []
    global chunk

    biome = float(random.randint(1,10))
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            height = int(noise.pnoise1(target_x * seed, repeat=9999999) * 5)
            if biome > 5: # GENERATE PURITY
                if target_y == 8 - height:
                    grass_type = random.randint(1,3)
                    if grass_type == 1:
                        tile_type = 1 # grass
                    elif grass_type == 2:
                        tile_type = 10 # grass 2
                    elif grass_type == 3:
                        tile_type = 11 # grass 3
                if target_y > 8 - height:
                    dirt_type = random.randint(1,3)
                    if dirt_type == 1:
                        tile_type = 2 # dirt
                    elif dirt_type == 2:
                        tile_type = 6 # dirt 2
                    elif dirt_type == 3:
                        tile_type = 7 # dirt 3
                if target_y == 8 - height - 1:
                    if random.randint(1,5) == 1:
                        tile_type = 3 # plant
            elif biome <= 5: # GENERATE DESERT
                if target_y == 8 - height:
                    sand_type = random.randint(1,3)
                    if sand_type == 1:
                        tile_type = 4 # sand
                    elif sand_type == 2:
                        tile_type = 12 # sand 2
                    elif sand_type == 3:
                        tile_type = 13
                if target_y > 8 - height:
                    stone_type = random.randint(1,3)
                    if stone_type == 1:
                        tile_type = 5 # stone
                    elif stone_type == 2:
                        tile_type = 8 # stone 2
                    elif stone_type == 3:
                        tile_type = 9 # stone 3

            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
                chunk = chunk_data
            #with open('data.txt', 'w') as world:
                #json.dump(chunk_data, world)

    return chunk_data

global tile_rects
mouse_img = pygame.image.load('mouse.png')

def mine(tiles):
    mos_x, mos_y = mouse_pos(WINDOW_SIZE)
    mouse_rect = pygame.Rect(mos_x,mos_y,1,1)
    mine_list = ()
    for block in tiles:
        if mouse_rect.colliderect(block):
            mine_list = block
            print(tiles[0][0],tiles[0][1])
    return mine_list



global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame


animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,7,40])

game_map = {}

tile_index = {1:grass1_img,
              2:dirt1_img,
              3:plant_img,
              4:sand1_img,
              5:stone1_img,
              6:dirt2_img,
              7:dirt3_img,
              8:stone2_img,
              9:stone3_img,
              10:grass2_img,
              11:grass3_img,
              12:sand2_img,
              13:sand3_img
              }

#jump_sound = pygame.mixer.Sound('sounds\jump.wav')
grass_sounds = [pygame.mixer.Sound('sounds\grass_0.wav'),pygame.mixer.Sound('sounds\grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0

player_rect = pygame.Rect(100,100,14,30)

parallax_farthest = pygame.image.load('background\parallax0.png')
parallax_2 = pygame.image.load('background\parallax1.png')
mountains = pygame.image.load('background\parallax3.png')
parallax_farthest_x = 120
parallax_farthest_y = 10
parallax_2_x = 300
parallax_2_y = 80
background_objects = [[0.25,[parallax_farthest_x,parallax_farthest_y]],[0.5,[parallax_2_x,parallax_2_y]]]

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
# title screen
title_screen = pygame.image.load('title_screen_placeholder.png')


start = False

while not start:
    menu_event = menu_main(display, WINDOW_SIZE)
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.time.wait(1)
    if start_world == True:
        start = True
    pygame.display.flip()
bg_scroll = 0
# game loop
while True:
    display.blit(parallax_farthest,(0,0)) # background

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #pygame.draw.rect(display,(7,80,75))

    for background_object in background_objects:
        horizontal_parallax = background_object[1][0]-scroll[0]*background_object[0]
        slow_horizontal_parallax = background_object[1][0]-scroll[0]*background_object[0]/2
        vertical_parallax = background_object[1][1]-scroll[1]*background_object[0]
        if background_object[0] == 0.5:
            display.blit(parallax_2, (slow_horizontal_parallax-bg_scroll,0))
    display.blit(mountains,(horizontal_parallax,-75))
    bg_scroll += 0.1
    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
                if tile[1] in [1,2,5,4,6,7,8,9,10,11,12,13]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))


    mos_x, mos_y = mouse_pos(WINDOW_SIZE)
    display.blit(mouse_img,(mos_x,mos_y))

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_d or event.key == K_RIGHT:
                moving_right = True
            if event.key == K_a or event.key == K_LEFT:
                moving_left = True
            if event.key == K_SPACE or event.key == K_UP:
                print("Jumped")
                if air_timer < 6:
                    #jump_sound.play()
                    vertical_momentum = -5
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mine(tile_rects)
        if event.type == KEYUP:
            if event.key == K_d or event.key == K_RIGHT:
                moving_right = False
            if event.key == K_a or event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
