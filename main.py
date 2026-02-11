import random
import arcade

WIDTH_WINDOW=800
HEIGHT_WINDOW=600
WINDOW_TITLE="PAC-MAN"
TILE_SIZE=32

class Coin(arcade.sprite):
    def __init__(self, x, y, value = 10):
        super().__init__()
        radius = TILE_SIZE//8
        texture = arcade.texture.make_circle_texture(radius, arcade.color.GOLDEN_YELLOW)
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.center_x = x
        self.center_y = y
        self.value = value


class Character(arcade.sprite):
    def __init__(self, started_x, started_y, speed, color):
        super().__init__()
        radius = TILE_SIZE//2-2
        texture = arcade.make_circle_texture(radius, color)
        self.texture= texture
        self.width = texture.width
        self.height = texture.height
        self.center_x = started_x
        self.center_y = started_y
        self.speed = speed
        self.change_x = 0
        self.change_y = 0


class Player(Character):
    def __init__(self, started_x, started_y):
        super().__init__(started_x, started_y, 2.5, arcade.color.YELLOW)
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Enemy(Character):
    def __init__(self, started_x, started_y):
        super().__init__(started_x, started_y, arcade.color.RED)
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


class Wall(arcade.sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        texture = arcade.texture.make_soft_square_texture(TILE_SIZE, arcade.color.BLUE)
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
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



    def setup(self):
        self.wall_list = arcade.spritelist()
        self.coin_list = arcade.spritelist()
        self.ghost_list = arcade.spritelist()
        self.player_list = arcade.spritelist()
        self.game_over = False

        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (row - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if LEVEL_MAP[col_idx][row_idx] == "wall":
                    self.wall_list.append((col_idx, row_idx))

                elif LEVEL_MAP[col_idx][row_idx] == "player":
                    self.player_list.append((col_idx, row_idx))

                elif LEVEL_MAP[col_idx][row_idx] == "coin":
                    self.coin_list.append((col_idx, row_idx))

                elif LEVEL_MAP[col_idx][row_idx] == "ghost":
                    self.ghost_list.append((col_idx, row_idx))




    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0

    def on_update(self, delta_time):
        if not self.game_over:
            now_x = self.center_x
            now_y = self.center_y
            self.player.move()
            wall_player = arcade.check_for_collision_with_list(self.player, self.wall_list)
            if len(wall_player)>0:
                self.center_x = now_x
                self.center_y = now_y

            for ghost in self.ghost_list:
                current_x = ghost.center_x
                current_y = ghost.center_y
                ghost.update(self)
                ghost_wall = arcade.check_for_collision_with_list(ghost, self.wall_list)
                while not len(ghost_wall)>0:
                    ghost.center_x = current_x
                    ghost.center_y = current_y
                    ghost.update(self)

                coin_check = arcade.check_for_collision_with_list(self.player, self.coin_list)
                if len(coin_check>0):
                    self.score+=1
                    self.coin_list.remove(coin_check)

                ghost_player = arcade.check_for_collision_with_list(self.player, self.ghost_list)
                if len(ghost_player):
                    self.player.lives-=1
                    self.player.center_x=self.started_x
                    self.player.center_y = self.started_y
                    self.player.speed = 0
                    if self.player.lives==0:
                        self.game_over= True














# מפה לדוגמה: # = קיר, . = מטבע, P = פקמן, G = רוח, רווח = כלום
LEVEL_MAP = [
    "###########",
    "#P....G...#",
    "#.........#",
    "###########",
]

