import curses
import os
import myrandom
import time
import horse

def display(parent_win):
    sh, sw = parent_win.getmaxyx()

    win = curses.newwin(sh, sw, 0, 0)

    win.addstr(0, 0, "Why just one?")
    win.refresh()

    for i in range(1, 5):
        win.addstr(1,0, str(5 - i) + "...")
        win.refresh()
        time.sleep(1)

    win.addstr(2, 0, "BOOM!")
    win.refresh()

    #open all the files in assets/horses
    frames = []

    for file in os.listdir("assets/horses"):
        with open("assets/horses/" + file, "r") as f:
            frames.append(f.readlines())

    max_height = horse.calculate_horse_height(frames)
    max_width = horse.calculate_horse_width(frames)

    while True:
        for frame in frames:
            #start printing the frame in random places but not outside the screen
            y = random.randint(0, sh - max_height -1)
            x = random.randint(0, sw - max_width -1)

            #remove newlines from the frame
            frame = [line[:-1] for line in frame]

            for i, line in enumerate(frame):
                win.addstr(y + i, x, line)
                win.refresh()
                time.sleep(0.01)