#!/usr/bin/env python3

import curses
from curses import textpad, wrapper

from screen import help
from screen import match
from screen import settings
from screen import display
from screen import config_game
from screen import exit

import mymovements

def setup_screen(stdscr):
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)
    stdscr.keypad(True)

# TODO: Re-implement in another way
# def print_debug(win, t):
#    sh, sw = win.getmaxyx()
#    
#    win.addstr(sh-1,1," " + t + " ")
#    win.refresh()

def main_menu(parent_win):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    options = [
        {
            'id': 'quick_match',
            'text': 'Quick Match'
        },
        {
            'id': 'start',
            'text': 'Start'
        },
        {
            'id': 'display_horse',
            'text': 'Display a horse'
        },
        {
            'id': 'help',
            'text': 'Help'
        },
        {
            'id':'settings',
            'text': 'Settings'
        },
        {
            'id': 'exit',
            'text': 'Exit'
        }
    ]

    return mymovements.menu_loop(parent_win, options, is_main_menu=True)

def main_handler(stdscr):
    setup_screen(stdscr)
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)

    while True:
        win.box()
        win.addstr(0, 2, ' Better ASCII horses ')
        win.refresh()

        res = main_menu(win)

        if res == 'exit' or res is None:
            exit.exit(stdscr)
        elif res == 'quick_match':
            match.quick(win)
        elif res == 'start':
            (horses, bet) = config_game.config_step(win)
            match.play(win, horses, bet, 0)
        elif res == 'display_horse':
            display.display(win)
        elif res == 'help':
            help.help(win)
        elif res == 'settings':
            settings.settings(win)
        else:
            win.addstr(2, 2, 'Invalid option, how did you get here?')

if __name__ == "__main__":
    curses.wrapper(main_handler)