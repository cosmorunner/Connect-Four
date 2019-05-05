import logging
from argparse import ArgumentParser

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
        while self.game_continues():
            current_player = self.current_turn
            self.print_board()
            while current_player == self.current_turn:
                position = input(self.players[self.current_turn] + ', place your next token: ')
                if position == 'quit':
                    quit()

                try:
                    self.place_token(position)
                    self.switch_current_player()

                except ValueError as err:
                    print(getattr(err, 'message', str(err)))

        self.switch_current_player()
        self.print_board()
        print('Congratulations, ' + self.get_player() + ', you won!')

    def game_continues(self):
        placed_tokens = list(filter(lambda e: e.state != ' ', self.fields))
        # minimum number of tokens required
        if len(placed_tokens) < 1:
            return True

        for field in self.fields:
            if field.state == ' ':
                continue

            col_index = self.cols.index(field.col)
            check_against = []

            # check vertical chain
            try:
                check_vert = [self.get_field(field.col, field.row + 1),
                              self.get_field(field.col, field.row + 2),
                              self.get_field(field.col, field.row + 3)]
                check_against.append(check_vert)
            except ValueError:
                pass

            # check horizontal chain
            try:
                check_vert = [self.get_field(self.cols[col_index + 1], field.row),
                              self.get_field(self.cols[col_index + 2], field.row),
                              self.get_field(self.cols[col_index + 3], field.row)]
                check_against.append(check_vert)
            except ValueError:
                pass
            except IndexError:
                pass

            # check ascending diagonal chain
            try:
                check_vert = [self.get_field(self.cols[col_index + 1], field.row + 1),
                              self.get_field(self.cols[col_index + 2], field.row + 2),
                              self.get_field(self.cols[col_index + 3], field.row + 3)]
                check_against.append(check_vert)
            except ValueError:
                pass
            except IndexError:
                pass

            # check descending diagonal chain
            try:
                check_vert = [self.get_field(self.cols[col_index + 1], field.row - 1),
                              self.get_field(self.cols[col_index + 2], field.row - 2),
                              self.get_field(self.cols[col_index + 3], field.row - 3)]
                check_against.append(check_vert)
            except ValueError:
                pass
            except IndexError:
                pass

            for chain in check_against:
                if chain[0].state == field.state and chain[1].state == field.state and chain[2].state == field.state:
                    return False

        return True

    def place_token(self, position):
        pos_obj = self.convert_position(position)
        field = self.get_field(pos_obj['col'], pos_obj['row'])
        self.validate_position(field)
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

    def validate_position(self, field):
        if field.state != ' ':
            raise ValueError(
                'Position ' + field.col + str(field.row) + ' is already taken. Please choose another position.')

        open_col_fields = list(filter(lambda e: e.col == field.col and e.state == ' ', self.fields))
        sorted_col_fields = sorted(open_col_fields, key=lambda x: x.row)
        if sorted_col_fields[0].row != field.row:
            raise ValueError('Position ' + field.col + str(field.row) + ' is invalid. Please choose another position.')

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

    def get_player(self):
        return self.players[self.current_turn]


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
