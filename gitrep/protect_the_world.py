from fractions import Fraction
import pygame , time
from pygame.locals import *
import math
from random import randint as Rint
from random import choice
import os
cwd = os.getcwd()
#initialising
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(.5)
clock = pygame.time.Clock()


#colours
black = (0, 0, 0) 

#screen size
WIDTH = 800
HEIGHT = WIDTH
center = WIDTH//2

#mouse
pygame.mouse.set_visible(False)
MANUAL_CURSOR = pygame.image.load(cwd+r'/data/sprites/cursor1.png')
MANUAL_CURSOR_scale = WIDTH//30
MANUAL_CURSOR = pygame.transform.scale(MANUAL_CURSOR, (MANUAL_CURSOR_scale,MANUAL_CURSOR_scale))

#tick and meteor amount start
global tick
global amount
global meteorList
global Tscore
global Hscore
global rep
global rep_check
global turret_amount
global turretTickMax
global shield
global repMult

rep = 0
repMult = 1
turretTick = 0
turretTickMax = 100
tick = 0
amount = 1
meteorList = []
Tscore = 0
Hscore = 0
rep_check = True
game_over = False

bullet_speed = 5
turret_amount = 0
shield = 50
maxspeed = 150
minspeed = 200

def load_save():
    global rep
    global repMult
    global turretTickMax
    global bullet_speed
    global turret_amount
    global shield
    global maxspeed
    global minspeed
    
    try:
        f = open(cwd+"/data/save.txt", "r")
        lines = f.readlines()

        for line in lines:
            if "rep=" in line:
                rep = float(line[4:])

            
            if "repMult=" in line:
                repMult = float(line[8:])
        
            
            if "turretTickMax=" in line:
                turretTickMax = float(line[14:])
            
            
            if "bullet_speed=" in line:
                bullet_speed = float(line[13:])
            
            
            if "turret_amount=" in line:
                turret_amount = float(line[14:])
            
            
            if "shield=" in line:
                shield = float(line[7:])
        
            
            if "maxspeed=" in line:
                maxspeed = float(line[9:])
        
            
            if "minspeed=" in line:
                minspeed = float(line[9:])
        

            if "bullet speed=" in line:
                item1.price = float(line[13:])

            if "turrets=" in line:
                item2.price = float(line[8:])

            if "turret speed=" in line:
                item3.price = float(line[13:])

            if "shields=" in line:
                item4.price = float(line[8:])

            if "rep multiplier=" in line:
                item5.price = float(line[15:])

            if "meteor speed=" in line:
                item6.price = float(line[13:])

    except:
        pass

#window setup
display_surface = pygame.display.set_mode((WIDTH, HEIGHT )) 
pygame.display.set_caption('operation ablation') 
class music():

    def __init__(self, name):
        self.name = name
        self.track = cwd+r"/data/sounds/" + name + ".wav"

    def play(self):

        get_busy = pygame.mixer.music.get_busy()
        if get_busy == 0:
            pygame.mixer.music.load(self.track)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
        else:
            pass

    def reset(self):
        pygame.mixer.music.stop()

