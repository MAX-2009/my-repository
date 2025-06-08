import pygame
from pygame.math import Vector2
from random import randint #загружаем рандом для чисел
import math

class Player(pygame.sprite.Sprite):#класс игрока
    def __init__(self,image,speed,screen_width,screen_height,scale,enim,atak,aim,walk,sound):
        super().__init__()
        self.sound = sound
        self.speed = speed
        self.angle = 90
        self.drop_angle = 90#градус на котором находится шагоход на данный момент
        self.image = image#базовая картинка шагохода это первый кадр из списка кадров с шагоходом
        self.rect = image.get_rect(center=(screen_width//1.321, screen_height//1.8))#начальное местоположения шагохода 
        self.screen_width = screen_width#загружаем границы экрана
        self.screen_height = screen_height
        self.scale = scale#загружаем разрешение экрана
        self.angle = 90
        self.walk = 90     
        self.drop_angle = 90
        self.walk_angle = 90
        self.energy = 123
        self.panel_index = 0
        self.step = 0
        self.time_p = 0
        self.panel_state = 1#состояние панелей
        self.gun_state = 1#состояние пушек
        self.aim = aim#картинки прицела

        
    
        self.animation_frames = {#список всех анимаций
        'charging_process':enim,
        'atak':atak,
        'walk':walk,
            }
        self.walk_step_timer = 0
        self.walk_step = 0
        self.rate_of_fire = 0#скорость цикла для вылета следующей пули (скорострельность)

        self.bul = [0,[0,0],0,0,0,[None],[None],[None]]#характеристики зараженой пули 
        self.hp = 110
    def update(self,screen,bt,mouse_x,mouse_y,bullets,bult):

        if self.bul[0] == 0:#если у нас нету пуль то 
            self.bul[-1] = None#ключь пули равен (None/отсутствует)

        self.angle_mouse = math.degrees(math.atan2(mouse_y - self.rect.y - 70, mouse_x - self.rect.x - 70))#вычисляем где находится курсор мыши относительно игрока
        self.purpose(bt)
        if ((any((bt[key] for key in (pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_w))) or pygame.mouse.get_pressed()[0])  and self.energy > 2 ):#условие проверяет (если нажата любая клавиша для движения) или (если нажата левая кнопка мыши)
            self.turn()
            if (any((bt[key] for key in (pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_w)))):#условие для запуска анимации шагания

                    self.walk_animation(len(self.animation_frames['walk'])-1)
                    self.walk_step_timer = self.walk_step_timer + 1
                    self.movement(bt)  

                    self.energy = self.energy - 0.1

        if self.gun_state == 3 and pygame.mouse.get_pressed()[2] and self.bul[0] > 0:#если состояние пушек (выдвинуты) и у нас есть патроны и нажата ПКМ
            self.rate_of_fire = self.rate_of_fire + self.bul[2]#скорость вылета следующей пули


            if self.rate_of_fire > 50:
                self.rate_of_fire = 0
                self.bul[-1].play() 
                for i in range (1, self.bul[3]+1):
                   
                    x_x = randint(mouse_x-self.bul[4]*round(self.scale), mouse_x+self.bul[4]*round(self.scale))#создаём разброс вылетающих пуль 
                    y_y = randint(mouse_y-self.bul[4]*round(self.scale), mouse_y+self.bul[4]*round(self.scale))
                    speed = randint(self.bul[1][0]-5, self.bul[1][0]+5)#скорость пуль
                    createBullet(bullets,self.rect.x,self.rect.y,self.bul[-2],x_x, y_y,speed,self.bul[1][1],self.rect,self.scale)#создаём пули



                self.bul[0] = self.bul[0] - 1#уменьшаем количество заряженых пуль 
        self.image = self.animation(bt,mouse_x,mouse_y,screen)


        drop_surf_rotated2 = pygame.transform.rotate(self.image, -self.drop_angle - 90)#шагоход всегда должен иметь сторону в которую он повёрнут  
        walk_surf_rotated3 = pygame.transform.rotate(self.animation_frames['walk'][self.walk_step], -self.walk_angle - 90)#сторона в которую направлены ноги шагохода

        self.draw(screen,drop_surf_rotated2,walk_surf_rotated3)#отображаем шагоход и его ноги

    def movement(self,bt):#функция для движения шагохода по экрану при вызове функции указываем колизию шагохода и его скорость
            dx = 0#скорость по x
            dy = 0#скорость по y
            if bt[pygame.K_a]:#нажата кнопка "a"
                dx =- self.speed
            if bt[pygame.K_d]:#нажата кнопка "d"
                dx =+ self.speed
            if bt[pygame.K_w]:#нажата кнопка "w"
                dy =- self.speed
            if bt[pygame.K_s]:#нажата кнопка "s"
                dy =+ self.speed
           
            self.rect.x += int(dx* self.scale)
            self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))#шагоход по оси x может быть только в диапазоне экрана
            self.rect.y +=  int(dy* self.scale)
            self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))#шагоход по оси y может быть только в диапазоне экран

    def purpose(self,bt):#функция установки цели поворота (устанавливает цель для будущего поворота шагохода)
            if bt[pygame.K_a]:#нажата кнопка "a"
                if self.angle > 0: #если ваш шагоход смотрит вверх и вы решили двигатся в лево то шагоход будет поворачиватся против часовой стрелки в левую сторону
                    self.angle = 180#угол к которому должен стремится шагоход
                    self.walk = 180#угол к которому должны поворачиватся ноги шагохода
                else:#если шагоход смотрит вниз то он будет поворачиватся по часовой стрелке в левую сторону
                    self.angle = -180 #угол к которому должен стремится шагоход
                    self.walk = -180#угол к которому должны поворачиватся ноги шагохода




            elif bt[pygame.K_d]:#нажата кнопка "d"
                self.angle = 0#угол к которому должен стремится шагоход
                self.walk = 0#угол к которому должны поворачиватся ноги шагохода

            if bt[pygame.K_w]:#нажата кнопка "w"
                self.angle = -90#угол к которому должен стремится шагоход
                self.walk = -90#угол к которому должны поворачиватся ноги шагохода

            elif bt[pygame.K_s]:#нажата кнопка "s"
                self.angle = 90#угол к которому должен стремится шагоход
                self.walk = 90#угол к которому должны поворачиватся ноги шагохода


            if pygame.mouse.get_pressed()[0]:# условие если нажата ЛКМ
                self.angle = self.angle_mouse#цель к которой должен стремится шагоход равен положению мыши (шагоход поворачивается к курсору)
            return self.angle

    def turn(self):#функция стремление к цели (стремится к цели не меняя саму цель)
            if self.angle == self.drop_angle:#если поворот шагохода равен углу к которому он должен стримится то он перестаёт поворачиватся
                    pass
            if self.drop_angle < self.angle:#если цель поворота выше то шагоход постепенно стримится к нему (создавая анимацию постепенного поворота)
                    self.drop_angle = self.drop_angle + 5#шагоход постепенно поворачивается в сторону цели
            if self.drop_angle > self.angle:#если цель поворота ниже то шагоход постепенно стримится к нему (создавая анимацию постепенного поворота)
                    self.drop_angle = self.drop_angle - 5#шагоход постепенно поворачивается в сторону цели


            if self.angle <= -90 and self.drop_angle >  90:
                    self.drop_angle = self.drop_angle + 10
            elif self.angle >= 90 and self.drop_angle < -90:
                    self.drop_angle = self.drop_angle - 10
            #эта чать предназначена для того чтобы шагоход поворачивался к цели коротким путём (по часовой стрелке или против часовой стрелки)


            if self.drop_angle > 180:
                self.drop_angle = -180
            elif self.drop_angle < -180:
                self.drop_angle = 180
            #эта часть отвечает за то чтобы drop_angl при поворотe не был равен (от -бесконечности до -180) и не был равен (от 180 до бесконечности)



            #ниже всё тоже самое но с ногами
            if self.walk == self.walk_angle:
                pass
            if self.walk_angle < self.walk:
                    self.walk_angle = self.walk_angle + 5
            if self.walk_angle > self.walk:
                    self.walk_angle = self.walk_angle - 5
            if self.walk <= -90 and self.walk_angle >  90:
                    self.walk_angle = self.walk_angle + 10
            elif self.walk >= 90 and self.walk_angle < -90:
                    self.walk_angle = self.walk_angle - 10
                    
            if self.walk_angle > 180:
                self.walk_angle = -180
            elif self.walk_angle < -180:
                self.walk_angle = 180
    def walk_animation(self,num):
        if self.walk_step_timer > 4:

            self.walk_step_timer = 0
            if self.walk_step < num:
                self.walk_step = self.walk_step +  1
            else:
                self.walk_step = 0
                self.sound['walk'].play()



    def animation(self,bt,mouse_x,mouse_y,screen):
        self.time_p = self.time_p - 1
        TOOL_STATE_close = 1
        TOOL_STATE_opening = 2
        TOOL_STATE_open = 3
        TOOL_STATE_closing = 4
        frames = None
        if self.time_p < -10:
                self.time_p = 0
                self.panel_index = self.panel_index + self.step   


        if bt[pygame.K_e] and self.gun_state == TOOL_STATE_close:
            if self.panel_state == TOOL_STATE_close:
                self.step = -1
                self.panel_state = TOOL_STATE_opening
            if self.panel_state == TOOL_STATE_open:
                self.step = 1
                self.panel_state = TOOL_STATE_closing
        if self.panel_index <= -(len(self.animation_frames["charging_process"]))and self.panel_state == TOOL_STATE_opening:
                    self.panel_state = TOOL_STATE_open
                    self.panel_index = 1
                    self.step = 0
        if self.panel_index >= (len(self.animation_frames["charging_process"]))and self.panel_state == TOOL_STATE_closing:
                    self.panel_state = TOOL_STATE_close
                    self.panel_index = 0
                    self.step = 0
        if self.panel_state == TOOL_STATE_open and self.energy < 123: 
            self.energy = self.energy + 0.5         



        if self.gun_state == TOOL_STATE_open and not pygame.mouse.get_pressed()[0]:
                self.step = 1
                self.gun_state = TOOL_STATE_closing  
        if pygame.mouse.get_pressed()[0] and (self.gun_state == TOOL_STATE_close)  and self.panel_state == TOOL_STATE_close:
                self.step = -1
                self.gun_state = TOOL_STATE_opening
        if self.panel_index <= -(len(self.animation_frames["atak"]))and self.gun_state == TOOL_STATE_opening:
                    self.gun_state = TOOL_STATE_open
                    self.panel_index = 1
                    self.step = 0
        if self.panel_index >= (len(self.animation_frames["atak"]))and self.gun_state == TOOL_STATE_closing :
                    self.gun_state = TOOL_STATE_close
                    self.panel_index = 0
                    self.step = 0

        if (self.panel_state == TOOL_STATE_close or self.panel_state == TOOL_STATE_open) and (self.panel_index == 2 or self.panel_index == -2) and self.time_p == -5:
                    self.sound['gun_ready'].play()
        

        if self.gun_state == TOOL_STATE_open:
            screen.blit(self.aim[-1],(mouse_x-23, mouse_y-23))
        elif self.gun_state == TOOL_STATE_closing or self.gun_state == TOOL_STATE_opening:
            screen.blit(self.aim[0],(mouse_x-23, mouse_y-23))



        if self.gun_state != 1:
            frames = 'atak'
        if self.panel_state != 1:
            frames = 'charging_process'
        if frames != None:
            return  self.animation_frames[frames][self.panel_index]
        else:
            return self.animation_frames['charging_process'][0]

    def draw(self, screen, drop_surf_rotated2,walk_surf_rotated3):
        screen.blit(walk_surf_rotated3, self.rect)
        screen.blit(drop_surf_rotated2, self.rect)



    
