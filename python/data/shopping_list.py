#!/usr/bin/env python3

from growser.growser import print_shopping_list, parse_options
from growser.data import Data
from growser.pantry import from_file

from menu import all_dishes
from extras import extras

if __name__ == "__main__":
    options = parse_options()
    data = Data(
        menu=all_dishes,
        extras=extras,
        pantry=tuple()
    )
    print_shopping_list(options, data)