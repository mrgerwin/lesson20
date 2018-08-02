import pygame as pygame
import sys as sys
import random as random

class Ball:
    def __init__(self, surface, color):
        self.surface = surface
        self.color = color
        self.image = pygame.Surface((40,40))
        pygame.draw.circle(self.image, self.color, (20, 20), 20)
        self.rect = self.image.get_rect()
        self.speed = [0,0]
        self.rect.x = self.surface.get_width()//2
        self.rect.y = self.surface.get_height()//2
    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
    def set_speed(self, x, y):
        self.speed[0]=x
        self.speed[1]=y
    def move(self):
        if self.rect.left<=0 and self.speed[0]<0:
            self.speed[0] = -self.speed[0]
        if self.rect.top<=0 and self.speed[1]<0:
            self.speed[1] = -self.speed[1]
        if self.rect.right>=self.surface.get_width() and self.speed[0] > 0:
            self.speed[0] = -self.speed[0]
        if self.rect.bottom>=self.surface.get_height() and self.speed[1] >0:
            self.speed[1] = -self.speed[1]
        self.rect.x = self.rect.x+self.speed[0]
        self.rect.y = self.rect.y + self.speed[1]
    def collide(self, paddles):
        if self.rect.collidelist(paddles) > -1:
            self.speed[0] = 0
            self.speed[1] = 0
class Paddle:
    def __init__(self, surface, color, left, top):
        self.surface = surface
        self.color = color
        self.image = pygame.Surface((20, 100))
        self.image.fill(color)
        self.rect = pygame.Rect((left, top), (20, 100))
        pygame.draw.rect(self.surface, self.color, self.rect)
        self.speed = 0
        
    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def move(self):
        if self.rect.y <= 0 and self.speed < 0:
            self.speed = 0
        if self.rect.bottom >= self.surface.get_height() and self.speed >0:
            self.speed = 0
        self.rect.y = self.rect.y + self.speed
    def go_up(self):
        self.speed = -2
    def go_down(self):
        self.speed = 2
    def stop(self):
        self.speed = 0

class Pong:
    def __init__(self, surface, Paddles, Balls):
        self.left_score = 0
        self.right_score = 0
        self.Paddles = Paddles
        self.Balls = Balls
        self.surface = surface
        self.font = pygame.font.init()
        self.font = pygame.font.Font(None, 72)
        self.pause = True
        self.end = False
    
    def increment_game(self):
        for ball in self.Balls:
            ball.move()
            ball.draw()
        for paddle in self.Paddles:
            paddle.move()
            paddle.draw()
        for ball in self.Balls:
            if ball.rect.collidelist(Paddles)>-1:
                ball.speed[0] = -ball.speed[0]
            if ball.rect.right >= self.surface.get_width():
                ball.set_speed(0,0)
                ball.rect.x = self.surface.get_width()//2
                ball.rect.y = self.surface.get_height()//2
                self.increment_score("Left")
            if ball.rect.x <= 0:
                ball.set_speed(0,0)
                ball.rect.x = self.surface.get_width()//2
                ball.rect.y = self.surface.get_height()//2
                self.increment_score("Right")
        self.draw_score()
        self.check_victory()
        return self.end
                
    def serve(self):
        for ball in self.Balls:
            ball.speed[0] = random.randrange(-3, 3, 1)
            ball.speed[1] = random.randrange(-3, 3, 1)
        if ball.speed[0] == 0:
            ball.speed[0] = 2
        self.pause = False
            
    def increment_score(self, side):
        if side == "Left":
            self.left_score = self.left_score + 1
        else:
            self.right_score = self.right_score + 1
        self.pause = True
        
    def check_victory(self):
        if self.left_score >= 2:
            text = self.font.render("The Left Player Has Won!!!", True, white)
            self.end = True
        elif self.right_score >= 2:
            text = self.font.render("The Right Player Has Won!!!", True, white)
            self.end = True
        else:
            text = self.font.render("", True, white)
            self.end = False
        
        if self.end == True:
            self.surface.blit(text, (200, self.surface.get_height()//2))
        
        return self.end
    
    def draw_score(self):
        text = self.font.render(str(self.left_score), True, white)
        self.surface.blit(text, (self.surface.get_width()//4, 24))
        text = self.font.render(str(self.right_score), True, white)
        self.surface.blit(text, (self.surface.get_width()//4*3, 24))
    
    def reset(self):
        self.left_score = 0
        self.right_score =0

fps = 60
ScreenSize = (1000, 600)
black = (0,0,0)
red = (255,0,0)
blue = (0,255,0)
white = (255, 255, 255)
timer = pygame.time.Clock()
window = pygame.display.set_mode(ScreenSize)

gameBall = Ball(window, red)
gameBall.set_speed(0, 0)

leftPaddle = Paddle(window, white, 0, 0)
rightPaddle = Paddle(window, white, ScreenSize[0]-20, 0)

Paddles = [leftPaddle, rightPaddle]
Balls = [gameBall]
theGame = Pong(window, Paddles, Balls)
result = False
quit = False
while quit == False:
    for event in pygame.event.get():
        #Check to see if it is a keyboard event or a quit event
        if event.type == pygame.QUIT:
            #if a quit event end the loop and quit pygame
          quit = True
          pygame.quit()
          sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                leftPaddle.go_up()
            elif event.key == pygame.K_DOWN:
                leftPaddle.go_down()
            elif event.key == pygame.K_KP8:
                rightPaddle.go_up()
            elif event.key == pygame.K_KP2:
                rightPaddle.go_down()
            elif event.key == pygame.K_SPACE and theGame.pause == True:
                if result == True:
                    theGame.reset()
                theGame.serve()
        elif event.type == pygame.KEYUP:
            #When you let up on the key, stops the paddle from moving
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                leftPaddle.stop()
            elif event.key ==pygame.K_KP8 or event.key == pygame.K_KP2:
                rightPaddle.stop()
    window.fill(black)
    result = theGame.increment_game()
    pygame.display.flip()
    timer.tick(fps)