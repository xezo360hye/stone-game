import pygame
import sys

# Constants
DEPTH = 15
DEFAULT_ALGORITHM = "minimax"
DEFAULT_STONES = ""


# Initialize Pygame
pygame.init()


# Set up the window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stones Game")


# Some text stuff
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)
make_black_text = lambda text: font.render(text, True, (0, 0, 0))
make_white_text = lambda text: font.render(text, True, (255, 255, 255))


# Decorator to display the window
def pygame_window(func):
    def wrapper(*args, **kwargs):
        window.fill((255, 255, 255))
        func(*args, **kwargs)
        pygame.display.update()
    return wrapper


# Function to display the entry screen
# Function to display the entry screen
@pygame_window
def entry_screen(stones, algorithm, player_moves):
    start = make_black_text("Select number of stones and press ENTER")
    welcome = make_black_text("Welcome to Stone Game")
    stones = make_black_text(f"Stones (50-70): {stones}")
    algorithm = make_black_text(f"Select algorithm: {'Minimax (M)' if algorithm == 'minimax' else 'Alpha-Beta (A)'}")
    player = make_black_text(f"Player moves first: {'Yes (P)' if player_moves else 'No (B)'}")

    window.blit(start, (50, 210))
    window.blit(welcome, (250, 50))
    window.blit(stones, (250, 350))
    window.blit(algorithm, (250, 400))
    window.blit(player, (250, 450))



# Function to display the game screen
@pygame_window
def game_screen(game):
    score = lambda name, player: f"{name} score: {player.points} points, {player.stones} stones"

    player_score = make_black_text(score("Player", game.player))
    ai_bot_score = make_black_text(score("AI bot", game.ai_bot))
    stones_left = make_black_text(f"Stones Left: {game.stones}")

    window.blit(player_score, (50, 50))
    window.blit(ai_bot_score, (50, 100))
    window.blit(stones_left, (50, 150))


# Function to display end game screen
@pygame_window
def end_game_screen(player_score, ai_bot_score):
    # Winner text
    if player_score > ai_bot_score:
        winner = make_black_text(f"Winner: Player")
    elif player_score < ai_bot_score:
        winner = make_black_text(f"Winner: AI bot")
    else:
        winner = make_black_text(f"It's a draw!")

    # Score text
    player_score = make_black_text(f"Player score: {player_score}")
    ai_bot_score = make_black_text(f"AI bot score: {ai_bot_score}")

    # Other texts
    game_over = make_black_text("GAME OVER")
    play_again = make_white_text("Play Again (R)")
    quit = make_white_text("Quit (Q)")

    # Buttons background
    pygame.draw.rect(window, BLACK, (200, 400, 200, 50))
    pygame.draw.rect(window, BLACK, (400, 400, 200, 50))

    # Display texts
    window.blit(game_over, (300, 200))
    window.blit(winner, (300, 250))
    window.blit(player_score, (300, 300))
    window.blit(ai_bot_score, (300, 350))
    window.blit(play_again, (210, 410))
    window.blit(quit, (450, 410))


# Function to simulate the game
from game import Game
def play_game(stones, algorithm, player_moves):
    game = Game(stones)
    algorithms = {"minimax": game.minimax, "alpha-beta": game.alpha_beta}
    while game:
        game_screen(game)
        if player_moves:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif (event.type == pygame.KEYDOWN and
                      event.key in (pygame.K_2, pygame.K_3)):
                    game.make_player_move(int(chr(event.key)))
                    player_moves = not player_moves
        else:
            _, move = algorithms[algorithm](DEPTH)
            game.make_ai_bot_move(move)

            player_moves = not player_moves

    return (game.player.points + game.player.stones,
            game.ai_bot.points + game.ai_bot.stones)



stones = DEFAULT_STONES
algorithm = DEFAULT_ALGORITHM
player_moves = True

while True:
    entry_screen(stones, algorithm, player_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if (num := event.unicode).isdigit():
                stones += num

            elif event.key == pygame.K_BACKSPACE:
                stones = stones[:-1]

            elif event.key == pygame.K_m:
                algorithm = "minimax"

            elif event.key == pygame.K_a:
                algorithm = "alpha-beta"

            elif event.key == pygame.K_p:
                player_moves = True

            elif event.key == pygame.K_b:
                player_moves = False

            elif event.key == pygame.K_RETURN:
                try:
                    stones_num = int(stones)
                    if stones_num > 70 or stones_num < 50:
                        continue
                except ValueError:
                    continue

                player_score, ai_bot_score = play_game(stones_num, algorithm, player_moves)
                end_game_screen(player_score, ai_bot_score)

                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if (event.type == pygame.QUIT or
                            event.type == pygame.KEYDOWN and
                            event.key == pygame.K_q):
                            pygame.quit()
                            sys.exit()

                        if (event.type == pygame.KEYDOWN and
                            event.key == pygame.K_r):
                            stones = ""
                            waiting_for_input = False
