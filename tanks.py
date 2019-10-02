import pygame
import time
import random


class Tank(pygame.sprite.Sprite):
    def __init__(self, group, x, y, img, color, columns, rows, hp):
        super().__init__(all_sprites)
        self.add(group)
        self.g = group
        self.color = color
        self.frames = []
        self.bullets = pygame.sprite.Group()
        self.max_bullets = 1
        self.level = 1
        self.hp = hp
        self.cut_sheet(img, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.direction_value = "up"
        self.go = False
        self.xm, self.ym = 0, 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        # divides the sheet into several rows and columns

    def update(self):
        if self.go:
            self.rect.x += self.xm
            self.rect.y += self.ym
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        # moves, changes image

    def direction(self, key):
        x, y = self.rect.x, self.rect.y
        img = pygame.transform.scale(
            pygame.image.load(f"images/{self.color}_tank_{key}_level{self.level}.png"),
            (64, 30))
        self.cut_sheet(img, 2, 1)
        # takes two frames from the image
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.frames = self.frames[-2:]
        self.direction_value = key

    def move(self, dir):
        if self.hp > 0:
            self.xm, self.ym = 0, 0
            if dir == "up":
                self.ym -= 8
            if dir == "down":
                self.ym += 8
            if dir == "right":
                self.xm += 8
            if dir == "left":
                self.xm -= 8
            self.rect.x += self.xm
            self.rect.y += self.ym
            h = 0
            if self.g == sprites_enemy:
                for sp in sprites_enemy:
                    k = pygame.sprite.spritecollideany(sp, self.g)
                    if k and k != sp:
                        h += 1
            if pygame.sprite.groupcollide(self.g, sprites_barrier, False, False) or pygame.sprite.groupcollide(
                    self.g, borders, False, False) or (
                                self.g != sprites_my and pygame.sprite.groupcollide(self.g, sprites_my, False,
                                                                                    False) or h) or (
                            self.g != sprites_enemy and pygame.sprite.groupcollide(self.g, sprites_enemy, False,
                                                                                   False)):
                self.rect.x -= self.xm
                self.rect.y -= self.ym
                self.go = False
                self.xm, self.ym = 0, 0
                # my tank doesn't move into objects (e.g. enemies)
            else:
                self.go = True
            self.rect.x -= self.xm
            self.rect.y -= self.ym

    def shoot(self, group):
        if self.direction_value == "up":
            x1, y1 = self.rect.x + 13, self.rect.y + 2
        if self.direction_value == "right":
            x1, y1 = self.rect.x + 28, self.rect.y + 13
        if self.direction_value == 'left':
            x1, y1 = self.rect.x + 2, self.rect.y + 13
        if self.direction_value == "down":
            x1, y1 = self.rect.x + 13, self.rect.y + 28
        Bullet(self.direction_value, x1, y1, group, self.bullets)
        # spawns (shots) the bullet

    def level_up(self):
        self.level += 1

    def spawn(self):
        if self.g == sprites_my:
            self.rect.y = 444
            self.rect.x = 188 + 16


class Bullet(pygame.sprite.Sprite): # a bullet
    def __init__(self, direction, x, y, group, group2):
        super().__init__(all_sprites)
        self.add(group)
        self.add(group2)
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load("images/bullet.png"), (4, 4))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        x, y = 0, 0
        if self.direction == "up":
            y -= 6
        if self.direction == "down":
            y += 6
        if self.direction == "right":
            x += 6
        if self.direction == "left":
            x -= 6
        self.rect.x += x
        self.rect.y += y
        # the bullet flies in needed direction

    def update(self):
        self.move()


class Gift(pygame.sprite.Sprite):
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


class Border(pygame.sprite.Sprite): # impassable wall
    def __init__(self, x1, y1, x2, y2):
        super().__init__(borders)
        self.image = pygame.transform.scale(pygame.image.load("images/border.png"), (x2, y2))
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1


class Stage(pygame.sprite.Sprite): # flying up text
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


class Wall(pygame.sprite.Sprite): # destroyable wall
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


class Game(pygame.sprite.Sprite): # flying down text/textures
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


