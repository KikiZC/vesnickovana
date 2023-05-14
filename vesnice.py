import heapq
import pygame

# Část první
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
    'A': {'O': 2},
    'B': {'P': 2},
    'C': {'P': 2},
    'D': {'Q': 2},
    'E': {'Q': 2},
    'F': {'R': 2},
    'G': {'S': 2},
    'O': {'A': 2, 'P': 2, 'S': 4},
    'P': {'O': 2, 'Q': 2, 'C': 2, 'B': 2},
    'Q': {'P': 2, 'R': 2, 'D': 2, 'E': 2},
    'R': {'Q': 2, 'S': 2, 'F': 2},
    'S': {'R': 2, 'G': 3, 'O': 4}
}

position = {
    'A': {211,158},
    'B': {747,279},
    'C': {508,556},
    'D': {1193,254},
    'E': {1178,607},
    'F': {917,991},
    'G': {232,941},
    'O': {388,296},
    'P': {604,455},
    'Q': {885,649},
    'R': {892,793},
    'S': {396,917}
}

start = 'E'
end = 'G'

path, distance, time = dijkstra(graph, start, end)
if path is not None:
    print(f"Skupina šla z bodu {start} do bodu {end} přes body: {path}")
    print("                                         ", time)
    print(f"Celková délka cesty: {distance}")
else:
    print(f"Nelze najít cestu z bodu {start} do bodu {end}") 

#Konec části první

# část druhá

import pygame
import math

# Nastavení rozměrů okna a barvy pozadí
WIDTH, HEIGHT = 1440, 1075

# Nastavení proměnných pro vzdálenosti a pozice bodů
distance = time
positions = {
    'A': [208, 151],
    'B': [752, 280],
    'C': [506, 562],
    'D': [1193, 254],
    'E': [1178, 607],
    'F': [920, 980],
    'G': [240, 935],
    'O': [388, 302],
    'P': [604, 455],
    'Q': [885, 649],
    'R': [892, 793],
    'S': [396, 917]
}

# Funkce pro vykreslení cesty
def draw_path(screen, path, start, end):
    # Výpočet nejkratší cesty
    shortest_path = [start]
    while len(shortest_path) < len(path):
        distances = [(p, math.dist(positions[shortest_path[-1]], positions[p])) for p in path if p not in shortest_path]
        closest = min(distances, key=lambda x: x[1])[0]
        shortest_path.append(closest)

    # Vykreslení pozadí
    screen.blit(map_image, map_rect)

    # Vykreslení bodů
    for point, pos in positions.items():
        color = (0, 0, 0)
        if point == start or point == end:
            color = (255, 0, 0)
        pygame.draw.circle(screen, color, pos, 10)

    # Vykreslení cesty skupiny
    current_pos = positions[start]
    for point in shortest_path:
        next_pos = positions[point]
        pygame.draw.line(screen, (0, 255, 0), current_pos, next_pos, 5)
        current_pos = next_pos

    # Vykreslení skupiny
    group_pos = positions[start]
    for dist in distance:
        if shortest_path:
            next_point = shortest_path.pop(0)
            next_pos = positions[next_point]
            dx, dy = next_pos[0] - group_pos[0], next_pos[1] - group_pos[1]
            direction = math.atan2(dy, dx)
            group_pos = [int(group_pos[0] + dist * math.cos(direction)), int(group_pos[1] + dist * math.sin(direction))]
            pygame.draw.circle(screen, (255, 0, 0), group_pos, 20)

# Inicializace knihovny Pygame a okna
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Skupina na cestě')

map_path = "c:/Users/kikiz/Desktop/map py/map3.jpg"
map_image = pygame.image.load(map_path)
map_rect = map_image.get_rect()
map_rect.center = screen.get_rect().center

# Nastavení startovacího a koncového bodu
start = 'A'
end = 'F'

# Hlavní smyčka hry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vykreslení cesty a skupiny
    draw_path(screen, path, start, end)

    # Zobrazit vykreslené objekty na obrazovce
    pygame.display.update()

# Ukončení Pygame
pygame.quit()
