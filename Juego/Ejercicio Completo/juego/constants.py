import pygame

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
BOARD_BORDER = 50
TIME = 60000

IA_MATCH = False
DB_ACTIVE = False
CAPTURA_OBLIGATORIA = True
PROFUNDIDAD = 4

pink_piece = pygame.transform.scale(pygame.image.load('assets/piezas/pink_piece.png'), (SQUARE_SIZE, SQUARE_SIZE))
blue_piece = pygame.transform.scale(pygame.image.load('assets/piezas/blue_piece2.png'), (SQUARE_SIZE, SQUARE_SIZE))
pink_crown = pygame.transform.scale(pygame.image.load('assets/piezas/pink_crown.png'), (SQUARE_SIZE // 2, SQUARE_SIZE // 2))
blue_crown = pygame.transform.scale(pygame.image.load('assets/piezas/blue_crown.png'), (SQUARE_SIZE // 2, SQUARE_SIZE // 2))

# array de imagenes de numeros
numeros_neon = [
    pygame.transform.scale(pygame.image.load(f'assets/numero/numero_{i}.png'), (SQUARE_SIZE // 2, SQUARE_SIZE // 2))
    for i in range(8, 0,-1)  # Carga numero_1.png hasta numero_8.png
]

letras = ["a", "b", "c", "d", "e", "f", "g", "h"]
letras_neon = [
    pygame.transform.scale(pygame.image.load(f'assets/letra/letra_{letra}.png'), (SQUARE_SIZE // 2, SQUARE_SIZE // 2)) for letra in letras
]


PINK = (133, 43, 229)  # jugaodr
BLUE = (46, 253, 253)  # ia
BLACK = (0, 0, 0)
# colores degradado
PURPLE = (140, 82, 255)
ORANGE = (255, 145, 77)

WHITE = (255, 255, 255)
COLOR_STROKE = (WHITE)
