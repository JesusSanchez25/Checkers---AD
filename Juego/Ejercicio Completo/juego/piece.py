from juego.constants import SQUARE_SIZE, PINK, pink_piece, BOARD_BORDER, pink_crown, BLUE, blue_piece, blue_crown


class Piece:
    PADDING = 8
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    # la posicion iguala a la casilla del tablero multiplicado por la columna/fila donde esta
    def calculate_position(self):
        self.x = SQUARE_SIZE * self.col
        self.y = SQUARE_SIZE * self.row

    def crowning(self):
        self.queen = True

    def draw(self, win):
        if self.color == PINK:
            for i in range(3):
                win.blit(pink_piece, (self.x + BOARD_BORDER, self.y + BOARD_BORDER))
            if self.queen:
                for i in range(1):
                    win.blit(pink_crown, ((self.x + pink_crown.get_width() // 2) + BOARD_BORDER,
                                          (self.y + pink_crown.get_width() // 2) + BOARD_BORDER))
        if self.color == BLUE:
            for i in range(5):
                win.blit(blue_piece, (self.x + BOARD_BORDER, self.y + BOARD_BORDER))
            if self.queen:
                for i in range(1):
                    win.blit(blue_crown, ((self.x + blue_crown.get_width() // 2) + BOARD_BORDER, (self.y + blue_crown.get_width() // 2) + BOARD_BORDER))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()

    def __repr__(self):
        return str(self.color)
