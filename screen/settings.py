import curses
import os

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

        if res == 'back':
            break
        elif res == 'enable_cheats':
            enable_cheats()
        elif res == 'disable_cheats':
            disable_cheats()
        else:
            pass

def settings_menu(parent_win):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    sh, sw = parent_win.getmaxyx()
    win = curses.newwin(5, 40, sh//2 - 2, sw//2 - 20)

    key = 0
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

    current_option = 0

    win.keypad(True)
    win.refresh()

    while True:
        win.clear()
        win.refresh()

        if key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(options)
        elif key == curses.KEY_UP:
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            win.clear()
            win.refresh()
            return options[current_option]['id']

        for i, option in enumerate(options):
            if i == current_option:
                win.attron(curses.color_pair(1))
                win.addstr(i+1, 2, '-> ' + option['text'])
                win.attroff(curses.color_pair(1))
            else:
                win.addstr(i+1, 2, option['text'])
        win.refresh()
        key = win.getch()