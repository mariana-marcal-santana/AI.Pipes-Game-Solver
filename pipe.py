# Grupo 25:
# 106992 Mariana Santana
# 106221 João Rodrigues

from sys import stdin
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

class PipeManiaState:
    state_id = 0
    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

class Board:

    def __init__(self, board: np.array, n_rows: int, n_cols: int):
        self.board = board
        self.n_rows = n_rows
        self.n_cols = n_cols

    """ Representação interna de uma grelha de PipeMania. """
    def adjacent_vertical_values(self, row: int, col: int):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        if row == 0:
            return (None, self.board[row + 1][col])
        elif row == len(self.board) - 1:
            return (self.board[row - 1][col], None)
        else:
            return (self.board[row - 1][col], self.board[row + 1][col])
        
    def adjacent_horizontal_values(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        if col == 0:
            return (None, self.board[row][col + 1])
        elif col == len(self.board[0]) - 1:
            return (self.board[row][col - 1], None)
        else:
            return (self.board[row][col - 1], self.board[row][col + 1])
        
    def get_value(self, row: int, col: int):
        """ Devolve o valor presente na posição (row, col) da grelha. """
        return self.board[row][col]
    
    def print(self):
        """ Imprime a grelha de PipeMania. """
        for row in self.board:
            for column in row:
                print(column , end = "")
                print('\t', end = "") 
            print("\n",end = "")

    def get_deductions(self, row: int, col: int):

        obj = self.board[row][col]
        obj_left, ob_right = self.adjacent_horizontal_values(row, col)
        obj_up, obj_down = self.adjacent_vertical_values(row, col)

        # check objs on corners and make deductions
        if row == 0 and col == 0 and not obj[0] == "VB":
            self.board[row][col] = "VB"
        elif row == 0 and col == self.board.n_cols - 1 and not obj[0] == "VE":
            self.board[row][col] = "VE"
        elif row == self.board.n_rows - 1 and col == 0 and not obj[0] == "VD":
            self.board[row][col] = "VD"
        elif row == self.board.n_rows - 1 and col == self.board.n_cols - 1 and not obj[0] == "VC":
            self.board[row][col] = "VC"
    
        # check objs on borders and make deductions 
        # if obj is a straith pipe
        if obj[0] == "L" :
            if (row == 0 and obj == "LH") or (row == self.board.n_rows - 1 and obj == "LH") :
                self.board[row][col] = "LV" 
            elif (col == 0 and obj == "LV") or (col == self.board.n_cols - 1 and obj == "LV") :
                self.board[row][col] = "LH"
        
        # if obj is a bifurcation pipe
        elif obj[1] == "B":
            if (row == 0 and not obj == "BB") :
                self.board[row][col] = "BB"
            elif (row == self.board.n_rows - 1 and not obj == "BC") :
                self.board[row][col] = "BC"
            elif (col == 0 and not obj == "BD") :
                self.board[row][col] = "BD"
            elif (col == self.board.n_cols - 1 and not obj == "BE") :
                self.board[row][col] = "BE"
        
    def run_deductions(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                # check if obj is a corner
                if (i == 0 and j == 0) \
                    or (i == 0 and j == len(self.board[i]) - 1) \
                    or (i == len(self.board) - 1 and j == 0) \
                    or (i == len(self.board) - 1 and j == len(self.board[i]) - 1):
                    Board.get_deductions(self, i, j)
                # check if obj is on a border
                elif i == 0 or i == len(self.board) - 1 or j == 0 or j == len(self.board[i]) - 1:
                    Board.get_deductions(self, i, j)
            
    @staticmethod
    def parse_instance():
        
        board_list = []
        for line in stdin:
            board_list.append(line.split())

        board = np.array(board_list)
        board_instance = Board(board, len(board), len(board[0]))

        board_instance.run_deductions()

        return board_instance




class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    board.print()
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
