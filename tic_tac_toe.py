import random
import numpy
import time

X = -1
O = 1
ROWS = 3
COLUMNS = 3


def create_matrix():  # creating zero matrix
    cell_matrix = numpy.zeros((ROWS, COLUMNS), dtype=int)
    return cell_matrix


def correct_coordinates(cell_matrix):  # checking if coordinates given by user are correct (from 0 to columns)
    while True:
        coordinates = input().split()
        try:
            coordinates = [(int(x) - 1) for x in coordinates]
        except ValueError:
            print("You should enter numbers!")
            continue
        if coordinates[0] not in range(0, COLUMNS) or coordinates[1] not in range(0, COLUMNS):
            print("Coordinates should be from 1 to 3!")
            continue
        elif cell_matrix[coordinates[0]][coordinates[1]] != 0:
            print("This cell is occupied! Choose another one!")
            continue
        elif len(coordinates) != 2:
            print("Please enter 2 coordinates separated by space")
        else:
            return coordinates


def print_board(cell_matrix):
    print("---------")
    for r in range(ROWS):
        print("| ", end="")
        for c in range(COLUMNS):
            if cell_matrix[r][c] == X:
                print("X", end=" ")
            elif cell_matrix[r][c] == O:
                print("O", end=" ")
            elif cell_matrix[r][c] == 0:
                print(" ", end=" ")
        print("|")
    print("---------")


def result(cell_matrix):  # checks what is the result of the game and if it is finished
    # uses counting the values of diagonals, rows or columns to check if they are equal to X or O value * columns

    first_diagonal = cell_matrix.trace()  # returns first diagonal as list
    second_diagonal = cell_matrix[::-1].trace()  # returns second diagonal using reversed matrix
    x_win = X * COLUMNS
    o_win = O * COLUMNS

    if first_diagonal == x_win or second_diagonal == x_win:
        return "X wins"
    elif first_diagonal == o_win or second_diagonal == o_win:
        return "O wins"

    for n in range(COLUMNS):
        column_sum = cell_matrix[:, n].sum()
        row_sum = cell_matrix[n].sum()
        if (column_sum or row_sum) == x_win:
            return "X wins"
        elif (column_sum or row_sum) == o_win:
            return "O wins"

    for ro in cell_matrix:
        if 0 in ro:
            return "not finished"
    return "Draw"


def easy_move(cell_matrix):  # makes random move
    moves = [x for x in range(COLUMNS)]
    while True:
        x = random.choice(moves)
        y = random.choice(moves)
        if cell_matrix[x][y] == 0:
            return [x, y]


def medium_move(cell_matrix, player):
    # blocks if there is danger of loosing or wins if there is 2 in a row, otherwise makes random moves
    # counts if it can win just like result function but columns - 1 because looks for 2 in a row
    first_diagonal = numpy.diag(cell_matrix)
    second_diagonal = numpy.diag(cell_matrix[::-1])
    first_diagonal_sum = int(cell_matrix.trace())
    second_diagonal_sum = int(cell_matrix[::-1].trace())
    computer_win = player * (COLUMNS - 1)
    opponent_win = (- player) * (COLUMNS - 1)
    if first_diagonal_sum == opponent_win or first_diagonal_sum == computer_win:
        # looks where the zero is in diagonal (there is only one) and returns its coordinates
        # they are the same because its first diagonal
        return [numpy.where(first_diagonal == 0)[0][0], numpy.where(first_diagonal == 0)[0][0]]
    elif second_diagonal_sum == computer_win or second_diagonal_sum == opponent_win:
        # subtracts coordinate from (columns - 1) to make reversed diagonal
        return [(COLUMNS - 1) - numpy.where(second_diagonal == 0)[0][0], numpy.where(second_diagonal == 0)[0][0]]

    # it returns coordinates just like with diagonals but for columns and rows
    for n in range(COLUMNS):
        column_sum = cell_matrix[:, n].sum()
        row_sum = cell_matrix[n].sum()
        if column_sum == computer_win or column_sum == opponent_win:
            return [numpy.where(cell_matrix[:, n] == 0)[0][0], n]
        elif row_sum == computer_win or row_sum == opponent_win:
            return [n, numpy.where(cell_matrix[n] == 0)[0][0]]
    return easy_move(cell_matrix)


def hard_move(cell_matrix, player):
    # uses minimax algorithm without alpha beta pruning
    computer_coordinates = [0, 0]
    returned_result = result(cell_matrix)
    # checks whether is the possibility to win
    if returned_result[0] == "O":
        return 1
    elif returned_result[0] == "X":
        return -1
    elif returned_result == "Draw":
        return 0

    empty_places = numpy.where(cell_matrix == 0)  # gives two lists with coordinates of zeros in mat5rix
    game_score = 10 * -player

    for i in range(len(empty_places[0])):
        actual_game_matrix = numpy.copy(cell_matrix)  # copies the matrix to not change the real one
        actual_game_matrix[empty_places[0][i]][empty_places[1][i]] = player
        new_score = hard_move(actual_game_matrix, -player)
        # checks if new_score is int or tuple because after first recursion it becomes the tuple
        if not isinstance(new_score, int):
            new_score = new_score[0]
        # compares if the new outcome (-1, 1, 0) is better than the last one, if it is coordinates and score are changed
        if compare(new_score, game_score, player):
            game_score = new_score
            computer_coordinates = [empty_places[0][i], empty_places[1][i]]

    return game_score, computer_coordinates


def place_move(player, coordinates, cell_matrix):
    cell_matrix[coordinates[0]][coordinates[1]] = player
    print_board(cell_matrix)
    return - player


def compare(x, y, player):
    if player == -1:
        return x < y
    else:
        return x > y


def check_input():
    while True:
        print("Input command:")
        user_input = input().split()
        possibilities = ["easy", "medium", "hard", "user"]
        if len(user_input) != 3:
            if user_input[0] == "exit":
                break
            else:
                print("Bad parameters")
        elif user_input[0] == "start" and user_input[1] in possibilities and user_input[2] in possibilities:
            player_list = user_input[1:]
            return player_list


def game():
    cell_matrix = create_matrix()
    player_list = check_input()
    player = X
    block_first_move = True
    print_board(cell_matrix)
    while result(cell_matrix) == "not finished":
        time.sleep(1)
        if "user" in player_list:
            if block_first_move and player_list[0] != "user":
                block_first_move = False
            else:
                print("Enter the coordinates:")
                coordinates = correct_coordinates(cell_matrix)
                player = place_move(player, coordinates, cell_matrix)
        if "easy" in player_list:
            print('Making move level "easy"')
            computer_coordinates = easy_move(cell_matrix)
            player = place_move(player, computer_coordinates, cell_matrix)
        if "medium" in player_list:
            print('Making move level "medium"')
            computer_coordinates = medium_move(cell_matrix, player)
            player = place_move(player, computer_coordinates, cell_matrix)
        if "hard" in player_list:
            print('Making move level "hard"')
            game_score, computer_coordinates = hard_move(cell_matrix, player)
            player = place_move(player, computer_coordinates, cell_matrix)
    print(result(cell_matrix))


game()
