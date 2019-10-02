# -*- coding: utf-8 -*-
import pygame #импортируем сторонние библиотеки
import time
import random


class Tank(pygame.sprite.Sprite):#создаем отвечающий за танки класс дочерний от спрайта
    def __init__(self, group, x, y, img, color, columns, rows, hp):
        super().__init__(all_sprites)# с помощью класса супер мы используем методы родительского класса если при обращении функция будет искаться по алгоритму то сначала все связанное с спрайтами будет искать в братьях а потом уже в родителе
        self.add(group)# добавляем танк к команде танков указанной в вводимых переменных
        self.g = group # в переменную движения танка так же записываем групу
        self.color = color#цвет танка = тип танка
        self.frames = []# массив с картинками
        self.bullets = pygame.sprite.Group()#делаем пули так же спрайтами
        self.max_bullets = 1#максимальное количество пуль
        self.level = 1#устанавливаем начальный уровень
        self.hp = hp #устанавливаем здоровье через вводимую в танк переменную
        self.cut_sheet(img, columns, rows) # в переменную - будущую функцию записиваем вводимые переменные
        self.cur_frame = 0 #переменная текущий фрейм на ноль
        self.image = self.frames[self.cur_frame] # пишем в переменную картинку из массива которую контролируем 3 переменной
        self.rect = self.rect.move(x, y) #назначаем на рект движение на х у
        self.directi = "up"#переменная движения для пули
        self.go = False #переменной присваеваем фолз
        self.xm, self.ym = 0, 0 # отдельные переменные координат на ноль

    def cut_sheet(self, sheet, columns, rows):# брезаем изображение в 2 раза
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)#делаем рект пайгеймовским ректом и в размеры ставим размер изображения в пропорции
        for j in range(rows):
            for i in range(columns):# циклы
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))# в массив с картинками добавляем созданный с помощью subsurface наследную копию ректангла с нужным размером и изображением

    def update(self): # если го имеет позицию тру то к координатам ректа прибавляем координаты-переменные
        if self.go:
            self.rect.x += self.xm
            self.rect.y += self.ym
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)#изменяем текущий фрейм на плюс 1 и получаем остаток от деления его номера на все изображения
            self.image = self.frames[self.cur_frame]#изображением становится элемент массива под номером текущий фрейм

    def direction(self, key):
        x, y = self.rect.x, self.rect.y #обновленные переменные кооринат становятся координатами для движения
        img = pygame.transform.scale(
            pygame.image.load("data/{}_tank_{}_level{}.png".format(self.color, key, self.level)),
            (64, 30))# изменяем изображение нужного танка на размер 64 30
        self.cut_sheet(img, 2, 1) # это изображение обрезаем в 2 раза
        self.cur_frame = 0 # обновляем переменную на 0
        self.image = self.frames[self.cur_frame] #в переменную изображения пишем самое первое изображение в массиве
        self.rect = self.rect.move(x, y) # рект делаем снова движением а не изображением 
        self.frames = self.frames[-2:] # оставляем в массиве только два последних изображения 
        self.directi = key # ставим переменную для направления стрельбы в нужную позицию

    def move(self, g):
        if self.hp > 0:#если танк жив
            self.xm, self.ym = 0, 0 # координирующие переменные обнуляем 
            if g == "up":# в зависимости от направления задаем переменные для движения 
                self.ym -= 8
            if g == "down":
                self.ym += 8
            if g == "right":
                self.xm += 8
            if g == "left":
                self.xm -= 8
            self.rect.x += self.xm#корректируем координаты остановки для проверки на врезания
            self.rect.y += self.ym
            h = 0#переменная новая на ноль 
            if self.g == sprites_enemy:# если двигается враг то 
                for sp in sprites_enemy:# каждый враг из их множества
                    k = pygame.sprite.spritecollideany(sp, self.g) # если кто то из них пересекается с другим 
                    if k and k != sp: # и такие вообще есть а так же не пересекают самих себя 
                        h += 1#переменная увеличивается 
            if pygame.sprite.groupcollide(self.g, sprites_barrier, False, False) or pygame.sprite.groupcollide(
                    self.g, borders, False, False) or (
                                self.g != sprites_my and pygame.sprite.groupcollide(self.g, sprites_my, False,
                                                                                    False) or h) or (
                            self.g != sprites_enemy and pygame.sprite.groupcollide(self.g, sprites_enemy, False,
                                                                                   False)):# если движущийся танк уткнулся в стену или если движется враг и он уткнулся в наш танк или были столкновения между врагами или движется наш танк и он уткнулся во врага 
                self.rect.x -= self.xm# делаем откат
                self.rect.y -= self.ym
                self.go = False#а gо меняем на фолз и в апдейте никто не движется
                self.xm, self.ym = 0, 0# обнуляем координирующие переменные
            else:
                self.go = True# иначе даем добро на обновление 
            self.rect.x -= self.xm#а затем делаем откат
            self.rect.y -= self.ym

    def shoot(self, group):#в зависимости направления пули даем корректированниые координаты для красивого движения пули и команду 
        if self.directi == "up":
            x1, y1 = self.rect.x + 13, self.rect.y + 2
        if self.directi == "right":
            x1, y1 = self.rect.x + 28, self.rect.y + 13
        if self.directi == 'left':
            x1, y1 = self.rect.x + 2, self.rect.y + 13
        if self.directi == "down":
            x1, y1 = self.rect.x + 13, self.rect.y + 28
        Bullet(self.directi, x1, y1, group, self.bullets)# и затем отправляем по нужным координатам пулю

    def level_up(self):# увеличение уровня 
        self.level += 1

    def spawn(self):# спавн нашего танка
        if self.g == sprites_my:
            self.rect.y = 444
            self.rect.x = 188 + 16


