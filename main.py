
import random

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle


# تنظیمات پنجره
Window.size = (420, 650)
Window.clearcolor = (0.08, 0.09, 0.12, 1)


# رنگ خانه ها
COLORS = {
    0: (0.18, 0.19, 0.23, 1),
    2: (0.85, 0.82, 0.74, 1),
    4: (0.90, 0.76, 0.55, 1),
    8: (0.95, 0.60, 0.35, 1),
    16: (0.95, 0.45, 0.30, 1),
    32: (0.92, 0.32, 0.25, 1),
    64: (0.85, 0.20, 0.18, 1),
    128: (0.85, 0.75, 0.35, 1),
    256: (0.85, 0.68, 0.25, 1),
    512: (0.90, 0.60, 0.20, 1),
    1024: (0.80, 0.50, 0.15, 1),
    2048: (0.95, 0.75, 0.15, 1),
}


# ---------------- MENU ----------------

class MenuScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=40,
            spacing=25
        )

        title = Label(
            text="2048",
            font_size=65,
            bold=True,
            color=(1, 0.75, 0.2, 1)
        )

        subtitle = Label(
            text="5 x 5 EDITION",
            font_size=20
        )

        start = Button(
            text="START",
            font_size=25,
            bold=True,
            size_hint=(1, 0.18),
            background_normal="",
            background_color=(0.2, 0.65, 0.4, 1)
        )
        start.bind(on_release=self.start_game)

        exit_btn = Button(
            text="EXIT",
            font_size=22,
            size_hint=(1, 0.15),
            background_normal="",
            background_color=(0.75, 0.2, 0.2, 1)
        )
        exit_btn.bind(on_release=lambda x: App.get_running_app().stop())

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(start)
        layout.add_widget(exit_btn)

        self.add_widget(layout)

    def start_game(self, instance):
        game = self.manager.get_screen("game")
        game.new_game()
        self.manager.current = "game"


# ---------------- GAME ----------------

class GameScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.board = []
        self.score = 0
        self.won = False

        main = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        header = BoxLayout(
            size_hint=(1, 0.12),
            spacing=10
        )

        self.score_label = Label(
            text="SCORE: 0",
            font_size=22,
            bold=True
        )

        menu_btn = Button(
            text="MENU",
            size_hint=(0.4, 1),
            background_normal="",
            background_color=(0.35, 0.38, 0.45, 1)
        )
        menu_btn.bind(on_release=self.go_menu)

        header.add_widget(self.score_label)
        header.add_widget(menu_btn)

        self.status = Label(
            text="Use arrow keys to play",
            size_hint=(1, 0.08),
            font_size=16
        )

        self.grid = GridLayout(
            cols=5,
            rows=5,
            spacing=6,
            padding=6,
            size_hint=(1, 0.68)
        )

        self.tiles = []

        for i in range(25):
            tile = Label(
                text="",
                font_size=25,
                bold=True,
                color=(0.1, 0.1, 0.1, 1)
            )

            with tile.canvas.before:
                tile.bg_color = Color(0.18, 0.19, 0.23, 1)
                tile.bg_rect = RoundedRectangle(
                    pos=tile.pos,
                    size=tile.size,
                    radius=[9]
                )

            tile.bind(
                pos=lambda widget, pos: self.update_tile_bg(widget),
                size=lambda widget, size: self.update_tile_bg(widget)
            )

            self.tiles.append(tile)
            self.grid.add_widget(tile)

        restart = Button(
            text="RESTART",
            font_size=20,
            size_hint=(1, 0.12),
            background_normal="",
            background_color=(0.2, 0.55, 0.8, 1)
        )
        restart.bind(on_release=lambda x: self.new_game())

        main.add_widget(header)
        main.add_widget(self.status)
        main.add_widget(self.grid)
        main.add_widget(restart)

        self.add_widget(main)

    def update_tile_bg(self, widget):
        widget.bg_rect.pos = widget.pos
        widget.bg_rect.size = widget.size

    # شروع بازی جدید
    def new_game(self):

        self.board = [[0 for _ in range(5)] for _ in range(5)]

        self.score = 0
        self.won = False

        self.status.text = "Use arrow keys to play"

        self.add_random_tile()
        self.add_random_tile()

        self.update_ui()

    # ساخت عدد تصادفی
    def add_random_tile(self):

        empty = [
            (r, c)
            for r in range(5)
            for c in range(5)
            if self.board[r][c] == 0
        ]

        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = random.choices(
                [2, 4], weights=[90, 10]
            )[0]

    # حرکت به چپ
    def move_left(self, row):

        values = [x for x in row if x != 0]

        result = []
        i = 0

        while i < len(values):

            if i + 1 < len(values) and values[i] == values[i + 1]:

                result.append(values[i] * 2)
                self.score += values[i] * 2
                i += 2

            else:
                result.append(values[i])
                i += 1

        return result + [0] * (5 - len(result))

    # انجام حرکت
    def move(self, direction):

        old_board = [row[:] for row in self.board]
        self.score = self.score

        if direction == "left":

            self.board = [
                self.move_left(row)
                for row in self.board
            ]

        elif direction == "right":

            self.board = [
                list(reversed(self.move_left(list(reversed(row)))))
                for row in self.board
            ]

        elif direction == "up":

            self.board = [
                list(row)
                for row in zip(*self.board)
            ]

            self.board = [
                self.move_left(row)
                for row in self.board
            ]

            self.board = [
                list(row)
                for row in zip(*self.board)
            ]

        elif direction == "down":

            self.board = [
                list(row)
                for row in zip(*self.board)
            ]

            self.board = [
                list(reversed(self.move_left(list(reversed(row)))))
                for row in self.board
            ]

            self.board = [
                list(row)
                for row in zip(*self.board)
            ]

        if self.board != old_board:

            self.add_random_tile()

            if any(2048 in row for row in self.board) and not self.won:
                self.won = True
                self.status.text = "YOU WIN! 🎉"

            elif not self.can_move():
                self.status.text = "GAME OVER!"

            elif self.won:
                self.status.text = "YOU WIN! 🎉"

            else:
                self.status.text = "Keep going!"

            self.update_ui()

    # بررسی امکان حرکت
    def can_move(self):

        for r in range(5):
            for c in range(5):

                if self.board[r][c] == 0:
                    return True

                if c < 4 and self.board[r][c] == self.board[r][c + 1]:
                    return True

                if r < 4 and self.board[r][c] == self.board[r + 1][c]:
                    return True

        return False

    # بروزرسانی صفحه
    def update_ui(self):

        self.score_label.text = f"SCORE: {self.score}"

        for i, tile in enumerate(self.tiles):

            r = i // 5
            c = i % 5

            number = self.board[r][c]

            tile.text = str(number) if number else ""

            tile.bg_color.rgba = COLORS.get(
                number, (0.4, 0.35, 0.2, 1)
            )

            if number <= 4:
                tile.color = (0.2, 0.2, 0.2, 1)
            else:
                tile.color = (1, 1, 1, 1)

    def go_menu(self, instance):
        self.manager.current = "menu"


# ---------------- MAIN APP ----------------

class Game2048(App):

    def build(self):

        self.title = "2048 Game"

        manager = ScreenManager()

        manager.add_widget(
            MenuScreen(name="menu")
        )

        manager.add_widget(
            GameScreen(name="game")
        )

        Window.bind(on_key_down=self.on_key_down)

        return manager

    def on_key_down(self, window, key, scancode, codepoint, modifiers):

        game = self.root.get_screen("game")

        if self.root.current != "game":
            return

        keys = {
            "left": "left",
            "right": "right",
            "up": "up",
            "down": "down",
            "a": "left",
            "d": "right",
            "w": "up",
            "s": "down"
        }

        direction = keys.get(codepoint.lower())

        if direction:
            game.move(direction)

        return True


if __name__ == "__main__":
    Game2048().run()
