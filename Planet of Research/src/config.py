import os
import pygame

#получаем абсолютный путь к папке, где находится config.py
base_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#теперь ASSETS_DIR будет относительно корневой директории проекта
ASSETS_DIR = os.path.join(base_dir, "..", "assets")

#остальные пути строим относительно ASSETS_DIR
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
MUSIC_DIR = os.path.join(BASE_DIR, "assets", "audio")

icon_image_path = os.path.join(IMAGES_DIR, "шагоход.png")






def load_icon():
  icon_image = pygame.image.load(icon_image_path)
  return icon_image

analysis_icon = []# Список иконок исследования

TEXTS = {
    "game_title":"продолжить игру",
    "menu_start":"как играть",
    "menu_exit":"Выход",
    "ok":["на планете Эспект обнаружена неопознаная активность","ваща цель изучить местную фауну и найти ответ причины активности","защищайтесь","изучайте","высадка!"]
  }

description_object = {

  'gumus_description':['дикий гумус','очень липкий','живучий','частый'],
  'flycatcher_description':['красивая мухоловка','очень пахучая','приманивает мух','частый'],
  'rock_description':['камень','вылазит из земли','с яркими кристалами','частый'],
  'lol':['тест','тест','тест','тест'],
  'pyro':['пироциний','воспламеняющийся', 'твёрдый'],
  'pyro1':['фироний','частый минерал', 'блестит'],
  'pyro2':['брюмий','частый минерал', 'рыхлый'],
  'pyro3':['биридиум','частый минерал', 'прочный'],
  'Angry_Fly':['мёртвая муха','злая','дикая'],
  'Angry_sork':['мёртвый сорк','использует минералы','для экзоскелета','одноглазый']  

  }

def game_images(images, icon, size, cycle):
    """
    Создает список кадров для анимаций и иконок для исследования.

    Args:
        images: Базовое имя файлов изображений (без номера).
        icon: True, если нужно добавить последний кадр в список analysis_icon; False иначе.
        size: Коэффициент масштабирования.
        cycle: Количество изображений (кадров).

    Returns:
        Список масштабированных изображений. Возвращает None, если произошла ошибка.
    """
    frames = []
    for i in range(1, cycle + 1):
        try:
            image_path = os.path.join(IMAGES_DIR, f"{images}{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            gum_image = pygame.transform.scale(image, (int(image.get_width() * size), int(image.get_height() * size)))

            frames.append(gum_image)
            if icon:
                if i == cycle:
                  analysis_icon.append(image)
        except pygame.error as e:
            print(f"Ошибка загрузки изображения {images}{i}.png: {e}")
            return None
    return frames

def load_game_sound():
  player_sound = {
       'walk':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"шаг.mp3")),
       'gun_ready':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"звук_пушки.mp3")),
       'took':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"что-то_подобрал.mp3")),    
    }
  bullet_sound ={
    'pyro':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"огнемёт.mp3")),
    'biridium':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"дробовик.mp3")),
    'fyroniy':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"фироний.mp3")),
    'brumiy':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"брюмий.mp3")),
    }
  drill_sound = {
       'start':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"бур_включается.mp3")),
       'work':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"бур_работает.mp3")),
    }
  UI_sound = {
       'start_game':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"азбука_морзе.mp3")),
       'button':pygame.mixer.Sound(os.path.join(MUSIC_DIR,"звук_кнопки.mp3")),

    }
  game_music = {
    'menu_music' :os.path.join(MUSIC_DIR,"меню_музыка.mp3"),
    'game_music' :os.path.join(MUSIC_DIR,"фоновая_музыка.mp3"),
    }
  enemy_sound = {
    'fly_attack' :pygame.mixer.Sound(os.path.join(MUSIC_DIR,"выстрел_мухи.mp3")),
    }
  
  #entities_sound =
  UI_sound['start_game'].set_volume(0.3)
  player_sound['walk'].set_volume(0.1)
  player_sound['took'].set_volume(0.3)
  player_sound['gun_ready'].set_volume(0.1)
  drill_sound['work'].set_volume(0.4)
  bullet_sound['biridium'].set_volume(0.4)
  return player_sound,bullet_sound,drill_sound,UI_sound,game_music,enemy_sound
  

