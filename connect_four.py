from argparse import ArgumentParser


def main():
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

    print("Name of Player 1: ", args.p1)
    print("Name of Player 2: ", args.p2)


if __name__ == '__main__':
    main()
