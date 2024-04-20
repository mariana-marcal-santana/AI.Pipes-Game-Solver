from search import Problem, Node
from sys import stdin
import numpy as np

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

    @staticmethod
    def parse_instance():
        
        board_list = []
        for line in stdin:
            board_list.append(line.split())

        board = np.array(board_list)
        
        return Board(board)

    def __init__(self, board: np.array):
        self.board = board

    """ Representação interna de uma grelha de PipeMania. """
    def adjacent_vertical_values(self, row: int, col: int):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        # TODO
        pass
    def adjacent_horizontal_values(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        # TODO
        pass
    # TODO: outros metodos da classe



Board.parse_instance()

class PipeMania(Problem):
    def __init__(self, initial_state: Board, goal_state: Board):
        """ O construtor especifica o estado inicial. """
    # TODO
    pass
    def actions(self, state: PipeManiaState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
    # TODO
    pass
    def result(self, state: PipeManiaState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
    # TODO
    pass
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
    # TODO
    pass