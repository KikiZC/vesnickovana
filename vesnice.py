import pygame
import os

class Vesnice:
    def __init__(self,x,y,p):
        self.x = x
        self.y = y
        pygame.draw.circle(map_image,(0,255,0),(x,y),p)

def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

class Cesta:
    def __init__(self,x,y,p):
        pygame.draw.circle(map_image,(255,0,0),(x,y),p)

class Skupina:
    def __init__(self, nazev, pocatecni_bod, koncovy_bod):
        self.nazev = nazev
        self.pocatecni_bod = pocatecni_bod
        self.koncovy_bod = koncovy_bod

class Mapa:
    def vykresli_skupiny(self, skupiny):
        for skupina in skupiny:
            # zjistíme, které body cesty je potřeba projít
            body_cesty = [skupina.pocatecni_bod, skupina.koncovy_bod]
            for cesta in cesty:
                if cesta.collidepoint(skupina.pocatecni_bod) and cesta.collidepoint(skupina.koncovy_bod):
                    body_cesty.append(cesta.center)

            # namalujeme čáru mezi body cesty
            pygame.draw.lines(map_image, (0,0,255), False, [bod.xy for bod in body_cesty], 5)

def read_groups_from_file(filename):
    groups = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split(",")
            if len(fields) != 3:
                print(f"Invalid line in {filename}: {line}")
                continue
            group_name, start_village, end_village = fields
            groups.append((group_name, start_village, end_village))
    return groups

def create_group(start, end):
    vesnice_list = [vesnice1, vesnice2, vesnice3, vesnice4, vesnice5, vesnice6, vesnice7]
    cesta_list = [cesta1, cesta2, cesta3, cesta4, cesta5]
    VESNICE_RADIUS = 10

    # nalezení všech sousedních vesnic
    neighbors = []
    for vesnice in vesnice_list:
        if distance(vesnice.x, vesnice.y, start[0], start[1]) <= VESNICE_RADIUS:
            neighbors.append(vesnice)

    # nalezení nejkratší cesty z startu do konce
    shortest_path = []
    current = start
    while current != end:
        shortest_distance = None
        next_vesnice = None
        for neighbor in neighbors:
            if neighbor in shortest_path:
                continue
            d = distance(current[0], current[1], neighbor[0], neighbor[1])
            if shortest_distance is None or d < shortest_distance:
                shortest_distance = d
                next_vesnice = neighbor
        if next_vesnice is None:
            break
        shortest_path.append(next_vesnice)
        current = next_vesnice

    # vytvoření cesty
    for i in range(len(shortest_path)-1):
        start_vesnice = shortest_path[i]
        end_vesnice = shortest_path[i+1]
        for cesta in cesta_list:
            if (start_vesnice[0], start_vesnice[1]) == cesta[0:2] and (end_vesnice[0], end_vesnice[1]) == cesta[2:4]:
                pygame.draw.line(map_image, (255, 0, 0), (start_vesnice[0], start_vesnice[1]), (end_vesnice[0], end_vesnice[1]), 5)
                break

    # aktualizace obrazovky
    pygame.display.update()



# inicializace Pygame
pygame.init()

# nastavení velikosti okna
window_size = (1434, 1075)
screen = pygame.display.set_mode(window_size)

# načtení obrázku mapy
map_path = "c:/Users/kikiz/Desktop/map py/map3.jpg"
map_image = pygame.image.load(map_path)

# nastavení pozice a velikosti mapy na obrazovce
map_rect = map_image.get_rect()
map_rect.center = screen.get_rect().center

# vesnice
vesnice1 = Vesnice(211,158,10)
vesnice2 = Vesnice(747,279,10)
vesnice3 = Vesnice(508,556,10)
vesnice4 = Vesnice(1193,254,10)
vesnice5 = Vesnice(1178,607,10)
vesnice6 = Vesnice(917,991,10)
vesnice7 = Vesnice(232,941,10)

vesnice_list = [vesnice1, vesnice2, vesnice3, vesnice4 ,vesnice5 ,vesnice6, vesnice7]
# cesty
cesta1 = Cesta(388,296,10)
cesta2 = Cesta(604,455,10)
cesta3 = Cesta(885,649,10)
cesta4 = Cesta(892,793,10)
cesta5 = Cesta(396,917,10)

# seznam skupin
skupiny = []

# přidání nové skupiny
skupiny.append(Skupina("Skupina 1", vesnice1, vesnice3))


while True:
    # zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # vykreslení mapy do okna
    screen.blit(map_image, map_rect)

    # aktualizace obrazovky
    pygame.display.update()

    # přečtení souboru a vytvoření skupin
    groups = read_groups_from_file("c:/Users/kikiz/Desktop/map py/skupiny.txt")
    for group in groups:
        start_vesnice = group[0]
        end_vesnice = group[1]
        create_group(start_vesnice, end_vesnice)

    # pauza
    pygame.time.delay(1000) # počkej 1 sekundu
    # aktualizace obrazovky
    pygame.display.update()
