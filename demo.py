#!/usr/bin/env python3

import os
import time
import secrets
import sys
import re
import hashlib

def my_random():
    return secrets.randbelow(4) # Non vorrai mica che Gaspare preveda chi vince!

def clear_screen(height=100):
    for i in range(height):
        print('\n')

def max_horses(height, horse_height):
    height -= 2
    return height // (horse_height + 1)

def calculate_horse_height(horse_frames):
    return max([len(frame) for frame in horse_frames])

def delete_file(path):
    if os.path.exists(path):
        with open(path,'r') as f:
            os.remove(path)

def print_and_remove_frame(frame):
    if os.path.exists(frame):
        with open(frame,'r') as f:
            print(f.read())
            time.sleep(0.1)
            os.remove(frame)

def generate_race(num_horses, horse_max_width, offsets, t_width, my_random_values):

    winner = -1

    for i in range(num_horses):
        my_random_values.append(my_random())
        offsets[i] += my_random_values[-1]
        if offsets[i] > t_width - horse_max_width:
            offsets[i] = t_width - horse_max_width
            winner = 1

    if winner == 1:
        return my_random_values

    return generate_race(num_horses, horse_max_width, offsets, t_width, my_random_values)

def create_frame_file(frame_file, iteration, num_horses, horse_frames, horse_max_width, offsets, t_width, my_random_values):
    winner = -1
    with open(frame_file,'a') as f:
        for i in range(num_horses):
            for line in horse_frames[iteration % 2 if i % 2 == 0 else (iteration + 1) % 2]:
                
                n_horse = i+1
                if n_horse < 10:
                    line = line.replace('x', str(n_horse))
                    line = line.replace('y', ' ')
                else:
                    line = line.replace('x', str(n_horse % 10))
                    line = line.replace('y', str(n_horse // 10))
                
                f.write(' '*offsets[i] + line)
                    
            f.write('\n')            
            f.write('-'*t_width + '\n')

            offsets[i] += my_random_values.pop(0)

            if offsets[i] > t_width - horse_max_width:
                print('Horse', i+1, 'wins!')
                winner = i
                offsets[i] = t_width - horse_max_width
                
        iteration += 1

    return iteration, winner, offsets

def main(t_width, t_height, num_horses, frame_file):
    horse_frames = ['','']
    horse_widths = [0,0]
    with open('assets/ascii_horse_1.txt') as f:
        horse_frames[0] = f.readlines()
        horse_widths[0] = max([len(line) for line in horse_frames[0]])
    with open('assets/ascii_horse_2.txt') as f:
        horse_frames[1] = f.readlines()
        horse_widths[1] = max([len(line) for line in horse_frames[1]])

    horse_max_width = max(horse_widths)
    offsets = [0] * num_horses

    winner = -1
    iteration = 0

    my_random_values = []
    my_random_values = generate_race(num_horses, horse_max_width, offsets, t_width, my_random_values)

    secret = secrets.randbelow(100_000_000 - 10_000_000) + 10_000_000

    my_random_values_str = ''.join(str(random_value) for random_value in my_random_values)

    print(f"sha256 value: {hashlib.sha256((str(secret)+my_random_values_str).encode()).hexdigest()}")

    offsets = [0] * num_horses
    input("Waiting for bets. . .")
    
    while winner == -1:
        clear_screen(t_height)
        print_and_remove_frame(frame_file)   
        iteration, winner, offsets = create_frame_file(frame_file, iteration, num_horses, horse_frames, horse_max_width, offsets, t_width, my_random_values)

    print(f"secret: {secret}")
    print(f"random values: {my_random_values_str}")

    delete_file(frame_file)

def print_help():
    print('Usage: python3 demo.py [OPTIONS]')
    print('Options:')
    print('  --help: Display this help message.')
    print('  --version: Display the version of the program.')
    print('  --number [NUMBER]: Set the number of horses in the race, IMPORTANT: this does not guarantee that all horses will be displayed.')

def print_version():
    print('Version 1.2.0')

if __name__ == '__main__':

    if os.geteuid() == 0:
        print('Do not run this program as root !!!')
        sys.exit(1)

    if '--help' in sys.argv:
        print_help()
        sys.exit(0)

    if '--version' in sys.argv:
        print_version()
        sys.exit(0)

    if '--number' in sys.argv:
        try:
            num_horses = int(sys.argv[sys.argv.index('--number') + 1])
            if num_horses < 1 or num_horses > 99:
                raise ValueError
        except:
            print('Invalid number of horses.')
            sys.exit(1)
    else:
        num_horses = 4

    if '--file' in sys.argv:
        try:
            path = sys.argv[sys.argv.index('--file') + 1]
            regex = re.compile(r'^[a-zA-Z0-9_./]+$')

            if not regex.match(path):
                raise ValueError
            if os.path.exists(path):
                raise FileExistsError
        except:
            print('Invalid file path.')
            sys.exit(1)
    else:
        path = 'frame.txt'

    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines

    print('Press Ctrl-C to quit.')
    print('Terminal width:', width)
    print('Terminal height:', height)

    time.sleep(2)
    main(width, height, num_horses, path)
