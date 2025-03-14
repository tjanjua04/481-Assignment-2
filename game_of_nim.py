from games import Game, GameState

class GameOfNim(Game):
    def __init__(self, board):
        """
        Initialize the Game of Nim.
        board: list or tuple of nonnegative integers, where each element is the number
               of objects in that heap. E.g., [7, 5, 3, 1]
        """
        board = tuple(board)
        self.initial = GameState(
            to_move="MAX",
            utility=0,
            board=board,
            moves=self._actions_from_board(board)
        )

    def _actions_from_board(self, board):
        """
        Helper function to generate the list of valid moves from a given board.
        A move is a tuple (r, n) where r is the row index (0-based) and n is the number
        of objects to remove (from 1 up to board[r]).
        """
        moves = []
        for r, count in enumerate(board):
            # Only generate moves if there are objects to remove.
            for n in range(1, count + 1):
                moves.append((r, n))
        return moves

    def actions(self, state):
        """
        Return a list of valid actions for the given state.
        (This recomputes the moves from the current board configuration.)
        """
        return self._actions_from_board(state.board)

    def result(self, state, move):
        """
        Given a state and a valid move (r, n), return the new GameState that results.
        The move removes n objects from row r.
        Also switches the player whose turn it is.
        If the resulting board is terminal (all heaps are 0), then the player who would have moved
        is declared the winner (since the mover who emptied the board loses).
        """
        r, n = move
        board = list(state.board)
        if n > board[r]:
            raise ValueError("Invalid move: trying to remove more objects than available.")
        board[r] -= n
        new_board = tuple(board)
        # Switch players
        next_player = "MIN" if state.to_move == "MAX" else "MAX"
        new_moves = self._actions_from_board(new_board)
        
        if self.terminal_test(new_board):
            winner = next_player
            utility = 1 if winner == "MAX" else -1
        else:
            utility = 0
        
        return GameState(
            to_move=next_player,
            utility=utility,
            board=new_board,
            moves=new_moves
        )

    def terminal_test(self, state_or_board):
        """
        Returns True if the game is over (i.e. when all heaps are empty).
        Accepts either a GameState or a board (tuple or list).
        """
        # Determine if we got a state (with a board attribute) or a board directly.
        board = state_or_board.board if hasattr(state_or_board, 'board') else state_or_board
        return all(x == 0 for x in board)

    def utility(self, state, player):
        """
        Return the utility of the state from the perspective of 'player'.
        For terminal states only: returns +1 if MAX wins and -1 if MIN wins.
        Note: In a terminal state, state.to_move is the player who would have moved,
        and by the rules of misère Nim that player is the winner.
        """
        if not self.terminal_test(state):
            return 0
        winner = state.to_move
        return 1 if player == winner else -1

    def display(self, state):
        """
        Print the current board configuration.
        """
        print("board:", list(state.board))


if __name__ == '__main__':
    # Initialize the game
    game = GameOfNim([7, 5, 3, 1])
    state = game.initial
    game.display(state)
    print("Available moves:", state.moves)
    
    # Sample move
    move = (0, 1)
    print("Move chosen:", move)
    state = game.result(state, move)
    game.display(state)
    print("Next player:", state.to_move)
