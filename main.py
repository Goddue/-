import os
import sys
import pygame
from Player import Player
from Tile import Tile
from Chooser import Chooser
from Particle import Particle

pygame.init()
pygame.mixer.init()
maps = 'menu.map'
scale = 2
size = WIDTH, HEIGHT = 64 * 12 * scale, 64 * 7 * scale
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
player_speed = 16
FPS = 64
tick = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data1', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    return image


def terminate():
    pygame.quit()
    pygame.mixer.quit()
    sys.exit()


def start_screen():
    intro_text = ["Hola)", '',
                  'Нажмите любую кнопку, чтобы продолжить']

    fon = pygame.transform.scale(load_image('mar.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('#7ba9c2'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 500
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def death_screen():
    death_sound.play()
    intro_text = ["(", '',
                  'Нажмите любую кнопку, чтобы попытаться заново', '',
                  'Нажмите ESC, чтобы выйти']

    fon = pygame.transform.scale(load_image('mard.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('#7ba9c2'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 500
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    terminate()
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data1/" + filename
    # читаем уровень, убирая символы перевода строки
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except FileNotFoundError as e:
        print('Ошибка')
        terminate()

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def create_particles(position):
    Particle(position, fire, [all_sprites, particles_group])


death_sound = pygame.mixer.Sound('data1/Default.wav')
box_sound = pygame.mixer.Sound('data1/Default2.wav')
move_sound = pygame.mixer.Sound('data1/Default3.wav')

tile_images = {
    'wall': [load_image('box2.png')],
    'empty': [load_image('grass.png')],
    'pit': [load_image('pit.png')],
    'exit': [load_image('exit.png')],
    'choose': [load_image('level1.png'), load_image('level2.png'), load_image('level3.png'), load_image('level4.png'),
               load_image('level5.png')],
    'arrows': [load_image('arws.png')]
}
fire = [load_image("particle.png"), load_image("particle3.png"),
        load_image("particle4.png")]
player_image = [load_image('marmove.png'), load_image('bmarmove.png')]
tile_width = tile_height = 64 * scale


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
boxs_group = pygame.sprite.Group()
choose_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
pits_group = pygame.sprite.Group()
particles_group = pygame.sprite.Group()
arws_group = pygame.sprite.Group()
crackd_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile(tile_images['empty'], x * tile_width, y * tile_height, [all_sprites, tiles_group])
            if level[y][x] == '#':
                Tile(tile_images['wall'], x * tile_width, y * tile_height, [all_sprites, boxs_group])
            elif level[y][x] == '@':
                Tile(tile_images['empty'], x * tile_width, y * tile_height, [all_sprites, tiles_group])
                new_player = Player(player_image, x * tile_width + 32, y * tile_height + 32,
                                    player_speed, [all_sprites, player_group])
            elif level[y][x] == 'p':
                Tile(tile_images['pit'], x * tile_width, y * tile_height, [all_sprites, pits_group])
            elif level[y][x] == 'e':
                Tile(tile_images['exit'], x * tile_width, y * tile_height, [all_sprites, exit_group])
            elif level[y][x] == 'a':
                Tile(tile_images['arrows'], x * tile_width, y * tile_height, [all_sprites, arws_group])
            elif level[y][x] == 'c' and maps == 'menu.map':
                Chooser(tile_images['choose'], x * tile_width, y * tile_height,
                        ['level' + str(len(choose_group)) + '.map', 'level' + str(len(choose_group) + 1) + '.map'],
                        [all_sprites, choose_group])
    return new_player, x, y


def read_saves():
    try:
        with open('data1/save.txt', 'r') as file:
            unlocked = [line.strip() for line in file]
            return unlocked
    except FileNotFoundError as e:
        with open('data1/save.txt', 'w') as file:
            file.writelines('level1.map\n')
            return ['level0.map']


def save_game(level):
    if level not in unlocked_levels:
        try:
            with open('data1/save.txt', 'w') as file:
                file.writelines('\n'.join(unlocked_levels) + '\n' + level)
        except FileNotFoundError as e:
            terminate()


def select_level(level):
    global all_sprites, player, level_x, level_y, level_map, isMoving, move, maps
    for i in all_sprites:
        i.kill()
    player, level_x, level_y = generate_level(load_level(level))
    level_map = load_level(level)
    isMoving = False
    move = 0, 0
    maps = level
    print(True)


running = True
player, level_x, level_y = generate_level(load_level(maps))
level_map = load_level(maps)
start_screen()
box_collide = 0
isMoving = False
move = 0, 0
can_move = 0
unlocked_levels = read_saves()
saving = 'level0.map'
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN and (not isMoving or pygame.sprite.spritecollideany(player, arws_group)):
            x, y = int(player.pos[0]), int(player.pos[1])
            if event.key == pygame.K_RIGHT:
                isMoving = True
                move = 1, 0
            elif event.key == pygame.K_LEFT:
                isMoving = True
                move = -1, 0
            elif event.key == pygame.K_DOWN:
                isMoving = True
                move = 0, 1
            elif event.key == pygame.K_UP:
                isMoving = True
                move = 0, -1
            elif event.key == pygame.K_r:
                select_level(maps)
                death_screen()
                continue
            else:
                continue
            move_sound.play()
            player.rotate(move)
    x, y = player.pos
    if isMoving:
        player.move(move[0], move[1])
        if not (-1 < x + move[0] * player_speed // FPS < WIDTH - 48 and
                -1 < y + move[1] * player_speed // FPS < HEIGHT - 48):
            isMoving = 0
            player.move(move[0] * -1, move[1] * -1)
            box_sound.play()
        elif pygame.sprite.spritecollideany(player, boxs_group):
            isMoving = 0
            player.move(move[0] * -1, move[1] * -1)
            box_sound.play()
        elif pygame.sprite.spritecollideany(player, choose_group):
            for i in choose_group:
                if pygame.sprite.spritecollideany(i, player_group):
                    print(unlocked_levels, i.level)
                    if i.level in unlocked_levels:
                        select_level(i.level)
                        saving = i.save
        elif pygame.sprite.spritecollideany(player, pits_group):
            select_level(maps)
            death_screen()
        elif pygame.sprite.spritecollideany(player, arws_group):
            isMoving = False
            player.move(move[0] * 5, move[1] * 5)
            for i in arws_group:
                if pygame.sprite.spritecollideany(i, player_group):
                    i.kill()
        elif pygame.sprite.spritecollideany(player, exit_group):
            if maps == 'menu.map':
                terminate()
            maps = 'menu.map'
            select_level('menu.map')
            print(saving)
            save_game(saving)
            unlocked_levels = read_saves()
            print(unlocked_levels)
        else:
            box_collide = 0
        print(x, y)
        if x % 32 == 0 and y % 32 == 0 and isMoving:
            create_particles((x + 16 * move[0] * -1, y + 16 * move[1] * -1))
    else:
        player.cur_frame = 4
        player.image = player.frames[player.cur_frame]
    for i in particles_group:
        if pygame.sprite.spritecollideany(i, player_group) and i.tick > 50:
            i.kill()
    particles_group.update()
    all_sprites.draw(screen)
    boxs_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
