from games import Game, GameState, alpha_beta_player, query_player

class GameOfNim(Game):
    def __init__(self, board=[3, 1]):
        self.initial = GameState(
            to_move='MAX',
            utility=0,
            state=tuple(board),
            moves=self.compute_moves(board)
        )

    def compute_moves(self, board):
        moves = []
        for r in range(len(board)):
            count = board[r]
            for n in range(1, count + 1):
                moves.append((r, n))
        return moves

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        r, n = move
        new_board = list(state.state)
        new_board[r] -= n
        new_board_tuple = tuple(new_board)
        next_player = 'MIN' if state.to_move == 'MAX' else 'MAX'
        new_utility = 0
        if sum(new_board_tuple) == 0:
            new_utility = 1 if next_player == 'MAX' else -1
        new_moves = self.compute_moves(new_board_tuple)
        return GameState(
            to_move=next_player,
            utility=new_utility,
            state=new_board_tuple,
            moves=new_moves
        )

    def terminal_test(self, state):
        return sum(state.state) == 0

    def utility(self, state, player):
        return state.utility if player == 'MAX' else -state.utility

    def display(self, state):
        print("board:", list(state.state))

if __name__ == "__main__":
    nim = GameOfNim(board=[0, 5, 3, 1])
    print(nim.initial.state)
    print(nim.initial.moves)
    print(nim.result(nim.initial, (1, 3)))
    utility = nim.play_game(alpha_beta_player, query_player)
    if utility < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")
