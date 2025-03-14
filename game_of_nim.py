from games import Game, GameState

class GameOfNim(Game):
    def __init__(self, initial_board):
        self.initial = GameState(
            to_move='MAX',
            utility=0,
            state=initial_board,  # Changed from 'board' to 'state'
            moves=self.compute_moves(initial_board)
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
        new_board = state.state.copy()  # Access 'state' attribute
        new_board[r] -= n

        next_player = 'MIN' if state.to_move == 'MAX' else 'MAX'

        new_utility = 0
        if sum(new_board) == 0:
            new_utility = 1 if next_player == 'MAX' else -1

        new_moves = self.compute_moves(new_board)

        return GameState(
            to_move=next_player,
            utility=new_utility,
            state=new_board,  # Changed to 'state'
            moves=new_moves
        )

    def terminal_test(self, state):
        return sum(state.state) == 0  # Access 'state' attribute

    def utility(self, state, player):
        return state.utility if player == 'MAX' else -state.utility

    def display(self, state):
        print("board: ", state.state)  # Access 'state' attribute
