from argparse import ArgumentParser
import logging

logger = logging.getLogger('cf')


class ConnectFour:
    def __init__(self, player1, player2):
        self.players = {1: player1, 2: player2}
        self.currentTurn = 1
        self.fields = []
        self.rows = [6, 5, 4, 3, 2, 1]
        self.cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        for row in self.rows:
            for col in self.cols:
                self.fields.append(Field(self, col, row))

        self.start()

    def start(self):
        self.print_board()

    def print_board(self):
        print('')
        for field in self.fields:
            field.print()

        print('   - - - - - - - -')
        print('   ', end='')
        for col in self.cols:
            print(col, end=' ')


class Field:
    def __init__(self, game, col, row):
        self.game = game
        self.col = col
        self.row = row
        self.startCol = True if col == game.cols[0] else False
        self.endCol = True if col == game.cols[-1] else False
        self.state = 0

    def print(self):
        if self.startCol:
            print(str(self.row) + '| ' + str(self.state), end=' ')
        elif self.endCol:
            print(self.state)
        else:
            print(self.state, end=' ')


def init():
    ap = ArgumentParser()
    ap.add_argument('p1',
                    default='Player 1',
                    nargs='?',
                    help='Name of Player 1')
    ap.add_argument('p2',
                    default='Player 2',
                    nargs='?',
                    help='Name of Player 2')
    args = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s %(funcName)s: %(message)s')
    ConnectFour(args.p1, args.p2)


if __name__ == '__main__':
    init()
