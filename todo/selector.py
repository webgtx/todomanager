import curses

class Selector:
    def __init__(self, options: list):
        self.stdscr = curses.initscr()
        self.options = options

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.noecho()
        curses.curs_set(0)
        curses.cbreak()

    def _display(self, cursor: int):
        for idx, f in enumerate(self.options):
            if idx == cursor:
                self.stdscr.addstr(f"{f.name}\n", curses.color_pair(1))
            self.stdscr.addstr(f"{f.name}\n")

    def select(self):
        curses.curs_set(0)
        cursor = 0

        while 1:
            self._display(cursor)
            key = self.stdscr.getch()
            self.stdscr.clear()
            if key == ord("\n"):
                return self.options[cursor]
            elif key == ord("j") or key == curses.KEY_DOWN:
                cursor += 1
            elif key == ord("k") or key == curses.KEY_UP:
                cursor -= 1
            self.stdscr.refresh()
        
        curses.doupdate()

