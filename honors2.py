"""
Honors Project, Part 2.

This program plays the dots and boxes game in two modes: single play and
multiple play. Single play plays one game in greater detail. Multiple play
plays a specified number of games detailing statistics.
"""

import random
import copy
import statistics
import time

MODE_OPTIONS = ['S', 'M']


class Board(object):
    """
    Creates the class board using an integer. Assigns methods: __init__,
    __str__, display_board, check_for_box, is_valid_move, update_board, win.
    """

    def __init__(self, board_length_int):
        """
        Creates a board in a square shape. Rows structured as lists and each
        row is part of a master list. Takes an integer input which defines how
        long one side of the board is.

        param self: The board being constructed.
        type self: Board

        param board_length_int: The size of one side of the board.
        type board_length_int: Int

        """

        # Creates a list with as many space elements in it as are in the length
        # of the list. This is used as the list between the numbered rows to
        # create space for vertical bars and A's and B's.
        in_between_list = [' ' for i in range(2 * board_length_int - 1)]

        master_board_lol = []
        new_first_value_int = 0
        row_count = 1

        # For each number in the range of the provided length iterate through.
        for num1 in range(board_length_int):
            # Sets the row range as the first value in the row, to the last
            row_range = range(new_first_value_int, (board_length_int +
                                                    new_first_value_int))

            row_list = []
            char_count = 0

            # Iterate throughout the row_range now
            for num2 in row_range:
                # If the number of characters is equal to 2 times the length
                # of the board minus 2, append the number and then break. This
                # is done so no errant spaces are generated at the end of each
                # line.
                if char_count == (2 * board_length_int - 2):
                    row_list.append(num2)
                    break
                # Otherwise append the number and then a space
                else:
                    row_list.append(num2)
                    row_list.append(' ')
                    char_count += 2

            master_board_lol.append(row_list)

            # If the not the last row append the previously generated list
            # that fits between the values.
            if row_count != board_length_int:
                in_between_list_copy = copy.deepcopy(in_between_list)
                master_board_lol.append(in_between_list_copy)

            # Set the new first value to be the value of the last number
            # generate plus 1.
            new_first_value_int = row_list[(2 * board_length_int - 2)] + 1
            row_count += 1

        # Set the board attribute to be the list of lists
        self.board = master_board_lol

    def __str__(self):
        """
        Formats the board properly so that the board is aligned. Only takes
        the instance of board. Returns a string.

        param self: The board
        Type self: Board

        returns: A string representation of the board.
        rtype: Str
        """

        len_of_board_list = len(self.board)

        # Finds the maximum number of digits in a number
        max_digit_count = len(str(self.board[len_of_board_list - 1]
                              [len_of_board_list - 1]))

        master_return_str = ''  # Initializes an empty master string
        row_count = 0  # Initializes a row_count

        # Iterates through every row in the board attribute
        for row in self.board:
            # Initializes a row string and resets for every new row
            row_str = ''
            char_count = 0  # Counts the number of chars in the row

            # Iterates through every element in the row.
            for char in row:

                char_str = str(char)  # Converts element to a string

                # If remainder of row_count divided by 2 is 0 execute
                # (i.e if a row with numbers).
                if (row_count % 2) == 0:
                    # If remainder of char_count divided by 2 is 0 execute
                    # (i.e if a character is number)
                    if (char_count % 2) == 0:
                        # Right justify any numbers with spacing equal to max
                        # digit count so that the right digit of all nums line
                        # up.
                        char_str = ('{:>' + (str(max_digit_count)) + '}'). \
                            format(char_str)

                    # If remainder of char_count divided by 2 is not 0 execute
                    # (i.e if a space between numbers horizontally).
                    elif (char_count % 2) != 0:
                        # Center formatting with spacing of 3
                        char_str = '{:^3}'.format(char_str)

                # If the remainder of the row count divided by 2 is not 0
                # execute (i.e if a all spaces line).
                elif (row_count % 2) != 0:
                    # If the remainder of the char_count divided by 2 is not 0
                    # execute (i.e if it lines up with a space vertically)
                    if (char_count % 2) != 0:
                        # Center formatting with spacing of 3
                        char_str = '{:^3}'.format(char_str)

                    # If the remainder of the char count divided by 2 is 0
                    # execute (i.e if it lines up with a number).
                    elif (char_count % 2) == 0:
                        # Right justified with spacing equal to max_digit_count
                        char_str = ('{:>' + (str(max_digit_count)) + '}'). \
                            format(char_str)

                row_str = row_str + char_str
                char_count += 1

            row_count += 1

            # Once row is finished add the row string to the master string and
            # go back a line.
            master_return_str = master_return_str + row_str + '\n'

        return master_return_str

    def check_for_box(self, row, column, player_letter):
        """
        Returns an integer that is the number of points. A change was made
        between honors part 1 and part 2 that enabled this method to only
        check the boxes next to it. This should allow drastically increased
        algorithm speed.

        param self: The board to perform the method on.
        type self: Board class.

        param row: The row index.
        type row: Int

        param column: The column index.
        type column: Int

        param player_letter: The letter of the player who made the move.
        type player_letter: Str

        return: Number of points generated.
        rtype: Int
        """

        # Executes suite if even row.
        if (row % 2) == 0:
            # Executes suite if the row is between 0 and the last row.
            if (len(self.board) - 1) > row > 0:

                # Gets the spaces from the top.
                top_box_list = [self.board[row - 1][column - 1],
                                self.board[row - 1][column + 1],
                                self.board[row - 2][column]]
                # Gets the spaces from the bottom.
                bottom_box_list = [self.board[row + 1][column - 1],
                                   self.board[row + 1][column + 1],
                                   self.board[row + 2][column]]

                # Checks whether each side is filled in.
                side_count = 0
                for side in top_box_list:
                    if (side == '-') or (side == '|'):
                        side_count += 1

                # Fills in letters and assigns points.
                if (side_count == 3) and (self.board[row - 1][column] != 'A') \
                        and (self.board[row - 1][column] != 'B'):
                    top_box_point = 1
                    self.board[row - 1][column] = player_letter
                else:
                    top_box_point = 0

                side_count = 0
                for side in bottom_box_list:
                    if (side == '-') or (side == '|'):
                        side_count += 1

                if (side_count == 3) and (self.board[row + 1][column] != 'A') \
                        and (self.board[row + 1][column] != 'B'):
                    bottom_box_point = 1
                    self.board[row + 1][column] = player_letter
                else:
                    bottom_box_point = 0

                return bottom_box_point + top_box_point

            # Elif suite executes if row is 0.
            elif row == 0:
                # Gets the moves from the box below.
                bottom_box_list = [self.board[row + 1][column - 1],
                                   self.board[row + 1][column + 1],
                                   self.board[row + 2][column]]

                # Checks whether sides are filled in.
                side_count = 0
                for side in bottom_box_list:
                    if (side == '-') or (side == '|'):
                        side_count += 1

                # If box is made, fills in letter and assigns point value.
                if (side_count == 3) and (self.board[row + 1][column] != 'A') \
                        and (self.board[row + 1][column] != 'B'):
                    bottom_box_point = 1
                    self.board[row + 1][column] = player_letter
                else:
                    bottom_box_point = 0

                return bottom_box_point

            # Elif suite executes if row is the last row on board.
            elif row == (len(self.board) - 1):
                # Gets a list of the box above elements.
                top_box_list = [self.board[row - 1][column - 1],
                                self.board[row - 1][column + 1],
                                self.board[row - 2][column]]

                # Checks if sides filled in.
                side_count = 0
                for side in top_box_list:
                    if (side == '-') or (side == '|'):
                        side_count += 1

                # If box is made above assigns points and fills in letter.
                if (side_count == 3) and (self.board[row - 1][column] != 'A') \
                        and (self.board[row - 1][column] != 'B'):
                    top_box_point = 1
                    self.board[row - 1][column] = player_letter
                else:
                    top_box_point = 0

                return top_box_point

        # If the row is odd the suite executes.
        elif (row % 2) != 0:
            # Executes suite if the column is between 0 and the last column.
            if (len(self.board) - 1) > column > 0:
                # Gets the spaces from the left.
                left_box_list = [self.board[row - 1][column - 1],
                                 self.board[row + 1][column - 1],
                                 self.board[row][column - 2]]
                # Gets the spaces from the right.
                right_box_list = [self.board[row - 1][column + 1],
                                  self.board[row + 1][column + 1],
                                  self.board[row][column + 2]]

                # Checks if sides are filled in.
                side_count = 0
                for side in left_box_list:
                    if (side == '-') or (side == '|'):
                        side_count += 1

                # If sides are filled in a point value is assigned and the box
                # letter is filled in.
                if (side_count == 3) and (self.board[row][column - 1] != 'A') \
                        and (self.board[row][column - 1] != 'B'):
                    left_box_point = 1
                    self.board[row][column - 1] = player_letter
                else:
                    left_box_point = 0

                side_count = 0
                for side in right_box_list:
                    if (side == '-') or (side == '|'):
                        side_count += 1

                if (side_count == 3) and (self.board[row][column + 1] != 'A') \
                        and (self.board[row][column + 1] != 'B'):
                    right_box_point = 1
                    self.board[row][column + 1] = player_letter
                else:
                    right_box_point = 0

                return left_box_point + right_box_point

            # If the column is 0 suite executes.
            elif column == 0:
                # Check the box to the right.
                right_box_list = [self.board[row - 1][column + 1],
                                  self.board[row + 1][column + 1],
                                  self.board[row][column + 2]]

                # Checks if box to right is filled in.
                side_count = 0
                for side in right_box_list:
                    if (side == '-') or (side == '|'):
                        side_count += 1

                # If box is made fills in letter and assigns points.
                if (side_count == 3) and (self.board[row][column + 1] != 'A') \
                        and (self.board[row][column + 1] != 'B'):
                    right_box_point = 1
                    self.board[row][column + 1] = player_letter
                else:
                    right_box_point = 0

                return right_box_point

            # Executes if last column on board.
            elif column == (len(self.board) - 1):
                # Checks left box elements.
                left_box_list = [self.board[row - 1][column - 1],
                                 self.board[row + 1][column - 1],
                                 self.board[row][column - 2]]

                # Checks if left box is filled in.
                side_count = 0
                for side in left_box_list:
                    if (side == '-') or (side == '|'):
                        side_count += 1

                # If box made, points are assigned and letter is filled in.
                if (side_count == 3) and (self.board[row][column - 1] != 'A') \
                        and (self.board[row][column - 1] != 'B'):
                    left_box_point = 1
                    self.board[row][column - 1] = player_letter
                else:
                    left_box_point = 0

                return left_box_point

        return 0

    def is_valid_move(self, row, column):
        """
        This method was updated for part 2 of the honors project. The update 
        should drastically increase speed. The new algorithm simply eliminates
        needless for loops and clauses.

        param self: The board to perform the method on.
        type self: Board class.

        param row: The row index.
        type row: Int

        param column: The column index.
        type column: Int

        return: True if valid move, False if invalid.
        rtype: Bool
        """

        if self.board[row][column] == ' ':
            return True

        return False

    def update_board(self, row, column):
        """
        With this method there were again major inefficiencies and the code 
        was largely rewritten to improve the run time. The basic changes 
        were to eliminate for loops and needless evaluations. The code updates
        board with the move.

        :param self: The board.
        :type self: Board class.

        :param row: The row index.
        :type row: Int

        :param column: The column index.
        :type column: Int

        returns: True or False depending on if the board was updated.
        rtype: Bool
        """
        # Checks validity of move and assigns the boolean value.
        valid_move_bool = self.is_valid_move(row, column)

        if valid_move_bool:  # If the move is valid execute the suite.
            if (row % 2) == 0:
                self.board[row][column] = '-'
            elif (row % 2) != 0:
                self.board[row][column] = '|'
            return True

        else:
            return False

    def win(self):
        """

        If all moves are taken then the game is over and the method returns
        True. Checks each element that can be taken by a move returns True if
        all are taken. If not returns False.

        param self: The board.
        type self: Board

        returns: True or false depending on if board won.
        rtype: Bool

        """

        row_count = 0

        for row in self.board:  # Iterates through rows in board.
            char_count = 0  # Resets the char_count/initializes it.
            for element in row:  # Iterates through the elements in the row.

                if (row_count % 2) == 0:  # If an even row executes the suite.
                    if (char_count % 2) != 0:
                        if element == ' ':
                            return False

                elif (row_count % 2) != 0:  # If odd row execute the suite.
                    if (char_count % 2) == 0:  # If char is even, execute.
                        if element == ' ':  # Otherwise return False
                            return False

                char_count += 1

            row_count += 1

        return True  # If all moves taken return True.


