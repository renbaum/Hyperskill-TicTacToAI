import random


class Board:
    """
    A class representing a tic-tac-toe board.

    Attributes
    ----------
    PlayerA : str
        The symbol for Player A.
    PlayerB : str
        The symbol for Player B.

    """
    PlayerA = 'X'
    PlayerB = 'O'

    def __init__(self, init_string: str = None) -> None:
        """
        Initialize the object with the given initial string.

        :param init_string: A string that represents the initial state of the board.
                            Default value is None.
        """
        self.init_string = init_string
        self.board = None
        if init_string is None:
            init_string = "         "
        self.init_board(init_string)

    def get_init_string(self) -> str:
        """
        Return the string representation of the board.

        :return: The string representation of the board.
        :rtype: str
        """
        init_string = ""
        for a in range(3):
            for b in range(3):
                init_string += " " if self.board[a][b] not in [Board.PlayerA, Board.PlayerB] else self.board[a][b]
        return init_string

    def init_board(self, string: str = "_________") -> bool:
        """
        Initialize the game board with the provided string.

        :param string: A string representing the game board. Each character represents a cell of the board.
                       The string should have exactly 9 characters.
                       Default value is "_________" which represents an empty game board.
        :return: Returns True if the game board is successfully initialized, False otherwise.
        """
        assert (len(string) == 9)

        if len(string) != 9:
            return False
        string = string.replace('_', ' ')
        self.board = [list(string[i:i + 3]) for i in range(0, len(string), 3)]

    def print_board(self):
        """
        Prints the current state of the board.

        :return: None
        """
        print('---------')
        for y in range(3):
            row = "| "
            for x in range(3):
                row += self.board[y][x] + " "
            row += "|"
            print(row)
        print('---------')

    def check_win(self) -> str:
        """
        Check if there is a winner in the Tic-Tac-Toe board.

        :return:
            - The symbol of the winner ('X' or 'O') if there is a winner.
            - 'impossible' if the game is in an impossible state.
            - empty string if there is no winner yet.
        """
        # check horizontal
        winner = []
        for row in self.board:
            if row.count(row[0]) == len(row) and row[0] != ' ':
                winner.append(row[0])

        # check vertical
        for col in range(len(self.board)):
            check = []
            for row in self.board:
                check.append(row[col])
            if check.count(check[0]) == len(check) and check[0] != ' ':
                winner.append(check[0])

        # check diagonal (top-left to bottom-right)
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != ' ':
            winner.append(self.board[0][0])

        # check diagonal (top-right to bottom-left)
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != ' ':
            winner.append(self.board[0][2])

        # if impossible
        if len(winner) > 1:
            return "impossible"
        # if winner, return the winner symbol
        if len(winner) == 1:
            return winner[0]
        # the game has no winner yet
        return ""

    def is_grid_full(self) -> bool:
        """
        Check if the grid is full.

        :return: True if all cells in the grid are filled, False otherwise.
        """
        for x in range(3):
            for y in range(3):
                if self.board[x][y] not in ['X', 'O']:
                    return False

        return True

    def get_player_moves(self) -> dict:
        """
        This method returns a dictionary containing the number of moves made by each player.

        :return: A dictionary with keys representing players (Board.PlayerA and Board.PlayerB) and
                 values representing the number of moves made by each player.
        """
        p = {Board.PlayerA: 0, Board.PlayerB: 0}
        for x in range(3):
            for y in range(3):
                if self.board[x][y] in [Board.PlayerA, Board.PlayerB]:
                    p[self.board[x][y]] += 1
        return p

    def count_player_moves(self) -> bool:
        """
        Count the number of moves made by each player on the game board.

        :return: True if the number of moves made by each player differs by at most 1,
                 False otherwise.
        """
        p = self.get_player_moves()
        if abs(p[Board.PlayerA] - p[Board.PlayerB]) >= 2:
            return False

        return True

    def check_solution(self) -> bool:
        """
        Checks if the current game solution has been reached.

        :return: Returns True if the game has been won or drawn, False otherwise.
        """
        a = self.check_win()
        if a == "impossible" or not self.count_player_moves():
            print("Impossible")
            return False
        if a in [Board.PlayerA, Board.PlayerB]:
            print(f"{a} wins")
            return True
        if self.is_grid_full():
            print("Draw")
            return True
        # print("Game not finished")
        return False

    def get_possible_moves(self) -> list:
        """

        Method: get_possible_moves
        Description: retrieves all the possible moves in the game board that are currently unoccupied.
        Parameters:
            self: The instance of the class.
        Return:
            :return: A list containing all the possible moves in the game board that are currently unoccupied.
        """
        free_position = []
        for a in range(3):
            for b in range(3):
                if self.board[a][b] not in [Board.PlayerA, Board.PlayerB]:
                    free_position.append(f"{a + 1} {b + 1}")
        return free_position

    def do_move(self, string: str, player: str) -> bool:
        """
        :param string: A string containing two space-separated numbers representing the x and y coordinates of the move.
        :param player: A string representing the player making the move.
        :return: A boolean indicating whether the move was successfully executed.

        This method takes in a string and a player symbol as parameters, and does the move on the board if possible.
        If the move is not valid, an error is printed.
        """
        try:
            if string is None:
                raise Exception("You should enter numbers!")
            input_move = string.split()
            if len(input_move) != 2:
                raise Exception("You should enter numbers!")
            x = int(input_move[0])
            y = int(input_move[1])
            if x not in range(1, 4) or y not in range(1, 4):
                raise Exception("Coordinates should be from 1 to 3!")
        except ValueError:
            print("You should enter numbers!")
            return False
        except Exception as e:
            print(e)
            return False

        return self.do_move_xy(x - 1, y - 1, player)

    def do_move_xy(self, x: int, y: int, player: str):
        """
        Perform a move on the game board at the specified location (x, y) for the given player.

        :param x: X-coordinate of the cell on the game board.
        :param y: Y-coordinate of the cell on the game board.
        :param player: The player making the move. It can be 'O' or 'X'.
        :return: True if the move is successfully made, False otherwise.
        """
        if self.board[x][y] in [Board.PlayerB, Board.PlayerA]:
            print("This cell is occupied! Choose another one!")
            return False
        self.board[x][y] = player
        return True


