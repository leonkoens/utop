#!/usr/bin/python

import curses
from model import Model


if __name__ == '__main__':
    curses.wrapper(Model)
