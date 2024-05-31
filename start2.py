import pygame
from os.path import join
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 850, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHOOTERS 2.0")
ICON = pygame.image.load(join("images", "spaceship.png"))
pygame.display.set_icon(ICON)

BG = pygame.image.load(join("images", "milky-way.jpg"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
PLAYER_SHIP_1 = pygame.image.load(join("images", "spaceship1.png"))
PLAYER_SHIP_1 = pygame.transform.scale(PLAYER_SHIP_1, (110, 100))
PLAYER_SHIP_1 = pygame.transform.rotate(PLAYER_SHIP_1, 270)
LASER_RED = pygame.image.load(join("images", "pixel_laser_red.png"))
LASER_RED = pygame.transform.rotate(LASER_RED, 90)
PLAYER_SHIP_2 = pygame.image.load(join("images", "spaceship2.png"))
PLAYER_SHIP_2 = pygame.transform.scale(PLAYER_SHIP_2, (110, 100))
PLAYER_SHIP_2 = pygame.transform.rotate(PLAYER_SHIP_2, 180)
LASER_BLUE = pygame.image.load(join("images", "pixel_laser_blue.png"))
LASER_BLUE = pygame.transform.rotate(LASER_BLUE, 90)

score1 = 0
score2 = 0

class Player:
    COOLDOWN = 30
    # score1 = 0
    # score2 = 0
    # main_font = pygame.font.SysFont("comicsans", 40)

    def __init__(self, x, y, ship_img, laser_img, score):
        self.x = x
        self.y = y
        self.ship_img = ship_img
        self.score = score
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.lasers = []
        self.cooldown_counter = 0
    def score_count(self, x, y, window):
        main_font = pygame.font.SysFont("comicsans", 40)
        score_label = main_font.render(f"SCORE : {self.score}", 1, (255, 255, 255))
        window.blit(score_label, (x, y))

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    def move_lasers(self, vel, obj):
        self.cooldown()
        # count1 = 0
        # count2 = 0
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH + 10):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                self.lasers.remove(laser)
                self.score += 1
        

class Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.x += vel
    def off_screen(self, width):
        return not(self.x <= width and self.x >= 0)
    def collision(self, obj):
        return collide(self, obj)
    
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

player_vel = 3
laser_vel_1 = 5
laser_vel_2 = -5
def move_player(key):
    if key[pygame.K_w] and player1.y > 10:
        player1.y -= player_vel
    if key[pygame.K_s] and player1.y + player1.ship_img.get_height() + player_vel < HEIGHT - 10:
        player1.y += player_vel
    if key[pygame.K_a] and player1.x > 10:
        player1.x -= player_vel
    if key[pygame.K_d] and player1.x + player1.ship_img.get_width() + player_vel < WIDTH/2 - 20:
        player1.x += player_vel
    if key[pygame.K_KP8] and player2.y > 10:
        player2.y -= player_vel    
    if key[pygame.K_KP5] and player2.y + player2.ship_img.get_height() + player_vel < HEIGHT - 10:
        player2.y += player_vel
    if key[pygame.K_KP4] and player2.x > WIDTH/2 + 20:
        player2.x -= player_vel
    if key[pygame.K_KP6] and player2.x + player2.ship_img.get_width() + player_vel < WIDTH - 10:
        player2.x += player_vel
    if key[pygame.K_SPACE]:
        player1.shoot()
    if key[pygame.K_KP0]:
        player2.shoot()

player1 = Player(50, HEIGHT/2 - 25, PLAYER_SHIP_1, LASER_RED, score1)
player2 = Player(WIDTH - 50 - PLAYER_SHIP_2.get_width(), HEIGHT/2 -25, PLAYER_SHIP_2, LASER_BLUE, score2)

def redraw_window():
    WIN.blit(BG, (0, 0))
    # score1_label = main_font.render(f"SCORE : {score1}", 1, (255, 255, 255))
    # score2_label = main_font.render(f"SCORE : {score2}", 1, (255, 255, 255))
    # WIN.blit(score1_label, (20, 10)
    # WIN.blit(score2_label, (WIDTH - 20 - score2_label.get_width(), 10))
    player1.score_count(40, 10, WIN)
    player2.score_count(WIDTH - 20 - 220, 10, WIN)
    player1.draw(WIN)
    player2.draw(WIN)
    pygame.display.update()

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        redraw_window()
        keys_pressed = pygame.key.get_pressed()
        move_player(keys_pressed)
        player1.move_lasers(laser_vel_1, player2)
        player2.move_lasers(laser_vel_2, player1)
    pygame.quit()

if __name__=="__main__":
    main()