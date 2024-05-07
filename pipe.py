# Grupo 25:
# 106992 Mariana Santana
# 106221 João Rodrigues

from sys import stdin
import time

import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

pieces_specs = {"FC": "0010", "FB": "0001", "FE": "1000", "FD": "0100",
                "BC": "1110", "BB": "1101", "BE": "1011", "BD": "0111",
                "VC": "1010", "VB": "0101", "VE": "1001", "VD": "0110",
                "LH": "1100", "LV": "0011"}

class PipeManiaState:
    state_id = 0
    def __init__(self, board, depth):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.depth = depth
    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

class Board:

    def __init__(self, board: np.array, n_rows: int, n_cols: int):
        self.board = board
        self.n_rows = n_rows
        self.n_cols = n_cols

    def copy_board(self):
        return Board(np.copy(self.board), self.n_rows, self.n_cols)
    
    """ Representação interna de uma grelha de PipeMania. """

    def get_piece(self, row: int, col: int):
        """ Devolve a peça presente na posição (row, col) da grelha. """
        return self.board[row][col]
    
    def get_value(self, row: int, col: int):
        """ Devolve o valor presente na posição (row, col) da grelha. """
        return self.get_piece(row, col)[0]

    def adjacent_vertical_values(self, row: int, col: int):
        """Returns the values immediately above and below the given position."""
        above = self.get_value(row - 1, col) if row > 0 else None
        below = self.get_value(row + 1, col) if row < len(self.board) - 1 else None
        return (above, below)
        
    def adjacent_horizontal_values(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        up = self.get_value(row, col - 1) if col > 0 else None
        down = self.get_value(row, col + 1) if col < len(self.board[0]) - 1 else None
        return (up, down)
        
    def adjacent_vertical_pieces(self, row: int, col: int):
        """Returns the pieces immediately above and below the given position."""
        above = self.get_piece(row - 1, col) if row > 0 else None
        below = self.get_piece(row + 1, col) if row < len(self.board) - 1 else None
        return (above, below)
    
    def adjacent_horizontal_pieces(self, row: int, col: int):
        """ Devolve as peças imediatamente à esquerda e à direita,
        respectivamente. """
        left = self.get_piece(row, col - 1) if col > 0 else None
        right = self.get_piece(row, col + 1) if col < len(self.board[0]) - 1 else None
        return (left, right) 
    
    def print_test(self):
        """ Imprime a grelha de PipeMania. """
        for row in self.board:
            for column in row:
                print(column , end = "")
                print('\t', end = "") 
            print("\n",end = "")
            
    def print(self):
        """ Imprime a grelha de PipeMania. """
        for row in self.board:
            for column in row:
                print(column[0], end = "")
                print('\t', end = "") 
            print("\n",end = "")
        
    def get_deductions(self, row: int, col: int):

        obj = self.board[row][col]
        obj_left, obj_right = self.adjacent_horizontal_pieces(row, col)
        obj_up, obj_down = self.adjacent_vertical_pieces(row, col)
        print(obj)
        print(obj_left, obj_right, obj_up, obj_down)
        print("\n")
        
        if obj_left is None or obj_left[0] is None:
            obj_left = [" ", None]
        if obj_right is None or obj_right[0] is None:    
            obj_right = [" ", None]
        if obj_up is None or obj_up[0] is None:
            obj_up = [" ", None]
        if obj_down is None or obj_down[0] is None:
            obj_down = [" ", None]
        
        # check objs on corners and turn pipes and make deductions
        if obj[0][0] == "V" :
            if row == 0 and col == 0 :
                self.board[row][col][0] = "VB"
                self.board[row][col][1] = 0
            elif row == 0 and col == self.n_cols - 1 :
                self.board[row][col][0] = "VE"
                self.board[row][col][1] = 0
            elif row == self.n_rows - 1 and col == 0 :
                self.board[row][col][0] = "VD"
                self.board[row][col][1] = 0
            elif row == self.n_rows - 1 and col == self.n_cols - 1 :
                self.board[row][col][0] = "VC"
                self.board[row][col][1] = 0

            elif row == 0 and col == 1 and obj_left[0][0] == "V":
                self.board[row][col][0] = "VE"
                self.board[row][col][1] = 0
            elif row == 0 and col == self.n_cols - 2 and obj_right[0][0] == "V":
                self.board[row][col][0] = "VB"
                self.board[row][col][1] = 0
            elif row == self.n_rows - 1 and col == 1 and obj_left[0][0] == "V":
                self.board[row][col][0] = "VC"
                self.board[row][col][1] = 0
            elif row == self.n_rows - 1 and col == self.n_cols - 2 and obj_right[0][0] == "V":
                self.board[row][col][0] = "VD"
                self.board[row][col][1] = 0
            elif row == 1 and col == 0 and obj_up[0][0] == "V":
                self.board[row][col][0] = "VD"
                self.board[row][col][1] = 0
            elif row == self.n_rows - 2 and col == 0 and obj_down[0][0] == "V":
                self.board[row][col][0] = "VB"
                self.board[row][col][1] = 0
            elif row == 1 and col == self.n_cols - 1 and obj_up[0][0] == "V":
                self.board[row][col][0] = "VC"
                self.board[row][col][1] = 0
            elif row == self.n_rows - 2 and col == self.n_cols - 1 and obj_down[0][0] == "V":
                self.board[row][col][0] = "VE"
                self.board[row][col][1] = 0
            
        # check objs on borders and make deductions 
        # if obj is a straith pipe
        elif obj[0][0] == "L":
            if  (row == 0 or row == self.n_rows - 1):
                self.board[row][col][0] = "LH"
                self.board[row][col][1] = 0
            elif (col == 0 or col == self.n_cols - 1):
                self.board[row][col][0] = "LV"
                self.board[row][col][1] = 0
        
        # if obj is a bifurcation pipe
        
        elif obj[0][0] == "B":
            if row == 0:
                self.board[row][col][0] = "BB"
                self.board[row][col][1] = 0
            elif row == self.n_rows - 1:
                self.board[row][col][0] = "BC"
                self.board[row][col][1] = 0
            elif col == 0:
                self.board[row][col][0] = "BD"
                self.board[row][col][1] = 0
            elif col == self.n_cols - 1:
                self.board[row][col][0] = "BE"
                self.board[row][col][1] = 0

            elif (obj_left[1] == 0) and (obj_left[0] in ["FC","FB","FD","BD","VB","VD","LV"]):
                print("entrou")
                self.board[row][col][0] = "BE"
                self.board[row][col][1] = 0
            elif (obj_right[1] == 0) and (obj_right[0] in ["FC","FB","FE","BE","VC","VE","LV"]):
                print("entrou")
                self.board[row][col][0] = "BD"
                self.board[row][col][1] = 0
            elif (obj_up[1] == 0) and (obj_up[0] in ["FC","FE","FD","BC","VC","VD","LH"]):
                print("entrou")
                self.board[row][col][0] = "BB"
                self.board[row][col][1] = 0
            elif (obj_down[1] == 0) and (obj_down[0] in ["FB","BE","BD","VB","VE","LH"]):
                print("entrou")
                self.board[row][col][0] = "BC"
                self.board[row][col][1] = 0
            
            
        # if obj is a close pipe
        elif obj[0][0] == "F":
        
            if (row == 0 or row == self.n_rows - 1) \
                and (obj_left[0][0] == "L" or obj_left[0][0] =="B"):
            
                self.board[row][col][0] = "FE"
                self.board[row][col][1] = 0
            elif (row == 0 or row == self.n_cols - 1) \
                and (obj_right[0][0] == "L" or obj_right[0][0] =="B"):
                self.board[row][col][0] = "FD"
                self.board[row][col][1] = 0
            elif (col == 0 or col == self.n_cols - 1) \
                and (obj_up[0][0] == "L" or obj_up[0][0] =="B"):
                self.board[row][col][0] = "FC"
                self.board[row][col][1] = 0
            elif (col == 0 or col == self.n_cols - 1) \
                and (obj_down[0][0] == "L" or obj_down[0][0] =="B"):
                self.board[row][col][0] = "FB"
                self.board[row][col][1] = 0
        
            elif ((row == 0 and col == 1) or (row == self.n_rows - 1 and col == 1)) \
                and (obj_left[0][0] == "L" ):
                self.board[row][col][0] = "FE"
                self.board[row][col][1] = 0
            elif ((row == 0 and col == self.n_cols - 2) or (row == self.n_rows - 1 and col == self.n_cols - 2)) \
                and (obj_right[0][0] == "L"):
                self.board[row][col][0] = "FD"
                self.board[row][col][1] = 0
            elif ((col == 0 and row == 1) or (col == self.n_cols - 1 and row == 1)) \
                and (obj_up[0][0] == "L"):
                self.board[row][col][0] = "FC"
                self.board[row][col][1] = 0
            elif ((col == 0 and row == self.n_rows - 2) or (col == self.n_cols - 1 and row == self.n_rows - 2)) \
                and (obj_down[0][0] == "L"):
                self.board[row][col][0] = "FB"
                self.board[row][col][1] = 0

            elif (obj_left[0][0] == "F" and obj_right[0][0] == "F"):
                if (row == 0):
                    self.board[row][col][0] = "FB"
                    self.board[row][col][1] = 0
                elif (row == self.n_rows - 1):
                    self.board[row][col][0] = "FC"
                    self.board[row][col][1] = 0
            elif (obj_up[0][0] == "F" and obj_down[0][0] == "F"):
                if (col == 0):
                    self.board[row][col][0] = "FE"
                    self.board[row][col][1] = 0
                elif (col == self.n_cols - 1):
                    self.board[row][col][0] = "FD"
                    self.board[row][col][1] = 0
            
            elif (obj_up[1] == 0 and obj_up[0] in ["BB","BE","BD","VB","VE","LV"]):
                self.board[row][col][0] = "FC"
                self.board[row][col][1] = 0
            elif (obj_down[1] == 0 and obj_down[0] in ["BC","BE","BD","VC","VD","LV"]):
                self.board[row][col][0] = "FB"
                self.board[row][col][1] = 0
            elif (obj_left[1] == 0 and obj_left[0] in ["BC","BB","BD","VB","VD","LH"]):
                self.board[row][col][0] = "FE"
                self.board[row][col][1] = 0
            elif (obj_right[1] == 0 and obj_right[0] in ["BC","BB","BD","VC","VE","LH"]):
                self.board[row][col][0] = "FD"
                self.board[row][col][1] = 0
          
    def run_deductions(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.get_deductions(i, j)
            
    @staticmethod
    def parse_instance():
        
        board_list = []
        for line in stdin:
            board_list.append([[word, 1] for word in line.split()])

        board = np.array(board_list)
        board_instance = Board(board, len(board), len(board[0]))

        board_instance.run_deductions()
        board_instance.print_test()
        return board_instance

class PipeMania(Problem):
    def __init__(self, board: Board, depth: int):
        """O construtor especifica o estado inicial."""
        self.state = PipeManiaState(board, depth)
        super().__init__(self.state)

    def get_filtered_actions(state, row, col):
        obj = state.board.get_piece(row,col)
        obj_left, obj_right = state.board.adjacent_horizontal_pieces(row, col)
        obj_up, obj_down = state.board.adjacent_vertical_pieces(row, col)

        #if obj_left[1] == '0':
        return []

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        row = state.depth // 2
        col = state.depth % 2

        #print(row, col)
        # too much depth for the board
        if state.board.n_rows <= row or state.board.n_cols <= col:
            return []

        if state.board.get_piece(row, col)[1] == '0':
            #print("entrou")
            state.depth += 1
            return PipeMania.actions(self, state)
        
        actions_ = []
        obj = state.board.get_piece(row, col)
        obj_left, obj_right = state.board.adjacent_horizontal_pieces(row, col)
        obj_up, obj_down = state.board.adjacent_vertical_pieces(row, col)

        """if obj_left[1] == '0' or obj_right[1] == '0' or obj_up[1] == '0' or obj_down[1] == '0' \
            or obj_left[0] == None or obj_right[0] == None or obj_up[0] == None or obj_down[0] == None:
            actions += PipeMania.get_filtered_actions(state, row, col)"""

        if state.board.get_piece(row, col)[0] == "FC":
            actions_ += [[row, col, "FB"], [row, col, "FE"], [row, col, "FD"]]
        elif state.board.get_piece(row, col)[0] == "FB":
            actions_ += [[row, col, "FC"], [row, col, "FE"], [row, col, "FD"]]
        elif state.board.get_piece(row, col)[0] == "FE":
            actions_ += [[row, col, "FC"], [row, col, "FB"], [row, col, "FD"]]
        elif state.board.get_piece(row, col)[0] == "FD":
            actions_ += [[row, col, "FC"], [row, col, "FB"], [row, col, "FE"]]
        elif state.board.get_piece(row, col)[0] == "BC":
            actions_ += [[row, col, "BB"], [row, col, "BE"], [row, col, "BD"]]
        elif state.board.get_piece(row, col)[0] == "BB":
            actions_ += [[row, col, "BC"], [row, col, "BE"], [row, col, "BD"]]
        elif state.board.get_piece(row, col)[0] == "BE":
            actions_ += [[row, col, "BC"], [row, col, "BB"], [row, col, "BD"]]
        elif state.board.get_piece(row, col)[0] == "BD":
            actions_ += [[row, col, "BC"], [row, col, "BB"], [row, col, "BE"]]
        elif state.board.get_piece(row, col)[0] == "VC":
            actions_ += [[row, col, "VB"], [row, col, "VE"], [row, col, "VD"]]
        elif state.board.get_piece(row, col)[0] == "VB":
            actions_ += [[row, col, "VC"], [row, col, "VE"], [row, col, "VD"]]
        elif state.board.get_piece(row, col)[0] == "VE":
            actions_ += [[row, col, "VC"], [row, col, "VB"], [row, col, "VD"]]
        elif state.board.get_piece(row, col)[0] == "VD":
            actions_ += [[row, col, "VC"], [row, col, "VB"], [row, col, "VE"]]
        elif state.board.get_piece(row, col)[0] == "LH":
            actions_ += [[row, col, "LV"]]
        elif state.board.get_piece(row, col)[0] == "LV":
            actions_ += [[row, col, "LH"]]
        #print("actions_", state.depth)
        #print(actions_)
        return actions_

        
    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        row, col, piece = action
        new_board : Board = state.board.copy_board()
        
        new_board.board[row][col][0] = piece
        new_board.board[row][col][1] = 0

        #new_board.print_test()
        #print(state.depth + 1)
        return PipeManiaState(new_board, state.depth + 1)

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        for row in range(self.state.board.n_rows):
            for col in range(self.state.board.n_cols):

                obj = state.board.get_value(row,col)
                obj_left, obj_right = state.board.adjacent_horizontal_values(row, col)
                obj_up, obj_down = state.board.adjacent_vertical_values(row, col)

                if obj == "FC":
                    if ((obj_left not in [None, "FC", "FB", "FE", "BE", "VC", "VE", "LV"]) or \
                        (obj_right not in [None, "FC", "FB", "FD", "BD", "VB", "VD", "LV"]) or \
                        (obj_up not in ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]) or \
                        (obj_down not in [None, "FB", "FE", "FD", "BB", "VB", "VE", "LH"])):
                        return False
                elif obj == "FB":
                    if ((obj_left not in [None, "FC", "FB", "FE", "BE", "VC", "VE", "LV"]) or \
                        (obj_right not in [None, "FC", "FB", "FD", "BD", "VB", "VD", "LV"]) or \
                        (obj_up not in [None, "FC", "FE", "FD", "BC", "VC", "VD", "LH"]) or \
                        (obj_down not in ["FC", "BC", "BE", "BD", "VC", "VD", "LH"])):
                        return False
                elif obj == "FE":
                    if ((obj_left not in ["FD", "BC", "BB", "BD", "VB", "VD", "LH"]) or \
                        (obj_right not in [None, "FC", "FB", "FD", "BD", "VB", "VD", "LV"]) or \
                        (obj_up not in [None, "FE", "FC", "FD", "BC", "VC", "VD", "LH"]) or \
                        (obj_down not in [None, "FB", "FE", "FD", "BB", "VB", "VE", "LH"])):
                        return False
                elif obj == "FD":
                    if ((obj_left not in [None, "FC", "FB", "FE", "BE", "VC", "VE", "LV"]) or \
                        (obj_right not in ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]) or \
                        (obj_up not in [None, "FC", "FE", "FD", "BC", "VC", "VD", "LH"]) or \
                        (obj_down not in [None, "FE", "FB", "FD", "BB", "VB", "VE", "LH"])):
                        return False
                elif obj == "BC":
                    if ((obj_left not in ["FD", "BC", "BB", "BD", "VB", "VD", "LH"]) or \
                        (obj_right not in ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]) or \
                        (obj_up not in ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]) or \
                        (obj_down not in [None, "FB", "FE", "FD", "BB", "VB", "VE", "LH"])):
                        return False
                elif obj == "BB":
                    if ((obj_left not in ["FD", "BC", "BB", "BD", "VB", "VD", "LH"]) or \
                        (obj_right not in ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]) or \
                        (obj_up not in [None, "FC", "FE", "FD", "BC", "VC", "VD", "LH"]) or \
                        (obj_down not in ["FC", "BC", "BE", "BD", "VC", "VD", "LV"])):
                        return False
                elif obj == "BE":
                    if ((obj_left not in ["FD", "BC", "BD", "BB", "VB", "VD", "LH"]) or \
                        (obj_right not in [None, "FC", "FB", "FD", "BD", "VB", "VD", "LV"]) or \
                        (obj_up not in ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]) or \
                        (obj_down not in ["FC", "BC", "BE", "BD", "VC", "VD", "LV"])):
                        return False
                elif obj == "BD":
                    if ((obj_left not in [None, "FC", "FB", "FE", "BE", "VC", "VE", "LV"]) or \
                        (obj_right not in ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]) or \
                        (obj_up not in ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]) or \
                        (obj_down not in ["FC", "BC", "BE", "BD", "VC", "VD", "LV"])):
                        return False
                elif obj == "VC":
                    if ((obj_left not in ["FD", "BC", "BD", "BB", "VB", "VD", "LH"]) or \
                        (obj_right not in [None, "FC", "FB", "FD", "BD", "VB", "VD", "LV"]) or \
                        (obj_up not in ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]) or \
                        (obj_down not in [None, "FB", "FE", "FD", "BB", "VB", "VE", "LH"])):
                        return False
                elif obj == "VB":
                    if ((obj_left not in [None, "FC", "FB", "FE", "BE", "VC", "VE", "LV"]) or \
                        (obj_right not in ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]) or \
                        (obj_up not in [None, "FC", "FE", "FD", "BC", "VC", "VD", "LH"]) or \
                        (obj_down not in ["FC", "BC", "BE", "BD", "VC", "VD", "LV"])):
                        return False
                elif obj == "VE":
                    if ((obj_left not in ["FD", "BC", "BD", "BB", "VB", "VD", "LH"]) or \
                        (obj_right not in [None, "FC", "FB", "FD", "BD", "VB", "VD", "LV"]) or \
                        (obj_up not in [None, "FC", "FE", "FD", "BC", "VC", "VD", "LH"]) or \
                        (obj_down not in ["FC", "BC", "BE", "BD", "VC", "VD", "LV"])):
                        return False
                elif obj == "VD":
                    if ((obj_left not in [None, "FC", "FB", "FE", "BE", "VC", "VE", "LV"]) or \
                        (obj_right not in ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]) or \
                        (obj_up not in ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]) or \
                        (obj_down not in [None, "FB", "FE", "FD", "BB", "VB", "VE", "LH"])):
                        return False
                elif obj == "LH":
                    if ((obj_left not in ["FD", "BC", "BD", "BB", "VB", "VD", "LH"]) or \
                        (obj_right not in ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]) or \
                        (obj_up not in [None, "FC", "FE", "FD", "BC", "VC", "VD", "LH"]) or \
                        (obj_down not in [None, "FB", "FE", "FD", "BB", "VB", "VE", "LH"])):
                        return False
                elif obj == "LV": 
                    if ((obj_left not in [None, "FC", "FB", "FE", "BE", "VC", "VE", "LV"]) or \
                        (obj_right not in [None, "FC", "FB", "FD", "BD", "VB", "VD", "LV"]) or \
                        (obj_up not in ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]) or \
                        (obj_down not in ["FC", "BC", "BE", "BD", "VC", "VD", "LV"])):
                        return False          

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

if __name__ == "__main__":

    board = Board.parse_instance()
    board.print()
    problem = PipeMania(board, 0)
    
    goal = depth_first_tree_search(problem)

    goal.state.board.print()