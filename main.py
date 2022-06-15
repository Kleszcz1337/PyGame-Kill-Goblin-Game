import pygame

pygame.init()

#tworzenie okna gry
screenWidth = 500
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("Animation game")

background = pygame.image.load('images/background.jpg')
characterStanding = pygame.image.load('images\hero\standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound("sounds/bullet.mp3")
hitSound = pygame.mixer.Sound("sounds\hit.mp3")

music = pygame.mixer.music.load("sounds\music.mp3")
pygame.mixer.music.play(-1)

score = 0


#data of character
class player():
    walkRight = [   
        pygame.image.load('images\hero\R1.png'), 
        pygame.image.load('images\hero\R2.png'), 
        pygame.image.load('images\hero\R3.png'), 
        pygame.image.load('images\hero\R4.png'), 
        pygame.image.load('images\hero\R5.png'), 
        pygame.image.load('images\hero\R6.png'), 
        pygame.image.load('images\hero\R7.png'), 
        pygame.image.load('images\hero\R8.png'), 
        pygame.image.load('images\hero\R9.png')
        ]
    walkLeft = [
        pygame.image.load('images\hero\L1.png'), 
        pygame.image.load('images\hero\L2.png'), 
        pygame.image.load('images\hero\L3.png'), 
        pygame.image.load('images\hero\L4.png'), 
        pygame.image.load('images\hero\L5.png'), 
        pygame.image.load('images\hero\L6.png'), 
        pygame.image.load('images\hero\L7.png'), 
        pygame.image.load('images\hero\L8.png'), 
        pygame.image.load('images\hero\L9.png')
        ]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCounter = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(player.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(player.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(player.walkRight[0], (self.x, self.y))
            else:
                win.blit(player.walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255, 0 ,0), self.hitbox, 2)

    def hit(self):
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-5", 1, (255, 0, 0))
        win.blit(text, (screenWidth/2 - (text.get_width()/2), screenHeight/2))
        pygame.display.update()
        i = 0
        while i < 150:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [
        pygame.image.load('images\enemie\R1E.png'),
        pygame.image.load('images\enemie\R2E.png'), 
        pygame.image.load('images\enemie\R3E.png'), 
        pygame.image.load('images\enemie\R4E.png'), 
        pygame.image.load('images\enemie\R5E.png'), 
        pygame.image.load('images\enemie\R6E.png'), 
        pygame.image.load('images\enemie\R7E.png'), 
        pygame.image.load('images\enemie\R8E.png'), 
        pygame.image.load('images\enemie\R9E.png'), 
        pygame.image.load('images\enemie\R10E.png'), 
        pygame.image.load('images\enemie\R11E.png')
        ]
    walkLeft = [
        pygame.image.load('images\enemie\L1E.png'), 
        pygame.image.load('images\enemie\L2E.png'), 
        pygame.image.load('images\enemie\L3E.png'), 
        pygame.image.load('images\enemie\L4E.png'), 
        pygame.image.load('images\enemie\L5E.png'), 
        pygame.image.load('images\enemie\L6E.png'), 
        pygame.image.load('images\enemie\L7E.png'), 
        pygame.image.load('images\enemie\L8E.png'), 
        pygame.image.load('images\enemie\L9E.png'), 
        pygame.image.load('images\enemie\L10E.png'), 
        pygame.image.load('images\enemie\L11E.png')
        ]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        if self.visible:
            self.move()
            if self.walkCount + 1 >= 33: #11 pics * 3
                self.walkCount = 0

            if self.vel > 0:
                win.blit(enemy.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(enemy.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0]-11, self.hitbox[1]-20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0]-11, self.hitbox[1]-20, 50 - (5 * (10 - self.health)), 10))
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel *= -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] + self.vel:
                self.x += self.vel
            else:
                self.vel *= -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


def redrawGameWindow():
    win.blit(background, (0,0))
    text = font.render("Your Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (320, 10))
    firstEnemie.draw(win)
    man.draw(win)

    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()

font = pygame.font.SysFont('comicsans', 20, True)

man = player(200, 410, 64, 64)
bullets = []
shoopLoop = 0

firstEnemie = enemy(100, 410, 64, 64, 300)

run = True
while run:
    clock.tick(27)

    if man.hitbox[0] >= firstEnemie.hitbox[0] and man.hitbox[0] <= firstEnemie.hitbox[0] + firstEnemie.hitbox[2]:
            if man.hitbox[1] >= firstEnemie.hitbox[1] and man.hitbox[1] <= firstEnemie.hitbox[1] + firstEnemie.hitbox[3]:
                hitSound.play()
                score -= 5
                man.hit()

    if shoopLoop > 0:
        shoopLoop += 1
    if shoopLoop > 6:
        shoopLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x >= firstEnemie.hitbox[0] and bullet.x <= firstEnemie.hitbox[0] + firstEnemie.hitbox[2]:
            if bullet.y >= firstEnemie.hitbox[1] and bullet.y <= firstEnemie.hitbox[1] + firstEnemie.hitbox[3]:
                hitSound.play()
                firstEnemie.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < screenWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    keys = pygame.key.get_pressed()

    mouse = pygame.mouse.get_pressed() #(left, middle, right)
    if mouse[0] and shoopLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(man.x+40, man.y+40, 6, (0, 0, 0), facing))

        shoopLoop = 1

    if keys[pygame.K_a] and man.x >= man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_d] and man.x < screenWidth - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        if keys[pygame.K_w]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCounter >= -10:
            neg = 1
            if man.jumpCounter < 0:
                neg = -1

            man.y -= (man.jumpCounter ** 2) / 2 * neg
            man.jumpCounter -= 1
        else:
            man.isJump = False
            man.jumpCounter = 10

    redrawGameWindow()

pygame.quit()







