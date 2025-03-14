from games import Game, GameState

class GameOfNim(Game):
    def __init__(self, board):
        """
        Initialize the Game of Nim.
        board: list of nonnegative integers, where each element is the number
               of objects in that heap. E.g., [7, 5, 3, 1]
        """
        # Copy board to ensure it remains a list.
        board_copy = board[:]  
        self.initial = GameState(
            to_move="MAX",
            utility=0,
            board=board_copy,
            moves=self._actions_from_board(board_copy)
        )

    def _actions_from_board(self, board):
        """
        Generate the list of valid moves from a given board.
        A move is a tuple (r, n) where r is the row index (0-based) and n is the number
        of objects to remove (from 1 up to board[r]).
        """
        moves = []
        for r, count in enumerate(board):
            for n in range(1, count + 1):
                moves.append((r, n))
        return moves

    def actions(self, state):
        """
        Return a list of valid moves for the given state.
        """
        return self._actions_from_board(state.board)

    def result(self, state, move):
        """
        Given a state and a valid move (r, n), return the new GameState that results.
        The move removes n objects from row r and switches the player.
        If the resulting board is terminal (all heaps are empty),
        then the player whose turn would be next wins (since the mover loses).
        """
        r, n = move
        # Make a copy of the board so as not to modify the current state.
        new_board = state.board[:]  
        if n > new_board[r]:
            raise ValueError("Invalid move: trying to remove more objects than available.")
        new_board[r] -= n
        
        # Determine next player.
        next_player = "MIN" if state.to_move == "MAX" else "MAX"
        new_moves = self._actions_from_board(new_board)
        
        # Terminal state: if all heaps are empty, the mover loses and the next player wins.
        if self.terminal_test(new_board):
            utility = 1 if next_player == "MAX" else -1
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
        Returns True if the game is over (i.e., all heaps are empty).
        Accepts either a GameState (using its board attribute) or a board (list).
        """
        board = state_or_board.board if hasattr(state_or_board, 'board') else state_or_board
        return all(x == 0 for x in board)

    def utility(self, state, player):
        """
        Return the utility of the state from the perspective of 'player'.
        For terminal states only: returns +1 if MAX wins and -1 if MIN wins.
        (In a terminal state, state.to_move is the player whose turn would be next, 
         and by the rules of misère Nim, that player is declared the winner.)
        """
        if not self.terminal_test(state):
            return 0
        winner = state.to_move
        return 1 if player == winner else -1

    def display(self, state):
        """
        Print the current board configuration.
        """
        print("board:", state.board)


# Example usage (for local testing):
if __name__ == '__main__':
    # Initialize the game with board [7, 5, 3, 1]
    game = GameOfNim([7, 5, 3, 1])
    state = game.initial
    game.display(state)
    print("Available moves:", state.moves)
    
    # Sample move: remove 1 object from row 0
    move = (0, 1)
    print("Move chosen:", move)
    state = game.result(state, move)
    game.display(state)
    print("Next player:", state.to_move)
