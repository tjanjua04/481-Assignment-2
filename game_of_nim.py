from games import Game, GameState, alpha_beta_player, query_player

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list with the number of objects in each row.
    """

    def __init__(self, board=[3, 1]):
        """Initialize the game state with the given board."""
        if not all(isinstance(x, int) for x in board):  # Ensure all values are integers
            raise ValueError("Board values must be integers.")

        self.initial = GameState(
            to_move='MAX',  # MAX (computer) starts
            utility=0,
            board=tuple(board),  # Store board as an immutable tuple
            moves=self.actions(board)
        )

    def actions(self, board):
        """Return a list of valid actions for the given board state."""
        print(f"DEBUG: Board received in actions(): {board}")  # Debugging line

        if not isinstance(board, (list, tuple)):
            raise TypeError(f"ERROR: Expected board to be a list or tuple, got {type(board)}.")

        moves = []
        for r, count in enumerate(board):
            print(f"DEBUG: Row {r}, count {count}, type: {type(count)}")  # Debugging line
            
            if not isinstance(count, int):  # Catch invalid types
                raise TypeError(f"ERROR: Row {r} has a non-integer value: {count}")

            for n in range(1, count + 1):  # Remove at least one object
                moves.append((r, n))
        return moves

    def result(self, state, move):
        """Return the new game state after making a move."""
        r, n = move
        new_board = list(state.board)  # Convert tuple to list for modification
        new_board[r] -= n  # Remove objects from the chosen row
        next_player = 'MIN' if state.to_move == 'MAX' else 'MAX'
        
        # Ensure `actions()` only receives `new_board`
        new_board_tuple = tuple(new_board)  # Convert to tuple for immutability
        print(f"DEBUG: New board after move {move}: {new_board_tuple}")  # Debugging

        return GameState(
            to_move=next_player,
            utility=self.utility(new_board, next_player),
            board=new_board_tuple,
            moves=self.actions(new_board_tuple)  # Correcting what is passed to actions()
        )

    def utility(self, board, player):
        """Return +1 if MAX wins, -1 if MIN wins."""
        if self.terminal_test(GameState(to_move=player, utility=0, board=board, moves=[])):
            return -1 if player == 'MAX' else 1  # The player who made the last move loses
        return 0  # Game is not over yet

    def terminal_test(self, state):
        """Check if the game has ended (i.e., all objects are removed)."""
        return all(count == 0 for count in state.board)

    def display(self, state):
        """Display the current board state."""
        print("board:", state.board)


if __name__ == "__main__":
    print("Starting Game of Nim...")

    nim = GameOfNim(board=[0, 5, 3, 1])  # Creating the game instance

    print(f"Initial Board: {nim.initial.board}")  # Expected: (0, 5, 3, 1)
    print(f"Valid Moves: {nim.initial.moves}")  # Expected: Valid moves list

    # Simulate a move
    new_state = nim.result(nim.initial, (1, 3))
    print(f"After move (1,3): {new_state.board}")

    # Start the game with AI first
    utility = nim.play_game(alpha_beta_player, query_player)

    if utility < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")
