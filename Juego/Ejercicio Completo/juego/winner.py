import pygame
from juego.constants import IA_MATCH, WIDTH, HEIGHT, BOARD_BORDER
def menu_winner():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH + BOARD_BORDER * 2, HEIGHT + BOARD_BORDER * 2))
    pygame.display.set_caption("Las Damas")

    background = pygame.image.load("assets/assets_menu/fondoWinner.png")
    background = pygame.transform.scale(background, (WIDTH + BOARD_BORDER * 2, HEIGHT + BOARD_BORDER * 2))

    WHITE = (255, 255, 255)
    RED = (200, 50, 50)

    pygame.font.init()
    button_font = pygame.font.Font(None, 30)

    def render_text_fit(text, font, max_width, color):
        while font.size(text)[0] > max_width - 20:
            font = pygame.font.Font(None, font.get_height() - 1)
        return font.render(text, True, color)

    button_width = 250
    button_height = 50
    button_x = (WIDTH - button_width) // 2 + BOARD_BORDER
    button_y1 = 480
    button_y2 = 550

    buttons = [
        {
            "text": "VOLVER AL MENÚ",
            "rect": pygame.Rect(button_x, button_y1, button_width, button_height),
            "original_rect": pygame.Rect(button_x, button_y1, button_width, button_height),
            "border_color": WHITE,
            "text_color": WHITE,
            "action": lambda: print("Modo Jugador seleccionado"),
            "hovered": False
        },
        {
            "text": "SALIR",
            "rect": pygame.Rect(button_x, button_y2, button_width, button_height),
            "original_rect": pygame.Rect(button_x, button_y2, button_width, button_height),
            "border_color": RED,
            "text_color": RED,
            "action": lambda: exit(),
            "hovered": False
        }
    ]

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        screen.blit(background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        button["action"]()

        for button in buttons:
            if button["rect"].collidepoint(mouse_pos):
                if not button["hovered"]:
                    button["hovered"] = True
                    new_width = int(button["original_rect"].width * 1.1)
                    new_height = int(button["original_rect"].height * 1.1)
                    new_x = button["original_rect"].centerx - new_width // 2
                    new_y = button["original_rect"].centery - new_height // 2
                    button["rect"] = pygame.Rect(new_x, new_y, new_width, new_height)
            else:
                if button["hovered"]:
                    button["hovered"] = False
                    button["rect"] = button["original_rect"].copy()

            pygame.draw.rect(screen, button["border_color"], button["rect"], width=2, border_radius=8)
            text_rendered = render_text_fit(button["text"], button_font, button["rect"].width, button["text_color"])
            text_x = button["rect"].x + (button["rect"].width - text_rendered.get_width()) // 2
            text_y = button["rect"].y + (button["rect"].height - text_rendered.get_height()) // 2
            screen.blit(text_rendered, (text_x, text_y))

        pygame.display.flip()

    pygame.quit()