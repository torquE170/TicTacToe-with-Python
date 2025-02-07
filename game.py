import os
import sys
from random import randint


class Game:
    x_won = False
    o_won = False
    game_finished = False
    player_turn = 0  # 0 for player with "X" and 1 for player with "O"
    x_controlled = 0  # 0 for player and 1 for CPU
    o_controlled = 0  # 0 for player and 1 for CPU
    choice_list = {
        (0, 0): ((0, 1), (1, 1), (1, 0), (0, 2), (2, 2), (2, 0)),
        (0, 1): ((0, 0), (0, 2), (1, 1), (2, 1)),
        (0, 2): ((0, 1), (1, 1), (1, 2), (0, 0), (2, 0), (2, 2)),
        (1, 0): ((0, 0), (1, 1), (2, 0), (1, 2)),
        (1, 1): ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)),
        (1, 2): ((0, 2), (1, 1), (2, 0), (1, 0)),
        (2, 0): ((1, 0), (1, 1), (2, 1), (0, 0), (0, 2), (2, 2)),
        (2, 1): ((1, 1), (2, 0), (2, 2), (0, 1)),
        (2, 2): ((1, 1), (1, 2), (2, 1), (0, 0), (0, 2), (2, 0))
    }
    last_symbol_position = {
        ((0, 0), (0, 1)): (0, 2),
        ((0, 0), (1, 0)): (2, 0),
        ((0, 0), (1, 1)): (2, 2),
        ((0, 0), (0, 2)): (0, 1),
        ((0, 0), (2, 2)): (1, 1),
        ((0, 0), (2, 0)): (1, 0),

        ((0, 1), (0, 0)): (0, 2),
        ((0, 1), (0, 2)): (0, 0),
        ((0, 1), (1, 1)): (2, 1),
        ((0, 1), (2, 1)): (1, 1),

        ((0, 2), (0, 1)): (0, 0),
        ((0, 2), (1, 2)): (2, 2),
        ((0, 2), (1, 1)): (2, 0),
        ((0, 2), (0, 0)): (0, 1),
        ((0, 2), (2, 0)): (1, 1),
        ((0, 2), (2, 2)): (1, 2),

        ((1, 0), (0, 0)): (2, 0),
        ((1, 0), (1, 1)): (1, 2),
        ((1, 0), (2, 0)): (0, 0),
        ((1, 0), (1, 2)): (1, 1),

        ((1, 1), (0, 0)): (2, 2),
        ((1, 1), (0, 1)): (2, 1),
        ((1, 1), (0, 2)): (2, 0),
        ((1, 1), (1, 0)): (1, 2),
        ((1, 1), (1, 2)): (1, 0),
        ((1, 1), (2, 0)): (0, 2),
        ((1, 1), (2, 1)): (0, 2),
        ((1, 1), (2, 2)): (0, 0),

        ((1, 2), (0, 2)): (2, 2),
        ((1, 2), (1, 1)): (1, 0),
        ((1, 2), (2, 2)): (0, 2),
        ((1, 2), (1, 0)): (1, 1),

        ((2, 0), (1, 0)): (0, 0),
        ((2, 0), (1, 1)): (0, 2),
        ((2, 0), (2, 1)): (2, 2),
        ((2, 0), (0, 0)): (1, 0),
        ((2, 0), (0, 2)): (1, 1),
        ((2, 0), (2, 2)): (2, 1),

        ((2, 1), (1, 1)): (0, 1),
        ((2, 1), (2, 0)): (2, 2),
        ((2, 1), (2, 2)): (2, 0),
        ((2, 1), (0, 1)): (1, 1),

        ((2, 2), (1, 1)): (0, 0),
        ((2, 2), (1, 2)): (0, 2),
        ((2, 2), (2, 1)): (2, 0),
        ((2, 2), (0, 0)): (1, 1),
        ((2, 2), (0, 2)): (1, 2),
        ((2, 2), (2, 0)): (2, 1),
    }

    def __init__(self, game_table):
        # formating game table
        self.game_table = []
        for i in range(len(game_table)):
            self.game_table.append([])
            for j in range(len(game_table[i])):
                if game_table[i][j] == "x" or game_table[i][j] == "X":
                    self.game_table[i].append("X")
                elif game_table[i][j] == "o" or game_table[i][j] == "O":
                    self.game_table[i].append("O")
                else:
                    self.game_table[i].append("_")

    @classmethod
    def game_start(cls):
        empty_table = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]
        new_game = Game(empty_table)
        return new_game

    def add_element(self, element, indexes):
        if indexes[0] > 2 or indexes[1] > 2 or indexes[0] < 0 or indexes[1] < 0:
            raise IndexError
        if self.game_table[indexes[0]][indexes[1]] != "_":
            raise ValueError
        if self.game_table[indexes[0]][indexes[1]] == "_":
            if element.upper() == "O":
                self.game_table[indexes[0]][indexes[1]] = "O"
            elif element.upper() == "X":
                self.game_table[indexes[0]][indexes[1]] = "X"

    def check_status(self, simulation=False):
        # Check if the game is finished in case of a draw
        empty_spot = False
        for line in self.game_table:
            if "_" in line:
                empty_spot = True
        if not empty_spot:
            self.game_finished = True

        for index in range(len(self.game_table)):
            # Line check for winning combo
            if self.game_table[index][0] != "_":
                if self.game_table[index][0] == self.game_table[index][1] and self.game_table[index][1] == \
                        self.game_table[index][2]:
                    if self.game_table[index][0] == "X":
                        self.x_won = True
                        self.game_finished = True
                    elif self.game_table[index][0] == "O":
                        self.o_won = True
                        self.game_finished = True
                    break

            # Column check for winning combo
            if self.game_table[0][index] != "_":
                if self.game_table[0][index] == self.game_table[1][index] and self.game_table[1][index] == \
                        self.game_table[2][index]:
                    if self.game_table[0][index] == "X":
                        self.x_won = True
                        self.game_finished = True
                    elif self.game_table[0][index] == "O":
                        self.o_won = True
                        self.game_finished = True
                    break

        # Diagonals check for winning combo
        if self.game_table[0][0] == self.game_table[1][1] and self.game_table[1][1] == self.game_table[2][2]:
            if self.game_table[0][0] == "X":
                self.x_won = True
                self.game_finished = True
            elif self.game_table[0][0] == "O":
                self.o_won = True
                self.game_finished = True

        if self.game_table[0][2] == self.game_table[1][1] and self.game_table[1][1] == self.game_table[2][0]:
            if self.game_table[0][2] == "X":
                self.x_won = True
                self.game_finished = True
            elif self.game_table[0][2] == "O":
                self.o_won = True
                self.game_finished = True

        # Display if the game is still going
        if empty_spot and (not self.o_won and not self.x_won):
            return "Game in progress..."

        # Check if draw of there's a winner or game finished
        if self.game_finished:
            if self.x_won:
                if simulation:
                    self.x_won = False
                    self.game_finished = False
                return ">> X won!"
            if self.o_won:
                if simulation:
                    self.o_won = False
                    self.game_finished = False
                return ">> O won!"
            if not self.x_won and not self.o_won:
                if simulation:
                    self.game_finished = False
                return ">> Draw!"

    def next_round(self):
        if self.player_turn:
            self.player_turn = 0
        else:
            self.player_turn += 1

    def play_round(self):
        if self.player_turn == 0:
            self.place_element("X", Game.x_controlled)
        elif self.player_turn == 1:
            self.place_element("O", Game.o_controlled)
        self.next_round()

    def place_element(self, player_string, controlled):
        position_error = False
        index_error = False
        while True:
            try:
                added = False
                Game.clear()
                if position_error:
                    print("Invalid position")
                    position_error = False
                if index_error:
                    print("Out of bounds index")
                    index_error = False
                self.print_out()
                if controlled:
                    # CPU logic

                    # First move - take center
                    if self.empty_slots() == 9:
                        self.add_element(player_string, [1, 1])
                        break

                    # Second move - take center or corners
                    choices = list(range(1, 10, 2))
                    if self.empty_slots() == 8:
                        for l in range(3):
                            for k in range(3):
                                if self.game_table[l][k] == self.other_symbol():
                                    choices.remove(l * 3 + k + 1)
                                    choice = choices[randint(1, 4) - 1]
                                    i = (choice - 1) // 3
                                    j = (choice - 1) % 3
                                    self.add_element(player_string, [i, j])
                                    added = True
                                    break
                            else:
                                continue
                            break
                    if added:
                        break

                    # Check for winning move
                    for i in range(3):
                        for j in range(3):
                            if self.is_empty((i, j)):
                                self.add_element(player_string, (i, j))
                                if self.check_status(True) == f">> {player_string} won!":
                                    added = True  # winning move made, break loop
                                    break
                                self.remove_element((i, j))  # Undo move
                        else:
                            continue
                        if added:
                            break
                    if added:
                        break

                    # Check for blocking move
                    for i in range(3):
                        for j in range(3):
                            if self.is_empty((i, j)):
                                self.add_element(self.other_symbol(), (i, j))
                                if self.check_status(True) == f">> {self.other_symbol()} won!":
                                    self.remove_element((i, j))  # Undo move
                                    self.add_element(player_string, (i, j))  # Block opponent
                                    added = True
                                    break
                                self.remove_element((i, j))  # Undo move
                        else:
                            continue
                    if added:
                        break

                    # Connect with another symbol
                    if 5 <= self.empty_slots() <= 7:
                        for i1 in range(3):
                            for j1 in range(3):
                                if self.game_table[i1][j1] == player_string:
                                    i2, j2 = self.second_position([i1, j1], player_string)
                                    self.add_element(player_string, [i2, j2])
                                    added = True
                                    break
                            else:
                                continue
                            break
                    if added:
                        break

                    if self.empty_slots() <= 3:
                        # Get a list of all empty slots
                        empty_slots_table = [(i, j) for i in range(3) for j in range(3) if self.is_empty((i, j))]

                        # If there are empty slots, choose one at random and place the symbol
                        if empty_slots_table:
                            i, j = empty_slots_table[randint(0, len(empty_slots_table) - 1)]
                            self.add_element(player_string, (i, j))
                            break

                else:
                    # Player logic
                    print(f"Player {player_string} insert on position:")
                    i = int(input("line = "))
                    j = int(input("column = "))
                    self.add_element(player_string, [i, j])
                break
            except ValueError:
                position_error = True
            except IndexError:
                index_error = True

    def remove_element(self, indexes):
        if indexes[0] > 2 or indexes[1] > 2 or indexes[0] < 0 or indexes[1] < 0:
            raise IndexError("Index out of bounds")
        self.game_table[indexes[0]][indexes[1]] = "_"

    def empty_slots(self):
        counter = 0
        for line in self.game_table:
            for element in line:
                if element == "_":
                    counter += 1
        return counter

    def is_empty(self, indexes):
        if self.game_table[indexes[0]][indexes[1]] == '_':
            return True
        else:
            return False

    # use only when placing in a one symbol combo
    def second_position(self, indexes, player_string):
        remove_positions = []
        for i1 in range(3):
            for j1 in range(3):
                if self.game_table[i1][j1] == player_string:
                    for m in range(len(Game.choice_list[(i1, j1)])):
                        i2 = Game.choice_list[(i1, j1)][m][0]
                        j2 = Game.choice_list[(i1, j1)][m][1]
                        i3, j3 = Game.third_position_assessment([i1, j1], [i2, j2])
                        if self.is_empty([i2, j2]) and self.is_empty([i3, j3]):
                            return i2, j2
                        elif self.game_table[i2][j2] == player_string and self.is_empty([i3, j3]):
                            return i3, j3
                        else:
                            if self.game_table[i2][i2] != player_string and self.game_table[i3][j3] != player_string:
                                remove_positions.append(i2 * 3 + j2 + 1)
                                remove_positions.append(i3 * 3 + j3 + 1)
                            continue
        else:
            empty_slots = []
            for i1 in range(3):
                for j1 in range(3):
                    if self.game_table[i1][j1] == '_':
                        empty_slots.append(i1 * 3 + j1 + 1)
            for iter1 in empty_slots:
                if iter1 in remove_positions:
                    empty_slots.remove(iter1)
            choice = empty_slots[randint(1, len(empty_slots)) - 1]
            return (choice - 1) // 3, (choice - 1) % 3

    # used in second_position(self, indexes, player_string): for assuring there is a clear path
    @staticmethod
    def third_position_assessment(indexes, second_indexes):
        if ((indexes[0], indexes[1]), (second_indexes[0], second_indexes[1])) in Game.last_symbol_position:
            i3 = Game.last_symbol_position[((indexes[0], indexes[1]), (second_indexes[0], second_indexes[1]))][0]
            j3 = Game.last_symbol_position[((indexes[0], indexes[1]), (second_indexes[0], second_indexes[1]))][1]
            return i3, j3
        else:
            return -1, -1

    def other_symbol(self):
        if self.player_turn:
            return "X"
        else:
            return "O"

    @staticmethod
    def main_menu():
        option = -1
        while option:
            Game.clear()
            print("1 - Play")
            print("2 - Options")
            print()
            print("0 - Exit")
            option = Game.read_menu_option(">> ")
            if option == 1:
                # Play action
                Game.clear()
                one_game = Game.game_start()
                one_game.print_out()
                result = one_game.check_status()
                print(result)
                input("Press enter to start")  # Wait for user input to start the game

                while not one_game.game_finished:
                    one_game.play_round()
                    result = one_game.check_status()
                    if one_game.game_finished:
                        Game.clear()
                        one_game.print_out()
                    print(result)
                    print()

                input("Press enter for main menu")
            elif option == 2:
                # Options action
                option = -1
                while option:
                    Game.clear()
                    print(f"1 - Switch first player - current {"O" if Game.player_turn else "X"}")
                    print(f"2 - Toggle X (Player/CPU) - current {"CPU" if Game.x_controlled else "Player"}")
                    print(f"3 - Toggle O (Player/CPU) - current {"CPU" if Game.o_controlled else "Player"}")
                    print()
                    print(f"0 - Back")
                    option = Game.read_menu_option(">> ")
                    if option == 1:
                        # Choose first player
                        if Game.player_turn:
                            Game.player_turn = 0
                        else:
                            Game.player_turn += 1
                        option = -1
                    elif option == 2:
                        # Toggle X
                        if Game.x_controlled:
                            Game.x_controlled = 0
                        else:
                            Game.x_controlled += 1
                    elif option == 3:
                        # Toggle O
                        if Game.o_controlled:
                            Game.o_controlled = 0
                        else:
                            Game.o_controlled += 1
                    elif option == 0:
                        # Back
                        option = -1
                        break

            elif option == 0:
                # Exit action
                return

    @staticmethod
    def read_menu_option(prompt):
        while True:
            try:
                read = input(prompt)
                number = int(read)
                return number
            except ValueError:
                return -1

    @staticmethod
    def clear():
        if "win" in sys.platform:
            os.system("cls")
        elif "linux" in sys.platform:
            os.system("clear")

    def print_out(self):
        for line in self.game_table:
            for element in line:
                print(element, end=" ")
            print()

# main
Game.main_menu()