#earth
class OGEarth():

    def __init__(self):
        earth = pygame.image.load(cwd+r'/data/sprites/earth.png')
        scale = WIDTH//5
        self.scale = scale
        self.earth = pygame.transform.scale(earth, (scale,scale))
        self.earthPos = (WIDTH/2)-(scale//2) , (HEIGHT/2)-(scale//2)
        self.earth_rect = pygame.Rect(*display_surface.get_rect().center, 0, 0).inflate(scale//2, scale//2)
        self.OGEarthIMG = self.earth
        self.rot_angle = 0

    def draw(self):
        display_surface.blit(self.earth, self.earthPos)

    def earth_move(self):
        self.rot_angle += 1
        self.earth = rot_center(self.OGEarthIMG, self.rot_angle)

#background
class Background():
    def __init__(self, No):
        self.BG = pygame.image.load(cwd+r'/data/sprites/starbackground.png').convert()
        self.rect = self.BG.get_rect()

        if No == 1:
            self.BGPOSX = 0

            self.BGPOS = self.BGPOSX

        if No == 2:
            self.BGPOSX = -self.rect.width

            self.BGPOS = self.BGPOSX

    def move(self):
        if self.BGPOSX >= self.rect.width:
            self.BGPOSX = -self.rect.width
        else:
            self.BGPOSX += 1
        
        self.BGPOS = self.BGPOSX,0

    def draw(self):
        display_surface.blit(self.BG, self.BGPOS)

#meteors
class normalMeteor():

    global minspeed
    global maxspeed

    maxscale = 20
    minscale = 10

    def __init__(self):
        #A ball need a position (x,y), a radius, a color and the screen where we will paint it, therefore
        #the constructor will take these as arguments and save their values in variables of the ball class by using the word self
        scaleMult = Rint( normalMeteor.minscale , normalMeteor.maxscale )
        meteorimg = pygame.image.load(cwd+r'/data/sprites/meteor.png')
        scale = WIDTH//scaleMult
        self.scale = scale
        self.angle = 0


        meteorimg = pygame.transform.scale(meteorimg, (scale,scale))
        meteorimg.convert()

        self.meteorimg = meteorimg
        self.OGmeteorimg = meteorimg
        
        xOrY = Rint(0,1)
        if xOrY == 1:
            XY = int(choice( [-scale , WIDTH + scale] )) ,Rint(0,WIDTH)
        else:
            XY = Rint(0,WIDTH) , int(choice( [-scale ,WIDTH + scale] ))

        self.meteorimgRect = pygame.Rect(*display_surface.get_rect().center, 0, 0).inflate(scale*2, scale*2)
        self.meteorimgRect.center = (XY)
        x,y = XY
        self.X = x
        self.Y = y

        dx, dy = (center - x, center - y)
        speed_choice = Rint(maxspeed, minspeed)
        self.stepx, self.stepy = (dx / speed_choice, dy / speed_choice)
        self.hit = pygame.mixer.Sound(cwd+r"/data/sounds/hit" + str(Rint(1,3)) + ".wav")
        self.shot = pygame.mixer.Sound(cwd+r"/data/sounds/Mhit" + str(Rint(1,3)) + ".wav")

    #The draw function will be responsible for drawing the ball in the screen
    def draw(self):
        imgx = self.X - (self.scale)//2 
        imgy = self.Y - (self.scale)//2 


        display_surface.blit(self.meteorimg, (imgx ,imgy))
        #pygame.draw.rect(display_surface, (255,0,0), self.meteorimgRect)

    def move(self):
        self.angle += Rint(1,3)
        meteorimg = rot_center(self.OGmeteorimg, self.angle)
        self.meteorimg = meteorimg
        
        self.X += self.stepx
        self.Y += self.stepy
        self.meteorimgRect.center = (self.X , self.Y)
        #self.meteorimgRect.center = (x+self.scale//2,y+self.scale//2)
    
    def is_collided_with(self, sprite):
        if self.meteorimgRect.colliderect(sprite):
            scaleMult = Rint( normalMeteor.minscale , normalMeteor.maxscale )
            meteorimg = pygame.image.load(cwd+r'/data/sprites/meteor.png')
            scale = WIDTH//scaleMult
            self.scale = scale
            self.angle = 0


            meteorimg = pygame.transform.scale(meteorimg, (scale,scale))
            meteorimg.convert()

            self.meteorimg = meteorimg
            self.OGmeteorimg = meteorimg
            
            xOrY = Rint(0,1)
            if xOrY == 1:
                XY = int(choice( [-scale , WIDTH + scale] )) ,Rint(0,WIDTH)
            else:
                XY = Rint(0,WIDTH) , int(choice( [-scale ,WIDTH + scale] ))

            self.meteorimgRect = pygame.Rect(*display_surface.get_rect().center, 0, 0).inflate(scale//2, scale//2)
            self.meteorimgRect.topleft = (XY)
            x,y = XY
            self.X = x
            self.Y = y

            dx, dy = (center - x, center - y)
            speed_choice = Rint(maxspeed, minspeed)

            self.stepx, self.stepy = (dx / speed_choice, dy / speed_choice)
            self.hit = pygame.mixer.Sound(cwd+r"/data/sounds/hit" + str(Rint(1,3)) + ".wav")
            self.shot = pygame.mixer.Sound(cwd+r"/data/sounds/Mhit" + str(Rint(1,3)) + ".wav")

        #pygame.draw.rect(display_surface, (0,0,0), self.meteorimgRect)

            global Tscore
            global shield
            global repMult
            if sprite == earth1.earth_rect:
                Tscore -= shield
                pygame.mixer.Sound.play(self.hit)
            for bullet in bullets:
                if sprite == bullet.bullet_rect:
                    Tscore += 1 * repMult
                    pygame.mixer.Sound.play(self.shot)


        return self.meteorimgRect.colliderect(sprite)

class Bullet():

    def __init__(self, x, y , mx = False  , my = False):

        self.pos = (x, y)

        if not mx and not my:
            mx, my = pygame.mouse.get_pos()

        else:
            pass

        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((10, 4)).convert_alpha()
        self.bullet.fill((255, 255, 255))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = bullet_speed
        self.bullet_rect = self.bullet.get_rect(center = self.pos)
        shot = pygame.mixer.Sound(cwd+r"/data/sounds/laser" + str(Rint(1,3)) + ".wav")
        pygame.mixer.Sound.play(shot)

    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        self.bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, self.bullet_rect)  

class ShopItems():
    price_multiplier = 1.5

    def __init__ (self,name,price , place, img):
        self.name = name
        self.price = price


        size = 100
        self.size = 100

        a = (WIDTH//2 *.5) - size//2
        b = (WIDTH//2) - size//2
        c = (WIDTH//2 * 1.5) - size//2

        z = (WIDTH//2 *.5) - size//2
        x = (WIDTH//2) - size//2
        v = (WIDTH//2 * 1.5) - size//2

        if True:
            if place == 1:
                pos = a , z
                self.text_pos = a+size//2, z+size//2

            if place == 2:
                pos = b, z
                self.text_pos = b+size//2, z+size//2

            if place == 3:
                pos = c, z
                self.text_pos = c+size//2, z+size//2

            if place == 4:
                pos = a, x
                self.text_pos = a+size//2, x+size//2

            if place == 5:
                pos = b, x
                self.text_pos = b+size//2, x+size//2

            if place == 6:
                pos = c, x
                self.text_pos = c+size//2, x+size//2

            if place == 7:
                pos = a, v
                self.text_pos = a+size//2, v+size//2

            if place == 8:
                pos = b, v
                self.text_pos = b+size//2, v+size//2

            if place == 9:
                pos = c, v
                self.text_pos = c+size//2, v+size//2

        itemBG = pygame.image.load(cwd+r'/data/sprites/shopitemBG.png')
        itemIMG = pygame.image.load(cwd+r"/data/sprites/" + img)

        itemIMG = pygame.transform.scale(itemIMG, (size,size))
        itemBG = pygame.transform.scale(itemBG, (size,size))

        itemBG.convert()
        itemIMG.convert()

        self.itemBG = itemBG , itemIMG

        self.area = pygame.Rect(pos[0],pos[1],100,100)

    def draw(self):

        #pygame.draw.rect(display_surface,(255,0,0),self.area)

        item_text = set_text(self.name + str(self.price), self.text_pos[0] , self.text_pos[1], 1)

        IPos = item_text[1]
        IPos.center = self.text_pos[0] - self.size//2,self.text_pos[1] - self.size//2

        display_surface.blit(self.itemBG[0], (IPos.center))
        display_surface.blit(self.itemBG[1], (IPos.center))
        item_text = set_text(f"{self.name} ${self.price:g}".format(float(str(round(self.price,0)))), self.text_pos[0], self.text_pos[1] + (self.size//1.5), self.size//5)
        display_surface.blit(item_text[0], item_text[1])

    def purchase(self):
        global rep
        global bullet_speed
        global turretTickMax
        global turret_amount
        global shield
        global minspeed
        global maxspeed
        global repMult
        
        power_up = pygame.mixer.Sound(cwd+r"/data/sounds/powerup.wav")
        error = pygame.mixer.Sound(cwd+r"/data/sounds/error.wav")

        if self.name == "bullet speed" and self.price <= rep and bullet_speed != 20:

            bullet_speed += 1
            rep -= self.price
            self.price *= ShopItems.price_multiplier
            self.price = round(self.price, 0)
            pygame.mixer.Sound.play(power_up)


        elif self.name == "turrets" and self.price <= rep and turret_amount != 9:

            turret_amount += 1
            turret_List.append(turret(turret_amount))
            rep -= self.price
            self.price *= ShopItems.price_multiplier
            self.price = round(self.price, 0)
            pygame.mixer.Sound.play(power_up)

        elif self.name == "turret speed" and self.price <= rep and turretTickMax > 5:


            turretTickMax -= 5

            rep -= self.price
            self.price *= ShopItems.price_multiplier
            self.price = round(self.price, 0)
            pygame.mixer.Sound.play(power_up)

        elif self.name == "shields" and self.price <= rep and shield > 5:
            shield -= 5
            rep -= self.price
            self.price *= ShopItems.price_multiplier
            self.price = round(self.price, 0)
            pygame.mixer.Sound.play(power_up)

        elif self.name == "meteor speed" and self.price <= rep and minspeed < 400:
            minspeed += 10
            maxspeed += 10
            rep -= self.price
            self.price *= ShopItems.price_multiplier
            self.price = round(self.price, 0)
            pygame.mixer.Sound.play(power_up)

        elif self.name == "rep multiplier" and self.price <= rep and repMult < 5:
            repMult += .1
            rep -= self.price
            self.price *= ShopItems.price_multiplier
            self.price = round(self.price, 0)
            pygame.mixer.Sound.play(power_up)

        elif self.name == "reset":
            repMult = 1
            turretTick = 0
            turretTickMax = 100
            tick = 0
            amount = 1
            meteorList = []
            Tscore = 0
            Hscore = 0
            rep_check = True
            game_over = False

            bullet_speed = 5
            turret_amount = 0
            shield = 50
            maxspeed = 150
            minspeed = 200
            pygame.mixer.Sound.play(power_up)
            item1.price = 50
            item2.price = 100
            item3.price = 100
            item4.price = 50
            item5.price = 150
            item6.price = 69

        else:
            pygame.mixer.Sound.play(error)

class turret():

    def __init__(self, turret_amount):

        if turret_amount == 1:
            self.start = WIDTH//2, WIDTH//2
            self.angle = WIDTH, WIDTH//2
        
        if turret_amount == 2:
            self.start = WIDTH//2, WIDTH//2
            self.angle = 0, WIDTH//2
        
        if turret_amount == 3:
            self.start = WIDTH//2, WIDTH//2
            self.angle = WIDTH//2, 0
        
        if turret_amount == 4:
            self.start = WIDTH//2, WIDTH//2
            self.angle = WIDTH//2, WIDTH

        if turret_amount == 5:
            self.start = WIDTH//2, WIDTH//2
            self.angle = WIDTH, 0
        
        if turret_amount == 6:
            self.start = WIDTH//2, WIDTH//2
            self.angle = WIDTH, WIDTH

        if turret_amount == 7:
            self.start = WIDTH//2, WIDTH//2
            self.angle = 0, WIDTH

        if turret_amount == 8:
            self.start = WIDTH//2, WIDTH//2
            self.angle = 1, 0

        if turret_amount == 9:
            self.start = WIDTH//2, WIDTH//2
            self.angle = 0, 0

    def shoot(self):
        global turretTick
        global turretTickMax

        #Bullet(self.start[0],self.start[1] , self.angle[0],self.angle[1])

        bullets.append(Bullet(self.start[0],self.start[1] , self.angle[0],self.angle[1]))
        turretTick = turretTickMax

    def tick_change(self , change):
        self.tick -= change

#function to add meteors
def addMeteor():
    global meteorList
    global amount
    if tick % 500 == 1:
        amount+=1
        newMeteor = "Meteor" + str(amount)
        globals()[newMeteor]=normalMeteor()
        meteorList.append(newMeteor)
        meteorList[-1] = normalMeteor()
    else:
        pass

#function to update gameObjects
def updateAll():
    global meteorList
    global turretTick
    display_surface.fill(black)
    bg1.move()
    bg1.draw()
    bg2.move()
    bg2.draw()



    for i in meteorList:
        i.move()
        i.is_collided_with(earth1.earth_rect)
        for bullet in bullets:
            i.is_collided_with(bullet.bullet_rect)
        i.draw()

    for bullet in bullets:
        bullet.draw(display_surface)
    score()

    for bullet in bullets[:]:
        bullet.update()
        if not display_surface.get_rect().collidepoint(bullet.pos):
            bullets.remove(bullet)

    if turretTick <= 0:
        for shootT in turret_List:
            shootT.shoot()

    turretTick -= 1


    earth1.earth_move()
    earth1.draw()

def updateEssential():

    x,y = pygame.mouse.get_pos()
    x -= MANUAL_CURSOR_scale//2
    y -= MANUAL_CURSOR_scale//2
    display_surface.blit( MANUAL_CURSOR, ( x,y ) )

def updateEnd():
    display_surface.fill(black)
    bg1.move()
    bg1.draw()
    bg2.move()
    bg2.draw()
    earth1.earth_move()
    earth1.draw()
    endScreen()

    for i in shop:
        i.draw()


#function to rotate images, without distorition
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image 

def score():
    global Tscore
    global Hscore
    if Tscore > Hscore:
        Hscore = round(Tscore,0)

    score = set_text("reputation: {0:g}".format(float(str(round(Tscore,0)))) , WIDTH//1.1, WIDTH//30, 20)
    display_surface.blit(score[0], score[1])

def endScreen():
    global Hscore
    global rep
    global rep_check_count

    if rep_check_count == 0:
        rep += Hscore

    if type(rep) == float:
        rep = round(rep , 0)

    score = set_text("highest reputation: {0:g}".format(float(str(Hscore))), WIDTH//2, WIDTH//10, 50)
    display_surface.blit(score[0], score[1])
    rep_T = set_text("total rep:{0:g}".format(float(str(rep))), WIDTH//2, WIDTH*.9, 50)
    display_surface.blit(rep_T[0], rep_T[1])
    restart_note = set_text("play again with R!", WIDTH//1.1, WIDTH//30, 15)
    display_surface.blit(restart_note[0], restart_note[1])
    restart_note = set_text("quit with the escape key!", WIDTH//8, WIDTH//30, 15)
    display_surface.blit(restart_note[0], restart_note[1])

def set_text(string, coordx, coordy, fontSize): #Function to set text

    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (255, 255, 255)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)

def play_music():
    global game_over
    if game_over:
        main_music.reset()
        menu_music.play()

    else:
        menu_music.reset()
        main_music.play()
        pass

#adding earth and backgrounds
bg1 = Background(1)
bg2 = Background(2)
earth1 = OGEarth()


item1 = ShopItems("bullet speed" , 50, 1, "faster-2-arrows.png")
item2 = ShopItems("turrets" , 100, 2, "turret.png")
item3 = ShopItems("turret speed" , 110, 3 , "turretSpeed.png")
item4 = ShopItems("shields" , 50, 4 , "shield.png")
item5 = ShopItems("rep multiplier" , 115, 5 , "rep multiplier.png")
item6 = ShopItems("meteor speed" , 69, 6 , "slower-arrows.png")
item8 = ShopItems("reset" , 0, 8 , "cursor1.png")

menu_music = music("menu music")
main_music = music("main music")

shop = [item1,
        item2,
        item3,
        item4,
        item5,
        item6,
        item8]

bullets = []
turret_List = []
load_save()

play_music()
#main game loop
while True :
    #add meteors
    addMeteor()

    #update gameObjects

    if game_over:
        updateEnd()
        rep_check_count += 1
    else:
        updateAll()
    updateEssential()

    #quit game
    for event in pygame.event.get() : 

        if event.type == pygame.QUIT or event.type == KEYDOWN:
        	if event.type == pygame.QUIT or event.key == K_ESCAPE:
	            f = open(cwd + "/data/save.txt","a+")
	            f.truncate(0)
	            save = f"rep={str(rep)}\nrepMult={str(repMult)}\nturretTickMax={str(turretTickMax)}\nbullet_speed={str(bullet_speed)}\nturret_amount={str(turret_amount)}\nshield={str(shield)}\nmaxspeed={str(maxspeed)}\nminspeed={str(minspeed)}"
	            for k in shop:
	                save += f"\n{k.name}={str(k.price)}"
	            f.write(save)
	            f.close()
	            pygame.quit() 
	            quit() 
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_over == False:
            pos = (center,center)
            bullets.append(Bullet(*pos))

        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            click = pygame.mixer.Sound(cwd+r"/data/sounds/click" + str(Rint(1,3)) + ".wav")
            pygame.mixer.Sound.play(click)




        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                bullets.clear()
                meteorList.clear()
                Tscore = 0
                tick = 0
                Hscore = 0
                game_over = False
                play_music()

            elif event.key == pygame.K_r and game_over == False:
                meteorList.clear()
                rep_check_count = 0
                game_over = True
                Tscore = 1
                play_music()


        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            for i in shop:
                if i.area.collidepoint(pygame.mouse.get_pos()):
                    i.purchase()    


    if pygame.mouse.get_pressed()[0] and game_over == False:
        try:
            pos = (center,center)
            if tick % 100 == 1:
                bullets.append(Bullet(*pos))
        
        except AttributeError:
            pass

    #update window

    #update tickrate
    if Tscore >= 0:
        tick+=1

    if Tscore < 0:
        meteorList.clear()
        rep_check_count = 0
        game_over = True
        Tscore = 1
        play_music()
    
    pygame.display.update()
    #set FPS
    clock.tick(30)