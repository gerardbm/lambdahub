#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------
# Name    : Multiplications game
# Version : 3.0.0
# Python  : 3.8.0
# License : MIT
# Author  : Gerard Bajona
# Created : 2025/06/01
# Changed : 2025/06/08
# URL     : http://github.com/gerardbm/lambdahub
# --------------------------------------------------
"""Multiplications game for the command line."""

import argparse
import random
import datetime
import time
from pathlib import Path

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
            description="Multiplications game for the command line.")
    parser.add_argument('-a',
            type=positive_digit,
            default=1,
            metavar='Int',
            help="Digits for the 1st operand (1 ≤ A ≤ 4; default = 1)")
    parser.add_argument('-b',
            type=positive_digit,
            default=1,
            metavar='Int',
            help="Digits for the 2nd operand (1 ≤ B ≤ 4; default = 1)")
    parser.add_argument('-r',
            type=int,
            default=10,
            metavar='Int',
            help="Number of rounds to play (default = 10)")
    parser.add_argument('-s',
            action='store_true',
            help="Save the scores if all answers are correct")
    parser.add_argument('-l',
            action='store_true',
            help="Show a list with the previous scores and exit")
    parser.add_argument('-c',
            action='store_true',
            help="Clear the previous saved scores and exit")
    return parser.parse_args()

def positive_digit(digit):
    """Allow only digits between 1 and 4."""
    int_digit = int(digit)
    if int_digit < 1 or int_digit > 4:
        raise argparse.ArgumentTypeError("Digits must be between 1 and 4.")
    return int_digit

def letsplay(digits_a, digits_b, rounds, save):
    """Start the game and show the score at the end."""
    score = 0
    count = 0

    print()
    print("Game starts. Play!")

    start = time.time()
    while count < rounds:
        count += 1
        score = operation(score, count, digits_a, digits_b)
    end = time.time()

    rights = score
    wrongs = rounds-score
    percent = round((score/rounds)*100, 0)
    emoticon = emoticons(percent)
    color = colorize(percent)
    clean = '\033[0m'
    interval = end-start

    if rights == rounds and save:
        savetocsv(interval, rounds, f"{digits_a}×{digits_b}")

    print()
    print(color + '>', str(percent) + "%", emoticon + clean)
    print()
    print("> Rights:", rights)
    print("> Wrongs:", wrongs)
    print()
    print('> Time:', round(interval, 2), 'sec')
    print('> Rate:', round((interval)/rounds, 2), 'sec/question')

def generate_operand(digits):
    """Generate a random number with a given number of digits."""
    min_val = 10 ** (digits - 1)
    max_val = (10 ** digits) - 1
    return random.randint(min_val, max_val)

def operation(score, count, digits_a, digits_b):
    """Do a question and check the answer."""
    numb1 = generate_operand(digits_a)
    numb2 = generate_operand(digits_b)

    result = numb1 * numb2
    problem = str(numb1) + "x" + str(numb2)
    enum = str(count).zfill(2)
    question = enum + ". The result of " + problem + " = "

    while True:
        print()
        answer = input(question)
        try:
            answer = int(answer)
            break
        except ValueError:
            print('\033[33m--- It must be an integer number.\033[0m')

    if answer == result:
        print('\033[32m' + "--- Good!" + '\033[0m')
        score += 1
    else:
        print('\033[31m' + "--- Wrong!" + '\033[0m')
    return score

def emoticons(percent):
    """Display an emoticon face according to the result."""
    if percent == 100:
        emoticon = ':-)'
    elif percent >= 50 < 100:
        emoticon = ':-|'
    elif percent >= 20 < 50:
        emoticon = ':-('
    else:
        emoticon = ':_('
    return emoticon

def colorize(percent):
    """Colorize the result"""
    if percent == 100:
        color = '\033[32m'
    elif percent >= 50 < 100:
        color = '\033[36m'
    elif percent >= 20 < 50:
        color = '\033[33m'
    else:
        color = '\033[31m'
    return color

def savetocsv(interval, rounds, level):
    """Save the result in a CSV file"""
    scores = Path.home() / '.multiplications_scores.csv'
    now = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"))
    lvl = f"{level} digits"
    rnd = f"{rounds} rounds"
    sec = f"{round(interval, 2):.2f} sec"
    rpq = f"{round(interval/rounds, 2):.2f} sec/round"
    reg = f"{now}, {lvl}, {rnd}, {sec}, {rpq}\n"
    with open(scores, 'a+', encoding='utf8') as file_handle:
        file_handle.write(reg)

def show_scores():
    """Show saved scores from file."""
    scores = Path.home() / '.multiplications_scores.csv'
    if scores.exists():
        print("\nMultiplications scores:")
        print("-----------------------")
        with open(scores, 'r', encoding='utf8') as file:
            print(file.read(), end='')
    else:
        print("No scores recorded yet.")

def main():
    """Main program."""
    args = parse_arguments()

    if args.l:
        show_scores()
        return

    if args.c:
        scores = Path.home() / '.multiplications_scores.csv'
        if scores.exists():
            scores.unlink()
            print("Scores file deleted.")
        else:
            print("No scores file found to delete.")
        return

    letsplay(args.a, args.b, args.r, args.s)

if __name__ == '__main__':
    main()
