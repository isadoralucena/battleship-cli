from ship import Ship
import random
import curses
import sys
from pprint import pprint

class Battleship:
    def __init__(self, stdscr, selected_option = 0, difficulty_index = 1, use_emoji=False):
        self.stdscr = stdscr

        self.difficulty_map = {
            0: 0.40,
            1: 0.01 
        }
        self.difficulty_percentage = self.difficulty_map[difficulty_index]

        self.num_ships = 0
        self.chances = 0

        self.use_emoji = use_emoji
        self.intermediate_character_of_ship = "🚢" if self.use_emoji else "N"
        self.explosion_character = "💥" if self.use_emoji else "*"
        self.ship_size_and_appearance = {
            1: ("S", "🟦"),
            2: ("D", "🟪"),
            3: ("C", "🟨"),
            4: ("P", "🟩")
        }

        self.menu_options = ["Jogar", "Configurações", "Sair"]
        self.selected_option = selected_option
        self.difficulty_levels = ["Fácil", "Difícil"]
        self.difficulty_index = difficulty_index 
        self.title = [
            "██████╗  █████╗ ████████╗ █████╗ ██╗     ██╗  ██╗ █████╗     ███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗     ",
            "██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║     ██║  ██║██╔══██╗    ████╗  ██║██╔══██╗██║   ██║██╔══██╗██║     ",
            "██████╔╝███████║   ██║   ███████║██║     ███████║███████║    ██╔██╗ ██║███████║██║   ██║███████║██║     ",
            "██╔══██╗██╔══██║   ██║   ██╔══██║██║     ██╔══██║██╔══██║    ██║╚██╗██║██╔══██║╚██╗ ██╔╝██╔══██║██║     ",
            "██████╔╝██║  ██║   ██║   ██║  ██║███████╗██║  ██║██║  ██║    ██║ ╚████║██║  ██║ ╚████╔╝ ██║  ██║███████╗",
            "╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝"
        ]

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

        self.num_ships = self.calculate_num_ships()
        self.chances = self.calculate_chances()
        self.generate_ships()


    def calculate_num_ships(self):
        rows, columns = self.stdscr.getmaxyx()
        max_ships = (rows//2) * (columns//2)
        return random.randint(int(self.difficulty_percentage * 100), int(max_ships * self.difficulty_percentage))


    def calculate_chances(self):
        return random.randint(5, max(10, int(self.num_ships * self.difficulty_percentage)))
   

    def draw_ship(self, positions):
        for (x, y) in positions:
            self.win.addstr(y, x, self.intermediate_character_of_ship)
        self.win.refresh()


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
                    #self.draw_ship(new_ship_positions)
                    break


    def draw_status(self):
        self.stdscr.addstr(1, 0, " " * self.columns)

        ships_text = f"Navios: {self.num_ships}"
        self.stdscr.addstr(0, self.columns - len(ships_text) - 1, ships_text)

        chances_text = f"Chances: {self.chances} Dificuldade: {self.difficulty_percentage}"
        self.stdscr.addstr(1, self.columns - len(chances_text) - 1, chances_text)

        self.stdscr.refresh()

    def stylized_title(self):
        empty_space = 2  
        rows, columns = self.stdscr.getmaxyx()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        for i, line in enumerate(self.title):
            self.stdscr.addstr(empty_space + i, (columns - len(line)) // 2, line, curses.color_pair(1))

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

    def menu(self):
        while True:
            self.draw_menu() 

            key = self.stdscr.getch()

            if key == curses.KEY_UP: 
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif key == curses.KEY_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif key in [curses.KEY_ENTER, 10, 13]:  
                if self.selected_option == 0: 
                    break
                elif self.selected_option == 1: 
                    self.show_settings()  
                elif self.selected_option == 2:  
                    sys.exit(0)
            elif key == ord('q'):
                sys.exit(0)

    def draw_menu(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        curses.curs_set(0)

        self.stylized_title()

        title = "MENU INICIAL"
        title_y = len(self.title) + 4 
        self.stdscr.addstr(title_y, (width - len(title)) // 2, title, curses.A_BOLD)

        for idx, option in enumerate(self.menu_options):
            option_y = title_y + 2 + idx 
            if idx == self.selected_option:
                self.stdscr.addstr(option_y, (width - len(option)) // 2, option, curses.A_REVERSE) 
            else:
                self.stdscr.addstr(option_y, (width - len(option)) // 2, option)

        self.stdscr.refresh()  

    def show_settings(self):
        while True:
            self.stdscr.clear() 
            height, width = self.stdscr.getmaxyx()

            self.stylized_title()

            settings_title = "CONFIGURAÇÕES"
            settings_title_y = len(self.title) + 4 
            self.stdscr.addstr(settings_title_y, (width - len(settings_title)) // 2, settings_title, curses.A_BOLD)

            start_line = settings_title_y + 2

            difficulty_text = f"Dificuldade: {self.difficulty_levels[self.difficulty_index]}"
            self.stdscr.addstr(start_line, (width - len(difficulty_text)) // 2, difficulty_text)

            # emojis_text = "Usar Emojis: " + ("Sim" if self.use_emoji else "Não")
            # self.stdscr.addstr(start_line + 1, (width - len(emojis_text)) // 2, emojis_text)

            instructions = [
                "Pressione 'd' para mudar a dificuldade.",
                #"Pressione 'e' para mudar a opção de emojis.",
                "Pressione qualquer tecla para voltar ao menu."
            ]
            
            for idx, instruction in enumerate(instructions):
                self.stdscr.addstr(start_line + 5 + idx, (width - len(instruction)) // 2, instruction)

            self.stdscr.refresh() 

            key = self.stdscr.getch()  
            if key == ord('d'):  
                self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulty_levels)
                self.difficulty_percentage = self.difficulty_map[self.difficulty_index]
            # elif key == ord('e'): 
            #     self.use_emoji = not self.use_emoji
            else:  
                break



    def fire(self):
        for ship in self.ship_list:
            if ship.register_hit(self.cursor_x, self.cursor_y):
                if ship.hit:
                    appearance = self.ship_size_and_appearance[len(ship.positions)][1] if self.use_emoji else self.ship_size_and_appearance[len(ship.positions)][0]
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
        self.menu()
        self.setup()

        while True:
            self.draw_status()
            self.win.move(self.cursor_y, self.cursor_x)
            self.win.addstr(self.cursor_y, self.cursor_x, '█')
            self.win.refresh()

            key = self.win.getch()
            self.win.addstr(self.cursor_y, self.cursor_x, self.last_char)

            if key == ord('q') or self.chances == 0 or self.num_ships == 0:
                break
            elif key == ord('\n'):
                self.fire()
            else:
                self.move_cursor(key)

            self.last_char = chr(self.win.inch(self.cursor_y, self.cursor_x) & 0xFF)
