#!/usr/bin/env python

from argparse import ArgumentParser
from prototype_layout_tool.core import read_specs, draw_cards


if __name__ == '__main__':
    parser = ArgumentParser(description="Game Prototype Layout")
    parser.add_argument('-s', '--spec', dest='spec_filename')
    parser.add_argument('-o', '--out', dest='out_filename')
    args = parser.parse_args()

    if not args.spec_filename or not args.out_filename:
        parser.print_help()
    else:
        (card_list, layout) = read_specs(args.spec_filename)
        draw_cards(card_list, args.out_filename, layout)
