# první část = výpočet nejkradší cesty
import heapq

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    predecessors = {}
    predecessors_time = {}
    while queue:
        (current_distance, current_node) = heapq.heappop(queue)
        time = []
        if current_node == end:
            path = []
            current_time = current_node
            while current_node in predecessors:
                path.append(current_node)
                current_node = predecessors[current_node]
            path.append(start)
            path.reverse()
            while current_time in predecessors_time:
                time.append(predecessors_time[current_time])
                current_time = predecessors[current_time]
                print(current_time)
            print(predecessors_time)
            time.append(0)
            time.reverse()
            return path, distances[end], time
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                predecessors[neighbor] = current_node
                predecessors_time[neighbor] = weight
    return None, None

graph = {
    'A': {'K': 2},
    'B': {'K': 2},
    'C': {'L': 2},
    'D': {'L': 2},
    'E': {'M': 3},
    'F': {'O': 2},
    'G': {'O': 2},
    'H': {'N': 2},
    'I': {'N': 2},
    'J': {'N': 2},
    'K': {'A': 2, 'B': 2, 'L': 2},
    'L': {'C': 2, 'D': 2, 'K': 2, 'M': 2},
    'M': {'L': 2, 'N': 2, 'O': 2, 'E': 2},
    'N': {'H': 2, 'I': 2, 'J': 4, 'M': 2},
    'O': {'M': 2, 'G': 2, 'H': 2}
}

start = 'A'
end = 'I'

path, distance, time = dijkstra(graph, start, end)
if path is not None:
    print(f"Skupina šla z bodu {start} do bodu {end} přes body: {path}")
    print("                                         ", time)
    print(f"Celková délka cesty: {distance}")
else:
    print(f"Nelze najít cestu z bodu {start} do bodu {end}") 
# první část konec



# druhá část začátek = zobrazení skupinky

import pygame
import sys

WIDTH, HEIGHT = 1440, 1075
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Skupina na cestě')

map_path = "c:/Users/kikiz/Desktop/map py/map 4.jpg"
map_image = pygame.image.load(map_path)
map_rect = map_image.get_rect()
map_rect.center = screen.get_rect().center

# Tabulka s pozicemi bodů
table = {
    'A': (211, 163),
    'B': (560, 152),
    'C': (257, 507),
    'D': (604, 366),
    'E': (461, 821),
    'F': (873, 529),
    'G': (988, 185),
    'H': (1250, 677),
    'I': (1205, 928),
    'J': (930, 894),
    'K': (377, 183),
    'L': (395, 470),
    'M': (637, 639),
    'N': (930, 666),
    'O': (814, 334),
}

# Vstupní seznam bodů
input_points = path

# Rychlost pohybu tečky (v pixelech za sekundu)
velocity = 5

# Počáteční pozice tečky
x, y = table[input_points[0]]

# Index aktuálního bodu v seznamu
current_point = 0

# Hlavní smyčka programu
while True:
    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Kontrola, zda existuje další bod v seznamu
    if current_point < len(input_points) - 1:
        # Získání aktuálního a následujícího bodu
        current_point_name = input_points[current_point]
        next_point_name = input_points[current_point + 1]

        # Získání aktuální a následující pozice
        current_x, current_y = table[current_point_name]
        next_x, next_y = table[next_point_name]

        # Výpočet vzdálenosti mezi body
        distance = ((next_x - current_x) ** 2 + (next_y - current_y) ** 2) ** 0.5

        # Výpočet směru pohybu tečky
        direction_x = (next_x - current_x) / distance
        direction_y = (next_y - current_y) / distance

        # Pohyb tečky směrem k následujícímu bodu
        if distance > 0:
            x += direction_x * min(distance, velocity)
            y += direction_y * min(distance, velocity)

        # Kontrola dosažení následujícího bodu
        if (direction_x > 0 and x >= next_x) or (direction_x < 0 and x <= next_x) or (direction_y > 0 and y >= next_y) or (direction_y < 0 and y <= next_y):
            current_point += 1

            # Zastavení tečky na bodě
            x, y = next_x, next_y

    # Vykreslení pozadí
    #screen.fill((0, 0, 0))
    screen.blit(map_image, map_rect)

    # Vykreslení tečky
    pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), 15)

    # Aktualizace obrazovky
    pygame.display.flip()

    # Pauza mezi snímky (časování 60 FPS)
    pygame.time.Clock().tick(60)
