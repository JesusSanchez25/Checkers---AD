import pygame
import sys
import time

# Inicializar pygame
pygame.init()

# Dimensiones y constantes
HEIGHT = 600
BOARD_BORDER = 20
SQUARE_SIZE = 75
IA_MATCH = False  # Ejemplo de partida sin IA

# Ventana del juego
win = pygame.display.set_mode((HEIGHT, HEIGHT))
pygame.display.set_caption("Tablero de Damas con Cuenta Atrás")

# Colores y fuente
WHITE = (255, 255, 255)
BLUE = (23, 151, 253)
PINK = (255, 0, 254)
font = pygame.font.Font(None, 36)  # Tamaño de fuente ajustable

# Duración del temporizador en segundos
initial_time = 300  # 5 minutos

# Función para formatear el tiempo
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

# Función principal
def main():
    clock = pygame.time.Clock()
    start_time = time.time()
    running = True

    while running:
        win.fill((0, 0, 0))  # Limpia la pantalla

        # Calcular el tiempo restante
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, initial_time - elapsed_time)

        # Formatear el tiempo restante
        time_text = font.render(format_time(remaining_time), True, WHITE)
        blue_time = font.render(format_time(remaining_time), True, BLUE)
        pink_time = font.render(format_time(remaining_time), True, PINK)

        # Dibujar el temporizador en el tablero
        for row in range(8):
            if row == 0:
                if IA_MATCH:
                    win.blit(time_text, (HEIGHT // 2 + BOARD_BORDER // 4, SQUARE_SIZE // 6))
                else:
                    win.blit(pink_time, (HEIGHT // 4 + BOARD_BORDER // 4, SQUARE_SIZE // 6))
                    win.blit(blue_time, (HEIGHT // 4 * 3 + BOARD_BORDER // 4, SQUARE_SIZE // 6))

        # Controlar los eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del bucle
        clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print(pygame.font.get_fonts())
    main()
