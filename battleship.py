from ship import Ship
import random
import curses

class Battleship:
    def __init__(self, stdscr, difficulty_level=0.1):
        self.stdscr = stdscr
        self.difficulty_level = difficulty_level
        self.num_ships = self.calculate_num_ships()
        self.points = self.calculate_points()

        self.ship_list = []
        self.cursor_x, self.cursor_y = 1, 1
        self.last_char = ' '


    def setup(self):
        curses.noecho()
        curses.curs_set(0)
        self.stdscr.clear()

        text = "BATALHA NAVAL"
        self.rows, self.columns = self.stdscr.getmaxyx()
        self.stdscr.addstr(0, (self.columns - len(text)) // 2, text)
        self.stdscr.refresh()

        self.win_height = self.rows - 2
        self.win_width = self.columns
        self.win = curses.newwin(self.win_height, self.win_width, 2, 0)
        self.win.border()
        self.win.keypad(True)
        curses.curs_set(1)

        self.generate_ships()


    def calculate_num_ships(self):
        rows, columns = self.stdscr.getmaxyx()
        max_ships = (rows - 2) * (columns - 2)
        return random.randint(5, int(max_ships * self.difficulty_level))


    def calculate_points(self):
        return random.randint(5, max(5, int(self.num_ships * self.difficulty_level)))
   

    def draw_ship(self, x, y):
        self.win.addstr(y, x, 'N')
        self.win.refresh()


    def generate_ships(self):
        for _ in range(self.num_ships):
            while True:
                x = random.randint(1, self.win_width - 2)
                y = random.randint(1, self.win_height-2)
                if not any(ship.position == (x, y) for ship in self.ship_list):
                    self.ship_list.append(Ship(x, y))
                    # self.draw_ship(x, y)
                    break


    def draw_status(self):
        self.stdscr.addstr(1, 0, " " * self.columns)

        ships_text = f"Navios: {self.num_ships}"
        self.stdscr.addstr(0, self.columns - len(ships_text) - 1, ships_text)

        points_text = f"Pontos: {self.points}"
        self.stdscr.addstr(1, self.columns - len(points_text) - 1, points_text)

        self.stdscr.refresh()


    def move_cursor(self, key):
        if key == curses.KEY_RIGHT and self.cursor_x < self.win_width - 2:
            self.cursor_x += 1
        elif key == curses.KEY_LEFT and self.cursor_x > 1:
            self.cursor_x -= 1
        elif key == curses.KEY_DOWN and self.cursor_y < self.win_height - 2:
            self.cursor_y += 1
        elif key == curses.KEY_UP and self.cursor_y > 1:
            self.cursor_y -= 1


    def fire(self):
        for ship in self.ship_list:
            if ship.hit_ship(self.cursor_x, self.cursor_y): 
                self.win.addstr(self.cursor_y, self.cursor_x, 'N') #🚢
                self.points += 1
                self.num_ships -= 1
                self.win.refresh() 
                return  
            
        if any(ship.position == (self.cursor_x, self.cursor_y) and ship.hit for ship in self.ship_list):
            return  

        self.win.addstr(self.cursor_y, self.cursor_x, '*') # 💥
        self.points -= 1
        self.win.refresh()  
       

    def play(self):
        self.setup()

        while True:
            self.draw_status()
            self.win.move(self.cursor_y, self.cursor_x)
            self.win.addstr(self.cursor_y, self.cursor_x, '█')
            self.win.refresh()

            key = self.win.getch()
            self.win.addstr(self.cursor_y, self.cursor_x, self.last_char)

            if key == ord('q') or self.points == 0 or self.num_ships == 0:
                break
            elif key == ord('\n'):
                self.fire()
            else:
                self.move_cursor(key)

            self.last_char = chr(self.win.inch(self.cursor_y, self.cursor_x) & 0xFF)