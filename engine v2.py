import pygame
import ast


table = {
    'M1': (303,131),
    'M2': (933,481),
    'M3': (1737,391),
    'M4': (1520,715),
    'M5': (1400,1281),
    'M6': (796,1083),
    'M7': (187,1164),
    'V1': (134,708),
    'V2': (509,593),
    'V3': (605,329),
    'V4': (211,359),
    'V5': (766,109),
    'V6': (1140,228),
    'V7': (1572,158),
    'V8': (1381,541),
    'V9': (1793,582),
    'V10': (1557,884),
    'V11': (1120,837),
    'V12': (1843,1054),
    'V13': (1689,1326),
    'V14': (1269,1120),
    'V15': (869,1315),
    'V16': (362,1369),
    'V17': (558,1064),
    'V18': (531,798),
    'V19': (134,896),
    'C1': (379,596),
    'C2': (436,154),
    'C3': (806,229),
    'C4': (1134,294),
    'C5': (1139,372),
    'C6': (1553,353),
    'C7': (1390,657),
    'C8': (1731,731),
    'C9': (1556,794),
    'C10': (1192,1001),
    'C11': (1124,939),
    'C12': (978,985),
    'C13': (638,1216),
    'C14': (568,1329),
    'C15': (457,937),
    'C16': (192,991),
}

pocet_skupin = 0
cesty = []
barvy = []
velocity = 0.5
positions = []
current_points = []
fractional_steps = []
finished = []

WIDTH, HEIGHT = 1920, 1440
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Skupina na cestě')

map_path = "mapa.jpg"
map_image = pygame.image.load(map_path)
map_rect = map_image.get_rect()
map_rect.center = screen.get_rect().center

processed_lines = set()

# Hlavní smyčka programu
running = True
while running:
    screen.blit(map_image, map_rect)
    try:
        with open("skupiny.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line not in processed_lines:  # Kontrola, zda řádka již byla zpracována
                    parts = line.strip().split(":")
                    if len(parts) == 4:
                        path = ast.literal_eval(parts[1])
                        barva = ast.literal_eval(parts[2])
                        progress = ast.literal_eval(parts[3])
                        cesty.append(path)
                        barvy.append(barva)
                        current_points.append(0)
                        fractional_steps.append(0.0)
                        positions.append(table[path[0]])
                        finished.append(False)
                        processed_lines.add(line)
            #os.remove("c:/Users/kikiz/Desktop/map py/mapa se souborem/skupiny.txt")
    except FileNotFoundError:
        print("soubor neni")
    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Pohyb teček
    for i, path in enumerate(cesty):
        if finished[i]:
            continue
        if current_points[i] < len(path) - 1:
            current_point_name = path[current_points[i]]
            next_point_name = path[current_points[i] + 1]

            current_x, current_y = table[current_point_name]
            next_x, next_y = table[next_point_name]

            distance = ((next_x - current_x) ** 2 + (next_y - current_y) ** 2) ** 0.5

            direction_x = (next_x - current_x) / distance
            direction_y = (next_y - current_y) / distance

            if distance > 0:
                fractional_steps[i] += velocity / distance
                if fractional_steps[i] >= 1.0:
                    current_points[i] += 1
                    fractional_steps[i] = 0.0
                x = current_x + fractional_steps[i] * (next_x - current_x)
                y = current_y + fractional_steps[i] * (next_y - current_y)
                positions[i] = (x, y)
        elif current_points[i] == len(path) - 1:
            current_point_name = path[current_points[i]]
            current_x, current_y = table[current_point_name]
            positions[i] = (current_x, current_y)
            finished[i] = True  # Skupina dosáhla cíle

    # Vykreslení teček s pohybem
    for i, path in enumerate(cesty):
        if current_points[i] < len(path) - 1:
            current_point_name = path[current_points[i]]
            next_point_name = path[current_points[i] + 1]

            current_x, current_y = table[current_point_name]
            next_x, next_y = table[next_point_name]

            distance = ((next_x - current_x) ** 2 + (next_y - current_y) ** 2) ** 0.5

            direction_x = (next_x - current_x) / distance
            direction_y = (next_y - current_y) / distance

            if distance > 0:
                x = current_x + fractional_steps[i] * (next_x - current_x)
                y = current_y + fractional_steps[i] * (next_y - current_y)
                positions[i] = (x, y)

        color = barvy[i % len(barvy)]
        pygame.draw.circle(screen, color, (int(positions[i][0]), int(positions[i][1])), 15)

    # Aktualizace obrazovky
    pygame.display.flip()

# Ukončení programu
pygame.quit()
