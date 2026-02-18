import random
import arcade

WIDTH_WINDOW=800
HEIGHT_WINDOW=600
WINDOW_TITLE="PAC-MAN"
TILE_SIZE=32

class Coin(arcade.Sprite):
    def __init__(self, x, y, value = 10):
        super().__init__()
        radius = TILE_SIZE//4
        texture = arcade.texture.make_circle_texture(radius, arcade.color.GOLDEN_YELLOW)
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.center_x = x
        self.center_y = y
        self.value = value


class Character(arcade.Sprite):
    def __init__(self, started_x, started_y, speed, color):
        super().__init__()
        radius = TILE_SIZE-6
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
        super().__init__(started_x, started_y, 0.125, arcade.color.YELLOW)
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Enemy(Character):
    def __init__(self, started_x, started_y):
        super().__init__(started_x, started_y, 2.5, arcade.color.RED)
        self.time_to_change_direction = 0

    def pick_new_direction(self):
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        fate = random.choice(movements)
        self.change_x = fate[0]
        self.change_y = fate[1]
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self, delta_time=1/60):
        if self.time_to_change_direction <= 0:
            self.pick_new_direction()
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
        self.time_to_change_direction -= delta_time


class Wall(arcade.Sprite):
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
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        arcade.draw_text(f"Score: {self.player.score}",50,550,arcade.color.WHITE)
        arcade.draw_text(f"Lives: {self.player.lives}",50,500, arcade.color.WHITE)
        if self.game_over:
            arcade.draw_text("GAME OVER", 200, 300, arcade.color.GOLD, 60)



    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.game_over = False

        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = row_idx * TILE_SIZE + TILE_SIZE // 2

                if LEVEL_MAP[row_idx][col_idx] == "#":
                    self.wall_list.append(Wall(x, y))

                elif LEVEL_MAP[row_idx][col_idx] == "P":
                    self.player=Player(x, y)
                    self.start_x = x
                    self.start_y = y
                    self.player_list.append(self.player)

                elif LEVEL_MAP[row_idx][col_idx] == ".":
                    self.coin_list.append(Coin(x, y))

                elif LEVEL_MAP[row_idx][col_idx] == "G":
                    self.ghost_list.append(Enemy(x, y))



    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = 32
        if key == arcade.key.DOWN:
            self.player.change_y = -32
        if key == arcade.key.LEFT:
            self.player.change_x = -32
        if key == arcade.key.RIGHT:
            self.player.change_x = 32

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0

    def on_update(self, delta_time):
        if not self.game_over:
            now_x = self.player.center_x
            now_y = self.player.center_y
            self.player.move()
            wall_player = arcade.check_for_collision_with_list(self.player, self.wall_list)
            if len(wall_player)>0:
                self.player.center_x = now_x
                self.player.center_y = now_y

            for ghost in self.ghost_list:
                current_x = ghost.center_x
                current_y = ghost.center_y
                ghost.update()
                ghost_wall = arcade.check_for_collision_with_list(ghost, self.wall_list)
                if len(ghost_wall):
                    ghost.center_x = current_x
                    ghost.center_y = current_y

                coin_check = arcade.check_for_collision_with_list(self.player, self.coin_list)
                if len(coin_check)>0:
                    self.player.score+=10
                    self.coin_list.remove(coin_check[0])

                ghost_player = arcade.check_for_collision_with_list(self.player, self.ghost_list)
                if len(ghost_player):
                    self.player.lives-=1
                    self.player.center_x=self.start_x
                    self.player.center_y = self.start_x
                    if self.player.lives==0:
                        self.game_over = True




# מפה לדוגמה: # = קיר, . = מטבע, P = פקמן, G = רוח, רווח = כלום
LEVEL_MAP = [
    "#########################",
    "#..................G....#",
    "#.###.####.#..#####.###.#",
    "#.......................#",
    "#.####.####.##.####.###.#",
    "#............##.........#",
    "#.########.####.#######.#",
    "#P......................#",
    "#.#########.####.######.#",
    "#............##.........#",
    "#.####.#####.##.###.###.#",
    "#.......................#",
    "#.####.#####.#..###.###.#",
    "#............#..........#",
    "#########################",
]

def main():
    """פונקציית main שמריצה את המשחק."""
    window = arcade.Window(WIDTH_WINDOW, HEIGHT_WINDOW, WINDOW_TITLE)
    game_view = PacmanGame()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()


# מפה לדוגמה: # = קיר, . = מטבע, P = פקמן, G = רוח, רווח = כלום
LEVEL_MAP = [
    "###########",
    "#P....G...#",
    "#.........#",
    "###########",
]
