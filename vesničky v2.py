import heapq
import pygame
import random

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
                current_time = predecessors_time[current_time]
            time.append(0)
            time.reverse()
            return path, time
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
    'O': {'M': 2, 'G': 2, 'F': 2}
}

pocet_skupin = int(input("Zadejte počet skupin: "))
cesty = []
barvy = []
velocity = 0.1

for i in range(pocet_skupin):
    start = input(f"Zadejte počáteční bod skupiny {i+1}: ")
    end = input(f"Zadejte koncový bod skupiny {i+1}: ")
    path, time = dijkstra(graph, start, end)
    if path:
        cesty.append((path, time))
        barva = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        barvy.append(barva)
    else:
        print(f"Pro skupinu {i+1} neexistuje cesta.")

WIDTH, HEIGHT = 1440, 1075
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Skupina na cestě')

map_path = "c:/Users/kikiz/Desktop/map py/map 4.jpg"
map_image = pygame.image.load(map_path)
map_rect = map_image.get_rect()
map_rect.center = screen.get_rect().center

current_points = [0] * pocet_skupin
fractional_steps = [0.0] * pocet_skupin
positions = [table[path[0]] for path, _ in cesty]
finished = [False] * pocet_skupin

# Hlavní smyčka programu
running = True
while running:
    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pohyb teček
    for i, (path, _) in enumerate(cesty):
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

    # Vykreslení pozadí
    screen.blit(map_image, map_rect)

    # Vykreslení teček
    for i, position in enumerate(positions):
        color = barvy[i % len(barvy)]  # Získání barvy pro každý bod na základě indexu
        pygame.draw.circle(screen, color, (int(position[0]), int(position[1])), 15)


    # Aktualizace obrazovky
    pygame.display.flip()

# Ukončení programu
pygame.quit()