def end_game(r, scr, score): # activates game over screen
    global do, k, W, H
    k = True
    do1 = True
    # g2 = pygame.sprite.Group()
    gg = pygame.transform.scale(pygame.image.load("images/game_over.png"), (165, 90))
    # Game Over text appears
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
    do1 = True
    if do:
        # if user pressed "t" or "down" shows information, else quits
        while do1:
            scr.fill((0, 0, 0))
            scr.blit(gg, ((W - 165) // 2, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    do1 = False
                    do = False

                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    do1 = False
                # quits game over screen if user pressed "space"
            font = pygame.font.Font(None, 50)
            text = font.render(f"You {r}", 1, (100, 255, 100))
            # shows "you win" or "you lose"
            text_x = W // 2 - text.get_width() // 2
            text_y = H // 2 - text.get_height() // 2
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
            # draws green text border
            font = pygame.font.Font(None, 50)
            text = font.render(f"Your score {score}", 1, (200, 255, 150))
            # shows score
            text_x = W // 2 - text.get_width() // 2
            text_y = H // 2 + text.get_height() + 10
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
            # draws green text border
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
    logo = Game(g, "battle_city.jpg")
    s = pygame.sprite.Group()
    tank1 = Tank(sprites_my, 92, 60, yel_up, "yellow", 2, 1, 3)
    tank1.spawn()
    # creates my yellow tank
    score = 0
    tanks_killed = 0
    game_over = False
    stage = Stage(s, (W - 205) // 2, 550, 'stage', 205, 40)
    one = Stage(s, (W - 40) // 4, 600, 'one', 40, 45)
    two = Stage(s, (W - 45) // 4 * 2, 600, 'two', 45, 45)
    three = Stage(s, (W - 45) // 4 * 3, 600, 'three', 40, 45)
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
            if event.type == pygame.QUIT:
                do = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = event.pos
                if one.rect.x < a[0] < one.rect.x + one.rect[2] and one.rect.y < a[1] < one.rect.y + one.rect[3]:
                    our_level = 1
                if two.rect.x < a[0] < two.rect.x + two.rect[2] and two.rect.y < a[1] < two.rect.y + two.rect[3]:
                    our_level = 2
                if three.rect.x < a[0] < three.rect.x + three.rect[2] and three.rect.y < a[1] < three.rect.y + three.rect[3]:
                    our_level = 3
                # plays the level that user clicked on
        if k:
            logo.render()
        if k1:
            stage.render()
            one.render()
            two.render()
            three.render()
        # renders flying text
        g.draw(screen)
        s.draw(screen)
        if our_level != 0:
            running = False
        time.sleep(0.01)

    if do:
        Stage(the_flag, 12 * 16 + 60, 24 * 16 + 60, 'flag', 32, 32)
        board = open(f"boards/board{our_level}.txt").read().split('\n')
        walls = []
        sprites_wall = pygame.sprite.Group()
        sprites_enemy = pygame.sprite.Group()
        images = {"1": "wall", "2": "water", "3": "grass", "4": "flag"}
        for i in range(26):
            for j in range(26):
                if board[i][j] != '0':
                    walls.append(Wall(sprites_barrier, j, i, images[board[i][j]]))
        # reads the level from the textfile
        replay = Stage(buttons, W - 200, H - 50, 'restart', 149, 44)
        pause = Stage(buttons, W - 360, H - 50, 'pause', 151, 44)
        replay.add(all_sprites)
        pause.add(all_sprites)
        # renders the buttons
        running = True
    screen.fill((0, 0, 0))
    while running:
        tank1.go = False
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                do = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = event.pos
                if replay.rect.x < a[0] < replay.rect.x + replay.rect[2] \
                    and replay.rect.y < a[1] < replay.rect.y + replay.rect[3]:
                    running = False
                if pause.rect.x < a[0] < pause.rect.x + pause.rect[2] \
                    and pause.rect.y < a[1] < pause.rect.y + pause.rect[3]:
                    pause.image = pygame.transform.scale(pygame.image.load("images/{}.png".format('play')), (92, 44))
                    pygame.display.flip()
                    if_paused = True
                    # changes pause button to play button and stops the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(tank1.bullets) < tank1.max_bullets:
                    tank1.shoot(sprites_bullet)
                if event.key == pygame.K_UP:
                    tank1.direction("up")
                elif event.key == pygame.K_DOWN:
                    tank1.direction("down")
                elif event.key == pygame.K_RIGHT:
                    tank1.direction("right")
                elif event.key == pygame.K_LEFT:
                    tank1.direction("left")
                # moves the tank

        while if_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    do = False
                    running = False
                    if_paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    a = event.pos
                    if replay.rect.x < a[0] < replay.rect.x + replay.rect[2] and replay.rect.y < a[1] < replay.rect.y + replay.rect[3]:
                        running = False
                        if_paused = False
                    if pause.rect.x < a[0] < pause.rect.x + pause.rect[2] and pause.rect.y < a[1] < pause.rect.y + pause.rect[3]:
                        pause.image = pygame.transform.scale(pygame.image.load("images/pause.png"), (151, 44))
                        pygame.display.flip()
                        if_paused = False
                        # resumes the game
            borders.draw(screen)
            all_sprites.draw(screen)
            pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            tank1.direction("down")
            tank1.move('down')
        elif keys[pygame.K_UP]:
            tank1.direction("up")
            tank1.move('up')
        elif keys[pygame.K_RIGHT]:
            tank1.direction("right")
            tank1.move('right')
        elif keys[pygame.K_LEFT]:
            tank1.direction("left")
            tank1.move('left')
        if len(sprites_enemy) < 4:
            chance_value = random.randint(0, 30)
            col = random.choice(["gray", "pink"])
            hp = {"gray": 1, "pink": 2}[col]
            if chance_value == 7:
                img = pygame.transform.scale(pygame.image.load(f"images/{col}_tank_up_level1.png"),
                                             (64, 30))
                sp = Tank(sprites_enemy, 60, 60, img, col, 2, 1, hp)
            if chance_value == 8:
                img = pygame.transform.scale(pygame.image.load(f"images/{col}_tank_up_level1.png"),
                                             (64, 30))
                sp = Tank(sprites_enemy, 442, 60, img, col, 2, 1, hp)
                # spawns enemies
            coll = 0
            for some_enemy_tank in sprites_enemy:
                if pygame.sprite.collide_rect(some_enemy_tank, sp):
                    coll += 1
                if coll > 1:
                    sp.kill()
        for some_enemy_tank in sprites_enemy:
            if pygame.sprite.spritecollide(some_enemy_tank, sprites_bullet, True):
                some_enemy_tank.hp -= 1
                if some_enemy_tank.hp == 1:
                    some_enemy_tank.color = "gray"
                    score += 150
                    some_enemy_tank.direction(some_enemy_tank.direction_value)
            if some_enemy_tank.hp == 0:
                some_enemy_tank.image = pygame.transform.scale(pygame.image.load("images/boom1.png"), (32, 32))
                sprites_enemy.draw(screen)
                tanks_killed += 1
                score += 100
                some_enemy_tank.hp -= 1
            if some_enemy_tank.hp <= 0:
                some_enemy_tank.hp -= 1
            if some_enemy_tank.hp == -2:
                some_enemy_tank.image = pygame.transform.scale(pygame.image.load("images/boom.png"), (32, 32))
                sprites_enemy.draw(screen)
            if some_enemy_tank.hp == -3:
                some_enemy_tank.image = pygame.transform.scale(pygame.image.load("images/boom3.png"), (32, 32))
                sprites_enemy.draw(screen)
                some_enemy_tank.kill()
                # kills the tank if hp<=0
            if not some_enemy_tank.go:
                direction_value = random.choice(["up", "down", "left", "right"])
                some_enemy_tank.direction(direction_value)
                some_enemy_tank.move(direction_value)
            else:
                some_enemy_tank.move(some_enemy_tank.direction_value)
            if len(some_enemy_tank.bullets) < some_enemy_tank.max_bullets:
                shoot_chance_value = random.randint(0, 20)
                if shoot_chance_value == 3:
                    some_enemy_tank.shoot(sprites_en_bullet)
                # enemy shots the bullet

        if tanks_killed == 16 and not gift:
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
            # gives the gift if 16 tanks are killed

        pygame.sprite.groupcollide(sprites_bullet, sprites_wall, True, True)
        pygame.sprite.groupcollide(sprites_bullet, borders, True, False)
        pygame.sprite.groupcollide(sprites_bullet, sprites_grass, True, False)
        pygame.sprite.groupcollide(sprites_en_bullet, sprites_wall, True, True)
        pygame.sprite.groupcollide(sprites_en_bullet, borders, True, False)
        pygame.sprite.groupcollide(sprites_en_bullet, sprites_grass, True, False)
        if pygame.sprite.groupcollide(sprites_en_bullet, sprites_my, True, False):
            tank1.hp -= 1
            tank1.spawn()
            # kills player's tank if bullet touches it
        if pygame.sprite.groupcollide(sprites_en_bullet, the_flag, True, False) \
            or pygame.sprite.groupcollide(sprites_bullet, the_flag, True, False):
            for i in the_flag:
                i.image = pygame.transform.scale(pygame.image.load("images/dead_flag.png"), (32, 32))
                pygame.display.flip()
                # time.sleep(5)
                game_over = "lose"
                running = False
                # game over if flag is destroyed
        if tank1.hp <= 0:
            game_over = "lose"
            running = False
        if tanks_killed == 16:
            game_over = "win"
            running = False
            # wins if 16 tanks are

        borders.draw(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        sprites_bullet.update()
        sprites_en_bullet.update()
        mini_tanks.draw(screen)
        the_flag.draw(screen)
        clock.tick(10)
        pygame.display.flip()
        # updates all sprites

    all_sprites.empty()
    sprites_barrier.empty()
    sprites_wall.empty()
    sprites_grass.empty()

    sprites_enemy.empty()
    sprites_my.empty()
    mini_tanks.empty()
    sprites_bullet.empty()
    sprites_en_bullet.empty()
    if game_over:
        end_game(game_over, screen, score)
    # erases all sprites, ends game


pygame.init()
W, H = 536, 536
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
yel_up = pygame.transform.scale(pygame.image.load("images/yellow_tank_up_level1.png"), (64, 30))
clock = pygame.time.Clock()
while do:
    main()
pygame.quit()
