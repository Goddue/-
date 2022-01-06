import os
import sys
import pygame
from Player import Player
from Tile import Tile

pygame.init()
maps = 'menu.map'
size = WIDTH, HEIGHT = 640, 640
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
player_speed = 16


def load_image(name, colorkey=None):
    fullname = os.path.join('data1', name)
    # если файл не существует, то выходим
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
    return image


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
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


tile_images = {
    'wall': [load_image('box.png')],
    'empty': [load_image('grass.png')],
    'pit': [load_image('pit.png')],
    'exit': [load_image('exit2.png')],
    'choose': [load_image('level1.png')]
}

player_image = load_image('mar.png')

tile_width = tile_height = 64


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
boxs_group = pygame.sprite.Group()
choose_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
pits_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(tile_images['empty'], x, y, tile_height, [all_sprites, tiles_group])
            elif level[y][x] == '#':
                Tile(tile_images['wall'], x, y, tile_height, [all_sprites, boxs_group])
            elif level[y][x] == '@':
                Tile(tile_images['empty'], x, y, tile_height, [all_sprites, tiles_group])
                new_player = Player(player_image, x * tile_width + 16, y * tile_height + 16,
                                    player_speed, [all_sprites, player_group])
            elif level[y][x] == 'p':
                Tile(tile_images['pit'], x, y, tile_height, [all_sprites, pits_group])
            elif level[y][x] == 'e':
                Tile(tile_images['exit'], x, y, tile_height, [all_sprites, exit_group])
            elif level[y][x] == 'c':
                Tile(tile_images['choose'], x, y, tile_height, [all_sprites, choose_group])
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
isMoving = False
move = 0, 0
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN and not isMoving:
            x, y = int(player.pos[0]), int(player.pos[1])
            if event.key == pygame.K_RIGHT:
                isMoving = True
                move = 1, 0
            if event.key == pygame.K_LEFT:
                isMoving = True
                move = -1, 0
            if event.key == pygame.K_DOWN:
                isMoving = True
                move = 0, 1
            if event.key == pygame.K_UP:
                isMoving = True
                move = 0, -1
    x, y = player.pos
    if isMoving:
        print('cant stop')
        print(x, y)
        player.move(move[0], move[1])
        print(move)
        print(x, y)
        if pygame.sprite.spritecollideany(player, boxs_group) or not (-1 < x + move[0] * player_speed < HEIGHT - 31 and
                                                                      -1 < y + move[1] * player_speed < WIDTH - 31):
            isMoving = 0
            player.move(move[0] * -1, move[1] * -1)
        elif pygame.sprite.spritecollideany(player, choose_group):
            isMoving = 0
            player.move(move[0] * -1, move[1] * -1)
            select_level('level1.map')
        elif pygame.sprite.spritecollideany(player, pits_group):
            select_level(maps)
        elif pygame.sprite.spritecollideany(player, exit_group):
            terminate()
        print(x, y)
    all_sprites.draw(screen)
    player_group.draw(screen)
    clock.tick(120)
    pygame.display.flip()
    clock.tick(FPS)
