import curses

from screen import exit

SELECTED_PROMPT = '-> '

def menu_loop(parent_win, options, current_option = 0, is_main_menu = False, create_window = True, longest_option_length = None):
    if longest_option_length is None:
        longest_option_length = max(len(option['text']) for option in options)

    if create_window:
        sh, sw = parent_win.getmaxyx()
        win = curses.newwin(len(options)+1,  # +1 because otherwise it would crash in settings.py, idk
                            longest_option_length + len(SELECTED_PROMPT),
                            sh//2 - len(options)//2,
                            sw//2 - longest_option_length//2)

        win.refresh()
        win.move(0, 0)
        win.keypad(True)
    else:
        win = parent_win

    key = 0
    while True:
        win.clear()
        win.refresh()

        if key == curses.KEY_DOWN or key == ord('j'):
            current_option = (current_option + 1) % len(options)
        elif key == curses.KEY_UP or key == ord('k'):
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13] or key == ord('l'):
            win.clear()
            win.refresh()
            return options[current_option]['id']

        if is_main_menu:
            if key == ord('q'):
                return None
        else:
            if check_go_back(key):
                return None

        for i, option in enumerate(options):
            if i == current_option:
                win.attron(curses.color_pair(1))
                win.addstr(i, 0, SELECTED_PROMPT + option['text'])
                win.attroff(curses.color_pair(1))
            else:
                win.addstr(i, 0, option['text'])
        win.refresh()
        key = win.getch()

GO_BACK_DIALOG = '<- Press backspace or h to continue'

def check_go_back(key):
    return key == ord('h') or key == curses.KEY_BACKSPACE or key == 127
