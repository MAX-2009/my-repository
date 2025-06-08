import pygame
import math
from random import randint
import time

from config import load_game_assets,load_game_sound, TEXTS, load_icon
from entities import Enemy, createEnemy
from entities import Оbject, createОbject
from entities import Drill, createDrill
from player import *
base_width_screen, base_height_screen = 1000, 562 #базовое разрешение окна 
FPS = 60 #количество кадров в секунду
player_speed = 4#зададим скорость перемещения шагохода

def main():
    pygame.init()

    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    #screen_width = 940
    #screen_height = 660
    #screen_width = 640
    #screen_height = 360
    
    scale_x = screen_width / base_width_screen
    scale_y = screen_height / base_height_screen
    scale = min(scale_x, scale_y)  # Выбираем наименьшее значение для сохранения соотношения сторон
    screen = pygame.display.set_mode((int(base_width_screen * scale), int(base_height_screen * scale)))

    pygame.display.set_caption("Planet of Research")#название на окне игры
    icon_image = load_icon()
    pygame.display.set_icon(icon_image)#загрузка иконки на окне игры
    clock = pygame.time.Clock()#время для фпс
    print(  scale)
    def scale_resources(resources, scale):#функция масштабирования картинок для игры (загружаем неотмастштабированые картинки и разрешение экрана)
        scaled_resources = {}
        if isinstance(resources, dict):
                    for key, value in resources.items():
                      if isinstance(value, pygame.Surface):
                          scaled_resources[key] = pygame.transform.scale(
                              value, (int(value.get_width() * scale), int(value.get_height() * scale))
                          )
                      elif isinstance(value, list):
                          scaled_resources[key] = [
                            pygame.transform.scale(item, (int(item.get_width() * scale), int(item.get_height() * scale)))
                            if isinstance(item, pygame.Surface) else scale_resources(item,scale)
                            for item in value
                          ]
                      elif isinstance(value, dict):
                          scaled_resources[key] = scale_resources(value, scale)
                      else:
                        scaled_resources[key] = value
        elif isinstance(resources, list):
                    scaled_resources = [
                        pygame.transform.scale(item, (int(item.get_width() * scale), int(item.get_height() * scale)))
                        if isinstance(item, pygame.Surface) else scale_resources(item,scale)
                        for item in resources
                    ]
        else:
                  return resources
        return scaled_resources

    font = pygame.font.SysFont('sans', int(50 * scale))#шрифт будущих надписей
    font2 = pygame.font.SysFont(None, int(30 * scale))
    font3 = pygame.font.SysFont(None, int(15 * scale))

    obj_frames,  analysis_icon, animation_images,scaled_images, minerals,enemy_animation,texts = load_game_assets()#загружаем все картинки из config
    player_sound,bullet_sound,drill_sound,UI_sound,game_music,enemy_sound  = load_game_sound()
    pygame.mixer.music.load(game_music['menu_music'])
    pygame.mixer.music.play(-1)
    resources = {
            "obj_frames": obj_frames,
            "analysis_icon": analysis_icon,
            "animation_images": animation_images,
            "scaled_images": scaled_images,
            "minerals": minerals,
            "enemy_animation": enemy_animation
    }
    scaled_resources = scale_resources(resources, scale)
    s_r = scaled_resources#абриеватура
    #walk_anim = game_images('анимация_шагания',False,2.5,6)#список кадров для анимации шагохода 
    station_rect = s_r["scaled_images"]["station"].get_rect(center=(screen_width//1.321, screen_height//1.8))#местоположение станции
    space_capsule = pygame.transform.rotate(s_r["scaled_images"]["capsule"], -30)#загружаем и поворачиваем картиинку капсулы на 30 градусов
    spaceship = s_r["animation_images"]["anim_spaceship"][0]#базовая картинка космического корабля

    def create_text_button(text, font, color, center_position):#функция для создания кнопок (берём текст из texts, указываем шрифт, указываем цвет, указываем позицию кнопки)
          text_surface = font.render(text, True, color)
          text_rect = text_surface.get_rect(center=center_position)
          return text_surface, text_rect
    text_color=(0,100,150)
    sc_text,pos = create_text_button("высадка", font,text_color,(170*scale,370*scale))
    sc_text0,pos0 = create_text_button("отказ", font,text_color,(170*scale,490*scale))
    
    sc_text1,pos1 = create_text_button(TEXTS["game_title"], font, text_color, (490 * scale,150 * scale))
    sc_text2,pos2 = create_text_button(TEXTS["menu_start"], font, text_color, (460 * scale,250 * scale))
    sc_text3,pos3 = create_text_button(TEXTS["menu_exit"], font, text_color, (460 * scale,350 * scale))
    sc_text4,pos4 = create_text_button("установить", font3,text_color,(47*scale,371*scale))
    sc_text5,pos5 = create_text_button("удалить", font3,text_color,(47*scale,345*scale))
    scaled_drop_shadow = pygame.transform.scale(scaled_images["drop_shadow"], (int(scaled_images["drop_shadow"].get_width() * scale), int(scaled_images["drop_shadow"].get_height() * scale)))
    shadow_rect = scaled_drop_shadow.get_rect(center=(300 * scale, 300 * scale))


    max_in_row = 5#максимальное количество объектов в ряду
    x_offset = 60#сдвиг по оси X между объектами
    y_offset = -50 * scale#сдвиг по оси Y между рядами


    def colОbject(test_tubes,energy,base_list,key_list,key_base_list):#функция колизии 
        for bullet in bullets:#колизия пуль с врагами
          #...
          for enemy in enemys:
            if bullet.rect.colliderect(enemy.rect) and enemy.health > 0:
              enemy.health -= bullet.bullet_damage#уменьшаем здоровье врага
              bullet.kill()#удаляем пулю
              break#переходим к следующей пуле

        for Enemy1 in enemys:#колизия между врагами (отталкиваем врагов друг от друга чтобы они не наслаивались)
            for Enemy in enemys:
                if Enemy1.rect.collidepoint(Enemy.rect.center):#если вы приблизились к цели для сбора
                    if Enemy1 != Enemy:
                        Enemy.pos.x = Enemy.pos.x + randint(-2,2)
                        Enemy.pos.y = Enemy.pos.y + randint(-2,2)                

        for Оbject in objects:#колизия игрока и объектов для исследования
            if player.rect.collidepoint(Оbject.rect.center) and len(test_tubes) < 3:#если вы приблизились к цели для сбора
                Оbject.kill()#объект исчезает с экрана
                player_sound['took'].play()
                if len(test_tubes) < 3:
                    test_tubes.append(Оbject.index_object)
                    key_list.append('object')

        for Enemy in enemys:#колизия врагов и игрока 
            if Enemy.distance < 100*scale and Enemy.health > 0:
                    player.hp = player.hp - 0.1
            if player.rect.collidepoint(Enemy.rect.center) and len(test_tubes) < 3 and Enemy.health < 1:#условие для сбора мёртвого врага
                    test_tubes.append(Enemy.index_object)
                    key_list.append('en')        
                    Enemy.kill()


        if player.rect.collidepoint(station_rect.center):#если вы находитесь на станции
            screen.blit(s_r["scaled_images"]["menu_ob"],(station_rect.x-75*scale,station_rect.y-170*scale))#отображение меню для изучений
            if player.hp < 110:
                player.hp = player.hp + 0.1
            if player.energy < 123:
                player.energy = player.energy + 0.1 
            for i in range(0, len(base_list)):#отображаем все объекты которые мы изучили       
                                row_x = (i % max_in_row)
                                #вычисляем индекс в колонке (по оси Y)
                                row_y = (i // max_in_row)
                                x_position = station_rect.x - (x_offset - 50 * row_x) * scale
                                y_position = station_rect.y - y_offset * row_y

                                text = (s_r["obj_frames"][key_base_list[i]][base_list[i]][0])
                                button_what_rect = s_r["scaled_images"]["iac"].get_rect(center=(x_position+10 * scale, y_position-145 * scale))#создаётся колизия рамочки для объектов 
                                screen.blit(s_r["scaled_images"]["iac"],(button_what_rect))#отображаем рамочку под перед объектом
                                screen.blit(s_r["obj_frames"][key_base_list[i]][base_list[i]][-1], (x_position, y_position-152 * scale))

                                if pygame.mouse.get_focused() and button_what_rect.collidepoint(pygame.mouse.get_pos()):#если мы навелись на рамочку
                                        screen.blit(s_r["scaled_images"]["ob"],(x_position-60 * scale, y_position-253 * scale))#отображаем рамку с описанием объекта
                                        for i1 in range(0,len(text)):#весь текст отображаем в ряд
                                                text1 = font3.render(str(text[-i1-1]), 1, (0, 100, 150))
                                                screen.blit(text1,(x_position-50 * scale, y_position-(180+20*i1) * scale))
            if len(test_tubes) >= 1:#пока в колбах есть объекты то добавляем объекты в базу изучений (если мы собрали объект который уже есть в базе то мы удаляем объект)
                        if  test_tubes[-1] not in base_list:
                                base_list.append(test_tubes[-1])
                                key_base_list.append(key_list[-1])
                        else:  
                            pass
                        test_tubes.pop()
                        key_list.pop()
            if energy < 123:#пока у нас заряд ниже полного то заряжаем шагоход
                energy = energy + 0.5      
        if len(test_tubes) > 0:#пока у нас есть объекты в колбах то отображаем иконки объектов в ряд
            for i in range(0,len(test_tubes)):
                    screen.blit(s_r["obj_frames"][key_list[i]][test_tubes[i]][-1], (((i+2) * 54 * scale)-78*scale, 467 * scale))

    enemy_frames = {
            'Angry_Fly':s_r["enemy_animation"]["злая_муха"],
            'Angry_sork':s_r["enemy_animation"]["сорк"]
            } #список всех кадров всех объектов с маленькими списками кадров каждого объекта
    logic_enemy = {
    'Angry_Fly':[1,2,3]
    
            }

    mineral_list = s_r["obj_frames"]['minerals']
    logic_mineral = {#характеристики минералов (иконка, скорость, урон)
        'pyro':[mineral_list['pyro'][-1], 7,1,10,20,100,mineral_list['pyro'][1],'пироциний',bullet_sound['pyro']],
        'fyr':[mineral_list['fyr'][-1], 20,50,2,1,50,mineral_list['fyr'][1], 'бр',bullet_sound['fyroniy']],
        'bru':[mineral_list['bru'][-1], 10,3,10,5,20,mineral_list['bru'][1],'аааа',bullet_sound['brumiy']],
        'bir':[mineral_list['bir'][-1], 10,5,1,15,100,mineral_list['bir'][1],'биридиум',bullet_sound['biridium']],


        }
    test_tubes = []#список в который мы будем сохранять собраные образцы (колбочки в нижнем левом углу на панели)
    key_list = []#список в который мы записываем тип объекта (образец минерала, образец окружающей фауны, образец врага)
    base_list = []#список объектов в базе
    key_base_list = []#список типа объекта в базе
    
    SPAWN_OBJECT_EVENT = pygame.USEREVENT + 1
    SPAWN_ENEMY_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_OBJECT_EVENT, 3000)
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, 10000)

    energy = 123#энергия шагохода
    button_pause = True#переключатель для кнопки паузы
    initial_menu_cycle = True#цикл для начального меню
    cycle = False#цикл для основной части игры
    capsule_x,capsule_y = 300,150#начальная позиция капсулы для будущей анимации
    animation = False#переключатель для анимации запуска капсулы
    build = False#переключатель для установки дрели
    dreel_ready = False#переключатель для анимации дрели
    pause_cycle = False#переключатель цикла паузы
    saturation_point_x = randint(150*scale, round(screen_width-350*scale))#x,y координаты точки насыщенной минералами
    saturation_point_y = randint(250*scale, round(screen_height-240*scale)) 
    game_over = False#переключатель для проигрыша

    objects = pygame.sprite.Group()#используем .Group() для создания группы спрайтов - object
    enemys = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player(s_r["animation_images"]["drop_charging"][0],player_speed,screen_width,screen_height,scale,s_r["animation_images"]["drop_charging"],s_r["animation_images"]["drop_active"],s_r["animation_images"]["aim"],s_r["animation_images"]['drop_walk'],player_sound)
    #загрузка класса игрока
    
    while initial_menu_cycle:#цикл начального меню
        for event in pygame.event.get():#перебор событий
            if event.type == pygame.QUIT:
                pygame.quit()#завершения работы модуля pygame окна
                exit()
        #station0=drop_animate(anim_spaceship,10)#вызываем функцию для анимации загружая список кадров и время с которой будут меняться эти кадры
        if pygame.mouse.get_focused() and pos0.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:# условие если мышка находится в области кнопки и если левая кнопка мыши нажата  
                exit()
        if pygame.mouse.get_focused() and pos.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and animation == False:# условие если мышка находится в области кнопки и если левая кнопка мыши нажата  
            UI_sound['start_game'].play()
            animation = True#включаем анимацию
        if animation == True:#переключатель анимации активен
            capsule_y +=2#двигаем капсулу по y
            capsule_x +=3#двигаем капсулу по x
        screen.blit(s_r["scaled_images"]["bg_surf0"], (0, 0))#отображаем фон начального меню (ставим фон первым в отображении чтобы он был самым нижним слоем для отображения будущих объектов на нём)
        screen.blit(space_capsule, (capsule_x * scale, capsule_y * scale))#отображаем капсулу (перед космическим кораблём чотбы былл эффект вылета капсулы из под космического корабля)
        screen.blit(spaceship, (200 * scale, 100 * scale))#отображаем сам космический корабль
        screen.blit(s_r["scaled_images"]["menu_button"], (50 * scale, 310 * scale))
        
        screen.blit(sc_text, pos)#отображаем кнопку
        screen.blit(sc_text0, pos0)#отображаем кнопку
        
        if capsule_y > 300:#если капсула долетела до планеты то
               cycle = True#запускаем основной цикл игры
               initial_menu_cycle = False#выключаем цикл начального меню игры
               pygame.mixer.music.load(game_music['game_music'])
               pygame.mixer.music.play(-1)
        pygame.display.update()#метод обновляет экран
        clock.tick(FPS)#количество кадров в секунду "60"

    while cycle: #главный цикл (выключен пока работает цикл начального меню)
        for event in pygame.event.get():#перебор событий
            if event.type == pygame.QUIT:
                pygame.quit()#завершения работы модуля pygame окна
                exit()
            elif event.type == SPAWN_OBJECT_EVENT:
                  createОbject(objects, s_r["obj_frames"]['object'], screen_width, screen_height, player.rect,station_rect,scale)#создается новый объект  
            elif event.type == SPAWN_ENEMY_EVENT and len(enemys)<6:
                  createEnemy(enemys,enemy_frames,screen_height,scale,player.rect,screen,s_r['scaled_images']['ded'],enemy_sound)#создается новый враг
        mouse_x, mouse_y = pygame.mouse.get_pos()#указываем позицию курсора в виде двух переменных
        bt = pygame.key.get_pressed()#bt - переменная в которую прописывается нажатая клавиша
        energy_color = (200 - player.energy,    player.energy * 2 - 1,    120 + player.energy)#цвет шкалы энергии (зависит от уровня эенергии)
        min_x = player.rect.x - saturation_point_x
        min_y = player.rect.y - saturation_point_y
        distance =  Vector2(min_x * scale, min_y * scale).length()#расчитиваем расстояние от игрока до точки нассыщеной минералами

        drop_surf_rotated_shadow = pygame.transform.rotate(s_r["scaled_images"]["drop_shadow"], -player.drop_angle - 90)#градус поворота тени шагохода 
        hp_color = (255 - player.hp, player.hp, 0)#цвет шкалы здоровья шагохода (зависит от уровня здоровья)
        text_bul = font2.render(str(player.bul[0]), 1, (0, 100, 150))
        coloro = 143
        
        if not bt[pygame.K_ESCAPE]:
                    button_pause = True  
        if bt[pygame.K_ESCAPE] and button_pause:#если нажата кнопка Escape то
            cycle = False#выключаем основной цикл
            pause_cycle = True#включаем цикл паузы
            button_pause = False
        if player.hp < 0:#если здоровье шагохода упало то выключаем цикл игры и включаем цикл проигрыша
                    game_over = True
                    cycle = False

        while pause_cycle:
            for event in pygame.event.get():#перебор событий
                if event.type == pygame.QUIT:
                    pygame.quit()#завершения работы модуля pygame окна
                    exit()
            bt = pygame.key.get_pressed()#bt - переменная в которую прописывается нажатая клавиша
            screen.blit(s_r["scaled_images"]["bg_surf_pause"], (0, 0))#меню паузы
            screen.blit(sc_text1, pos1)#отображаем кнопки
            screen.blit(sc_text3, pos3)
            if pygame.mouse.get_focused() and pos3.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:# условие если мышка находится в области кнопки и если левая кнопка мыши нажата  
                    exit()
            if pygame.mouse.get_focused() and pos1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:# условие если мышка находится в области кнопки и если левая кнопка мыши нажата  
                cycle = True#включаем основной цикл
                pause_cycle = False#выключаем цикл паузы
            pygame.display.update()#метод обновляет экран
            clock.tick(FPS)#количество кадров в секунду "60"
            if not bt[pygame.K_ESCAPE]:
                    button_pause = True  
            if bt[pygame.K_ESCAPE] and button_pause == True:
                cycle = True#включаем основной цикл
                pause_cycle = False#выключаем цикл паузы
                button_pause = False

        while game_over:
            for event in pygame.event.get():#перебор событий
                if event.type == pygame.QUIT:
                    pygame.quit()#завершения работы модуля pygame окна
                    exit()
            screen.blit(s_r["scaled_images"]["ded2"], (0, 0))#отображаем экран проигрыша
            pygame.display.update()#метод обновляет экран
            clock.tick(FPS)#количество кадров в секунду "60"

        screen.blit(s_r["scaled_images"]["bg_surf"], (0, 0))#отображаем фон (ставим фон первым в отображении чтобы он был самым нижним слоем для отображения будущих объектов на нём)
        if pygame.mouse.get_focused() and pos4.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]  and ((143-distance/scale))/3 * scale > 0 and build == False:#если нажата q и переключатель бура выключен то
                UI_sound['button'].play()
                build = True#включаем переключатель бура
                drill_x, drill_y = player.rect.x,player.rect.y#координаты бура по двум осям равны координатам шагохода
                drill = createDrill(player.rect,s_r["animation_images"]["drill_images"],s_r["scaled_images"]["drill_menu"],distance,scale,logic_mineral,player,screen_width,screen_height,drill_sound,UI_sound)
                #создаём объект класса бур

        if pygame.mouse.get_focused() and pos5.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:#если нажата q и переключатель бура выключен то
            build = False
            UI_sound['button'].play()
        objects.draw(screen)#.draw отрисовывает группу объектов

        if build:
            drill.update(screen,test_tubes,key_list)#метод .update() для буровой установки
        bullets.draw(screen)#отрисовываем группу пуль
        screen.blit(drop_surf_rotated_shadow, (player.rect.x + 7 - drop_surf_rotated_shadow.get_width() // 15, player.rect.y + 7 - drop_surf_rotated_shadow.get_height() // 15))#отображаем тень шагохода (перед шагоходом!)

            
            
        player.update(screen,bt,mouse_x,mouse_y,bullets,s_r["scaled_images"]["bullet"])#метод .update() для игрока
        enemys.draw(screen)#.draw отрисовывает группу врагов
        if ((143-distance))/3 * scale > 0:
            screen.blit(s_r["scaled_images"]["tab"], (player.rect.x, player.rect.y-36 * scale))#фон для шкалы расстояния до точки насышенной минералами
        else:
            screen.blit(s_r["scaled_images"]["tab0"], (player.rect.x, player.rect.y-36 * scale))#фон для шкалы расстояния до точки насышенной минералами
       
        pygame.draw.rect(screen, (0,int(coloro),0), (player.rect.x+5 * scale, player.rect.y-23 * scale, (143-distance)/3 * scale, 7 * scale))#шкала расстояния до точки насыщенной минералами
        screen.blit(s_r["scaled_images"]["thickets_surf"], (0, 0))#отображаем заросли (отображаем после шагохода чтобы шагоход был под зарослями)
        screen.blit(s_r["scaled_images"]["panel"], s_r["scaled_images"]["panel"].get_rect(center=(100 * scale, 482 * scale)))#панель в левом нижнем углу
        pygame.draw.rect(screen, hp_color, (182 * scale, 442 * scale,7 * scale, player.hp * scale))#отображаем шкалу здоровья
        screen.blit(s_r["scaled_images"]["station"], (station_rect.x, station_rect.y))#отображаем станцию 
        screen.blit(s_r["scaled_images"]["drill_indicator"], (0, 250*scale))#отображаем станцию 

        screen.blit(sc_text4, pos4)
        screen.blit(sc_text5, pos5)

        objects.update(screen_width)#метод .update() для объектов
        enemys.update(player.rect.y,player.rect.x,player.rect,scale,screen_width)#метод .update() для врагов
        bullets.update(scale)#метод .update() для пуль
        colОbject(test_tubes,energy,base_list,key_list,key_base_list)#запуск функции колизий
        screen.blit(text_bul, (94*scale, 422*scale))#циферблат отображающий количество пуль в шагоходе
        pygame.draw.rect(screen, energy_color, (15 * scale, 549 * scale, player.energy * scale, 9 * scale))#отображаем шкалу энергии
        pygame.display.update()#метод обновляет экран 
        clock.tick(FPS)#количество кадров в секунду "60"

if __name__ == "__main__":
  main()
