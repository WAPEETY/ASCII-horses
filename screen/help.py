import curses

import mymovements

def help(parent_win):
    sh, sw = parent_win.getmaxyx()
    win = curses.newwin(sh//2 - 4, sw//2 - 4, sh//2 - sh//4 + 2, sw//2 - sw//4 + 2)

    help_text =     ('This is a simple implementation of the famous virtual horses bet game,'
                    'you can bet on your favourite horse and even help it to win by spamming the space key. \n\n' 
                    'With cheats enabled (in settings) you can also have, once in a game, the chance to stop'
                    ' a random horse by clicking letter K but mind the fact that it could also be yours. \n\n'
                    'This software is released under the Gnu Public License v3 \n' 
                    'with it you should have recieved a copy of it, if not please take it from here: \n'
                    'https://www.gnu.org/licenses/gpl-3.0.html')

    win.refresh()
    win.addstr(0,0,help_text)

    win.refresh()

    win.attron(curses.color_pair(1))
    win.addstr(sh//2 - sh//4 ,0,"<- Back")
    win.attroff(curses.color_pair(1))
    
    while True:
        key = win.getch()
        if mymovements.check_go_back(key):
            break
    
    win.clear()
    win.refresh()