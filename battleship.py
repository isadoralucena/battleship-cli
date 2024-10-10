from ship import Ship
import random
import curses
import sys
import time

class Battleship:
    def __init__(self, stdscr, selected_option = 0, difficulty_index = 1, use_emoji=False):
        self.stdscr = stdscr

        self.difficulty_map = {
            0: 0.40,
            1: 0.05
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

        text = "VOCÊ CONSEGUE VENCER O ALGORITMO?"
        self.rows, self.columns = self.stdscr.getmaxyx()
        self.stdscr.addstr(1, (self.columns - len(text)) // 2, text)
        self.stdscr.refresh()

        self.win_height = self.rows - 6
        self.win_width = self.columns//2 + 2

        start_y = (self.rows - self.win_height) // 2
        start_x = (self.columns - self.win_width) // 2


        self.win = curses.newwin(self.win_height, self.win_width, start_y, start_x)
        self.win.border()
        self.win.keypad(True)
        curses.curs_set(1)

        self.num_ships = self.calculate_num_ships()
        self.chances = self.calculate_chances()
        self.generate_ships()


    def draw_battle_naval_blocks(self, y, x, flash_on):
        if flash_on:
            for i, line in enumerate(self.title):
                self.stdscr.addstr(y + i, x, line, curses.color_pair(2))

        credits = "por Isadora Lucena - UFCG, 2024.1"
        self.stdscr.addstr(y + len(self.title) + 1, x + (101 - len(credits)) // 2, credits, curses.color_pair(1))


    def animate(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        curses.curs_set(0)

        self.stdscr.nodelay(True)

        height, width = self.stdscr.getmaxyx()

        flash_on = True
        flash_delay = 0.5
        last_flash_time = time.time()

        text_height = len(self.title)
        text_width = max(len(line) for line in self.title)

        start_y = (height - text_height) // 2
        start_x = (width - text_width) // 2

        intro_duration = 5
        intro_start_time = time.time()

        while True:
            self.stdscr.clear()

            self.draw_battle_naval_blocks(start_y, start_x, flash_on)

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
        self.stdscr.addstr(3, 0, " " * self.columns)
        self.stdscr.addstr(2, 0, " " * self.columns)

        ships_text = f"Navios: {self.num_ships}"
        self.stdscr.addstr(2, self.columns - len(ships_text) - 1, ships_text)

        chances_text = f"Chances: {self.chances}"
        self.stdscr.addstr(3, self.columns - len(chances_text) - 1, chances_text)

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

    def end_game(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        curses.curs_set(0)

        self.stylized_title()

        title = "NÃO FOI DESSA VEZ..." if self.chances == 0 else "PARABÉNS!!! VOCÊ GANHOU"
        title_y = len(self.title) + 4
        self.stdscr.addstr(title_y, (width - len(title)) // 2, title, curses.A_BOLD)

        options = ["Jogar de novo", "Sair"]
        selected_option = 0

        option_start_y = title_y + 2

        while True:
            for idx, option in enumerate(options):
                if idx == selected_option:
                    self.stdscr.addstr(option_start_y + idx, (width - len(option)) // 2, option, curses.A_REVERSE)
                else:
                    self.stdscr.addstr(option_start_y + idx, (width - len(option)) // 2, option)

            self.stdscr.refresh()

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
        min_height = len(self.title) + 9
        min_width = max(len(line) for line in self.title)

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

        while True:
            self.draw_status()
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
