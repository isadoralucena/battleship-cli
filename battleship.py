from ship import Ship
from display import Display
import random
import curses
import sys
import time

class Battleship:
    def __init__(self, stdscr, selected_option = 0, difficulty_index = 1):
        self.stdscr = stdscr
        self.display = Display(stdscr)

        self.difficulty_map = {
            0: 0.40,
            1: 0.05
        }

        self.difficulty_percentage = self.difficulty_map[difficulty_index]

        self.num_ships = 0
        self.chances = 0

        self.intermediate_character_of_ship = "N"
        self.explosion_character = "*"
        self.ship_size_and_appearance = {
            1: "S",
            2: "D",
            3: "C",
            4: "P"
        }

        self.menu_options = ["Jogar", "Configurações", "Sair"]
        self.selected_option = selected_option
        self.difficulty_levels = ["Fácil", "Difícil"]
        self.difficulty_index = difficulty_index 

        self.ship_list = []
        self.cursor_x, self.cursor_y = 1, 1
        self.last_char = ' '


    def setup(self):
        curses.noecho()
        curses.curs_set(0)
        self.stdscr.clear()

        self.display.display_setup()

        self.win_height = self.rows//2
        self.win_width = self.columns//3

        start_y = (self.rows - self.win_height) // 2
        start_x = (self.columns - self.win_width) // 2

        self.win = curses.newwin(self.win_height, self.win_width, start_y, start_x)
        self.win.border()
        self.win.keypad(True)
        curses.curs_set(1)

        self.num_ships = self.calculate_num_ships()
        self.chances = self.calculate_chances()
        self.generate_ships()


    def animate(self):
        curses.curs_set(0)

        self.stdscr.nodelay(True)

        flash_on = True
        flash_delay = 0.5
        last_flash_time = time.time()

        intro_duration = 3
        intro_start_time = time.time()

        while True:
            self.stdscr.clear()

            self.display.intro(flash_on)

            self.stdscr.refresh()

            if time.time() - last_flash_time > flash_delay:
                flash_on = not flash_on
                last_flash_time = time.time()

            key = self.stdscr.getch()
            if key != -1 or (time.time() - intro_start_time > intro_duration):
                self.stdscr.nodelay(False)
                break

            time.sleep(0.1)


    def calculate_num_ships(self):
        rows, columns = self.stdscr.getmaxyx()
        max_ships = (rows//2) * (columns//2)
        return random.randint(int(self.difficulty_percentage * 100), int(max_ships * self.difficulty_percentage))


    def calculate_chances(self):
        return random.randint(5, max(10, int(self.num_ships * self.difficulty_percentage)))


    def generate_ships(self):
        for _ in range(self.num_ships):
            while True:
                ship_size = random.choice([1, 2, 3, 4])
                orientation = random.choice(["horizontal", "vertical"])

                x = random.randint(1, self.win_width - 2 - (ship_size if orientation == "horizontal" else 0))
                y = random.randint(1, self.win_height - 2 - (ship_size if orientation == "vertical" else 0))

                new_ship_positions = [(x + i, y) if orientation == "horizontal" else (x, y + i) for i in range(ship_size)]

                if not any(set(new_ship_positions) & set(ship.positions) for ship in self.ship_list):
                    new_ship = Ship(new_ship_positions)
                    self.ship_list.append(new_ship)
                    break


    def move_cursor(self, key):
        if key == curses.KEY_RIGHT and self.cursor_x < self.win_width - 2:
            self.cursor_x += 1
        elif key == curses.KEY_LEFT and self.cursor_x > 1:
            self.cursor_x -= 1
        elif key == curses.KEY_DOWN and self.cursor_y < self.win_height - 2:
            self.cursor_y += 1
        elif key == curses.KEY_UP and self.cursor_y > 1:
            self.cursor_y -= 1

    def end_game(self):
        title = "NÃO FOI DESSA VEZ..." if self.chances == 0 else "PARABÉNS!!! VOCÊ GANHOU"
        options = ["Jogar de novo", "Sair"]
        selected_option = 0

        while True:
            self.display.display_menu(title, options, selected_option) 

            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(options)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if selected_option == 0:
                    self.play()
                elif selected_option == 1:
                    sys.exit(0)

    def settings(self):
        while True:
            self.display.display_settings(self.difficulty_levels, self.difficulty_index, self.difficulty_map, self.difficulty_percentage)  
            
            key = self.stdscr.getch()  
            if key == ord('d'):  
                self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulty_levels)
                self.difficulty_percentage = self.difficulty_map[self.difficulty_index]
            else:  
                break


    def menu(self):
        while True:
            self.display.display_menu("MENU INICIAL", self.menu_options, self.selected_option) 

            key = self.stdscr.getch()

            if key == curses.KEY_UP: 
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif key == curses.KEY_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif key in [curses.KEY_ENTER, 10, 13]:  
                if self.selected_option == 0: 
                    break
                elif self.selected_option == 1: 
                    self.settings()
                elif self.selected_option == 2:  
                    sys.exit(0)
            elif key == ord('q'):
                sys.exit(0)


    def fire(self):
        for ship in self.ship_list:
            if ship.register_hit(self.cursor_x, self.cursor_y):
                if ship.hit:
                    appearance = self.ship_size_and_appearance[len(ship.positions)]
                    for (x, y) in ship.positions:
                        self.win.addstr(y, x, appearance)
                    self.num_ships -= 1
                else:
                    self.win.addstr(self.cursor_y, self.cursor_x, self.intermediate_character_of_ship)
                self.chances += 1
                self.win.refresh() 
                return  

        if any((self.cursor_x, self.cursor_y) in ship.positions and ship.register_hit for ship in self.ship_list):
            return  

        self.win.addstr(self.cursor_y, self.cursor_x, self.explosion_character)
        self.chances -= 1
        self.win.refresh()  


    def play(self):
        min_height = len(self.display.title) + 9
        min_width = max(len(line) for line in self.display.title)

        self.rows, self.columns = self.stdscr.getmaxyx()

        if self.rows < min_height or self.columns < min_width:
            self.stdscr.clear()
            message1 = "Tela muito pequena!"
            central_y1 = self.rows // 2
            central_x1 = (self.columns - len(message1)) // 2
            self.stdscr.addstr(central_y1, central_x1, message1)

            message2 = "Aumente a janela."
            central_y2 = self.rows // 2 + 1
            central_x2 = (self.columns - len(message2)) // 2
            self.stdscr.addstr(central_y2, central_x2, message2)
            self.stdscr.refresh()
            self.stdscr.getch()
            sys.exit(0)

        self.animate()
        self.menu()
        self.setup()

        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        while True:
            self.display.display_status(self.num_ships, self.chances)
            self.display.display_ship_legend()
            self.win.move(self.cursor_y, self.cursor_x)
            self.win.addstr(self.cursor_y, self.cursor_x, '█')
            self.win.refresh()

            key = self.win.getch()
            self.win.addstr(self.cursor_y, self.cursor_x, self.last_char)

            if key == ord('q'):
                break
            elif self.chances == 0 or self.num_ships == 0:
                self.end_game()
            elif key == ord('\n'):
                self.fire()
            else:
                self.move_cursor(key)

            self.last_char = chr(self.win.inch(self.cursor_y, self.cursor_x) & 0xFF)
