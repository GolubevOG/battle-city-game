# -*- coding:utf-8 -*-
import pygame
import time
import random


class Tank(pygame.sprite.Sprite):##танк
    def __init__(self, controls=None):
        super().__init__(all_sprites)
        if not controls:##если не назначены кнопки (т.е. если танк - враг)
            self.group = sprites_enemy
            self.x = random.choice((60, 442))
            self.y = 60
            self.hp = random.randint(1, 2)
            self.color = ('', 'gray', 'pink')[self.hp]
        else:##если этот танк - танк игрока
            self.group = sprites_my
            if len(sprites_my) == 0:
                self.x = 92
                self.spawn_x = 204
                self.color = 'yellow'
            else:
                self.x = 92
                self.spawn_x = 304
                self.color = 'green'
            self.y = 60
            self.spawn_y = 444
            self.hp = 3
            self.controls = {
                'up': controls[0],
                'down': controls[1],
                'left': controls[2],
                'right': controls[3],
                'shoot': controls[4]
            }
        self.add(self.group)
        self.img = pygame.transform.scale(
                                          pygame.image.load("images/{}_tank_up_level1.png".format(self.color)),
                                          (64, 30)
        )
        self.frames = []##картинки
        self.bullets = pygame.sprite.Group()##пули
        self.max_bullets = 1##максимальное количество пуль от данного танка
        self.level = 1##первоначальный уровень
        self.cut_sheet(self.img, 2, 1)
        self.cur_frame = 0##изначальное выбирается какой именно картинкой будет танк(изначально 0-вверх дуло направлено)
        self.image = self.frames[self.cur_frame]##собственно присваевается именно нужная картинка
        self.rect = self.rect.move(self.x, self.y)##первоначальный прямоугольник с координатами заданными
        self.compas = "up"##первоначальное направление - вверх
        self.go = False##можно ли идти вперед
        self.x_speed, self.y_speed = 0, 0##первоначальные скорости по координатам


    def cut_sheet(self, sheet, columns, rows):##разрезаем картинку по количеству столбоцв и строк
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):##обновление
        if self.go:
            self.rect.x += self.x_speed#добавляется скорость по х
            self.rect.y += self.y_speed#добавляется скорость по у
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]##меняется изображение если танк едет вперед

    def direction(self, key):##направление
        x, y = self.rect.x, self.rect.y
        img = pygame.transform.scale(
            pygame.image.load("images/{}_tank_{}_level{}.png".format(self.color, key, self.level)),
            (64, 30))
        self.cut_sheet(img, 2, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.frames = self.frames[-2:]
        self.compas = key##меняем картинку там чтобы шины двигались все такое

    def move(self, g):
        if self.hp > 0:##если еще живой
            self.x_speed, self.y_speed = 0, 0##скорость по координатам х и у делаем 0 и 0
            if g == "up":
                self.y_speed -= 8##скорость по координате у делаем равной 8(дивжется вверх)
            if g == "down":
                self.y_speed += 8##скорость по координате у делаем равной 8(дивжется вниз)
            if g == "right":
                self.x_speed += 8##скорость по координате x делаем равной 8(дивжется вправо)
            if g == "left":
                self.x_speed -= 8##скорость по координате x делаем равной 8(дивжется влево)
            self.rect.x += self.x_speed ##перемещаемся
            self.rect.y += self.y_speed
            h = 0
            if self.group == sprites_enemy:
                for sp in sprites_enemy:
                    k = pygame.sprite.spritecollideany(sp, self.group)
                    if k and k != sp:
                        h += 1
            if pygame.sprite.groupcollide(self.group, sprites_barrier, False, False) or pygame.sprite.groupcollide(
                    self.group, borders, False, False) or (
                                self.group != sprites_my and pygame.sprite.groupcollide(self.group, sprites_my, False,
                                                                                    False) or h) or (
                            self.group != sprites_enemy and pygame.sprite.groupcollide(self.group, sprites_enemy, False,
                                                                                   False)):
                ##проверка можно ли идти вперед
                #print('USA', self.group)
                self.rect.x -= self.x_speed
                self.rect.y -= self.y_speed
                self.go = False
                self.x_speed, self.y_speed = 0, 0
            else:
                self.go = True
            self.rect.x -= self.x_speed
            self.rect.y -= self.y_speed

    def shoot(self, group):##выстрел
        if self.compas == "up":
            x_bullet, y_bullet = self.rect.x + 13, self.rect.y + 2##первоначальные координаты пули
        if self.compas == "right":
            x_bullet, y_bullet = self.rect.x + 28, self.rect.y + 13
        if self.compas == 'left':
            x_bullet, y_bullet = self.rect.x + 2, self.rect.y + 13
        if self.compas == "down":
            x_bullet, y_bullet = self.rect.x + 13, self.rect.y + 28
        Bullet(self.compas, x_bullet, y_bullet, group, self.bullets)

    def level_up(self):##повышение уровня
        self.level += 1

    def spawn(self):##появление
        self.rect.y = self.spawn_y
        self.rect.x = self.spawn_x
    '''
    def spawn_1(self):##появление
        self.rect.y = 444
        self.rect.x = 188 + 16 + 50
    '''


class Bullet(pygame.sprite.Sprite):##пуля
    def __init__(self, compas, x, y, group, group2):
        super().__init__(all_sprites)
        self.add(group)
        self.add(group2)
        self.compas = compas
        self.image = pygame.transform.scale(pygame.image.load("images/bullet.png"), (4, 4))##присвоение картинки и уменьшение ее до 4*4 пикселя
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):##движение 
        x, y = 0, 0
        if self.compas == "up":##вверх
            y -= 6
        if self.compas == "down":##вниз
            y += 6
        if self.compas == "right":##вправо
            x += 6
        if self.compas == "left":##влево
            x -= 6
        self.rect.x += x
        self.rect.y += y

    def update(self):
        self.move()


