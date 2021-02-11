import os
import sys

import pygame
import requests


map_file = None
spn_number = [0.01, 0.02, 0.03, 0.05, 0.09, 0.18, 0.35, 0.7, 1.4, 2.8, 5.6, 11.1, 21.65, 40]
spn_count = 0
spn = 0.01


def draw():
    global map_file

    map_params = {
        "ll": "37.530887,55.703118",
        "spn": str(spn) + ',' + str(spn),
        "l": "map"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
draw()
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
running = True
while running:
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_PAGEUP or event.key == pygame.K_UP:
                os.remove(map_file)
                if spn_count + 1 != len(spn_number):
                    spn_count += 1
                spn = spn_number[spn_count]
                draw()
            if event.type == pygame.K_PAGEDOWN or event.key == pygame.K_DOWN:
                os.remove(map_file)
                if spn_count > 0:
                    spn_count -= 1
                spn = spn_number[spn_count]
                draw()

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)