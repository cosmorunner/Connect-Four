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
                self.fields.append(Field(col, row))

        self.start()

    def start(self):
        counter = 0
        while counter < 5:
            self.print_board()
            counter += 1
            position = input('Place your next token: ')
            self.place_token(position)

    def place_token(self, position):
        col = position[:1]
        row = position[1:]

        for field in self.fields:
            if field.col == col and field.row == int(row):
                field.state = 'X'

    def print_board(self):
        print('')
        for row in self.rows:
            print(str(row) + '| ', end='')
            items = list(filter(lambda e: e.row == row, self.fields))
            for ele in items:
                print(ele.state, end=' ')
            print('')

        print('   ', end='')

        for col in self.cols:
            print(col, end=' ')

        print('')


class Field:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.state = ' '

    def __repr__(self):
        return 'Field(%s, %s, %s)' % (self.col, self.row, self.state)

    def print(self):
        print(self.state, end='')


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
