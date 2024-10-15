import curses
import time

class Display:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.rows, self.columns = self.stdscr.getmaxyx()
        self.title = [
            "██████╗  █████╗ ████████╗ █████╗ ██╗     ██╗  ██╗ █████╗     ███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗     ",
            "██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║     ██║  ██║██╔══██╗    ████╗  ██║██╔══██╗██║   ██║██╔══██╗██║     ",
            "██████╔╝███████║   ██║   ███████║██║     ███████║███████║    ██╔██╗ ██║███████║██║   ██║███████║██║     ",
            "██╔══██╗██╔══██║   ██║   ██╔══██║██║     ██╔══██║██╔══██║    ██║╚██╗██║██╔══██║╚██╗ ██╔╝██╔══██║██║     ",
            "██████╔╝██║  ██║   ██║   ██║  ██║███████╗██║  ██║██║  ██║    ██║ ╚████║██║  ██║ ╚████╔╝ ██║  ██║███████╗",
            "╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝"
        ]
    

    def display_title(self, empty_space=2):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.stdscr.clear()
        for i, line in enumerate(self.title):
            self.stdscr.addstr(empty_space + i, (self.columns - len(line)) // 2, line, curses.color_pair(1))
        self.stdscr.refresh()


    def display_menu(self, title, options, selected_option):
        self.stdscr.clear()
        width = self.columns
        curses.curs_set(0)

        self.display_title()

        title_y = len(self.title) + 4 
        self.stdscr.addstr(title_y, (width - len(title)) // 2, title, curses.A_BOLD)

        for idx, option in enumerate(options):
            option_y = title_y + 2 + idx 
            if idx == selected_option:
                self.stdscr.addstr(option_y, (width - len(option)) // 2, option, curses.A_REVERSE) 
            else:
                self.stdscr.addstr(option_y, (width - len(option)) // 2, option)
        self.stdscr.refresh()  


    def display_credits(self, start_y):
        width = self.columns
        credits = "por Isadora Lucena - UFCG, 2024.1"
        self.stdscr.addstr(start_y + len(self.title) + 1, (width - len(credits)) // 2, credits)
        self.stdscr.refresh()


    def display_status(self, num_ships, chances):
        self.stdscr.addstr(2, 0, " " * self.columns)
        self.stdscr.addstr(3, 0, " " * self.columns)
        ships_text = f"Navios: {num_ships}"
        self.stdscr.addstr(2, self.columns - len(ships_text) - 1, ships_text)
        chances_text = f"Chances: {chances}"
        self.stdscr.addstr(3, self.columns - len(chances_text) - 1, chances_text)
        self.stdscr.refresh()


    def intro(self, flash_on):
        height = self.rows
        text_height = len(self.title)

        start_y = (height - text_height) // 2

        if flash_on:
            self.display_title(start_y)

        self.display_credits(start_y)


    def display_setup(self):
        text = "VOCÊ CONSEGUE VENCER O ALGORITMO?"
        self.stdscr.addstr(1, (self.columns - len(text)) // 2, text)
        self.stdscr.refresh()


    def display_ship_legend(self):
        legend_text = [
            "S - Submarino",
            "DD - Destroyer",
            "CCC - Cruzador",
            "PPPP - Porta-avião"
        ]

        height = self.rows

        start_y = height - len(legend_text)
        start_x = 1
        
        for i, line in enumerate(legend_text):
            self.stdscr.addstr(start_y + i, start_x, line)
        
        self.stdscr.refresh()

    def display_settings(self, difficulty_levels, difficulty_index, difficulty_map, difficulty_percentage):
        self.stdscr.clear() 
        width = self.columns

        self.display_title()

        settings_title = "CONFIGURAÇÕES"
        settings_title_y = len(self.title) + 4 
        self.stdscr.addstr(settings_title_y, (width - len(settings_title)) // 2, settings_title, curses.A_BOLD)

        start_line = settings_title_y + 2

        difficulty_text = f"Dificuldade: {difficulty_levels[difficulty_index]}"
        self.stdscr.addstr(start_line, (width - len(difficulty_text)) // 2, difficulty_text)

        instructions = [
            "Pressione 'd' para mudar a dificuldade.",
            "Pressione qualquer tecla para voltar ao menu."
        ]
        
        for idx, instruction in enumerate(instructions):
            self.stdscr.addstr(start_line + 5 + idx, (width - len(instruction)) // 2, instruction)

        self.stdscr.refresh() 