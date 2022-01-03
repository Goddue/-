import os
import sys
import pygame
from Player import Player
from Tile import Tile

pygame.init()
if len(sys.argv) > 1:
    maps = sys.argv[1]
else:
    maps = 'map.map'
size = WIDTH, HEIGHT = 640, 640
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


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
    'exit': [load_image('exit.png')]
}

player_image = load_image('mar.png')

tile_width = tile_height = 64


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(tile_images['empty'], x, y, tile_height, [all_sprites, tiles_group])
            elif level[y][x] == '#':
                Tile(tile_images['wall'], x, y, tile_height, [all_sprites, tiles_group])
            elif level[y][x] == '@':
                Tile(tile_images['empty'], x, y, tile_height, [all_sprites, tiles_group])
                new_player = Player(player_image, x, y, tile_height, [all_sprites, player_group])
            elif level[y][x] == 'p':
                Tile(tile_images['pit'], x, y, tile_height, [all_sprites, tiles_group])
            elif level[y][x] == 'e':
                Tile(tile_images['exit'], x, y, tile_height, [all_sprites, tiles_group])
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


running = True
player, level_x, level_y = generate_level(load_level(maps))
level_map = load_level(maps)
start_screen()
isMoving = False
move = 0, 0
lmove = 0, 0
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN and not isMoving:
            x, y = int(player.pos[0]), int(player.pos[1])
            if event.key == pygame.K_RIGHT and level_map[y][x + 1] in ['.', '@']:
                if x < level_x - 1:
                    isMoving = True
                    move = 1, 0
            if event.key == pygame.K_LEFT and level_map[y][x - 1] in ['.', '@']:
                if x > 0:
                    isMoving = True
                    move = -1, 0
            if event.key == pygame.K_DOWN and level_map[y + 1][x] in ['.', '@']:
                if y < level_y - 1:
                    isMoving = True
                    move = 0, 1
            if event.key == pygame.K_UP and level_map[y - 1][x] in ['.', '@']:
                if y > 0:
                    isMoving = True
                    move = 0, -1
    x, y = player.pos
    if isMoving:
        if int(x) != x or int(y) != y or level_map[int(y) + move[1]][int(x) + move[0]] in ['.', '@']:
            player.move(move[0], move[1], lmove)
            print('cant stop')
        elif level_map[int(y) + move[1]][int(x) + move[0]] == 'p':
            all_sprites = pygame.sprite.Group()
            tiles_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            player, level_x, level_y = generate_level(load_level(maps))
            level_map = load_level(maps)
            isMoving = False
            move = 0, 0
            lmove = 0, 0
        elif level_map[int(y) + move[1]][int(x) + move[0]] == 'e':
            terminate()
        else:
            print('stop')
            if move[0] != 0:
                lmove = move[0], lmove[1]
            if move[1] != 0:
                lmove = lmove[0], move[1]
            move = 0, 0
            isMoving = False

    all_sprites.draw(screen)
    player_group.draw(screen)
    clock.tick()
    pygame.display.flip()
    clock.tick(FPS)
