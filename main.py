#!/usr/bin/python

import curses
from model import Model


if __name__ == '__main__':
    try:
        curses.wrapper(Model)
    except KeyboardInterrupt:
        Model.running = False
