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
        self.angle = 0
        self.mouth_open = True
        self.mouth_timer = 0

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
        if self.change_x > 0:
            self.angle = 0
        elif self.change_x < 0:
            self.angle = 180
        elif self.change_y > 0:
            self.angle = 90
        elif self.change_y < 0:
            self.angle = 270

    def update_animation(self, delta_time):
        self.mouth_timer += delta_time
        if self.mouth_timer > 0.15:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0

    def draw(self):
        radius = (TILE_SIZE-6) * 0.5
        start_angle = 0
        end_angle = 360
        if self.mouth_open:
            start_angle = 30
            end_angle = 330
        arcade.draw_arc_filled(self.center_x, self.center_y,
                               radius*2, radius*2,
                               arcade.color.YELLOW,
                               start_angle + self.angle,
                               end_angle + self.angle)

class Enemy(Character):
    def __init__(self, started_x, started_y, color=arcade.color.RED):
        super().__init__(started_x, started_y, 4, color)
        self.time_to_change_direction = 0
        self.target_x = self.center_x
        self.target_y = self.center_y
        self.color = color

    def pick_new_direction(self):
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        fate = random.choice(movements)
        self.change_x = fate[0]
        self.change_y = fate[1]
        self.time_to_change_direction = random.uniform(0.1, 1.0)
        self.target_x = self.center_x + self.change_x * TILE_SIZE
        self.target_y = self.center_y + self.change_y * TILE_SIZE

    def update(self, delta_time=1/60):
        if self.time_to_change_direction <= 0:
            self.pick_new_direction()
        self.center_x += (self.target_x - self.center_x) * 0.1
        self.center_y += (self.target_y - self.center_y) * 0.1
        self.time_to_change_direction -= delta_time

    def draw(self):
        x = self.center_x
        y = self.center_y
        width = TILE_SIZE - 8
        height = TILE_SIZE - 8

        # גוף מלא חצי עיגול למעלה
        arcade.draw_ellipse_filled(x, y, width, height, self.color)


        eye_radius = 3
        arcade.draw_circle_filled(x - width*0.2, y + height*0.15, eye_radius, arcade.color.WHITE)
        arcade.draw_circle_filled(x + width*0.2, y + height*0.15, eye_radius, arcade.color.WHITE)
        arcade.draw_circle_filled(x - width*0.2, y + height*0.15, eye_radius-1, arcade.color.BLUE)
        arcade.draw_circle_filled(x + width*0.2, y + height*0.15, eye_radius-1, arcade.color.BLUE)


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
        for ghost in self.ghost_list:
            ghost.draw()
        self.player.draw()
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
                if cell == "#":
                    self.wall_list.append(Wall(x, y))
                elif cell == "P":
                    self.player=Player(x, y)
                    self.start_x = x
                    self.start_y = y
                    self.player_list.append(self.player)
                elif cell == ".":
                    self.coin_list.append(Coin(x, y))
                elif cell == "G":
                    self.ghost_list.append(Enemy(x, y))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = TILE_SIZE
        if key == arcade.key.DOWN:
            self.player.change_y = -TILE_SIZE
        if key == arcade.key.LEFT:
            self.player.change_x = -TILE_SIZE
        if key == arcade.key.RIGHT:
            self.player.change_x = TILE_SIZE

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
            self.player.update_animation(delta_time)
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
                    self.player.center_y = self.start_y
                    if self.player.lives==0:
                        self.game_over = True

LEVEL_MAP = [
    "#########################",
    "#.......................#",
    "#.###.####.#..#####.###.#",
    "#.............G.........#",
    "#.####.####.##.####.###.#",
    "#............##.........#",
    "#.########.####.#######.#",
    "#P......................#",
    "#.#########.####.######.#",
    "#............##.........#",
    "#.####.#####.##.###.###.#",
    "#.......G...............#",
    "#.####.#####.#..###.###.#",
    "#............#..........#",
    "#########################",
]

def main():
    window = arcade.Window(WIDTH_WINDOW, HEIGHT_WINDOW, WINDOW_TITLE)
    game_view = PacmanGame()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()