class Player:

    def __init__(self, symbol: str = "X") -> None:
        self.symbol = symbol
        self.player = 0 if symbol == 'X' else 1

    def create_move(self, board: Board) -> bool:
        pass

    def get_opposite_player(self):
        if self.player == 0:
            return Board.PlayerB
        return Board.PlayerA


class HumanPlayer(Player):

    def create_move(self, board: Board) -> bool:
        proper_move = False
        while not proper_move:
            human_move = input("Enter the coordinates: ")
            proper_move = board.do_move(human_move, self.symbol)
        return proper_move


class ComputerPlayerEasy(Player):

    def create_move(self, board: Board) -> bool:
        possible_moves = board.get_possible_moves()
        chosen_move = random.choice(possible_moves)
        print("Making move level \"easy\"")
        return board.do_move(chosen_move, self.symbol)


class ComputerPlayerMedium(Player):
    def create_move(self, board: Board) -> bool:
        possible_moves = board.get_possible_moves()
        best_move = None
        for move in possible_moves:
            board_copy = Board(board.get_init_string())
            board_copy.do_move(move, self.symbol)
            if board_copy.check_win() == self.symbol:
                best_move = move
                break
        if best_move is None:
            best_move = random.choice(possible_moves)
        print("Making move level \"medium\"")
        return board.do_move(best_move, self.symbol)


class ComputerPlayerHard(Player):

    def create_move(self, board: Board) -> bool:
        best_move = None
        best_score = float('-inf')
        possible_moves = board.get_possible_moves()
        init_string = board.get_init_string()
        for move in possible_moves:
            sub_board = Board(init_string)
            sub_board.do_move(move, self.symbol)
            score = self.minimax(sub_board, 0, False)
            if score['score'] > best_score:
                best_score = score['score']
                best_move = move
        return board.do_move(best_move, self.symbol)

    def minimax(self, board, depth, is_maximizing_player):
        empty_cells = board.get_possible_moves()
        ini_string = board.get_init_string()

        # If the game is over, return the evaluation of the board
        winner = board.check_win()
        if winner != '':
            if len(empty_cells) == 0:
                return {'score': 0}
            if board.check_win() == self.symbol:
                return {'score': 1}
            elif winner == self.get_opposite_player():
                return {'score': -1}

        if is_maximizing_player:
            max_eval = {'score': float('-inf')}
            for cell in empty_cells:
                # Make the move temporarily
                sub_board = Board(ini_string)
                sub_board.do_move(cell, self.symbol)
                current_eval = self.minimax(sub_board, depth + 1, False)
                if current_eval['score'] > max_eval['score']:
                    max_eval = current_eval
            return max_eval

        else:
            min_eval = {'score': float('inf')}
            for cell in empty_cells:
                sub_board = Board(ini_string)
                sub_board.do_move(cell, self.get_opposite_player())
                current_eval = self.minimax(sub_board, depth + 1, True)
                if current_eval['score'] < min_eval['score']:
                    min_eval = current_eval
            return min_eval

def get_player_type(string: str, symbol: str) -> Player or None:
    match string:
        case "easy":
            return ComputerPlayerEasy(symbol)
        case "user":
            return HumanPlayer(symbol)
        case "medium":
            return ComputerPlayerMedium(symbol)
        case "hard":
            return ComputerPlayerHard(symbol)
    return None


is_exit = False

while not is_exit:
    start_cmd = ""
    check_cmd = False
    while not check_cmd:
        start_cmd = input("Input command: ").split()
        if len(start_cmd) == 1 and start_cmd[0] == "exit":
            break
        if len(start_cmd) != 3:
            print("Bad parameters!")
            continue
        if start_cmd[0] not in ["start", "exit"]:
            print("Bad parameters!")
            continue
        if start_cmd[1] not in ["user", "easy", "medium", "hard"]:
            print("Bad parameters!")
            continue
        if start_cmd[2] not in ["user", "easy", "medium", "hard"]:
            print("Bad parameters!")
            continue
        check_cmd = True

    # if there is an exit command, just do it
    if start_cmd[0] == "exit":
        is_exit = True
        continue

    # this must be a start command
    players = [get_player_type(start_cmd[1], 'X'), get_player_type(start_cmd[2], 'O')]
    currentPlayer = 0

    c = Board()
    c.print_board()

    win = False

    while not win:
        players[currentPlayer].create_move(c)
        c.print_board()
        currentPlayer = (currentPlayer + 1) % 2
        win = c.check_solution()
