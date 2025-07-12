import curses
import os

import mymovements

def enable_cheats():
    with open('.cheats', 'w') as f:
        f.write('')
    return

def disable_cheats():
    os.remove('.cheats')
    return

def settings(parent_win):
    sh, sw = parent_win.getmaxyx()

    win = curses.newwin(sh//2 - 4, sw//2 - 4, sh//2 - sh//4 + 2, sw//2 - sw//4 + 2)
    win.refresh()

    while True:
        res = settings_menu(win)

        if res == 'back' or res is None:
            break
        elif res == 'enable_cheats':
            enable_cheats()
        elif res == 'disable_cheats':
            disable_cheats()
        else:
            pass

def settings_menu(parent_win):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    options = [
        {
            'id': 'back',
            'text': 'Back'
        }
    ]

    if os.path.exists('.cheats'):
        options.append({
            'id': 'disable_cheats',
            'text': 'Disable cheats'
        })
    else:
        options.append({
            'id': 'enable_cheats',
            'text': 'Enable cheats'
        })

    return mymovements.menu_loop(parent_win, options)