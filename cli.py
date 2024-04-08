from utils import ask_range, ask_in
from game import Game

stones = ask_range("> Enter number of stones (50-70): ", 50, 70)
game = Game(stones)

player_moves = ask_in("> Who goes first? (P)layer or (A)I bot: ", ('p', 'a'))
algorithm = ask_in("> Choose algorithm: (M)inimax or (A)lpha-beta: ", ('m', 'a'))
depth = ask_range("> Enter search depth (1-15): ", 1, 15)

depth = int(depth)
player_moves = (player_moves == 'p')
algorithm = {'m': game.minimax,
             'a': game.alpha_beta}[algorithm]


# Game loop
while game:
    print()
    print(f"=====================")
    print(f"| Stones left: {game.stones}")
    print(f"| Player: {game.player}")
    print(f"| AI bot: {game.ai_bot}")

    if player_moves:
        move = ask_range("> Enter number of stones to remove (2-3): ", 2, min(3, game.stones))
        game.make_player_move(move)

    else:
        _, move = algorithm(depth)
        game.make_ai_bot_move(move)

        print(f"* AI bot moves: {move}")

    player_moves = not player_moves


# Final scores
player_score = game.player.stones + game.player.points
ai_bot_score = game.ai_bot.stones + game.ai_bot.points

print(f"Player score: {game.player.stones} + {game.player.points} = {player_score}")
print(f"AI bot score: {game.ai_bot.stones} + {game.ai_bot.points} = {ai_bot_score}")

if player_score > ai_bot_score:
    print("Player wins!")

elif player_score < ai_bot_score:
    print("AI bot wins!")

else:
    print("It's a draw!")
