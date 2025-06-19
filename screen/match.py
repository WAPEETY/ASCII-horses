import curses
import os
import horse
import time
import myrandom
import math

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

                offset[i] = offset[i] + myrandom.use(0,3)

                if(key == 107 and cheats):
                    
                    alive_and_running = list(range(horses))

                    for r in ranking:
                        alive_and_running.remove(r)
                    for k in killed_horses:
                        alive_and_running.remove(k)

                    kill = myrandom.choice(alive_and_running)
                    
                    killed_horses.append(kill)
                    horse.print_killed_horse(horse_win[kill],kill,round,dead_horse_height,killed_horse_frames,offset[kill])
                    print_arrival(win,sw,sh)
                    key = -1
                    continue

                if(key == 32 and bet-1 == i and i not in killed_horses):
                    offset[i] = offset[i] + myrandom.use(0,1)
            
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

def print_ranking(parent_win: curses.window, ranking: list[int], bet: int):
    parent_win.clear()
    parent_win.refresh()

    sh, sw = parent_win.getmaxyx()

    board_top_coord = 3
    board_size = sh - board_top_coord*2 # rows in a scoreboard
    n_boards = math.ceil(len(ranking) / board_size)

    board_widths: list[int] = [] # to space the boards neatly we need to know where to start horizontally, and for that we need to know how wide they all are
    for board_idx in range(n_boards):
        # we want to make the scoreboard as narrow as possible to fit as many scoreboards as we can on the screen,
        # so we have to know the longest text we'll write on it; this depends on the horse rankings, if the horse we bet on is in this board,
        # and if it's the last board (press backspace to blablabla)

        ranks = ranking[board_size * board_idx : board_size * (board_idx + 1)]
        max_horse = board_size * board_idx + ranks.index(max(ranks)) # index of ranking[] for the horse with the highest rank in this board
        is_last = board_idx == n_boards - 1

        try:
            bet_idx = board_size * board_idx + ranks.index(bet - 1) # the rankings are 0-relative and the bet is 1-relative. like max_horse, this is an index for ranking[]
        except:
            bet_idx = -1
        
        max_horse_width = len(f"{ranking[max_horse] + 1}. Horse {max_horse + 1}")
        bet_width = 0 if bet_idx == -1 else len(f"{bet_idx + 1}. Horse {bet} <- Bet")
        last_width = 0 if not is_last else len("<- Press backspace to continue")
        board_width = max(max_horse_width, bet_width, last_width) + 5
        board_widths.append(board_width)
    
    """
    initially the x coordinate of the first board, then slides to the right each time
    with too many horses this might become negative, so we just set a minimum value, and that means that we won't be able to show all of the scoreboards
    """
    current_x_coord = max((sw - sum(board_widths)) // 2, 5)
    windows: list[curses.window] = []

    # create all of the windows from left to right
    for board_idx in range(n_boards):
        window = curses.newwin(board_size, board_widths[board_idx], board_top_coord, current_x_coord)
        current_x_coord += board_widths[board_idx]
        windows.append(window)
    
    rank_len = len(str(len(ranking)))
    for i, rank in enumerate(ranking):
        window = windows[i // board_size]
        row = i % board_size

        text = str(i + 1).rjust(rank_len) + f". Horse {rank + 1}"
        if rank + 1 == bet:
            window.attron(curses.color_pair(1))
            text += " <- Bet"
        
        window.addstr(row, 0, text)
        window.attroff(curses.color_pair(1))
    
    windows[-1].attron(curses.color_pair(1))
    windows[-1].addstr(len(ranking) % board_size, 0, "<- Press backspace to continue")
    windows[-1].attroff(curses.color_pair(1))
    
    for window in windows:
        window.refresh()
    
    while parent_win.getch() != 127: # wait for backspace
        pass

    for window in windows:
        window.clear()
        window.refresh()

def quick(win):
    play(win, 0, 0, False)