import random

import arcade
WIDTH_WINDOW=800
HEIGHT_WINDOW=600
WINDOW_TITLE="PAC-MAN"
TILE_SIZE=32

class Coin:
    def __init__(self, x, y, value = 10):
        self.center_x = x
        self.center_y = y
        self.value = value


class Character:
    def __init__(self, started_x, started_y, speed = 0, change_x = 0, change_y = 0):
        self.center_x = started_x
        self.center_y = started_y
        self.speed = speed
        self.change_x = change_x
        self.change_y = change_y


class Player(Character):
    def __init__(self, started_x, started_y):
        super().__init__(started_x, started_y)
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Enemy(Character):
    def __init__(self, started_x, started_y):
        super().__init__(started_x, started_y)
        self.time_to_change_direction = 0

    def pick_new_direction(self):
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        fate = random.choice(movements)
        self.change_x = fate[0]
        self.change_y = fate[1]
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self,  delta_time = 1/60):
        if self.time_to_change_direction == 0:
            self.pick_new_direction()
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
        self.time_to_change_direction -= delta_time


class Wall:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y



class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.wall_list=arcade.SpriteList()
        self.coin_list=arcade.SpriteList()
        self.ghost_list=arcade.SpriteList()
        self.player_list=arcade.SpriteList()
        self.player = None
        self.game_over = False
        self.background_color = arcade.color.BLACK
        self.start_x=0
        self.start_y=0

    def on_draw(self):
        arcade.open_window(WIDTH_WINDOW, HEIGHT_WINDOW, WINDOW_TITLE)
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        arcade.draw_text(f"Score: {self.player.score}",50,550,arcade.color.WHITE)
        arcade.draw_text(f"Lives: {self.player.lives}",50,500, arcade.color.WHITE)
        if self.game_over:
            arcade.draw_text("GAME OVER", 400, 300, arcade.color.GOLD, 100)

    def setup(self, ):
        self.wall_list = arcade.spritelist()
        self.coin_list = arcade.spritelist()
        self.ghost_list = arcade.spritelist()
        self.player_list = arcade.spritelist()
        self.game_over = False

        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (rows - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if LEVEL_MAP[x][y] == wall:
                    self.wall_list.append((x, y))

                elif LEVEL_MAP[x][y] == player:
                    self.player_list.append((x, y))

                elif LEVEL_MAP[x][y] == coin:
                    self.coin_list.append((x, y))

                elif LEVEL_MAP[x][y] == ghost:
                    self.ghost_list.append((x, y))

    def key_on_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.change_y = 0

    def on_key_release(self, key, modifiers):
        if self.key == arcade.key.Up or self.key == arcade.key.Down:
            self.change_y = 0
        if self.key == arcade.key.Left or self.key == arcade.key.Right:
            self.change_x = 0









# מפה לדוגמה: # = קיר, . = מטבע, P = פקמן, G = רוח, רווח = כלום
LEVEL_MAP = [
    "###########",
    "#P....G...#",
    "#.........#",
    "###########",
]

