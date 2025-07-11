import curses

def config_step(parent_win):
    sh, sw = parent_win.getmaxyx()
    win = curses.newwin(sh//2 - 4, sw//2 - 4, sh//2 - sh//4 + 2, sw//2 - sw//4 + 2)

    win.addstr(0, 2, "Game Configuration", curses.A_BOLD)

    win.addstr(2, 2, "Number of horses: ")
    win.addstr(3, 2, "Bet amount: ")

    win.refresh()

    curses.echo()
    win.keypad(True)
    curses.curs_set(1)

    win.move(2, 20)
    horses = int(win.getstr().decode())
    win.move(3, 14)
    bet = int(win.getstr().decode())

    curses.curs_set(0)
    win.keypad(False)
    curses.noecho()

    return (horses, bet)