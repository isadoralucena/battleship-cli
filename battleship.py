import curses
from curses import wrapper
import random


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.noecho()
    curses.curs_set(0)

    stdscr.clear()

    text = "BATALHA NAVAL"
    rows, columns = stdscr.getmaxyx()
    stdscr.addstr(0, (columns - len(text)) // 2, text)

    stdscr.refresh()

    win_height = rows - 2 
    win_width = columns 
    win = curses.newwin(win_height, win_width, 2,0)  
    win.border()
    
    win.keypad(True)
    curses.curs_set(1)

    difficulty_level = 10/100 

    max_ships = (win_height - 2) * (win_width - 2)
    num_ships = random.randint(5, int(max_ships * difficulty_level)) 

    points = random.randint(5, max(5, int(num_ships * difficulty_level))) 

    ship_positions = []

    for _ in range(num_ships):
        while True:
            x = random.randint(1, win_width - 2) 
            y = random.randint(3, win_height) 
            if (x, y) not in ship_positions:  
                ship_positions.append((x, y))
                break
 
    cursor_x, cursor_y = 1, 1 
    last_char = ' '
    while True:
        text = f"Pontos: {points}"
        stdscr.addstr(0, columns - len(text) - 1, text)
        
        text = f"Navios: {num_ships}"
        stdscr.addstr(1, columns - len(text) - 1, text)    
        stdscr.refresh()

        win.move(cursor_y, cursor_x)  
        win.addstr(cursor_y, cursor_x, '█') 
        win.refresh()

        key = win.getch() 

        win.addstr(cursor_y, cursor_x, last_char) 

        if key == curses.KEY_RIGHT and cursor_x < win_width - 2:
            cursor_x += 1
        elif key == curses.KEY_LEFT and cursor_x > 1:
            cursor_x -= 1
        elif key == curses.KEY_DOWN and cursor_y < win_height - 2:
            cursor_y += 1
        elif key == curses.KEY_UP and cursor_y > 1:
            cursor_y -= 1
        elif key == ord('q') or points == 0 or num_ships == 0:
            break
        elif key == ord('\n'):  
            if (cursor_x, cursor_y) in ship_positions:
                win.addstr(cursor_y, cursor_x, 'N') #🚢
                points += 1 
                num_ships -= 1
            else:
                win.addstr(cursor_y, cursor_x, '*') #💥
                points -= 1
            win.refresh()

        last_char = chr(win.inch(cursor_y, cursor_x) & 0xFF)


wrapper(main)
