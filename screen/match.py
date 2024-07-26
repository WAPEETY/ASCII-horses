import curses
import os
import horse
import random
import time

def random_num(min, max):
    rnd = random.SystemRandom()
    return rnd.choice(range(min, max))

def play(parent_win, horses, bet, cheats):
    sh, sw = parent_win.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.box()
    win.addstr(0, 2, ' Match ')
    win.refresh()
    horse_frames = []
    killed_horse_frames = []

    for file in os.listdir('assets/horses'):
        if file.endswith('.txt'):
            with open('assets/horses/' + file, 'r') as f:
                horse_frames.append(f.readlines())
    
    for file in os.listdir('assets/dead_horses'):
        if file.endswith('.txt'):
            with open('assets/dead_horses/' + file, 'r') as f:
                killed_horse_frames.append(f.readlines())

    horse_height = horse.calculate_horse_height(horse_frames)
    horse_width = horse.calculate_horse_width(horse_frames)
    dead_horse_height = horse.calculate_horse_height(killed_horse_frames)

    if horses == 0:
        horses = horse.max_horses(sh - 2, horse_height)

    if bet == 0:
        #bet = random_num(1, horses)
        bet = -1

    win.addstr(2, 2, 'Starting match with ' + str(horses) + ' horses')
    win.addstr(3, 2, 'Bet has been placed on horse ' + str(bet))
    win.refresh()
    time.sleep(2)

    horse_win = []
    for i in range(horses):
        horse_win.append(curses.newwin(horse_height + 2, sw-4, 2 + i*(horse_height + 2), 2))

    print_arrival(win,sw,sh)

    ranking = []
    offset = [0] * horses
    round = 0
    key = -1
    killed_horses = []
    cheats = True if os.path.exists('.cheats') else False

    win.nodelay(True)

    while len(ranking) + len(killed_horses) < horses:
        key = win.getch()
        for i in range(horses):
            if(i in ranking or i in killed_horses):
                continue
            else:
                horse.print_horse_in_game(horse_win[i],i,round,horse_height,horse_frames,offset[i], (key == 32 and bet-1==i))
                print_arrival(win,sw,sh)

                offset[i] = offset[i] + random_num(0,3)

                if(key == 107 and cheats):
                    
                    alive_and_running = list(range(horses))

                    for r in ranking:
                        alive_and_running.remove(r)
                    for k in killed_horses:
                        alive_and_running.remove(k)

                    kill = random.choice(alive_and_running)
                    
                    killed_horses.append(kill)
                    horse.print_killed_horse(horse_win[kill],kill,round,dead_horse_height,killed_horse_frames,offset[kill])
                    print_arrival(win,sw,sh)
                    key = -1
                    continue

                if(key == 32 and bet-1 == i and i not in killed_horses):
                    offset[i] = offset[i] + random_num(0,1)
            
                if(offset[i] >= sw-4 - horse_width):
                
                    offset[i] = sw-4 - horse_width
                    if(i not in ranking):
                        ranking.append(i)

        time.sleep(.1)
        round+=1

    print_ranking(parent_win, ranking, bet)

def print_arrival(win, sw,sh):
    for i in range(sh-1):
        if i % 2 == 0:
            win.addstr(i, sw-2, '█')
            win.addstr(i, sw-1, '█')
            win.addstr(i, sw-3, ' ')
            win.addstr(i, sw-4, ' ')
        else:
            win.addstr(i, sw-2, ' ')
            win.addstr(i, sw-1, ' ')
            win.addstr(i, sw-3, '█')
            win.addstr(i, sw-4, '█')
    win.refresh()

def print_ranking(parent_win, ranking, bet):
    parent_win.clear()
    parent_win.refresh()

    sh, sw = parent_win.getmaxyx()
    rows = len(ranking)

    win = curses.newwin(rows + 3, 40, sh//2 - rows//2 + 1, sw//2 - 20)
    i = 0

    for i, r in enumerate(ranking):
        if r+1 == bet:
            win.attron(curses.color_pair(1))
            win.addstr(i, 2,  str(i+1) + '. Horse ' + str(r+1) + ' <- Bet')
            win.attroff(curses.color_pair(1))
        else:
            win.addstr(i, 2,  str(i+1) + '. Horse ' + str(r+1))

    win.attron(curses.color_pair(1))
    win.addstr(i+2, 2, "<- Press backspace to continue")
    win.attroff(curses.color_pair(1))
    win.refresh()

    key = 0
    while key != 127:
        key = win.getch()

    win.clear()
    win.refresh()

def quick(win):
    play(win, 0, 0, False)