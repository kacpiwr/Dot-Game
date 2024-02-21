from turtle import Turtle, Screen
import random
import math


def initTurtle():
    screen = Screen()
    screen.tracer(8, 25)
    screen.bgcolor('white')
    screen.setworldcoordinates(0, 0, 500, 500)
    return screen


# ------------------------------------------------------------------------------------------------

class Player:
    def __init__(self, screen, enemies, color="black"):
        self.screen = screen
        self.body = Turtle()
        self.r = 8
        self.body.penup()
        self.body.hideturtle()
        self.body.color(color)
        self.body.pensize(self.r + 25)
        self.x = 250
        self.y = 250
        self.enemies = enemies
        self.unlocked = True
        self.alive = True
        self.draw()

    def draw(self):
        self.body.clear()
        self.body.pensize(self.r * 5)
        if self.alive:
            self.body.setpos(self.x, self.y)
            self.body.pendown()
            self.body.circle(self.r)
            self.body.penup()
            self.collision()

    def move_right(self):
        if self.alive:
            self.x = self.x + 5
            self.draw()

    def move_left(self):
        if self.alive:
            self.x = self.x - 5
            self.draw()

    def move_up(self):
        if self.alive:
            self.y = self.y + 5
            self.draw()

    def move_down(self):
        if self.alive:
            self.y = self.y - 5
            self.draw()

    def collision(self):
        for i in range(10):
            check_result = self.enemies[i].check(self.x, self.y, self.r)
            if check_result == 1:
                self.alive = False
                self.body.clear()
            elif check_result == 2:
                self.r += 3
                print(1)

    def get_points(self, point_x, point_y):
        if (math.sqrt((self.y - point_y) ** 2 + (self.x - point_x) ** 2)) < (self.r + 3):
            self.r += 1
            self.body.pensize(self.r+30)
            return True
        else:
            return False


class Bot:
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.body = Turtle()
        self.r = random.randint(2, 14)
        self.body.penup()
        self.body.hideturtle()
        self.body.color(color)
        self.body.pensize(self.r + 30)
        self.x = x
        self.y = y
        self.draw()
        self.unlocked = True
        self.change_x = random.randint(-5, 5)
        self.change_y = random.randint(-5, 5)
        self.alive = True

    def check(self, player_x, player_y, player_r):
        if math.sqrt((self.y - player_y) ** 2 + (self.x - player_x) ** 2) < (player_r + self.r) and self.r > player_r:
            return 1
        elif math.sqrt((abs(self.y - player_y)) ** 2 + (abs(self.x - player_x)) ** 2) < (
                player_r + self.r) and self.r < player_r:
            self.alive = False
            self.r = 0
            self.body.clear()
            self.x = -10000
            self.y = -10000
            return 2

        else:
            return 0

    # def kill(self):
    #     self.x = -10000
    #     self.y = -10000

    def draw(self):
        self.body.clear()

        self.body.setpos(self.x, self.y)
        self.body.pendown()
        self.body.circle(self.r)
        self.body.penup()

    def move(self):
        chance = [False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                  True]
        change = random.choice(chance)

        if change:
            self.change_x = random.randint(0, 10)
            self.change_x -= 5
            self.change_y = random.randint(0, 10)
            self.change_y -= 5

        if self.x >= 490 or self.x <= 10 or self.y >= 490 or self.y <= 10:
            self.change_x = random.randint(0, 10)
            self.change_x -= 5
            self.change_y = random.randint(0, 10)
            self.change_y -= 5
        self.x += self.change_x
        self.y += self.change_y
        if self.alive:
            self.draw()

            self.screen.ontimer(self.move, 100)

    def get_points(self, point_x, point_y):
        if (math.sqrt((self.y - point_y) ** 2 + (self.x - point_x) ** 2)) < (self.r + 3):
            self.r += 3
            self.body.pensize(self.r+30)
            return True
        else:
            return False


class Point:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.body = Turtle()
        self.r = 3
        self.body.penup()
        self.body.hideturtle()
        self.body.color("red")
        self.body.pensize(25)
        self.x = x
        self.y = y
        self.alive = True
        self.draw()

    def draw(self):
        self.body.clear()

        self.body.setpos(self.x, self.y)
        self.body.pendown()
        for number in range(4):
            self.body.forward(5)
            self.body.right(90)
        self.body.penup()

    def kill(self):
        self.body.clear()


class Spawner:
    def __init__(self, screen, bots, player):
        self.screen = screen
        self.bots = bots
        self.player = player
        self.points = []
        self.cords_points = []
        self.spawn_start()

    def spawn_start(self):
        for i in range(20):
            x = random.randint(10, 490)
            y = random.randint(10, 490)
            cords = [x, y]
            self.cords_points.append(cords)
            self.points.append(Point(screen, x, y))
        self.screen.ontimer(self.spawn, 5000)
        self.screen.ontimer(self.gen_check(), 100)

    def spawn(self):
        x = random.randint(10, 490)
        y = random.randint(10, 490)
        cords = [x, y]
        self.cords_points.append(cords)
        self.points.append(Point(screen, x, y))
        self.screen.ontimer(self.spawn, 5000)

    def gen_check(self):
        for i in range(len(self.points)):
            verdict_player = self.player.get_points(self.cords_points[i - 1][0], self.cords_points[i - 1][1])
            if verdict_player:
                self.points[i - 1].kill()
                del (self.points[i - 1])
                del (self.cords_points[i - 1])
            for j in range(len(self.bots)):
                verdict = self.bots[j].get_points(self.cords_points[i-1][0], self.cords_points[i-1][1])
                if verdict:
                    self.points[i-1].kill()
                    del (self.points[i-1])
                    del (self.cords_points[i-1])
        self.screen.ontimer(self.gen_check, 100)


screen = initTurtle()

bots = []
colors = ["yellow", "gold", "orange", "maroon", "violet", "magenta", "purple", "navy", "blue", "skyblue", "cyan",
          "turquoise", "lightgreen", "green", "darkgreen", "chocolate", "brown", "gray"]
for i in range(10):
    bots.append(Bot(screen, random.randint(10, 490), random.randint(10, 490), random.choice(colors)))

    bots[i].move()
tank = Player(screen, enemies=bots)

spawner = Spawner(screen, bots=bots, player=tank)

screen.onkey(tank.move_left, "a")
screen.onkey(tank.move_right, "d")
screen.onkey(tank.move_up, "w")
screen.onkey(tank.move_down, "s")

screen.listen()
screen.mainloop()
