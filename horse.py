import random

def calculate_horse_width(horse_frames):
    return max(max(len(row) for row in frame) for frame in horse_frames)

def calculate_horse_height(horse_frames):
    return max([len(frame) for frame in horse_frames])

def max_horses(sh, hh):
    wh_for_horse = hh+2
    return sh // wh_for_horse

def generate_boost(s):
    return ''.join(['=' if random.randint(0,1) == 1 else ' ' for i in range(s)])

def print_horse_in_game(win,i,round,hh,horse_frames,offset,boosted):
    sh, sw = win.getmaxyx()
    win.clear()
    
    for j in range(hh):
        
        row = horse_frames[(round + i) % 2][j][:-1]
        n_horse = i+1
        if n_horse < 10:
            row = row.replace('x', str(n_horse))
            row = row.replace('y', ' ')
        else:
            row = row.replace('x', str(n_horse % 10))
            row = row.replace('y', str(n_horse // 10))
        if boosted:
            slen = 5
            start = offset-slen
            if start < 0:
                slen = slen + start
                start = 0
            boost_str = generate_boost(slen)

        win.addstr(j,offset, row)
        if boosted:
            win.addstr(j,start,boost_str)
        win.addstr(6, 0, '-'*(sw-4))
    win.refresh()

def print_killed_horse(win,i,round,hh,horse_frames,offset):
    sh, sw = win.getmaxyx()
    win.clear()
    
    for j in range(hh):
        
        row = horse_frames[0][j][:-1]
        n_horse = i+1
        if n_horse < 10:
            row = row.replace('x', str(n_horse))
            row = row.replace('y', ' ')
        else:
            row = row.replace('x', str(n_horse % 10))
            row = row.replace('y', str(n_horse // 10))
        win.addstr(j,offset, row)
        win.addstr(6, 0, '-'*(sw-4))
    win.refresh()