class RandomPlayer(object):
    """
    Creates a RandomPlayer with associated methods to add points, make a move,
    and return the score. Also includes __init__ and __str__.
    """

    def __init__(self, player_letter, score=0):
        """
        Initializes the RandomPlayer class with attributes: player_name, and
        score_att.

        param self: The random player.
        type self: RandomPlayer

        param player_letter: The player's letter.
        type player_letter: Str

        param score: The score to initialize to, default to 0.
        type score: Int

        """
        self.name = player_letter

        # Named score_att to denote that this is an attribute and to
        # differentiate between the score method and the attribute.
        self.score_att = score
        self.move_indices_set = set()

    def __str__(self):
        """
        Returns the string of the player name and score.

        param self: The RandomPlayer
        type self: RandomPlayer

        returns: The string displaying player name and score.
        rtype: Str
        """
        return 'Player name: {}, Player Score: {}'.format(self.player_name,
                                                          self.score)

    def generate_move_indices_set(self, board):
        """
        Creates a set of legal moves possible. Uses random.choice to pick a
        random tuple in the list that is a move. Takes the board as param.

        param self: The RandomPlayer
        type self: RandomPlayer

        param board: The board to check for legal moves.
        type board: Board

        """
        # We need to create the list of possible moves if this is the first
        # turn. Otherwise the legal moves list should be provided in the input.
        move_indices_set = set()
        row_count = 0
        for row in board.board:
            column_count = 0
            for column in row:
                if (row_count % 2) == 0:
                    if (column_count % 2) != 0:
                        move_indices_set.add((row_count, column_count))
                elif (row_count % 2) != 0:
                    if (column_count % 2) == 0:
                        move_indices_set.add((row_count, column_count))
                column_count += 1

            row_count += 1

        self.move_indices_set = move_indices_set

    def remove_move_indices(self, row, column):
        """
        Removes a move from the move set.

        param self: The RandomPlayer
        type self: RandomPlayer

        param row: The row index
        type row: Int

        param column: The column index
        type column: Int

        """
        self.move_indices_set.discard((row, column))

    def choose_move(self, rand_seed_int):
        """
        Chooses a move at random from the move_set.

        param self: The RandomPlayer
        type self: RandomPlayer

        param rand_seed_int: The random seed integer to initialize the
        random generator.
        type rand_seed_int: Int

        returns: A tuple of the row and column index in that order.
        rtype: Tuple

        """

        # Intialize random seed, create a deepcopy of the move set, then
        # use the random module to choose one.
        random.seed(rand_seed_int)
        copied_move_indices_set = copy.deepcopy(self.move_indices_set)
        choice_move_indices = random.choice(tuple(copied_move_indices_set))
        return choice_move_indices

    def score(self):
        """
        Returns the score of the player.

        param self: The RandomPlayer
        type self: RandomPlayer

        returns: The score attribute.
        rtype: Int
        """
        return self.score_att

    def add_points(self, points_int):
        """
        Adds one to the .score_att attribute.

        param self: The RandomPlayer
        type self: RandomPlayer

        param points_int: The number of points to be added.
        type: Int

        """
        self.score_att = self.score_att + points_int


