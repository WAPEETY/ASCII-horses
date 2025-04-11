#!/usr/bin/env python3

import curses
from curses import textpad, wrapper
import time

from screen import help
from screen import match
from screen import settings
from screen import display
from screen import config_game

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

    sh, sw = parent_win.getmaxyx()
    menu_win = curses.newwin(12, 40, sh//2 - 6, sw//2 - 20)

    key = 0
    options = [
        {
            'id': 'quick_match',
            'text': '0. Quick Match'
        },
        #{
        #    'id': 'start',
        #    'text': '1. Start'
        #},
        {
            'id': 'display_horse',
            'text': '1. Display a horse'
        },
        #{
        #    'id': 'help',
        #    'text': '2. Help'
        #},
        #{
        #    'id':'settings',
        #    'text': '5. Settings'
        #},
        {
            'id': 'exit',
            'text': '2. Exit'
        }
    ]
    current_option = 0

    menu_win.refresh()
    menu_win.move(1, 2)
    menu_win.keypad(True)

    #while True:
    menu_win.clear()
    menu_win.refresh()

        #if key == curses.KEY_DOWN or key == ord('d'):
        #    current_option = (current_option + 1) % len(options)
        #elif key == curses.KEY_UP or key == ord('u'):
        #    current_option = (current_option - 1) % len(options)
        #elif key == curses.KEY_ENTER or key in [10, 13]:
        #    menu_win.clear()
        #    menu_win.refresh()
        #    return options[current_option]['id']

    for i, option in enumerate(options):
        menu_win.addstr(i+2, 2, option['text'])
    menu_win.refresh()
    key = menu_win.getch()

    if key >= 48 and key <= 57:
        key = key - 48
    else:
        key = 0

    if key < 0 or key >= len(options):
        key = 0
    
    return options[key]['id']

def main_handler(stdscr):
    setup_screen(stdscr)
    sh, sw = stdscr.getmaxyx()

    win = curses.newwin(sh, sw, 0, 0)
    win.box()
    win.addstr(0, 2, ' Better ASCII horses ')
    win.refresh()

    while True:
        res = main_menu(win)

        if res == 'exit':
            win.addstr(2, 2, 'Goodbye!')
            win.refresh()
            time.sleep(2)
            return 0
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