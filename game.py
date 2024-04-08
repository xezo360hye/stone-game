from dataclasses import dataclass

@dataclass
class Player:
    points: int = 0
    stones: int = 0


class Game:
    def __init__(self, stones: int) -> None:
        self.stones = stones
        self.player = Player()
        self.ai_bot = Player()

    def heuristic_eval(self) -> int:
        """
        Heuristic evaluation function

        Implemented as the difference between the AI bot's and player's points and stones
        """
        return ((self.ai_bot.points + self.ai_bot.stones)-
                (self.player.points + self.player.stones))


    def make_move(self, current: Player, move: int) -> None:
        self.stones -= move
        current.stones += move

        if self.stones % 2 == 1:
            current.points += 2

        else:
            opponent = (self.player, self.ai_bot)[current is self.player]
            opponent.points += 2


    def undo_move(self, current: Player, move: int) -> None:
        opponent = (self.player, self.ai_bot)[current is self.player]
        if self.stones % 2 == 0:
            opponent.points -= 2

        else:
            current.points -= 2

        current.stones -= move
        self.stones += move

    @dataclass
    class GameTreeNode:
        is_maximizing: bool
        heuristic_value: int = None
        children: dict = None

    def generate_subtree(self, current: Player, depth: int) -> GameTreeNode:
        if depth == 0 or self.stones < 2:
            return self.GameTreeNode(current is self.ai_bot, self.heuristic_eval())

        node = self.GameTreeNode(current is self.ai_bot)
        node.children = {}
        possible_moves = (2, 3) if self.stones >= 3 else (2,)
        for move in possible_moves:
            self.make_move(current, move)
            child = self.generate_subtree((self.player, self.ai_bot)[current is self.player], depth - 1)
            self.undo_move(current, move)

            node.children[move] = child

        return node


    def minimax(self, depth: int, is_maximizing: bool = True) -> (int, int or None):
        def _minimax(node: self.GameTreeNode, depth: int, is_maximizing: bool) -> (int, int or None):
            if depth == 0 or node.children is None:
                return node.heuristic_value, None

            best_move = None
            best_value = (float('inf'),
                          float('-inf'))[is_maximizing]

            condition = (lambda x: x < best_value,
                         lambda x: x > best_value)[is_maximizing]

            for move, child_node in node.children.items():
                new_value, _ = _minimax(child_node, depth - 1, not is_maximizing)

                if condition(new_value):
                    best_value = new_value
                    best_move = move

            return best_value, best_move

        root = self.generate_subtree(self.ai_bot, depth)
        return _minimax(root, depth, is_maximizing)


    def alpha_beta(self, depth: int,
                   alpha: int = float('-inf'), beta: int = float('inf'),
                   is_maximizing: bool = True) -> (int, int or None):
        def _alpha_beta(node: self.GameTreeNode,
                        alpha: int, beta: int,
                        is_maximizing: bool) -> (int, int or None):
            if node.children is None:
                return node.heuristic_value, None

            best_move = None
            condition = (lambda x: x < beta,
                         lambda x: x > alpha)[is_maximizing]

            for move, child_node in node.children.items():
                new_value, _ = _alpha_beta(child_node, alpha, beta, not is_maximizing)

                if condition(new_value):
                    best_move = move

                if is_maximizing:
                    alpha = max(alpha, new_value)
                    if alpha >= beta:
                        break
                else:
                    beta = min(beta, new_value)
                    if beta <= alpha:
                        break

            return (beta, alpha)[is_maximizing], best_move

        root = self.generate_subtree(self.ai_bot, depth)
        return _alpha_beta(root, alpha, beta, is_maximizing)




    # Boilerplate code
    def make_player_move(self, move: int) -> None:
        self.make_move(self.player, move)

    def make_ai_bot_move(self, move: int) -> None:
        self.make_move(self.ai_bot, move)

    def undo_player_move(self, move: int) -> None:
        self.undo_move(self.player, move)

    def undo_ai_bot_move(self, move: int) -> None:
        self.undo_move(self.ai_bot, move)

    def __bool__(self) -> bool:
        return self.stones >= 2