class Bullet (pygame.sprite.Sprite):
        def __init__(self,x,y,image,mouse_x, mouse_y,bullet_speed,ror,dam,group):
            pygame.sprite.Sprite.__init__(self)#создание спрайта
            self.image = image#загружаем картинку
            self.rect = self.image.get_rect(center=(x, y))#создаём объект по загруженым координатам (x, y)
            self.add(group)#добавляем объект в группу
            self.mouse_x = mouse_x
            self.mouse_y = mouse_y
            self.bullet_speed = bullet_speed
            self.pos = Vector2(x, y)#дробные координаты
            self.vector = Vector2(0, 0)#вектор скорости
            self.bullet_damage = dam    
        def update(self,scale):
            self.move_towards_player(scale)         
        def move_towards_player(self,scale):#функция преследования врага за игроком
            dx = self.mouse_x - self.rect.x
            dy = self.mouse_y - self.rect.y
            distance = Vector2(dx, dy).length()
            if distance > 20:#проверяем, что игрок не находится в той же точке, что и враг
                direction = Vector2(dx, dy).normalize()#нормализация вектора
                self.vector = direction * self.bullet_speed*scale
                self.pos += self.vector
                self.rect.center = (int(self.pos.x), int(self.pos.y))
            else:
                self.kill()#уничтожаем пулю
        def check_collision(self, enemies):
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    #обработка столкновения
                    self.kill()#уничтожаем пулю
                    break#не проверяем другие враги, если уже уничтожили одного

def createBullet(group,x,y,image,mouse_x, mouse_y,bullet_speed,dam,player,scale):
    x,y = player.x+50*scale, player.y+50*scale
    return Bullet(x, y,image,mouse_x, mouse_y,bullet_speed,player,dam,group)