class Gift(pygame.sprite.Sprite):##подарок, который не работает, так что разбираться в нем я, конечно же, не буду
    def __init__(self):
        super().__init__(all_sprites)
        self.add(gifts)
        self.image = pygame.transform.scale(pygame.image.load("images/star.png"), (32, 32))
        self.rect = self.image.get_rect()
        x, y = 0, 0
        for i in range(13):
            for j in range(13):
                self.rect.x = i * 32 + 60
                self.rect.y = j * 32 + 60
            if not pygame.sprite.groupcollide(gifts, all_sprites, True, False):
                x, y = i * 32 + 60, j * 32 + 60
        self.rect.x, self.rect.y = x, y
        print(self.rect.x, self.rect.y)

    def update(self):
        pass


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(borders)
        self.image = pygame.transform.scale(pygame.image.load("images/border.png"), (x2, y2))##вот такой серенький фон сзади
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1


class Stage(pygame.sprite.Sprite):
    def __init__(self, group, x, y, img, a, b):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("images/{}.png".format(img)), (a, b))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def render(self):
        global k1
        self.rect.y -= 2
        if self.rect.y <= 250:
            k1 = False


class Wall(pygame.sprite.Sprite):
    def __init__(self, group, x, y, img):
        super().__init__(all_sprites)
        self.add(group)
        self.add(sprites_barrier)
        if img == "wall":
            self.add(sprites_wall)
        if img == "grass":
            self.add(sprites_grass)
        self.image = pygame.transform.scale(pygame.image.load("images/{}.png".format(img)), (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = 16 * x + 60
        self.rect.y = 16 * y + 60


class Game(pygame.sprite.Sprite):
    def __init__(self, group, img):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("images/{}".format(img)), (416, 132))
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = -150

    def render(self):
        global k, k1
        self.rect.y += 2
        if self.rect.y >= 70:
            k = False


def end_game(r, scr, score):
    global do, k, W, H
    k = True
    do1 = True
    # g2 = pygame.sprite.Group()
    gg = pygame.transform.scale(pygame.image.load("images/game_over.png"), (165, 90))
    while do1:
        scr.blit(gg, ((W - 165) // 2, (H - 90) // 2))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                do1 = False
                do = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_t:
                do1 = False
        # g2.draw(scr)
        pygame.display.flip()


def main():
    global k, k1, screen, g, s, borders, buttons, sprites_wall, sprites_enemy, do, if_paused
    if_paused = False
    k = True
    k1 = True
    screen = pygame.display.set_mode((W, H))
    screen.fill((0, 0, 0))
    running = True
    g = pygame.sprite.Group()
    game = Game(g, "battle_city.jpg")
    s = pygame.sprite.Group()
    tank1 = Tank([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE])##это наш танк
    #tank_beta = Tank(sprites_my, 0, 0, yel_up, "yellow", 2, 1, 3)##это second танк
    tank1.spawn()##заспавнили
    tank2 = Tank([pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_RETURN])
    tank2.spawn()
    #tank_beta.spawn_1()
    score = 0
    tanks_killed = 0
    game_over = False
    stage = Stage(s, (W - 205) // 2, 550, 'stage', 205, 40)##первоначальная кнопка выбора уровня
    one = Stage(s, (W - 40) // 4, 600, 'one', 40, 45)## первый уровень
    two = Stage(s, (W - 45) // 4 * 2, 600, 'two', 45, 45)## второй уровень
    three = Stage(s, (W - 45) // 4 * 3, 600, 'three', 40, 45)## третий уровень
    our_level = 0
    borders = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    Border(0, 0, W, 60)
    Border(0, 0, 60, H)
    Border(0, H - 60, W, 60)
    Border(W - 60, 0, 60, H)
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                do = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = event.pos ##определение куда именно попал щелчок
                if one.rect.x < a[0] and one.rect.x + one.rect[2] > a[0] and one.rect.y < a[1] and one.rect.y + \
                        one.rect[3] > a[1]:## если попал на первую кнопку
                    our_level = 1
                if two.rect.x < a[0] and two.rect.x + two.rect[2] > a[0] and two.rect.y < a[1] and two.rect.y + \
                        two.rect[3] > a[1]:##если попал на вторую
                    our_level = 2
                if three.rect.x < a[0] and three.rect.x + three.rect[2] > a[0] and three.rect.y < a[
                    1] and three.rect.y + three.rect[3] > a[1]: ## если на третью
                    our_level = 3
        if k:
            game.render()
        if k1:
            stage.render()
            one.render()
            two.render()
            three.render()
        g.draw(screen)
        s.draw(screen)
        if our_level != 0:
            running = False
        time.sleep(0.01)

    if do:
        Stage(the_flag, 12 * 16 + 60, 24 * 16 + 60, 'flag', 32, 32)
        board = open("board{}.txt".format(our_level)).read().split('\n')## открываем тот текстовый фойл, в котором хранится информация о нужном нам поле и превращаем его в двумерный массив
        walls = []
        sprites_wall = pygame.sprite.Group()
        sprites_enemy = pygame.sprite.Group()
        images = {"1": "wall", "2": "water", "3": "grass", "4": "flag"}
        for i in range(26):
            for j in range(26):
                if board[i][j] != '0':
                    walls.append(Wall(sprites_barrier, j, i, images[board[i][j]]))##добавляем тот объект, который указан по уровню
        replay = Stage(buttons, W - 200, H - 50, 'restart', 149, 44)##добавляем кнопки
        pause = Stage(buttons, W - 360, H - 50, 'pause', 151, 44)
        replay.add(all_sprites)
        pause.add(all_sprites)
        running = True
        gift = None
    screen.fill((0, 0, 0))
    while running:
        tank1.go = False
        tank2.go = False ##малююююююююсенькая незаметная строчка, отвечающая за то, чтобы танк не уезжал за пределы экрана, когда не надо
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):##если нажимаем на крестик то выходим
                do = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:##если нажимаем на кнопку мышки
                a = event.pos##считываем позицию куда нажили
                if replay.rect.x < a[0] and replay.rect.x + replay.rect[2] > a[0] and replay.rect.y < a[
                    1] and replay.rect.y + replay.rect[3] > a[1]:
                    running = False ## начинаем все с самого начала, даже выбираем заново уровень
                if pause.rect.x < a[0] and pause.rect.x + pause.rect[2] > a[0] and pause.rect.y < a[
                    1] and pause.rect.y + pause.rect[3] > a[1]:
                    pause.image = pygame.transform.scale(pygame.image.load("images/{}.png".format('play')), (92, 44))
                    pygame.display.flip()
                    if_paused = True ## ставим на паузу
            '''
            if event.type == pygame.KEYDOWN:##если нажимаем на любую кнопку
                if event.key == pygame.K_SPACE and len(tank1.bullets) < tank1.max_bullets:##если нажали на пробел и число пуль не превысило максимум
                    tank1.shoot(sprites_bullet)## создаем пулю
                if event.key == pygame.K_UP:##если нажали вверх
                    tank1.direction("up")##меняем направление на вверх
                elif event.key == pygame.K_DOWN:##если нажали вниз
                    tank1.direction("down")##меняем направление на вниз
                elif event.key == pygame.K_LEFT:##если нажали влево
                    tank1.direction("left")##меняем направление на влево
                elif event.key == pygame.K_RIGHT:##если нажали вправо
                    tank1.direction("right")##меняем направление на вправо

                elif event.key == tank2.controls['up']:
                    tank2.direction('up')
                elif event.key == tank2.controls['down']:
                    tank2.direction('down')
                elif event.key == tank2.controls['left']:
                    tank2.direction('left')
                elif event.key == tank2.controls['right']:
                    tank2.direction('right')
            '''

        while if_paused:##пока находимся в состоянии паузы
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):##если выходим
                    do = False
                    running = False
                    if_paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:##если нажимаем на кнопку мышки
                    a = event.pos## считываем ее позицию
                    if replay.rect.x < a[0] and replay.rect.x + replay.rect[2] > a[0] and replay.rect.y < a[
                        1] and replay.rect.y + replay.rect[3] > a[1]:
                        running = False##начинаем сначала
                        if_paused = False
                    if pause.rect.x < a[0] and pause.rect.x + pause.rect[2] > a[0] and pause.rect.y < a[
                        1] and pause.rect.y + pause.rect[3] > a[1]:
                        pause.image = pygame.transform.scale(pygame.image.load("images/{}.png".format('pause')),
                                                             (151, 44))
                        pygame.display.flip()
                        if_paused = False##снимаем с паузы
            borders.draw(screen)
            all_sprites.draw(screen)
            pygame.display.flip()

        keys = pygame.key.get_pressed()##читываем куда мы нажимаем и соответсвенно двигаемся в соответсвующем направлении
        for pressed_direction in ['up', 'down', 'left', 'right']:
            if keys[tank1.controls[pressed_direction]]:
                tank1.direction(pressed_direction)
                tank1.move(pressed_direction)
            if keys[tank2.controls[pressed_direction]]:
                tank2.direction(pressed_direction)
                tank2.move(pressed_direction)
        if keys[tank1.controls['shoot']] and len(tank1.bullets) < tank1.max_bullets:
            tank1.shoot(sprites_bullet)
        if keys[tank2.controls['shoot']] and len(tank2.bullets) < tank2.max_bullets:
            tank2.shoot(sprites_bullet)
        
        if len(sprites_enemy) < 4:## если вражеских танчиков меньше 4 то генерируем новый
            h = random.randint(0, 30)
            if h == 7 or h == 8:##если случайное число это 7 или 8, то появляется танк
                sp = Tank()
            coll = 0
            for t in sprites_enemy:
                if pygame.sprite.collide_rect(t, sp):
                    coll += 1
                if coll > 1:
                    sp.kill()
        for t in sprites_enemy:
            if pygame.sprite.spritecollide(t, sprites_bullet, True):##если пулька попала во вражеский танк, то минус жизнь
                t.hp -= 1
                if t.hp == 1:
                    t.color = "gray"
                    score += 150
                    t.direction(t.compas)
            if t.hp == 0:
                t.image = pygame.transform.scale(pygame.image.load("images/{}.png".format('boom1')), (32, 32))##если застрелили, то происхожит взрыв1
                sprites_enemy.draw(screen)
                tanks_killed += 1
                score += 100
                t.hp -= 1
            if t.hp <= 0:
                t.hp -= 1
            if t.hp == -2:
                t.image = pygame.transform.scale(pygame.image.load("images/{}.png".format('boom')), (32, 32))##взрыв2
                sprites_enemy.draw(screen)
            if t.hp == -3:
                t.image = pygame.transform.scale(pygame.image.load("images/{}.png".format('boom3')), (32, 32))##взрыв3
                sprites_enemy.draw(screen)
                t.kill()##наконец-то убиваем танк
            if not t.go:##если не можем идти вперед, меняем направление
                d = ["up", "down", "left", "right"][random.randint(0, 3)]
                t.direction(d)
                t.move(d)
            else:##идем вперед
                t.move(t.compas)
            if len(t.bullets) < t.max_bullets:##если они выпустили меньше чем максимальное число пуль, то кто-нибудь стреляет и то, не факт
                sh = random.randint(0, 20)
                if sh == 3:
                    t.shoot(sprites_en_bullet)

        if tanks_killed == 16 and not gift:##сесли убито 16 танков и еще не выдли подарок
            x, y = 0, 0
            while not gift:
                gift = Gift()
            for i in range(x, 13):
                for j in range(y, 13):
                    x, y = i, j
                    gift.rect.x = i * 32 + 60
                    gift.rect.y = j * 32 + 60
                if pygame.sprite.groupcollide(gifts, all_sprites, False, False):
                    gift.kill()
            print(x, y)
        ##если наша пуля попала куда-то:
        pygame.sprite.groupcollide(sprites_bullet, sprites_wall, True, True)
        pygame.sprite.groupcollide(sprites_bullet, borders, True, False)
        pygame.sprite.groupcollide(sprites_bullet, sprites_grass, True, False)
        ##если вражеская пуля попала куда-то
        pygame.sprite.groupcollide(sprites_en_bullet, sprites_wall, True, True)
        pygame.sprite.groupcollide(sprites_en_bullet, borders, True, False)
        pygame.sprite.groupcollide(sprites_en_bullet, sprites_grass, True, False)
        if pygame.sprite.groupcollide(sprites_en_bullet, sprites_my, True, False):##если вражеская пуля попала в меня то минус жизнь и к началу позиция танка
            tank1.hp -= 0.5
            tank1.spawn()
            tank2.hp -= 0.5
            tank2.spawn()
        if pygame.sprite.groupcollide(sprites_en_bullet, the_flag, True, False) or pygame.sprite.groupcollide(
                sprites_bullet, the_flag, True, False):##если кто-то попал во флаг, то конец
            for i in the_flag:
                i.image = pygame.transform.scale(pygame.image.load("images/{}.png".format('dead_flag')), (32, 32))
                pygame.display.flip()
                
                game_over = "lose"
                running = False
        if tank1.hp <= 0:
            game_over = "lose"
            running = False
        if tanks_killed == 16:
            game_over = "win"
            running = False

        borders.draw(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        sprites_bullet.update()
        sprites_en_bullet.update()
        mini_tanks.draw(screen)
        the_flag.draw(screen)
        clock.tick(10)
        pygame.display.flip()

    all_sprites.empty()
    sprites_barrier.empty()
    sprites_wall.empty()
    sprites_grass.empty()

    sprites_enemy.empty()
    tank1.group.empty()
    mini_tanks.empty()
    sprites_bullet.empty()
    sprites_en_bullet.empty()
    if game_over:
        end_game(game_over, screen, score)


pygame.init()
W, H = 32 * 13 + 120, 32 * 13 + 120
do = True
all_sprites = pygame.sprite.Group()

walls = []
sprites_barrier = pygame.sprite.Group()
sprites_wall = pygame.sprite.Group()
sprites_my = pygame.sprite.Group()
sprites_bullet = pygame.sprite.Group()
sprites_en_bullet = pygame.sprite.Group()
sprites_grass = pygame.sprite.Group()
sprites_enemy = pygame.sprite.Group()
gifts = pygame.sprite.Group()
mini_tanks = pygame.sprite.Group()
the_flag = pygame.sprite.Group()
clock = pygame.time.Clock()
while do:
    main()
pygame.quit()
