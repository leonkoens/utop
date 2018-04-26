#!/usr/bin/python3

import curses
from utop.model import Model
import logging


if __name__ == '__main__':
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)

    try:
        curses.wrapper(Model)
    except KeyboardInterrupt:
        Model.running = False
