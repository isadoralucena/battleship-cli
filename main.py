import curses
from battleship import Battleship

def main(stdscr):
    game = Battleship(stdscr)
    game.play()

curses.wrapper(main)
