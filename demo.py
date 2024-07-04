#!/usr/bin/env python3

import os
import time
import random
import sys

def clear_screen(height=100):
    for i in range(height):
        print('\n')

def main(width, height):
    random.seed(time.time())

    horse_frames = ['','']
    horse_widths = [0,0]
    with open('assets/ascii_horse_1.txt') as f:
        horse_frames[0] = f.readlines()
        horse_widths[0] = max([len(line) for line in horse_frames[0]])
    with open('assets/ascii_horse_2.txt') as f:
        horse_frames[1] = f.readlines()
        horse_widths[1] = max([len(line) for line in horse_frames[1]])

    horse_max_width = max(horse_widths)
    offsets = [0,0,0,0]

    winner = -1
    iteration = 0

    while winner == -1:
        clear_screen(height)

        #if the file exists, read it and print it
        if os.path.exists('frame.txt'):
            with open('frame.txt','r') as f:
                print(f.read())
                time.sleep(0.1)
                os.remove('frame.txt')
                
        with open('frame.txt','a') as f:
            for i in range(4):
                for line in horse_frames[iteration % 2 if i % 2 == 0 else (iteration + 1) % 2]:
                    f.write(' '*offsets[i] + line)
                f.write('\n')            
                f.write('-'*width + '\n')

                offsets[i] += random.randint(0,3)
                if offsets[i] > width - horse_max_width:
                    print('Horse', i+1, 'wins!')
                    winner = i
                    offsets[i] = width - horse_max_width
            iteration += 1

    if winner != -1 and os.path.exists('frame.txt'):
        with open('frame.txt','r') as f:
            os.remove('frame.txt')
                
            
if __name__ == '__main__':
    print('Press Ctrl-C to quit.')
    width = os.get_terminal_size().columns
    print('Terminal width:', width)
    
    height = os.get_terminal_size().lines
    print('Terminal height:', height)

    time.sleep(2)
    main(width, height)