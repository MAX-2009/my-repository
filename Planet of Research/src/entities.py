
import pygame #загружаем модуль pygame
import os #загружаем модуль os
from random import randint #загружаем рандом для чисел
import math#загружаем модуль матиматики
from pygame.math import Vector2
import random
class Enemy(pygame.sprite.Sprite):#создаем класс Enemy
    def __init__(self, surf, x, y,animation_speed,enemy_speed, random_object,index_object,scale,screen,ded,enemy_sound, group):#передаём в класс переменные
        pygame.sprite.Sprite.__init__(self)#создание спрайта
        self.sound = enemy_sound
        self.image = surf#загружаем картинку
        self.rect = self.image.get_rect(center=((x*scale, y*scale)))#создаём объект по загруженым координатам (x, y)
        self.pos = Vector2(x, y) #дробные координаты
        self.add(group)#добавляем объект в группу
        self.timer = 0#таймер для анимации
        self.screen = screen
        self.index = 0#переменная индекса для зацикленной анимации
        self.animation_frames = random_object[0]#список кадров объекта который мы получили из функции createEnemy
        self.index_object = index_object
        self.over_time = animation_speed
        self.enemy_speed = enemy_speed * scale#сокрость передвижения врага по экрану зависит от размера экрана
        self.ded = random_object[2]
        self.vector = Vector2(0, 0)#вектор скорости
        self.scale = scale
        self.health = 100
        self.atak_fram = random_object[1]
        self.distance = 1000
        self.im = random_object[0][0]
        self.group = group


        
    def update(self,y1, x1,drop_rect,scale,*args):#update входит в базовый класс Sprite и отвечает за его обновление
        if self.health > 0:       
            self.timer = self.timer - 1#бесконечно идущий таймер       
            self.move_towards_player(drop_rect)       
            pygame.draw.rect(self.screen, (1,1,1), (self.rect.x, self.rect.y, 103 * self.scale, 9 * self.scale))#отображаем шкалу энергии
            pygame.draw.rect(self.screen, (200,1,1), (self.rect.x+2*self.scale, self.rect.y+2*self.scale, self.health * self.scale, 6 * self.scale))#отображаем шкалу энергии
        else:
            self.image = pygame.transform.rotate(self.ded,  -self.rotation + 90)
            
    def animation_enemy(self,frames,drop_rect):
        self.rotation = math.degrees(math.atan2(self.rect.y - drop_rect.y, self.rect.x - drop_rect.x))#положение врага относительно шагохода записываем в переменную
        if self.timer<-self.over_time:#если таймер стал меньше -5:
            self.timer = 0#обновляем таймер
            self.index = (self.index + 1) % (len(frames))#индекс становиться выше (если индекс стал выше len(списка) то благодаря "%" индекс становится обратно нулём)
            self.im = frames[self.index]
        self.image = pygame.transform.rotate(self.im,  -self.rotation + 90)#картинка меняется с помощью индексации из списка
        if self.index_object == 'Angry_Fly' and self.distance < 100*self.scale and self.index == 1 and self.timer == 0:
            self.sound['fly_attack'].play()
    def move_towards_player(self, drop_rect):#функция преследования врага за игроком
        dx = drop_rect.x - self.rect.x
        dy = drop_rect.y - self.rect.y
        self.distance = Vector2(dx, dy).length()
        if self.distance >= 100 *  self.scale:  # Проверяем, что игрок не находится в той же точке, что и враг
            self.animation_enemy(self.animation_frames,drop_rect)
            direction = Vector2(dx, dy).normalize() # Нормализация вектора
            self.vector = direction * self.enemy_speed
            self.pos += self.vector
            self.rect.center = (int(self.pos.x * self.scale), int(self.pos.y * self.scale))
        else:
            self.animation_enemy(self.atak_fram,drop_rect)   
         
def createEnemy(group,enemy_frames,screen_height,scale,drop_rect,screen,ded,enemy_sound):#функция для создание нового объекта в классе
    enemy_speed = randint(1, 2)
    animation_speed = randint(1, 4)
    random_object = random.choice(list(enemy_frames))
    x = randint(0, screen_height)
    y = randint(-100, 0)
    return Enemy(enemy_frames[random_object][0][0], x, y,animation_speed,enemy_speed, enemy_frames[random_object],random_object,scale,screen,ded,enemy_sound, group)

