from argparse import ArgumentParser
import logging

logger = logging.getLogger('cf')


class ConnectFour:
    def __init__(self, player1, player2):
        self.players = {1: player1, 2: player2}
        self.symbols = {1: 'X', 2: 'O'}
        self.current_turn = 1
        self.fields = []
        self.rows = [6, 5, 4, 3, 2, 1]
        self.cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        for row in self.rows:
            for col in self.cols:
                self.fields.append(Field(col, row))

        self.start()

    def start(self):
        counter = 0
        while counter < 3:
            current_player = self.current_turn
            self.print_board()
            while current_player == self.current_turn:
                position = input(self.players[self.current_turn] + ', place your next token: ')
                try:
                    self.place_token(position)
                    self.switch_current_player()
                    counter += 1
                except ValueError as err:
                    print(getattr(err, 'message', str(err)))

    def place_token(self, position):
        position_obj = self.convert_position(position)
        field = self.get_field(position_obj['col'], position_obj['row'])
        self.validate_position(position_obj['col'], position_obj['row'])
        field.state = self.symbols[self.current_turn]

    def convert_position(self, position):
        try:
            col = position[0:1].upper()
            row = int(position[1:2])
            return {'col': col, 'row': row}
        except ValueError:
            raise ValueError('Position ' + position + ' does not exist.')

    def get_field(self, col, row):
        for field in self.fields:
            if str(field.col) == col and int(field.row) == row:
                return field
        raise ValueError('Position ' + col + str(row) + ' does not exist.')

    def get_open_fields(self):
        fields = []
        # Filter blocked fields
        for field in self.fields:
            if field.state == ' ':
                fields.append(field)
        for col in self.cols:
            col_fields = list(filter(lambda e: e.col == col, fields))
            sorted_col_fields = sorted(col_fields, key=lambda x: x.row)
            fields.append(sorted_col_fields[0])
        return fields

    def validate_position(self, col, row):
        open_fields = self.get_open_fields()

        for field in open_fields:
            if str(field.col) == col and int(field.row) == row and field.state == ' ':
                return field
        raise ValueError('Position ' + col + str(row) + ' is already taken. Please choose another position.')

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

    def switch_current_player(self):
        self.current_turn = 2 if self.current_turn == 1 else 1


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