class Bullet(pygame.sprite.Sprite):#теперь пуля
    def __init__(self, d, x, y, group, group2):
        super().__init__(all_sprites)
        self.add(group)# у пули есть команда и добавляем ее в нужную команду
        self.add(group2)
        self.directi = d# направление
        self.image = pygame.transform.scale(pygame.image.load("data/bullet.png"), (4, 4))#картинка нужного размера
        self.rect = self.image.get_rect()# ну и наш дорогой рект с его координатами 
        self.rect.x = x
        self.rect.y = y

    def move(self):# простое движение с скоростью 6 пикселей в обновление
        x, y = 0, 0
        if self.directi == "up":
            y -= 6
        if self.directi == "down":
            y += 6
        if self.directi == "right":
            x += 6
        if self.directi == "left":
            x -= 6
        self.rect.x += x
        self.rect.y += y

    def update(self):# при обновлении двигаем пулю 
        self.move()


class Gift(pygame.sprite.Sprite):# подарочек
    def __init__(self):
        super().__init__(all_sprites)
        self.add(gifts)# к спрайтам добавляем подарок
        self.image = pygame.transform.scale(pygame.image.load("data/star.png"), (32, 32))#картинка подарка нужного размера 
        self.rect = self.image.get_rect()#наш рект
        x, y = 0, 0
        for i in range(13):# циклы 
            for j in range(13):
                self.rect.x = i * 32 + 60#рандомный спавн подарка 
                self.rect.y = j * 32 + 60
            if not pygame.sprite.groupcollide(gifts, all_sprites, True, False):# если нет пересечений со всеми спрайтами то добро на спавн
                x, y = i * 32 + 60, j * 32 + 60
        self.rect.x, self.rect.y = x, y
        #print(self.rect.x, self.rect.y)

    def update(self):# при апдейте проходим уровень 
        pass


class Border(pygame.sprite.Sprite):#граница
    def __init__(self, x1, y1, x2, y2):
        super().__init__(borders)
        self.image = pygame.transform.scale(pygame.image.load("data/border.png"), (x2, y2))#картинка по указанным размерам
        self.rect = self.image.get_rect()#рект для картинки
        self.rect.x = x1
        self.rect.y = y1


class Stage(pygame.sprite.Sprite):#надпись стэйдж
    def __init__(self, group, x, y, img, a, b):# присваеваем ее к нужной группе спрайтов
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("data/{}.png".format(img)), (a, b))# подстраиваем под указанный размер
        self.rect = self.image.get_rect()# рект под размер
        self.rect.x = x
        self.rect.y = y

    def render(self):# прорисовка
        global k1
        self.rect.y -= 2# выезжание надписи пока не на месте 
        if self.rect.y <= 250:
            k1 = False