class Оbject(pygame.sprite.Sprite):#создаем класс Оbject
        def __init__(self, surf, x, y, random_object,index_object, group):#передаём в класс некоторые переменные
            pygame.sprite.Sprite.__init__(self)#создание спрайта
            self.image = surf#загружаем картинку
            self.rect = self.image.get_rect(center=(x, y))#создаём объект по загруженым координатам (x, y)
            self.add(group)#добавляем объект в группу
            self.timer = 100#таймер для анимации проростания/появления а затем зацикленной анимации
            self.rotation = randint(-180, 180)#рандомный поворот
            self.index = 0#переменная индекса для зацикленной анимации
            self.animation_frames = random_object#список кадров объекта который мы получили из функции createОbject
            self.index_object = index_object
        def update(self, *args):#update входит в базовый класс Sprite и отвечает за его обновление
            self.timer = self.timer - 1#бесконечно идущий таймер       
            self.animate()
        def animate(self):
            if self.timer== 50:#короткое условие для не зацикленной мини анимации проростания/появления которая произойдёт раз за всю жизнь объекта
                self.image = pygame.transform.rotate(self.animation_frames[0],  self.rotation)#берём кадр проростания из списка выше
            if self.timer<-5:#если таймер стал меньше -5:
                self.timer = 0#обновляем таймер
                self.index = (self.index + 1) % (len(self.animation_frames))#индекс становиться выше (если индекс стал выше len(списка) то благодаря "%" индекс становится обратно нулём)
                if self.index == 0:#если индекс == 0
                    self.index = 1#индекс = 1 (чтобы объект не повторял кадр проростания/появления)
                self.image = pygame.transform.rotate(self.animation_frames[self.index],  self.rotation)#картинка меняется с помощью индексации из списка а переменная индекса тоже меняется каждый раз когда "self.timer" становится меньше -5

def createОbject(group,animation_frames,screen_width,screen_height,drop_rect,station_rect,scale):#функция для создание нового объекта в классе
        random_object = random.choice(list(animation_frames))#рандомное значение random_object будет выбирать рандомный список кадров из большого списка с кадрами

        x = randint(50*scale, screen_width-100*round(scale)) #координата x будет рандомная от 50 до противоположного края экрана 
        y = randint(150*scale, screen_height-100*round(scale)) #координата y будет рандомная от 30 до противоположного края экрана
        if not ((drop_rect.x-100 <= x <= drop_rect.x+150) and (drop_rect.y-100 <= y <= drop_rect.y+150)):#условие если объект хочет появится рядом с шагоходом то не создавать его(сделано чтобы объекты не появлялись внутри шагохода)
            if not ((station_rect.x-50 <= x <= station_rect.x+120) and (station_rect.y-50 <= y <= station_rect.y+120)):#условие если объект хочет появится рядом с станцией то не создавать его(сделано чтобы объекты не появлялись внутри станции)
                return Оbject(animation_frames[random_object][1][0], x, y, animation_frames[random_object][1][1::],random_object, group)#передаем классу (базавую картинку объекта, коор.х, коор.у, рандомный список кадров)

