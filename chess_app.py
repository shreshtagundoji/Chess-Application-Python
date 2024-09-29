import chess_board
import pygame as py
from player import Player

WIDTH = HEIGHT = 512  # width and height of the chess board
CENTER = 256
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color(238, 238, 210), py.Color(105, 146, 62)]  # Light green, Dark green
HIGHLIGHT_COLOR = py.Color(255, 255, 0)  # Bright yellow for highlighting

MARGIN = 50  # margin for the golden border
WINDOW_SIZE = (WIDTH + 2 * MARGIN, HEIGHT + 2 * MARGIN)

SCREEN = py.display.set_mode(WINDOW_SIZE)

py.init()
py.mixer.init()
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = py.image.load("images/Background.png")

try:
    BACKGROUND_MUSIC = py.mixer.Sound("sounds/game.wav")
    BACKGROUND_MUSIC.set_volume(0.2)  # Set volume to 50%, adjust as needed
except py.error.PYGAME_ERROR:
    print("Warning: Background music file not found or audio device unavailable.")
    BACKGROUND_MUSIC = None

try:
    MOVE_SOUND = py.mixer.Sound("sounds/move.wav")
    CAPTURE_SOUND = py.mixer.Sound("sounds/capture.wav")
    MOVE_SOUND.set_volume(0.9)  # Set volume to 90%
    CAPTURE_SOUND.set_volume(0.9)  # Set volume to 90%
except py.error.PYGAME_ERROR:
    print("Warning: Sound files not found or audio device unavailable.")
    MOVE_SOUND = None
    CAPTURE_SOUND = None

py.mixer.set_num_channels(8)  # Increase the number of audio channels

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
    return py.font.Font("images/font.ttf", size)

def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))

def draw_game_state(screen, game_state, valid_moves, square_selected):
    '''
    Draw the complete chess board with pieces
    Keyword arguments:
    :param screen -- the pygame screen
    :param game_state -- the state of the current chess game
    '''
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)

# def draw_squares(screen):
#     '''
#     Draw the chess board with the alternating two colors
#     :param screen: -- the pygame screen
#     '''
#     for r in range(DIMENSION):
#         for c in range(DIMENSION):
#             color = colors[(r + c) % 2]
#             py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
def draw_squares(screen):
    '''
    Draw the chess board with the alternating light and dark green colors
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, game_state):
    '''
    Draw the chess pieces onto the board
    :param screen: -- the pygame screen
    :param game_state: -- the current state of the chess game
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()], py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# def draw_menu_background():
#     SCREEN.fill((0, 0, 0))  # Black background
#     py.draw.rect(SCREEN, (182, 143, 64), (MARGIN, MARGIN, WIDTH, HEIGHT))  # Golden border

def draw_rounded_rect(surface, color, rect, radius):
    py.draw.rect(surface, color, rect, border_radius=radius)

class RoundedButton(Button):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        super().__init__(image, pos, text_input, font, base_color, hovering_color)
        self.rect = py.Rect(pos[0] - 100, pos[1] - 20, 200, 40)
        self.color = (238, 238, 210)  # Light beige color

    def update(self, screen):
        draw_rounded_rect(screen, self.color, self.rect, 20)
        self.changeColor(py.mouse.get_pos())
        screen.blit(self.text, self.text_rect)

def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row, col = square_selected
        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
           (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # highlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(HIGHLIGHT_COLOR)
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            
            # highlight move squares
            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))

def draw_text(screen, text):
    font = py.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, True, py.Color(238, 238, 210))  # Green color
    
    # Create a black rectangle
    rect_width = text_object.get_width() + 20  # Add some padding
    rect_height = text_object.get_height() + 20
    rect = py.Rect(0, 0, rect_width, rect_height)
    rect.center = (WIDTH // 2, HEIGHT // 2)
    
    # Draw the black rectangle
    py.draw.rect(screen, py.Color("Black"), rect)
    
    # Draw the text
    text_rect = text_object.get_rect(center=rect.center)
    screen.blit(text_object, text_rect)

def play_background_music():
    if BACKGROUND_MUSIC:
        BACKGROUND_MUSIC.play(-1)  # -1 means loop indefinitely

def stop_background_music():
    if BACKGROUND_MUSIC:
        BACKGROUND_MUSIC.stop()

def multi_player():
    SCREEN.fill("black")
    clock = py.time.Clock()
    game_state = chess_board.game_state()
    load_images()
    play_background_music()  # Start background music

    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    game_over = False

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
                stop_background_music()  # Stop background music when quitting
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                        else:
                            move_made = game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                                              (player_clicks[1][0], player_clicks[1][1]), False)
                            if move_made:
                                if MOVE_SOUND and CAPTURE_SOUND:
                                    if game_state.get_piece(player_clicks[1][0], player_clicks[1][1]) == Player.EMPTY:
                                        MOVE_SOUND.play()
                                    else:
                                        CAPTURE_SOUND.play()
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                    else:
                        valid_moves = game_state.get_valid_moves((row, col))
                        if valid_moves is None:
                            valid_moves = []
            elif e.type == py.KEYDOWN:
                if e.key == py.K_r:
                    game_over = False
                    game_state = chess_board.game_state()
                    valid_moves = []
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                elif e.key == py.K_u:
                    game_state.undo_move()
                    print(len(game_state.move_log))

        draw_game_state(SCREEN, game_state, valid_moves, square_selected)

        endgame = game_state.checkmate_stalemate_checker()
        if endgame == 0:
            game_over = True
            draw_text(SCREEN, "Black wins!")
            stop_background_music()
        elif endgame == 1:
            game_over = True
            draw_text(SCREEN, "White wins!")
            stop_background_music()
        elif endgame == 2:
            game_over = True
            draw_text(SCREEN, "Uh oh! Stalemate.")
            stop_background_music()

        clock.tick(MAX_FPS)
        py.display.flip()


def menu():
    py.display.set_caption("Chess")
    while True:
        SCREEN.fill((0, 0, 0))  # Black background
        MENU_MOUSE_POS = py.mouse.get_pos()

        MENU_TEXT = get_font(45).render("Chess", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        MULTI_PLAYER_BUTTON = RoundedButton(image=None, pos=(WIDTH // 2, 250),
                                            text_input="Start Game", font=get_font(25), 
                                            base_color="#b68f40", hovering_color="Green")

        QUIT_BUTTON = RoundedButton(image=None, pos=(WIDTH // 2, 350),
                                    text_input="QUIT", font=get_font(25), 
                                    base_color="#b68f40", hovering_color="Green")

        for button in [MULTI_PLAYER_BUTTON, QUIT_BUTTON]:
            button.update(SCREEN)

        for event in py.event.get():
            if event.type == py.QUIT:
                stop_background_music()
                py.quit()
                exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if MULTI_PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    multi_player()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    stop_background_music()
                    py.quit()
                    exit()

        py.display.update()

if __name__ == "__main__":
    menu()