class Wall(pygame.sprite.Sprite):#стена
    def __init__(self, group, x, y, img):
        super().__init__(all_sprites)
        self.add(group)#добавляем сначала в указанную группу
        self.add(sprites_barrier)# а потом в спрайты-барьеры
        if img == "wall":#если это просто  бомже-стена то кидаем еще и в спрайты стены
            self.add(sprites_wall)
        if img == "grass":#иначе в траву
            self.add(sprites_grass)
        self.image = pygame.transform.scale(pygame.image.load("data/{}.png".format(img)), (16, 16))# получаем нужное изображение
        self.rect = self.image.get_rect()# и рект со сложными координатами
        self.rect.x = 16 * x + 60
        self.rect.y = 16 * y + 60


class Game(pygame.sprite.Sprite):#класс игра 
    def __init__(self, group, img):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("data/{}".format(img)), (416, 132))# изображение игра на начальном экране
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = -150

    def render(self):# такой же понтоватый рендер как и у стэйдж вы не подумайте что я не уважаю человека писавшего просто сейчас 1 ночи и мне надо себя развлекать
        global k, k1
        self.rect.y += 2
        if self.rect.y >= 70:
            k = False


def end_game(r, scr, score):#наконец-то пошли функции управления игрой
    global do, k, W, H#сандартные глобалы
    k = True
    do1 = True
    # g2 = pygame.sprite.Group()
    gg = pygame.transform.scale(pygame.image.load("data/game_over.png"), (165, 90))# подготовливаем картинку с проигранной игрой 
    while do1:# пока ду1 тру
        scr.blit(gg, ((W - 165) // 2, (H - 90) // 2))  # прорисовываем поверх основной плоскости в какой-то не столь отдаленной местности
        for e in pygame.event.get():#если в последовательности последних действий нажата кнопка выхода
            if e.type == pygame.QUIT:
                do1 = False# то оба ду меняем на фолс
                do = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_t:# если же была  нажата клавиша t  
                do1 = False# то фолс только ду1
        # g2.draw(scr)
        pygame.display.flip()#обновляем честь экрана
    do1 = True# и так понятно
    if do:#если ду остался тру
        while do1:# если ду1 тру
            scr.fill((0, 0, 0))#наполняем черным плоскость
            scr.blit(gg, ((W - 165) // 2, 0))#выталкиваем проигрышь
            for e in pygame.event.get():#если была нажата кнопка выхода то ду1 и ду фолс
                if e.type == pygame.QUIT:
                    do1 = False
                    do = False

                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:#если же был нажат пробел то только ду1 фолс
                    do1 = False
            font = pygame.font.Font(None, 50)#настройки для надписей ты проиграл или ты выиграл и твой счет
            text = font.render("You {}".format(r), 1, (100, 255, 100))
            text_x = W // 2 - text.get_width() // 2
            text_y = H // 2 - text.get_height() // 2
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
            font = pygame.font.Font(None, 50)
            text = font.render("Your score {}".format(score), 1, (200, 255, 150))
            text_x = W // 2 - text.get_width() // 2
            text_y = H // 2 + text.get_height() + 10
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
            pygame.display.flip()# обновляем часть экрана


def main():#главная программа
    global k, k1, screen, g, s, borders, buttons, sprites_wall, sprites_enemy, do, if_paused# всякие глобалы
    if_paused = False#всякие логические установки
    k = True
    k1 = True
    screen = pygame.display.set_mode((W, H))#возводим экран
    screen.fill((0, 0, 0))#наполняем его черным
    running = True#логические установки
    g = pygame.sprite.Group()#g делаем спрайтом
    game = Game(g, "battle_city.jpg")#главная картинка игры
    s = pygame.sprite.Group()#с тоже спрайт
    tank1 = Tank(sprites_my, 92, 60, yel_up, "yellow", 2, 1, 3)#задаем главны танк
    tank1.spawn()#спавним его
    score = 0#установки очков на ноль
    tanks_killed = 0
    game_over = False#игра не проиграна
    stage = Stage(s, (W - 205) // 2, 550, 'stage', 205, 40)#картинки с выборами уровня
    one = Stage(s, (W - 40) // 4, 600, 'one', 40, 45)
    two = Stage(s, (W - 45) // 4 * 2, 600, 'two', 45, 45)
    three = Stage(s, (W - 45) // 4 * 3, 600, 'three', 40, 45)
    our_level = 0
    borders = pygame.sprite.Group()#границы-спрайты
    buttons = pygame.sprite.Group()# кнопнки-спрайты
    Border(0, 0, W, 60)#границы по границе поля БАДУМТС
    Border(0, 0, 60, H)
    Border(0, H - 60, W, 60)
    Border(W - 60, 0, 60, H)
    while running:#пока играем
        pygame.display.flip()#обновляем часть экрана
        for event in pygame.event.get():#рассматриваем пооследовательность последних клавиш
            if event.type == pygame.QUIT:#если нажали выход то все ливаем
                do = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:#если куда-то кто-то тыкнул мышкой
                a = event.pos#на а вешаем место куда кто-то тыкнул
                if one.rect.x < a[0] and one.rect.x + one.rect[2] > a[0] and one.rect.y < a[1] and one.rect.y + \
                        one.rect[3] > a[1]:#если тыкнул на 1 то 1 лвл аналогично со 2 и 3
                    our_level = 1
                if two.rect.x < a[0] and two.rect.x + two.rect[2] > a[0] and two.rect.y < a[1] and two.rect.y + \
                        two.rect[3] > a[1]:
                    our_level = 2
                if three.rect.x < a[0] and three.rect.x + three.rect[2] > a[0] and three.rect.y < a[
                    1] and three.rect.y + three.rect[3] > a[1]:
                    our_level = 3
        if k:#если тру то запускаем шарманку
            game.render()
        if k1:
            stage.render()
            one.render()
            two.render()
            three.render()
        g.draw(screen)#присваиваем их как спрайты для взаимодействий
        s.draw(screen)
        if our_level != 0:# если уровень не 0 то убираем меню 
            running = False
        time.sleep(0.01)# спим

    if do:# есои ду еще тру
        Stage(the_flag, 12 * 16 + 60, 24 * 16 + 60, 'flag', 32, 32)#спавним флаг где надо
        board = open("board{}.txt".format(our_level)).read().split('\n')#читаем расстановку уровня 
        walls = []#массив со стенами
        sprites_wall = pygame.sprite.Group()#стены и враги спрайты
        sprites_enemy = pygame.sprite.Group()
        images = {"1": "wall", "2": "water", "3": "grass", "4": "flag"}# соответствие между номерами и объектами
        for i in range(26):#циклы
            for j in range(26):
                if board[i][j] != '0':#если элемент в расстановке доски не 0 то
                    walls.append(Wall(sprites_barrier, j, i, images[board[i][j]]))#в массив сиен с нужными для прорисови параметрами записываем элемент
        replay = Stage(buttons, W - 200, H - 50, 'restart', 149, 44)# кнопки рестарт и пауза
        pause = Stage(buttons, W - 360, H - 50, 'pause', 151, 44)
        replay.add(all_sprites)#добавляем их во всех спрайтов
        pause.add(all_sprites)
        running = True#раннинг снова тру
    screen.fill((0, 0, 0))#скрин черный
    while running:#цикл
        tank1.go = False# го у нашего танка фолс поэтому он стоит
        screen.fill((0, 0, 0))# черный экран
        for event in pygame.event.get():# чекаем нажмаемые клавиши
            if event.type == pygame.QUIT:#если выход то ливаем
                do = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:#если мышка нажала на что то
                a = event.pos#пишем место куда она нажала в а 
                if replay.rect.x < a[0] and replay.rect.x + replay.rect[2] > a[0] and replay.rect.y < a[
                    1] and replay.rect.y + replay.rect[3] > a[1]:#если попала в спрайт реплей о раннинг фолс
                    running = False
                if pause.rect.x < a[0] and pause.rect.x + pause.rect[2] > a[0] and pause.rect.y < a[
                    1] and pause.rect.y + pause.rect[3] > a[1]:#если попала в паузу то меняем паузу на плей и обновляем экран и меняем переменную на фолс
                    pause.image = pygame.transform.scale(pygame.image.load("data/{}.png".format('play')), (92, 44))
                    pygame.display.flip()
                    if_paused = True
            if event.type == pygame.KEYDOWN:# если нажимали на клавиатуру то 
                if event.key == pygame.K_SPACE and len(tank1.bullets) < tank1.max_bullets:#если тыкнули на пробел то стреляем
                    tank1.shoot(sprites_bullet)
                if event.key == pygame.K_UP:#если кнопки направления то выполняем функцию направления
                    tank1.direction("up")
                elif event.key == pygame.K_DOWN:
                    tank1.direction("down")
                elif event.key == pygame.K_RIGHT:
                    tank1.direction("right")
                elif event.key == pygame.K_LEFT:
                    tank1.direction("left")

        while if_paused:# если прожали паузу то 
            for event in pygame.event.get():#чекаем если нажали на выход то ливаем
                if event.type == pygame.QUIT:
                    do = False;
                    running = False;
                    if_paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:# чекаем если нажали 
                    a = event.pos# пишем данные в а 
                    if replay.rect.x < a[0] and replay.rect.x + replay.rect[2] > a[0] and replay.rect.y < a[
                        1] and replay.rect.y + replay.rect[3] > a[1]:#если попали в реплей то раннинг фолс и паузу отжимаем
                        running = False;
                        if_paused = False
                    if pause.rect.x < a[0] and pause.rect.x + pause.rect[2] > a[0] and pause.rect.y < a[
                        1] and pause.rect.y + pause.rect[3] > a[1]:#если попал по продолжению то отжимаем паузу и меняем кнопку и отрисовываем часть экрана
                        pause.image = pygame.transform.scale(pygame.image.load("data/{}.png".format('pause')),
                                                             (151, 44))
                        pygame.display.flip()
                        if_paused = False
            borders.draw(screen)#рисуем границы
            all_sprites.draw(screen)#рисуем всех остальных спрайтов
            pygame.display.flip()# отрисовываем часть экрана как апдейт
        keys = pygame.key.get_pressed()#получаем в кейс последовательность которая говорит про каждую клавишу на клавиатуре нажата он или нет
        if keys[pygame.K_DOWN]:#в зависимости от того какая клавиша направления нажата поворачиваем танк туда и двигаем 
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
        if len(sprites_enemy) < 4:# если врагов меньше 4
            h = random.randint(0, 30)# рандомим число ш
            col = ["gray", "pink"][random.randint(0, 1)]# рандомим вид танка
            hp = {"gray": 1, "pink": 2}[col]# здоровье у серого противника 1 у  розового 2
            if h == 7:
                img = pygame.transform.scale(pygame.image.load("data/{}_tank_up_level1.png".format(col)), (64, 30))#подготовливаем картинку
                sp = Tank(sprites_enemy, 60, 60, img, col, 2, 1, hp)#если нароллили 7 то спавним в один угол
            if h == 8:
                img = pygame.transform.scale(pygame.image.load("data/{}_tank_up_level1.png".format(col)),#подготовливаем кртинку
                                             (64, 30))
                sp = Tank(sprites_enemy, 442, 60, img, col, 2, 1, hp) # если нароллили 8 то спавним в другой угол
            coll = 0#переменная новая
            for t in sprites_enemy:#если 
                if pygame.sprite.collide_rect(t, sp):# если новорожденный танк более двух раз стукнулся то его попросят удалиться
                    coll += 1
                if coll > 1:
                    sp.kill()
        for t in sprites_enemy:# если кого-то из противников задела пуля то у него отимают хп  а саму пулю удаляют из спрайтов 
            if pygame.sprite.spritecollide(t, sprites_bullet, True):
                t.hp -= 1
                if t.hp == 1:# если у противника хп = 1 то он сереет и добавляет нам очков и меняет направление
                    t.color = "gray"
                    score += 150
                    t.direction(t.directi)
            if t.hp == 0:# если противник помер то его детонирует 
                t.image = pygame.transform.scale(pygame.image.load("data/{}.png".format('boom1')), (32, 32))
                sprites_enemy.draw(screen)# на плоскости перерисовывают группу противников
                tanks_killed += 1#плюс очки и убитые танки а у них минус хп
                score += 100
                t.hp -= 1
            if t.hp <= 0:# если хп мньше 0 то отимаем еще 
                t.hp -= 1
            if t.hp == -2:# если хп = -2 то детонируем противника второй раз по другому 
                t.image = pygame.transform.scale(pygame.image.load("data/{}.png".format('boom')), (32, 32))
                sprites_enemy.draw(screen)# перерисоваем противников
            if t.hp == -3:#если уж хп -3 то третий раз детонируем и удаляем ну и перерисовываем противников
                t.image = pygame.transform.scale(pygame.image.load("data/{}.png".format('boom3')), (32, 32))
                sprites_enemy.draw(screen)
                t.kill()
            if not t.go:# если противник не может куда-то пройти то рандомом поворачиваем его и еще двигаем
                d = ["up", "down", "left", "right"][random.randint(0, 3)]
                t.direction(d)
                t.move(d)
            else:#иначе просто двигаем
                t.move(t.directi)
            if len(t.bullets) < t.max_bullets:#если кол во пуль меньше максимального то стреляем на самом деле просто стреляем
                sh = random.randint(0, 20)#рандомим sh если попали в 3 то стреляем доп пулями
                if sh == 3:
                    t.shoot(sprites_en_bullet)

        if tanks_killed == 16 and not gift:# если ты завалил 16 танков и не собрал подарок то 
            x, y = 0, 0# координаты по 0
            while not gift:# пока не получил подарок 
                gift = Gift()# начинаем спавнить подарок с прверкой на не попадание в спрайты иначе уничтожаем его и принтим координаты
            for i in range(x, 13):
                for j in range(y, 13):
                    x, y = i, j
                    gift.rect.x = i * 32 + 60
                    gift.rect.y = j * 32 + 60
                if pygame.sprite.groupcollide(gifts, all_sprites, False, False):
                    gift.kill()
            #print(x, y)

        pygame.sprite.groupcollide(sprites_bullet, sprites_wall, True, True)# в зависимости от того куда ты попал либо уничтожаешь, либо нет, либо пуля уничтожается и это и для противников
        pygame.sprite.groupcollide(sprites_bullet, borders, True, False)
        pygame.sprite.groupcollide(sprites_bullet, sprites_grass, True, False)
        pygame.sprite.groupcollide(sprites_en_bullet, sprites_wall, True, True)
        pygame.sprite.groupcollide(sprites_en_bullet, borders, True, False)
        pygame.sprite.groupcollide(sprites_en_bullet, sprites_grass, True, False)
        if pygame.sprite.groupcollide(sprites_en_bullet, sprites_my, True, False):#если тебя подбили то у тебя убирают хп и переспавнивают танк
            tank1.hp -= 1
            tank1.spawn()
        if pygame.sprite.groupcollide(sprites_en_bullet, the_flag, True, False) or pygame.sprite.groupcollide(
                sprites_bullet, the_flag, True, False):# если кто то попал в твою базу даже если ты то он заменяется на уничтоженный
            for i in the_flag:
                i.image = pygame.transform.scale(pygame.image.load("data/{}.png".format('dead_flag')), (32, 32))
                pygame.display.flip()#затем обновляем часть экрана и проигрываем
                # time.sleep(5)
                game_over = "lose"
                running = False
        if tank1.hp <= 0:#если ты омер то приграл
            game_over = "lose"
            running = False
        if tanks_killed == 16:#если ты убил 16 противников то выиграл
            game_over = "win"
            running = False

        borders.draw(screen)# все снова пррисовываем по новой и обновляем 
        all_sprites.draw(screen)
        all_sprites.update()
        sprites_bullet.update()
        sprites_en_bullet.update()
        mini_tanks.draw(screen)
        the_flag.draw(screen)
        clock.tick(10)#ждем
        pygame.display.flip()#обновляем часть экрана

    all_sprites.empty()#очищаем все спрайты
    sprites_barrier.empty()
    sprites_wall.empty()
    sprites_grass.empty()

    sprites_enemy.empty()
    sprites_my.empty()
    mini_tanks.empty()
    sprites_bullet.empty()
    sprites_en_bullet.empty()
    if game_over:# если проиграл то проиграл
        end_game(game_over, screen, score)


pygame.init()#запускаем основную прогу и пишем всякие константы и спрайтв присваеваем
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
yel_up = pygame.transform.scale(pygame.image.load("data/yellow_tank_up_level1.png"), (64, 30))#ну и наш танк
clock = pygame.time.Clock()
while do:# пока do is True выполняем main
    main()
pygame.quit()#выходим их пайгейма