def load_game_assets():

    gumus_frames =  game_images("гумус", True, 2, 5)
    flycatcher_frames = game_images("мухоловка", True, 2, 5)
    rock_frames = game_images("камушек", True, 2, 5)
    lol_frames = game_images("test", True, 2, 5)




    images = {
        "drop_shadow": pygame.image.load(os.path.join(IMAGES_DIR, "тень_шагохода.png")).convert_alpha(),
        "station": pygame.image.load(os.path.join(IMAGES_DIR, "станция.png")).convert_alpha(),

        "thickets_surf": pygame.image.load(os.path.join(IMAGES_DIR, "заросли1.png")).convert_alpha(),
        "bg_surf": pygame.image.load(os.path.join(IMAGES_DIR, "фон.png")).convert_alpha(),
        "bg_surf0": pygame.image.load(os.path.join(IMAGES_DIR, "начальное_меню.png")).convert_alpha(),
        "bg_surf_pause": pygame.image.load(os.path.join(IMAGES_DIR, "меню_пауза.png")).convert_alpha(),
        "capsule": pygame.image.load(os.path.join(IMAGES_DIR, "капсула.png")).convert_alpha(),
        "drill_menu": pygame.image.load(os.path.join(IMAGES_DIR, "меню_бура (2).png")).convert_alpha(),
        "bullet": pygame.image.load(os.path.join(IMAGES_DIR, "пуля.png")).convert_alpha(),   
        "iac": pygame.image.load(os.path.join(IMAGES_DIR, "яч.png")).convert_alpha(),   
        "menu_ob": pygame.image.load(os.path.join(IMAGES_DIR, "меню_об.png")).convert_alpha(),   
        "ob": pygame.image.load(os.path.join(IMAGES_DIR, "оп.png")).convert_alpha(),   
        "zoz1": pygame.image.load(os.path.join(IMAGES_DIR, "заряд1.png")).convert_alpha(),   
        "zoz2": pygame.image.load(os.path.join(IMAGES_DIR, "заряд2.png")).convert_alpha(),  
        "tab": pygame.image.load(os.path.join(IMAGES_DIR, "индикатор.png")).convert_alpha(), 
        "tab0": pygame.image.load(os.path.join(IMAGES_DIR, "индикатор_тревога.png")).convert_alpha(), 
        "ded": pygame.image.load(os.path.join(IMAGES_DIR, "мёртвая_муха.png")).convert_alpha(), 
        "ded1": pygame.image.load(os.path.join(IMAGES_DIR, "иконка_мухи.png")).convert_alpha(),

        "ded_sork": pygame.image.load(os.path.join(IMAGES_DIR, "сорк_умер.png")).convert_alpha(), 
        "ded_sork1": pygame.image.load(os.path.join(IMAGES_DIR, "иконка_сорка.png")).convert_alpha(),



        "ded2": pygame.image.load(os.path.join(IMAGES_DIR, "меню_проигрыша.png")).convert_alpha(),
        "menu_button": pygame.image.load(os.path.join(IMAGES_DIR, "меню_кнопки.png")).convert_alpha(),  

        'pyro':pygame.image.load(os.path.join(IMAGES_DIR, "пироциний.png")).convert_alpha(),
        'fyr':pygame.image.load(os.path.join(IMAGES_DIR, "фироний.png")).convert_alpha(),
        'bru':pygame.image.load(os.path.join(IMAGES_DIR, "брюмий.png")).convert_alpha(),
        'bir':pygame.image.load(os.path.join(IMAGES_DIR, "биридиум.png")).convert_alpha(),
        'fraction':pygame.image.load(os.path.join(IMAGES_DIR, "дробь.png")).convert_alpha(),       
        'fire':pygame.image.load(os.path.join(IMAGES_DIR, "пламя.png")).convert_alpha(),
        'firo_bullet':pygame.image.load(os.path.join(IMAGES_DIR, "фироновая_пуля.png")).convert_alpha(),
        'brum_bullet':pygame.image.load(os.path.join(IMAGES_DIR, "брюмовая_пуля.png")).convert_alpha(),

        'drill_indicator':pygame.image.load(os.path.join(IMAGES_DIR, "индикатор_состояния_бура.png")).convert_alpha(),      
    }

    scaled_game_images = {
      "drop_shadow": pygame.transform.scale(images["drop_shadow"], (int(images["drop_shadow"].get_width()//0.4), int(images["drop_shadow"].get_height()//0.4))),
      "station": pygame.transform.scale(images["station"], (int(images["station"].get_width()//0.3), int(images["station"].get_height()//0.3))),

      "thickets_surf": pygame.transform.scale(images["thickets_surf"], (int(images["thickets_surf"].get_width()//0.12), int(images["thickets_surf"].get_height()//0.12))),
      "bg_surf": pygame.transform.scale(images["bg_surf"], (int(images["bg_surf"].get_width()//0.12), int(images["bg_surf"].get_height()//0.12))),
      "bg_surf0": pygame.transform.scale(images["bg_surf0"], (int(images["bg_surf0"].get_width()//0.23), int(images["bg_surf0"].get_height()//0.23))),
      "bg_surf_pause": pygame.transform.scale(images["bg_surf_pause"], (int(images["bg_surf_pause"].get_width()//0.12), int(images["bg_surf_pause"].get_height()//0.12))),
      "capsule": pygame.transform.scale(images["capsule"], (int(images["capsule"].get_width()//0.5), int(images["capsule"].get_height()//0.5))),
      "drill_menu": pygame.transform.scale(images["drill_menu"], (int(images["drill_menu"].get_width()//0.5), int(images["drill_menu"].get_height()//0.5))),
      "panel": pygame.image.load(os.path.join(IMAGES_DIR, "панель.png")).convert_alpha(),
      "button_what": pygame.image.load(os.path.join(IMAGES_DIR, "объяснение.png")).convert_alpha(),
      "button_what0": pygame.image.load(os.path.join(IMAGES_DIR, "объяснение0.png")).convert_alpha(),
      "bullet": pygame.transform.scale(images["bullet"], (int(images["bullet"].get_width()//1), int(images["bullet"].get_height()//1))),
      "iac": pygame.transform.scale(images["iac"], (int(images["iac"].get_width()//0.25), int(images["iac"].get_height()//0.25))),
      "menu_ob": pygame.transform.scale(images["menu_ob"], (int(images["menu_ob"].get_width()//0.6), int(images["menu_ob"].get_height()//0.6))),
      "ob": pygame.transform.scale(images["ob"], (int(images["ob"].get_width()//1.2), int(images["ob"].get_height()//1.2))),

      "zoz1": pygame.transform.scale(images["zoz1"], (int(images["zoz1"].get_width()//0.6), int(images["zoz1"].get_height()//0.6))),
      "zoz2": pygame.transform.scale(images["zoz2"], (int(images["zoz2"].get_width()//0.6), int(images["zoz2"].get_height()//0.6))),
      "tab": pygame.transform.scale(images["tab"], (int(images["tab"].get_width()//0.6), int(images["tab"].get_height()//0.6))),
      "tab0": pygame.transform.scale(images["tab0"], (int(images["tab0"].get_width()//0.6), int(images["tab0"].get_height()//0.6))),

      "ded": pygame.transform.scale(images["ded"], (int(images["ded"].get_width()//0.3), int(images["ded"].get_height()//0.3))),

      "ded2": pygame.transform.scale(images["ded2"], (int(images["ded2"].get_width()//0.12), int(images["ded2"].get_height()//0.12))),


      "ded_sork": pygame.transform.scale(images["ded_sork"], (int(images["ded_sork"].get_width()//0.3), int(images["ded_sork"].get_height()//0.3))),
      "ded_sork1": pygame.transform.scale(images["ded_sork1"], (int(images["ded_sork1"].get_width()//100000), int(images["ded_sork1"].get_height()//0.01))),


      "menu_button": pygame.transform.scale(images["menu_button"], (int(images["menu_button"].get_width()//0.2), int(images["menu_button"].get_height()//0.2))),

      "pyro": pygame.transform.scale(images["pyro"], (int(images["pyro"].get_width()//0.5), int(images["pyro"].get_height()//0.5))),
      "fyr": pygame.transform.scale(images["fyr"], (int(images["fyr"].get_width()//0.5), int(images["fyr"].get_height()//0.5))),
      "bru": pygame.transform.scale(images["bru"], (int(images["bru"].get_width()//0.5), int(images["bru"].get_height()//0.5))),
      "bir": pygame.transform.scale(images["bir"], (int(images["bir"].get_width()//0.5), int(images["bir"].get_height()//0.5))),
      "fraction": pygame.transform.scale(images["fraction"], (int(images["fraction"].get_width()//0.5), int(images["fraction"].get_height()//0.5))),
      "fire": pygame.transform.scale(images["fire"], (int(images["fire"].get_width()//0.4), int(images["fire"].get_height()//0.4))),
      "firo_bullet": pygame.transform.scale(images["firo_bullet"], (int(images["firo_bullet"].get_width()//0.7), int(images["firo_bullet"].get_height()//0.7))),
      "brum_bullet": pygame.transform.scale(images["brum_bullet"], (int(images["brum_bullet"].get_width()//0.8), int(images["brum_bullet"].get_height()//0.8))),


      "drill_indicator": pygame.transform.scale(images["drill_indicator"], (int(images["drill_indicator"].get_width()//0.22), int(images["drill_indicator"].get_height()//0.22))),


    }
    enemy_animation = {
      "злая_муха":[game_images('муха',False,3.3,3),game_images('атака_мухи',False,3.3,5),scaled_game_images['ded']],
      "сорк":[game_images('сорк',False,3.3,3),game_images('сорк_атакует',False,3.3,5),scaled_game_images['ded_sork']]

      
    } 
    ic = {
    'gumus_icon':pygame.transform.scale(gumus_frames[-1], (int(gumus_frames[-1].get_width()//2), int(gumus_frames[-1].get_height()//2))),
    'flycatcher_icon':pygame.transform.scale(flycatcher_frames[-1], (int(flycatcher_frames[-1].get_width()//2), int(flycatcher_frames[-1].get_height()//2))),
    'roc_icon':pygame.transform.scale(rock_frames[-1], (int(rock_frames[-1].get_width()//2), int(rock_frames[-1].get_height()//2))),
    'lol_icon':pygame.transform.scale(lol_frames[-1], (int(lol_frames[-1].get_width()//2), int(lol_frames[-1].get_height()//2))),

    'Angry_Fly': pygame.transform.scale(images["ded1"], (int(images["ded1"].get_width()//1.2), int(images["ded1"].get_height()//1.2))),
    'Angry_sork': pygame.transform.scale(images["ded_sork1"], (int(images["ded_sork1"].get_width()//1.2), int(images["ded_sork1"].get_height()//1.2))),
      }

    obj_frames ={


      'object':{
      
      'gumus':[description_object['gumus_description'],gumus_frames, ic['gumus_icon']],
      'flycatcher':[description_object['flycatcher_description'],flycatcher_frames,  ic['flycatcher_icon']],
      'roc':[description_object['rock_description'],rock_frames,  ic['roc_icon']],
      #'lol':[description_object['lol'],lol_frames,  ic['lol_icon']]


      },


    'minerals':{
         'pyro':[description_object['pyro'],scaled_game_images['fire'],scaled_game_images['pyro']],
         'fyr':[description_object['pyro1'],scaled_game_images['firo_bullet'],scaled_game_images['fyr']],
         'bru':[description_object['pyro2'],scaled_game_images['brum_bullet'],scaled_game_images['bru']],
         'bir':[description_object['pyro3'],scaled_game_images['fraction'],scaled_game_images['bir']],
    },

    "en":{
      'Angry_Fly':[description_object['Angry_Fly'],ic['Angry_Fly']],
      'Angry_sork':[description_object['Angry_sork'],ic['Angry_sork']]
      }


    }
    animation_images = {
    "drop_walk": game_images('анимация_шагания',False,2.5,6),
    "drop_charging": game_images('шаг',False,2.5,5),
    "drop_active": [game_images('шаг',False,2.5,5)[0]] + game_images('боевой_шаг',False,2.5,4),
    "drill_images":game_images('бур',False,3,7),
    "anim_spaceship":game_images('корабль',False,3.3,3),
    "training":[1]+game_images('пояснение',False,7.5,4),
    "aim": game_images('прицел',False,3,2),

    }





    minerals = []
    return obj_frames, analysis_icon, animation_images, scaled_game_images, minerals,enemy_animation,TEXTS