class WinningPlayer(object):

    def __init__(self, name, first_move_bool, score=0):
        """
        Initializes attributes for the WinningPlayer class.
        Attributes include: name, score_att, master_chain_headers_list,
        master_chains_list, exe_chain_list, first move bool,
        move_indices_set, and move_tup.

        param self: The WinningPlayer being constructed.
        type self: WinningPlayer

        param name: The name for the player.
        type name: Str

        param first_move_bool: True if WinningPlayer moves first, False if
        WinningPlayer moves second.
        type first_move_bool: Bool

        param score: The score to set WinningPlayer as.
        type score: Int

        """
        self.name = name
        self.score_att = score
        self.master_chain_headers_list = []
        self.master_chains_list = []
        self.exe_chain_list = []
        self.first_move_bool = first_move_bool
        self.move_indices_set = set()
        self.move_tup = ()

    def __str__(self):
        """
        Returns a string of the WinningPlayer with the player name and score.

        param self: The WinningPlayer
        type self: WinningPlayer

        returns: String with player name and score.
        rtype: Str
        """
        return 'Player name: {}, Player Score: {}'.format(self.player_name,
                                                          self.score)

    def score(self):
        """
        Returns the score attribute.

        param self: The WinningPlayer
        type self: WinningPlayer

        returns: Player score
        rtype: Int
        """
        return self.score_att

    def add_points(self, points_int=0):
        """
        Adds points to the score attribute.

        param self: The WinningPlayer
        type self: WinningPlayer

        param points_int: The points to be added.
        type points_int: Int
        """
        self.score_att += points_int

    def generate_move_indices_set(self, board):
        """
        Generates a set of legal moves from the board.

        param self: The WinningPlayer
        type self: WinningPlayer

        param board: The board to generate the set from.
        type board: Board

        """

        # Initialize the set.
        move_indices_set = set()
        row_count = 0
        # Iterate through the rows and columns and get the indexes that
        # are valid moves.
        for row in board.board:
            column_count = 0
            for column in row:
                if (row_count % 2) == 0:
                    if (column_count % 2) != 0:
                        move_indices_set.add((row_count, column_count))
                elif (row_count % 2) != 0:
                    if (column_count % 2) == 0:
                        move_indices_set.add((row_count, column_count))
                column_count += 1

            row_count += 1

        # Set the WinningPlayers move_indices_set equal to the new set.
        self.move_indices_set = move_indices_set

    def remove_move_indices(self, row, column):
        """
        Removes a move from the legal moves set.

        param self: The WinningPlayer
        type self: WinningPlayer

        param row: The row index of the move to be removed.
        type row: Int

        param column: The column index of the move to be removed.
        type column: Int

        """
        self.move_indices_set.discard((row, column))

    def id_chain_headers(self, board):
        """
        Finds a space with three moves around a box full. Returns a tuple with
        the row index, column index, and side of the box that the empty space
        is on.

        param self: The WinningPlayer
        type self: WinningPlayer

        param board: The board to find the chain headers in.
        type board: Board
        """

        # Initialize the chain header list.
        chain_header_list = []
        row_count = 1

        # Iterates through each row and column in the board starting at
        # index 1 to index -1 with a two step, this eliminates
        # unnecessary iterations.
        for row in board.board[1:-1:2]:
            column_count = 1
            for column in row[1:-1:2]:
                # Gets the characters to each side of the box.
                full_spaces = 0
                top_char = board.board[row_count - 1][column_count]
                left_char = board.board[row_count][column_count - 1]
                right_char = board.board[row_count][column_count + 1]
                bottom_char = board.board[row_count + 1][column_count]

                # Checks how many have moves taken.
                if top_char == '-':
                    full_spaces += 1
                if bottom_char == '-':
                    full_spaces += 1
                if right_char == '|':
                    full_spaces += 1
                if left_char == '|':
                    full_spaces += 1

                # If three spaces are full it checks which one is open and
                # generates the chain header.
                if (full_spaces == 3) and (left_char == ' '):
                    chain_header = (row_count, (column_count - 1), 'l')
                    chain_header_list.append(chain_header)
                if (full_spaces == 3) and (right_char == ' '):
                    chain_header = (row_count, (column_count + 1), 'r')
                    chain_header_list.append(chain_header)
                if (full_spaces == 3) and (top_char == ' '):
                    chain_header = ((row_count - 1), column_count, 't')
                    chain_header_list.append(chain_header)
                if (full_spaces == 3) and (bottom_char == ' '):
                    chain_header = ((row_count + 1), column_count, 'b')
                    chain_header_list.append(chain_header)

                column_count += 2

            row_count += 2

        # Sets the attribute to the new list.
        self.master_chain_headers_list = chain_header_list

    def find_chains(self, board):
        """
        Finds chains from the chain headers list generated in id_chain_headers
        method. Sets the attribute master_chains_list to any chains found.
        Chains must be two moves or longer to qualify.

        param self: The WinningPlayer.
        type self: WinningPlayer

        param board: The board to find the chains in.
        type board: Board

        """

        # If there are no chain headers it returns false.
        if not self.master_chain_headers_list:
            return False

        # Iterates through each chain header.
        for chain_header_tup in self.master_chain_headers_list:

            # Assigns the row, column, and last open side to
            # variables. Also starts the chain list with the
            # row and column.
            row = chain_header_tup[0]
            column = chain_header_tup[1]
            chain_list = [(row, column)]
            last_open_side_str = chain_header_tup[2]

            # Loops through until the chain is ended.
            while True:

                # Selects an if clause dependent on the last_open_side_str.
                if last_open_side_str == 't':

                    # Fixes the error where the chain will have negative
                    # indexes inside, resulting in selection of incorrect and
                    # illegal moves.
                    if row == 0:
                        break

                    # Tries to get the relevant move spaces, since the last
                    # open side was a top we only need the other sides.
                    try:
                        top_char = board.board[row - 2][column]
                        left_char = board.board[row - 1][column - 1]
                        right_char = board.board[row - 1][column + 1]
                    except IndexError:
                        break

                    # Counts the number of empty spaces.
                    empty_chars_count = 0
                    if top_char == ' ':
                        empty_chars_count += 1
                    if left_char == ' ':
                        empty_chars_count += 1
                    if right_char == ' ':
                        empty_chars_count += 1

                    # If the number of empty spaces is 1 find the correct
                    # empty space and execute the suite. The suite gets the new
                    # relevant row and column indexes as well as the string
                    # indicating which side is empty.
                    if (empty_chars_count == 1) and (top_char == ' '):
                        row -= 2
                        chain_list.append((row, column))
                        last_open_side_str = 't'
                        if row == 0:
                            break

                    elif (empty_chars_count == 1) and (right_char == ' '):
                        row -= 1
                        column += 1
                        chain_list.append((row, column))
                        last_open_side_str = 'r'
                        if column == (len(board.board) - 1):
                            break

                    elif (empty_chars_count == 1) and (left_char == ' '):
                        row -= 1
                        column -= 1
                        chain_list.append((row, column))
                        last_open_side_str = 'l'
                        if column == 0:
                            break

                    else:
                        break

                # Selects an if clause dependent on the last_open_side_str.
                elif last_open_side_str == 'r':

                    # Fixes the error where the chain will have negative
                    # indexes inside, resulting in selection of incorrect and
                    # illegal moves.
                    if column == (len(board.board) - 1):
                        break

                    # Tries to get the relevant move spaces, since the last
                    # open side was a right we only need the other sides.
                    try:
                        top_char = board.board[row - 1][column + 1]
                        bottom_char = board.board[row + 1][column + 1]
                        right_char = board.board[row][column + 2]
                    except IndexError:
                        break

                    # Counts the number of empty spaces.
                    empty_chars_count = 0
                    if top_char == ' ':
                        empty_chars_count += 1
                    if bottom_char == ' ':
                        empty_chars_count += 1
                    if right_char == ' ':
                        empty_chars_count += 1

                    # If the number of empty spaces is 1 find the correct
                    # empty space and execute the suite. The suite gets the new
                    # relevant row and column indexes as well as the string
                    # indicating which side is empty.
                    if (empty_chars_count == 1) and (top_char == ' '):
                        row -= 1
                        column += 1
                        chain_list.append((row, column))
                        last_open_side_str = 't'
                        if row == 0:
                            break

                    elif (empty_chars_count == 1) and (right_char == ' '):
                        column += 2
                        chain_list.append((row, column))
                        last_open_side_str = 'r'
                        if column == (len(board.board) - 1):
                            break

                    elif (empty_chars_count == 1) and (bottom_char == ' '):
                        row += 1
                        column += 1
                        chain_list.append((row, column))
                        last_open_side_str = 'b'
                        if row == (len(board.board) - 1):
                            break

                    else:
                        break

                # Selects an if clause dependent on the last_open_side_str.
                elif last_open_side_str == 'b':

                    # Fixes the error where the chain will have negative
                    # indexes inside, resulting in selection of incorrect and
                    # illegal moves.
                    if row == (len(board.board) - 1):
                        break

                    # Tries to get the relevant move spaces, since the last
                    # open side was a bottom we only need the other sides.
                    try:
                        left_char = board.board[row + 1][column - 1]
                        bottom_char = board.board[row + 2][column]
                        right_char = board.board[row + 1][column + 1]
                    except IndexError:
                        break

                    # Counts the number of empty spaces.
                    empty_chars_count = 0
                    if left_char == ' ':
                        empty_chars_count += 1
                    if bottom_char == ' ':
                        empty_chars_count += 1
                    if right_char == ' ':
                        empty_chars_count += 1

                    # If the number of empty spaces is 1 find the correct
                    # empty space and execute the suite. The suite gets the new
                    # relevant row and column indexes as well as the string
                    # indicating which side is empty.
                    if (empty_chars_count == 1) and (left_char == ' '):
                        row += 1
                        column -= 1
                        chain_list.append((row, column))
                        last_open_side_str = 'l'
                        if column == 0:
                            break

                    elif (empty_chars_count == 1) and (right_char == ' '):
                        row += 1
                        column += 1
                        chain_list.append((row, column))
                        last_open_side_str = 'r'
                        if column == (len(board.board) - 1):
                            break

                    elif (empty_chars_count == 1) and (bottom_char == ' '):
                        row += 2
                        chain_list.append((row, column))
                        last_open_side_str = 'b'
                        if row == (len(board.board) - 1):
                            break

                    else:
                        break

                # Selects an if clause dependent on the last_open_side_str.
                elif last_open_side_str == 'l':

                    # Fixes the error where the chain will have negative
                    # indexes inside, resulting in selection of incorrect and
                    # illegal moves.
                    if column == 0:
                        break

                    # Tries to get the relevant move spaces, since the last
                    # open side was a left we only need the other sides.
                    try:
                        left_char = board.board[row][column - 2]
                        bottom_char = board.board[row + 1][column - 1]
                        top_char = board.board[row - 1][column - 1]
                    except IndexError:
                        break

                    # Counts the number of empty spaces.
                    empty_chars_count = 0
                    if top_char == ' ':
                        empty_chars_count += 1
                    if bottom_char == ' ':
                        empty_chars_count += 1
                    if left_char == ' ':
                        empty_chars_count += 1

                    # If the number of empty spaces is 1 find the correct
                    # empty space and execute the suite. The suite gets the new
                    # relevant row and column indexes as well as the string
                    # indicating which side is empty.
                    if (empty_chars_count == 1) and (top_char == ' '):
                        row -= 1
                        column -= 1
                        chain_list.append((row, column))
                        last_open_side_str = 't'
                        if row == 0:
                            break

                    elif (empty_chars_count == 1) and (left_char == ' '):
                        column -= 2
                        chain_list.append((row, column))
                        last_open_side_str = 'l'
                        if column == 0:
                            break

                    elif (empty_chars_count == 1) and (bottom_char == ' '):
                        row += 1
                        column -= 1
                        chain_list.append((row, column))
                        last_open_side_str = 'b'
                        if row == (len(board.board) - 1):
                            break

                    else:
                        break

            # If the chain will fill in enough boxes it gets appended.
            if len(chain_list) >= 2:
                self.master_chains_list.append(chain_list)

    def turn_execution(self, board, row=None, column=None):
        """
        The turn execution for player B. Selects the best move for the
        player to make and sets the attribute move_tup to that move.

        param self: The WinningPlayer
        type self: WinningPlayer

        param board: The board to execute on.
        type board: Board

        param row: The row index.
        type row: Int

        param column: The column index.
        type column: Int

        """

        # Loop to ensure validity of move.
        while True:
            # Execute id_chain_headers and find_chains methods
            # to find chains for this turn.
            if (row is not None) and (column is not None):
                self.id_chain_headers(board)
                self.find_chains(board)

            # If the executable chain list is active get the next
            # move.
            if self.exe_chain_list:
                move_tup = self.exe_chain_list.pop(0)
                self.move_tup = move_tup

            # If there is a chain that can be executed get that chain.
            elif self.master_chains_list:

                chain_list = self.master_chains_list.pop()
                self.exe_chain_list = chain_list
                move_tup = self.exe_chain_list.pop(0)
                self.move_tup = move_tup

            # Otherwise get a random move_tup from the legal moves
            # set.
            else:
                move_tup = self.move_indices_set.pop()
                self.move_tup = move_tup

            # If the move is valid break the loop.
            if board.is_valid_move(self.move_tup[0], self.move_tup[1]):
                break