class Drill(pygame.sprite.Sprite):
        def __init__(self,drill_x, drill_y,frames,drill_menu,drop_rect,distance,scale,mineral_list,player,drill_sound,UI_sound):
            pygame.sprite.Sprite.__init__(self)#создание спрайта
            self.sound = drill_sound
            self.UI_sound = UI_sound           
            self.image = frames[0]#загружаем картинку
            self.rect = self.image.get_rect(center=(drill_x, drill_y))#создаём объект по загруженым координатам (x, y)
            self.drop_rect = drop_rect
            self.frames = frames
            self.time = 30
            self.drill_x = drill_x
            self.drill_y = drill_y
            self.drill_timer = 0
            self.animate_drill = 0
            self.drill_menu=drill_menu
            self.scale = scale
            self.mineral_list = mineral_list
            self.mineral_timer = 0
            self.mineral_cells = [0,0,0]#количество минералов в ячейках
            self.type_minerals = []#переменная обозначает какими минералами заняты ячейки
            self.index = 0
            self.font2 = pygame.font.SysFont(None, int(10 * scale))#шрифт будущих надписей
            self.sc_text = self.font2.render(("образец"), 1, (0, 200, 150),(0, 0, 0))
            self.sc_text2 = self.font2.render(("боеприпас"), 1, (200, 200, 0),(0, 0, 0))
            self.sc_text3 = self.font2.render(("удалить"), 1, (200, 0, 0),(0, 0, 0))
            self.pos1 = self.sc_text.get_rect(center=(self.drill_x-35*self.scale, self.drill_y-150*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам
            self.pos2 = self.sc_text.get_rect(center=(self.drill_x-35*self.scale, self.drill_y-92*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам
            self.pos3 = self.sc_text.get_rect(center=(self.drill_x-35*self.scale, self.drill_y-35*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам

            self.pos01 = self.sc_text2.get_rect(center=(self.drill_x+5*self.scale, self.drill_y-150*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам
            self.pos02 = self.sc_text2.get_rect(center=(self.drill_x+5*self.scale, self.drill_y-92*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам
            self.pos03 = self.sc_text2.get_rect(center=(self.drill_x+5*self.scale, self.drill_y-35*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам

            self.delete_pos1 = self.sc_text3.get_rect(center=(self.drill_x+45*self.scale, self.drill_y-150*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам
            self.delete_pos2 = self.sc_text3.get_rect(center=(self.drill_x+45*self.scale, self.drill_y-92*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам
            self.delete_pos3 = self.sc_text3.get_rect(center=(self.drill_x+45*self.scale, self.drill_y-35*self.scale))#делаем колизию из текста создавая прямоуголюную кнопку и создаём кнопку по координатам


            self.player = player
            self.speed = 0
            self.distance = distance
            self.delete_timer = 100
        def update(self,screen,test_tubes,key_list, *args):
            self.drill_animation(screen)
            self.mineral(screen,test_tubes,key_list)
            self.draw(screen)

        def drill_animation(self,screen):
                    self.drill_timer = self.drill_timer + 1#прибавляем к таймеру 1
                    if self.animate_drill == 1 and self.drill_timer == 1:
                        self.sound['start'].play()
                        
                    if self.drill_timer > self.time:#если таймер стал выше "time" то 
                            self.drill_timer = 0#обновляем таймер
                            self.animate_drill = self.animate_drill + 1#увеличиваем индекс
                    if self.animate_drill == len(self.frames):#если индекс достигает предела списка кадров
                                self.animate_drill = 4#то индекс становится 4 (не обновляем индекс до нуля чтобы проигрывалась вечная анимация бура)
                                self.sound['work'].play()
                    self.image = self.frames[self.animate_drill]
                    if  (self.drill_x  < self.drop_rect.x+50*self.scale and self.drill_y  < self.drop_rect.y+50*self.scale) and (self.drill_x  > self.drop_rect.x-50*self.scale and self.drill_y  > self.drop_rect.y-50*self.scale):#если мы рядом с буром то
                                screen.blit(self.drill_menu, (self.drill_x-55*self.scale, self.drill_y-200*self.scale))#отображаем меню минералов 

        def create_random_mineral(self):#функция генерации рандомного минерала
            mineral_random = random.choice(list(self.mineral_list))
            return mineral_random

        def update_mineral_count(self, mineral_cells, indxm):#функция отвечает за обновления минералов в стаках
            if indxm >= 0 and indxm < 3:#MAX_MINERAL_CELLS:
                self.mineral_cells[indxm] += 1

        def mineral(self,screen,test_tubes,key_list):#,font2, build):#основная функция логики добычи минералов
            if self.mineral_timer == 0:
              self.mineral_type_index = self.create_random_mineral()
            self.mineral_timer = self.mineral_timer + 1
            if self.mineral_timer > self.distance/0.5:
               if len(self.type_minerals) > 0:#проверка что у нас есть стак для добавления
                 random_stack = randint(0, len(self.type_minerals) - 1)
                 self.update_mineral_count(self.mineral_cells, random_stack)
               self.mineral_timer = 0
               if len(self.type_minerals) < 3:#фиксированное значение 3 (игровая условность)
                    self.mineral_type_index = self.create_random_mineral()
                    self.type_minerals.append(self.mineral_type_index)
            if  (self.drill_x  < self.drop_rect.x+50*self.scale and self.drill_y  < self.drop_rect.y+50*self.scale) and (self.drill_x  > self.drop_rect.x-50*self.scale and self.drill_y  > self.drop_rect.y-50*self.scale):#если мы рядом с буром то
                self.display_minerals(screen,test_tubes,key_list)
                self.use_button(test_tubes,key_list)
        def display_minerals(self,screen,test_tubes,key_list):#функция отображения минералов
            for i, self.mineral_type_index in enumerate(self.type_minerals):
                if self.mineral_type_index is not None and i < len(self.mineral_cells):
                    text = self.font2.render(str(self.mineral_cells[i]), 1, (0, 100, 150))
                    screen.blit(self.mineral_list[self.type_minerals[i]][0], (int(self.drill_x-45*self.scale), int(self.drill_y+((i*58)-189)*self.scale)))#отображаем картинки минералов(каждый новый минерал должен быть ниже предыдущего)
                    screen.blit(text, (int(self.drill_x+10*self.scale), int(self.drill_y+((i*58)-189)*self.scale)))#отображаем текста(каждый новый текст должен быть ниже прежнего)

            screen.blit(self.sc_text, self.pos1)#отображаем кнопку
            screen.blit(self.sc_text, self.pos2)
            screen.blit(self.sc_text, self.pos3)

            screen.blit(self.sc_text2, self.pos01)#отображаем кнопку
            screen.blit(self.sc_text2, self.pos02)
            screen.blit(self.sc_text2, self.pos03)

            screen.blit(self.sc_text3, self.delete_pos1)#отображаем кнопку
            screen.blit(self.sc_text3, self.delete_pos2)
            screen.blit(self.sc_text3, self.delete_pos3)

            self.pos = [self.pos1,self.pos2,self.pos3]
            self.pos0 = [self.pos01,self.pos02,self.pos03]
            self.delete_pos = [self.delete_pos1,self.delete_pos2,self.delete_pos3]




        def use_button(self,test_tubes,key_list):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                for y in range(0, len(self.type_minerals)):

                    if pygame.mouse.get_focused() and self.pos0[y].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and (self.player.bul[-1] == self.mineral_list[self.type_minerals[y]][-1] or self.player.bul[-1] == None ):# условие если мышка находится в области кнопки и если левая кнопка мыши нажата  
                        #заменяем каждую характеристику заряженой пули в игроке
                        self.UI_sound['button'].play()
                        self.player.bul[0] = self.player.bul[0] + self.mineral_cells[y]
                        self.player.bul[1][0] = self.mineral_list[self.type_minerals[y]][1]
                        self.player.bul[1][1] = self.mineral_list[self.type_minerals[y]][2] 
                        self.mineral_cells[y] = 0
                        self.player.bul[-1]  = self.mineral_list[self.type_minerals[y]][-1]
                        self.player.bul[-2]  = self.mineral_list[self.type_minerals[y]][-2]
                        self.player.bul[-2]  = self.mineral_list[self.type_minerals[y]][6]
                        self.player.bul[2]  = self.mineral_list[self.type_minerals[y]][3]
                        self.player.bul[3]  = self.mineral_list[self.type_minerals[y]][4]
                        self.player.bul[4]  = self.mineral_list[self.type_minerals[y]][5]
                        
                for i in range(0, len(self.mineral_cells)):
                    if len(self.type_minerals)-1 >= i:
                        if len(test_tubes) < 3 and len(self.type_minerals) > 0 and self.type_minerals[i] not in test_tubes:   
                            if pygame.mouse.get_focused() and self.pos[i].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:# условие если мышка находится в области кнопки и если левая кнопка мыши нажата  
                                self.UI_sound['button'].play()
                                key_list.append('minerals')
                                test_tubes.append(self.type_minerals[i])
                        if pygame.mouse.get_focused() and self.delete_pos[i].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.delete_timer == 0:# условие если мышка находится в области кнопки и если левая кнопка мыши нажата  
                            self.UI_sound['button'].play()
                            self.type_minerals[i] = self.create_random_mineral()
                            self.mineral_cells[i] = 0
                self.delete_timer = self.delete_timer - 1
                if self.delete_timer < 0:
                    self.delete_timer = 100
                
        def draw(self, screen):
            screen.blit(self.image, self.rect)

                    
def createDrill(drop_rect,images,drill_menu,distance,scale,mineral_list,player,screen_width,screen_height,drill_sound,UI_sound):
    drill_x, drill_y = drop_rect.x,drop_rect.y
    frames = images
    return Drill(drill_x, drill_y,frames,drill_menu,drop_rect,distance,scale,mineral_list,player,drill_sound,UI_sound)
