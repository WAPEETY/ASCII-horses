import sys
import time

def exit(win):
    win.addstr(2, 4, 'Goodbye!')
    win.refresh()
    time.sleep(2)
    sys.exit(0)