class Game(object):
    """
    Initiates a game between two players A and B. Has a detailed
    single_play method. Also has multiple_play method for playing multiple
    games. Coin flip method included for choosing who goes first.
    """

    def __init__(self):
        """Initiates the game and creates the winner attribute."""
        self.winner = None

    def single_play(self, fp, first_player='A'):
        """
        Plays one game with a RandomPlayer and a WinningPlayer.

        param self: The Game
        type self: Game

        param fp: The file pointer to write to.
        type fp: File-pointer

        param first_player: Tells which player should go first in the game.
        type first_player: Str
        """

        # Display heading for the game.
        fp.write("Single play mode game details.\n\n")
        print('\nSingle play mode. Plays a game in great detail'
              ' showing individual moves.\n')

        # Loops to gather board size and random seed input.
        while True:
            try:
                board_input_int = int(input('Please enter what length and '
                                            'width you would like to make the board: '))
                break
            except ValueError:
                print('Please try again, enter a positive integer.')

        while True:
            try:
                random_seed_int = int(input('Please enter what seed you would '
                                        'like to use for the random player: '))
                break
            except ValueError:
                print('Please try again, enter a positive integer.')

                # Initialize random seed and board.
        board = Board(board_input_int)
        random.seed(random_seed_int)

        # Initialize players.
        player_a = RandomPlayer('A')
        if first_player == 'A':
            player_b = WinningPlayer('B', False)
        if first_player == 'B':
            player_b = WinningPlayer('B', True)

        # Generate player move sets and turn num.
        player_a.generate_move_indices_set(board)
        player_b.generate_move_indices_set(board)

        turn_num = 1

        # Displays the newly generated board.
        print('\nGenerated Board:\n')
        print('{}'.format(board))
        fp.write('Generated Board:\n\n')
        fp.write('{}\n'.format(board.__str__()))

        # Separates the turn.
        print(50 * '~', '\n')
        fp.write(50 * '~')
        fp.write('\n\n')

        if first_player == 'A':

            # Gets the move_tup using the choose move method.
            # Removes the move from the legal moves sets.
            # Updates board.
            move_tup = player_a.choose_move(random_seed_int)
            player_a.remove_move_indices(move_tup[0], move_tup[1])
            player_b.remove_move_indices(move_tup[0], move_tup[1])
            board.update_board(move_tup[0], move_tup[1])

            # Displays turn summary.
            print("Turn {}, Player A's (RandomPlayer) Move:\n".format(turn_num))
            fp.write("Turn {}, Player A's (RandomPlayer) Move:\n\n".format(turn_num))

            print("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
            print("Updated Board:\n")
            print(board)
            print('Score: A:{}, B:{}\n'.format(str(player_a.score()),
                                               str(player_b.score())))
            print(50 * '~', '\n')
            fp.write("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
            fp.write('Updated Board:\n\n')
            fp.write('{}\n'.format(board.__str__()))
            fp.write('Score: A:{}, B:{}\n\n'.format(str(player_a.score()),
                                                    str(player_b.score())))
            fp.write(50 * '~')
            fp.write('\n\n')

            last_turn = 'A'
            turn_num += 1

        elif first_player == 'B':

            # Uses turn execution method and removes move from legal
            # moves set. Updates board.
            player_b.turn_execution(board)
            move_tup = player_b.move_tup
            player_a.remove_move_indices(move_tup[0], move_tup[1])
            player_b.remove_move_indices(move_tup[0], move_tup[1])
            board.update_board(move_tup[0], move_tup[1])

            # Displays turn summary.
            print("Turn {}, Player B's (WinningPlayer) Move:\n".format(turn_num))
            fp.write("Turn {}, Player B's (WinningPlayer) Move:\n\n".format(turn_num))

            print("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
            print("Updated Board:\n")
            print(board)
            print('Score: A:{}, B:{}\n'.format(str(player_a.score()),
                                               str(player_b.score())))
            print(50 * '~', '\n')
            fp.write("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
            fp.write('Updated Board:\n\n')
            fp.write('{}\n'.format(board.__str__()))
            fp.write('Score: A:{}, B:{}\n\n'.format(str(player_a.score()),
                                                    str(player_b.score())))
            fp.write(50 * '~')
            fp.write('\n\n')

            last_turn = 'B'
            turn_num += 1

        while not board.win():

            if last_turn == 'B':
                # Display who's turn it is.
                print("Turn {}, Player A's (RandomPlayer) Move:\n".format(turn_num))
                fp.write("Turn {}, Player A's (RandomPlayer) Move:\n\n".format(turn_num))

                # Uses choose move method and removes the moves from
                # the legal move sets.
                move_tup = player_a.choose_move(random_seed_int)
                player_a.remove_move_indices(move_tup[0], move_tup[1])
                player_b.remove_move_indices(move_tup[0], move_tup[1])
                for i, chain_header in \
                        enumerate(player_b.master_chain_headers_list):
                    if chain_header[0] == move_tup[0]:
                        if chain_header[1] == move_tup[1]:
                            del player_b.master_chain_headers_list[i]

                # Update the board
                board.update_board(move_tup[0], move_tup[1])

                # Check for boxes.
                box_points = board.check_for_box(move_tup[0], move_tup[1], 'A')

                # If a box was made, execute.
                if box_points > 0:
                    player_a.add_points(box_points)

                    # Displays turn summary.
                    print("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
                    print("Updated Board:\n")
                    print(board)
                    print('Score: A:{}, B:{}\n'.format(str(player_a.score()),
                                                       str(player_b.score())))
                    print('Box made player goes again if board not won.\n')
                    print(50 * '~', '\n')
                    fp.write("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
                    fp.write('Updated Board:\n\n')
                    fp.write('{}\n'.format(board.__str__()))
                    fp.write('Score: A:{}, B:{}\n\n'.format
                             (str(player_a.score()), str(player_b.score())))
                    fp.write(
                        'Box made player goes again if board not won.\n\n')
                    fp.write(50 * '~')
                    fp.write('\n\n')
                    turn_num += 1
                    continue

                # Displays turn summary.
                print("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
                print("Updated Board:\n")
                print(board)
                print('Score: A:{}, B:{}\n'.format(str(player_a.score()),
                                                   str(player_b.score())))
                print(50 * '~', '\n')
                fp.write("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
                fp.write('Updated Board:\n\n')
                fp.write('{}\n'.format(board.__str__()))
                fp.write('Score: A:{}, B:{}\n\n'.format(str(player_a.score()),
                                                        str(player_b.score())))
                fp.write(50 * '~')
                fp.write('\n\n')

                last_turn = 'A'
                turn_num += 1

            elif last_turn == 'A':
                # Display who's turn it is.
                print("Turn {}, Player B's (WinningPlayer) Move:\n".format(turn_num))
                fp.write("Turn {}, Player B's (WinningPlayer) Move:\n\n".format(turn_num))

                # Uses turn execution method and removes the moves from
                # the legal move sets.
                player_b.turn_execution(board, move_tup[0], move_tup[1])
                move_tup = player_b.move_tup
                player_a.remove_move_indices(move_tup[0], move_tup[1])
                player_b.remove_move_indices(move_tup[0], move_tup[1])
                for i, chain_header in \
                        enumerate(player_b.master_chain_headers_list):
                    if chain_header[0] == move_tup[0]:
                        if chain_header[1] == move_tup[1]:
                            del player_b.master_chain_headers_list[i]

                # Update the board
                board.update_board(move_tup[0], move_tup[1])

                # Check for boxes.
                box_points = board.check_for_box(move_tup[0], move_tup[1], 'B')

                # If a box was made, execute.
                if box_points > 0:
                    player_b.add_points(box_points)

                    # Displays turn summary.
                    print("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
                    print("Updated Board:\n")
                    print(board)
                    print('Score: A:{}, B:{}\n'.format(str(player_a.score()),
                                                       str(player_b.score())))
                    print('Box made player goes again if board not won.\n')
                    print(50 * '~', '\n')
                    fp.write("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
                    fp.write('Updated Board:\n\n')
                    fp.write('{}\n'.format(board.__str__()))
                    fp.write('Score: A - {}, B - {}\n\n'.format
                             (str(player_a.score()), str(player_b.score())))
                    fp.write(
                        'Box made player goes again if board not won.\n\n')
                    fp.write(50 * '~')
                    fp.write('\n\n')

                    turn_num += 1
                    continue

                # Displays turn summary.
                print("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
                print("Updated Board:\n")
                print(board)
                print('Score: A:{}, B:{}\n'.format(str(player_a.score()),
                                                   str(player_b.score())))
                print(50 * '~', '\n')
                fp.write("Move made at: \n\
Row : {}, Column : {}\n".format(move_tup[0], move_tup[1]))
                fp.write('Updated Board:\n\n')
                fp.write('{}\n'.format(board.__str__()))
                fp.write('Score: A:{}, B:{}\n\n'.format(str(player_a.score()),
                                                        str(player_b.score())))
                fp.write(50 * '~')
                fp.write('\n\n')

                last_turn = 'B'
                turn_num += 1

        # Displays final score.
        print('Final Score: A (RandomPlayer):{}, B (WinningPlayer):{}\n'
              .format(str(player_a.score()), str(player_b.score())))
        fp.write('Final Score: A (RandomPlayer):{}, B (WinningPlayer):{}\n'
                 .format(str(player_a.score()), str(player_b.score())))

        # If the player a score is greater than the player b score, display
        # a as the winner.
        if player_a.score() > player_b.score():
            print('Winner: A')
            fp.write('Winner: A')
            self.winner = 'A'

        # If the player b score is greater than the player a score, display
        # b as the winner.
        elif player_b.score() > player_a.score():
            print('Winner: B')
            fp.write('Winner: B')
            self.winner = 'B'

        # If the scores are equal declare a tie.
        elif player_b.score() == player_a.score():
            print('Tie')
            fp.write('Tie')

        print('\nThank you for playing Single Play Mode')

    def multiple_play(self, fp2):
        """
        Plays the specified number of games with a WinningPlayer against
        the RandomPlayer. Displays statistics about the games.

        param self: The Game being played.
        type self: Game

        param fp2: The file pointer to the file to write information to.
        type fp2: File-pointer
        """
        # Displays headers.
        fp2.write("Multiple play mode game details.\n\n")
        print('\nMultiple play game mode ')

        # Gathers input info for board size, random seed int, and number of
        # games to play. Error checking included.
        while True:
            try:
                board_input_int = int(input('Please enter what length and '
                                            'width you would like to make '
                                            'the board: '))
                break
            except ValueError:
                print('Please try again, enter a positive integer.')

        while True:
            try:
                random_seed_int = int(input('Please enter what seed you '
                                            'would like to use for the '
                                            'random player: '))
                break
            except ValueError:
                print('Please try again, enter a positive integer.')

        while True:
            try:
                game_int = int(input('Please enter the number of games '
                                     'you would like to play: '))
                break
            except ValueError:
                print('Please try again, enter a positive integer.')

        # Gets the start time and initializes the random seed.
        start_time = time.time()
        random.seed(random_seed_int)

        # Initializes the relevant variables to get statistics with.
        game_count = 0
        player_a_scores_list = []
        player_b_scores_list = []
        a_starts_int = 0
        b_starts_int = 0
        a_wins_int = 0
        b_wins_int = 0
        ties_int = 0

        # Iterates through the number of times specified.
        for p in range(game_int):

            # Randomize seed each game to ensure different move outcomes.
            random_seed_int = random.randint(1, 10000)
            random.seed(random_seed_int)
            random_seed_int = random.randint(1, 10000)
            random.seed(random_seed_int)

            # Initialize board and flip coin for who moves first.
            board = Board(board_input_int)
            first_choice = self.coin_flip(random_seed_int)

            # Initialize players.
            player_a = RandomPlayer('A')
            if first_choice == 'A':
                player_b = WinningPlayer('B', False)
            elif first_choice == 'B':
                player_b = WinningPlayer('B', True)

            # Get legal moves set indexes.
            player_a.generate_move_indices_set(board)
            player_b.generate_move_indices_set(board)

            turn_num = 1

            # If player A is set to move first.
            if first_choice == 'A':
                # Use choose move method, update board, and remove the move
                # from legal move sets.
                move_tup = player_a.choose_move(random_seed_int)
                player_a.remove_move_indices(move_tup[0], move_tup[1])
                player_b.remove_move_indices(move_tup[0], move_tup[1])
                board.update_board(move_tup[0], move_tup[1])

                a_starts_int += 1
                last_turn = 'A'
                turn_num += 1

            # If player B is set to move first.
            elif first_choice == 'B':
                # Use turn execution method to get move, remove move from
                # legal move sets. Update board.
                player_b.turn_execution(board)
                move_tup = player_b.move_tup
                player_a.remove_move_indices(move_tup[0], move_tup[1])
                player_b.remove_move_indices(move_tup[0], move_tup[1])
                board.update_board(move_tup[0], move_tup[1])

                b_starts_int += 1
                last_turn = 'B'
                turn_num += 1

            # If the board is not won.
            while not board.win():

                # If B moved last execute.
                if last_turn == 'B':
                    # Use choose move method to get move and remove move
                    # from legal move sets.
                    move_tup = player_a.choose_move(random_seed_int)
                    player_a.remove_move_indices(move_tup[0], move_tup[1])
                    player_b.remove_move_indices(move_tup[0], move_tup[1])
                    for i, chain_header in \
                            enumerate(player_b.master_chain_headers_list):
                        if chain_header[0] == move_tup[0]:
                            if chain_header[1] == move_tup[1]:
                                del player_b.master_chain_headers_list[i]

                    # Update board and check for box.
                    board.update_board(move_tup[0], move_tup[1])
                    box_points = board.check_for_box(
                        move_tup[0], move_tup[1], 'A')

                    # If a box is made execute this suite.
                    if box_points > 0:
                        player_a.add_points(box_points)
                        turn_num += 1
                        continue

                    last_turn = 'A'
                    turn_num += 1

                # If A moved last execute this suite.
                elif last_turn == 'A':
                    # Use turn execution method to get move and then remove
                    # move from legal move sets.
                    player_b.turn_execution(board, move_tup[0], move_tup[1])
                    move_tup = player_b.move_tup
                    player_a.remove_move_indices(move_tup[0], move_tup[1])
                    player_b.remove_move_indices(move_tup[0], move_tup[1])
                    for i, chain_header in \
                            enumerate(player_b.master_chain_headers_list):
                        if chain_header[0] == move_tup[0]:
                            if chain_header[1] == move_tup[1]:
                                del player_b.master_chain_headers_list[i]

                    # Update the board and check for boxes
                    board.update_board(move_tup[0], move_tup[1])
                    box_points = board.check_for_box(
                        move_tup[0], move_tup[1], 'B')

                    # If box(es) made execute.
                    if box_points > 0:
                        player_b.add_points(box_points)
                        turn_num += 1
                        continue

                    last_turn = 'B'
                    turn_num += 1

            # Determine who won and update the stats.
            if player_b.score_att > player_a.score_att:
                b_wins_int += 1
            elif player_a.score_att > player_b.score_att:
                a_wins_int += 1
            else:
                ties_int += 1
            player_a_scores_list.append(player_a.score())
            player_b_scores_list.append(player_b.score())
            game_count += 1

        # Sort the lists and generate relevant stats using statistics
        # module and functions.
        player_a_scores_list = sorted(player_a_scores_list)
        player_b_scores_list = sorted(player_b_scores_list)

        total_scores_list = sorted(
            player_a_scores_list + player_b_scores_list)
        total_median_score = statistics.median(total_scores_list)
        total_mean_score = statistics.mean(total_scores_list)

        a_scores_list_copy = copy.deepcopy(player_a_scores_list)
        b_scores_list_copy = copy.deepcopy(player_b_scores_list)

        a_median_score = statistics.median(a_scores_list_copy)
        b_median_score = statistics.median(b_scores_list_copy)

        a_mean_score = statistics.mean(a_scores_list_copy)
        b_mean_score = statistics.mean(b_scores_list_copy)

        a_score_max = max(a_scores_list_copy)
        b_score_max = max(b_scores_list_copy)

        a_score_min = min(a_scores_list_copy)
        b_score_min = min(b_scores_list_copy)

        # Give the header, game count, and board size.
        print("\n{}\n".format('Multiple Play Statistics:'))

        print("Board Size: {}x{}\n".format(board_input_int,
                                           board_input_int))

        print("{:<25s}{:<d}\n".format('Game Count:', game_count))

        # Give the data total average and median.
        print("{:<25s}{:<.1f}".format("Median Total Score: ",
                                      total_median_score))
        print("{:<25s}{:<.1f}".format("Mean Total Score: ", total_mean_score))

        # Give player A data.
        print("\n{}".format('Player A (RandomPlayer):'))
        print("{:<25s}{:.2%}".format("Win Percent:",
                                     (a_wins_int / game_count)))
        print("{:<25s}{:<d}".format("Wins:", a_wins_int))
        print("{:<25s}{:<d}".format('Games A started:', a_starts_int))
        print("{:<25s}{:<.1f}".format('Median Score:', a_median_score))
        print("{:<25s}{:<.4f}".format('Mean Score:', a_mean_score))
        print("{:<25s}{:<d}".format('Max Score:', a_score_max))
        print("{:<25s}{:<d}\n".format('Min Score:', a_score_min))

        fp2.write("{}\n\n".format('Dots and Boxes Multiple Play Statistics:'))
        fp2.write("Board size: {}x{}\n\n".format(board_input_int,
                                                 board_input_int))
        fp2.write("{:<25s}{:<d}\n\n".format('Game Count:', game_count))

        fp2.write("{:<25s}{:<.1f}\n".format("Average Total Score: ",
                                            ((a_mean_score + b_mean_score) / 2)))
        fp2.write("{:<25s}{:<.1f}\n\n".format("Median Total Score: ",
                                              ((a_mean_score + b_mean_score) / 2)))

        fp2.write("{}\n".format('Player A (RandomPlayer):'))
        fp2.write("{:<25s}{:.2%}\n".format("Win Percent:",
                                           (a_wins_int / game_count)))
        fp2.write("{:<25s}{:<d}\n".format("Wins:", a_wins_int))
        fp2.write("{:<25s}{:<d}\n".format('Games A started:', a_starts_int))
        fp2.write("{:<25s}{:<.1f}\n".format('Median Score:', a_median_score))
        fp2.write("{:<25s}{:<.4f}\n".format('Mean Score:', a_mean_score))
        fp2.write("{:<25s}{:<d}\n".format('Max Score:', a_score_max))
        fp2.write("{:<25s}{:<d}\n\n".format('Min Score:', a_score_min))

        # Give the data for player b.
        print("{}".format('Player B (WinningPlayer):'))
        print("{:<25s}{:.2%}".format("Win Percent:",
                                     (b_wins_int / game_count)))
        print("{:<25s}{:<d}".format("Wins:", b_wins_int))
        print("{:<25s}{:<d}".format('Games B started:', b_starts_int))
        print("{:<25s}{:.1f}".format('Median Score:', b_median_score))
        print("{:<25s}{:.4f}".format('Mean Score:', b_mean_score))
        print("{:<25s}{:<d}".format('Max Score:', b_score_max))
        print("{:<25s}{:<d}\n".format('Min Score:', b_score_min))

        fp2.write("{}\n".format('Player B (WinningPlayer):'))
        fp2.write("{:<25s}{:.2%}\n".format("Win Percent:",
                                           (b_wins_int / game_count)))
        fp2.write("{:<25s}{:<d}\n".format("Wins:", b_wins_int))
        fp2.write("{:<25s}{:<d}\n".format('Games B started:', b_starts_int))
        fp2.write("{:<25s}{:.1f}\n".format('Median Score:', b_median_score))
        fp2.write("{:<25s}{:.4f}\n".format('Mean Score:', b_mean_score))
        fp2.write("{:<25s}{:<d}\n".format('Max Score:', b_score_max))
        fp2.write("{:<25s}{:<d}\n\n".format('Min Score:', b_score_min))

        # Give the time taken to calculate.
        print("Calculations performed in: {:.4f} seconds".
              format(time.time() - start_time))
        fp2.write("Calculations performed in: {:.4f} seconds\n\n".
                  format(time.time() - start_time))
        print('\nThank you for playing Multiple Play Mode\n')
        fp2.write("Thank you for playing!")

    def coin_flip(self, random_seed_int):
        """
        Makes a random choice between A and B to determine who goes first.
        Returns the string value. Takes a the random seed for the random
        seed generator.
        """
        # Initialize the random seed.
        random.seed(random_seed_int)
        # Choose who goes first.
        coin_flip_choice = random.choice(['A', 'B'])

        return coin_flip_choice


def main():
    # Open relevant txt files for writing.
    fp1 = open('single_play.txt', 'w')
    fp2 = open('multiple_play.txt', 'w')

    print('Hello, welcome to dots and boxes.')
    print('Created by Hank Murdock.\n')

    # Embedding notes on strategy within single_play.txt

    fp1.write("Strategy Notes: \n\
The strategy I followed was the long chains rule, with this rule \n\
I created an algorithm that searches for chains. A chain being a \n\
sequence of moves that will take boxes one after another. In the \n\
single play games you can see this occur, player B will use moves \n\
that look like a winding snake. It starts with a box that has three \n\
sides full, from the open side there must be at least one more box \n\
to take, that box will have the side that will be taken by the first \n\
box open, as well as a new side that is open. Some chains are only \n\
two moves long and some will fill in half of a large board.\n\n")

    fp1.write(100 * '~')
    fp1.write('\n\n')

    print("Strategy Notes: \n\
The strategy I followed was the long chains rule, with this rule \n\
I created an algorithm that searches for chains. A chain being a \n\
sequence of moves that will take boxes one after another. In the \n\
single play games you can see this occur, player B will use moves \n\
that look like a winding snake. It starts with a box that has three \n\
sides full, from the open side there must be at least one more box \n\
to take, that box will have the side that will be taken by the first \n\
box open, as well as a new side that is open. Some chains are only \n\
two moves long and some will fill in half of a large board.\n")

    print(100 * '~')
    print()

    fp1.write("Welcome to Single Play Mode. Player A is the random player, \n\
Player B is the winning player for all games and game modes. This \n\
first game will have Player A go first, then a second game will occur \n\
with Player B going first.\n\n")

    fp1.write(100 * '~')
    fp1.write('\n\n')

    print("Welcome to Single Play Mode. Player A is the random player, \n\
Player B is the winning player for all games and game modes. This \n\
first game will have Player A go first, then a second game will occur \n\
with Player B going first.")

    # Play game 1 (single_play, random player first.)
    game1 = Game()
    game1.single_play(fp1, 'A')

    fp1.write('\n\nPlaying Second Game With Player B Going First\n\n')
    print('Playing Second Game With Player B Going First')

    # Play game 2 (single_play, winning player first)
    game2 = Game()
    game2.single_play(fp1, 'B')
    fp1.close()

    # Play game 3 (multiple play)
    game3 = Game()
    game3.multiple_play(fp2)

    fp2.close()

    print("Thank you for playing!")


if __name__ == "__main__":
    main()
