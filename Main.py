import pygame,sys,math
#health bar & text things
#nb - pygame rectangles (wheretodraw,color, (x,y,length,width)) :p
x = 400
y = 400
vel = 10
spell1 = ["Rongaire Balorum Eunarach Vicit Romnia."]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, startx, starty):
        super().__init__() #inherits sprite
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center = (startx,starty))

        #health variables
        self.maximum_health = 1000
        self.health_bar_length = 100
        self.health_ratio = self.maximum_health/self.health_bar_length #for converting health -> bar length
        self.current_health = 1000
        self.target_health = 1000
        self.health_transition_speed = 5

    def update(self, x, y): 
        self.health(x, y)

    #subtract from player health
    def take_damage(self,damage):
        if self.target_health > 0:
            self.target_health -= damage
        if self.target_health <= 0:
            self.target_health = 0

    #draw health bar
    def health(self, x, y):
        transition_width = 0
        transition_color = (0,255,0)

        #if player took damage -> yellow/orange rectangle
        if self.current_health > self.target_health:
            self.current_health -= self.health_transition_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (255,200,0)

        #creates rectangles
        health_bar_rect = pygame.Rect(x, y,self.current_health/self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,45,transition_width/self.health_ratio,25)
        transition_bar_rect.normalize() #flip -ive rectangle
        #draws main heath bar, transitional health bar & surrounding white grid
        pygame.draw.rect(screen, (255,0,0), health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen,(255,255,255), (x,y, self.health_bar_length,25),4)


class Player(pygame.sprite.Sprite):
    
    def __init__(self, startx, starty):
        super().__init__() #inherits sprite
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center = (startx,starty))
        
        #health variables
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health/self.health_bar_length #for converting health -> bar length
        self.current_health = 1000
        self.target_health = 1000
        self.health_transition_speed = 5

    def update(self): 
        self.health()
        self.movement()

    #subtract from player health
    def take_damage(self,damage):
        if self.target_health > 0:
            self.target_health -= damage
        if self.target_health <= 0:
            self.target_health = 0
            
    #add to player health
    '''def get_health(self,health):
        if self.target_health < self.maximum_health:
            self.target_health += health
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health'''
    
    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= vel

        if keys[pygame.K_RIGHT] :
            if self.rect.x < 760:
                self.rect.x += vel

        if keys[pygame.K_UP]:
            if self.rect.y > 0:
                self.rect.y -= vel

        if keys[pygame.K_DOWN]:
            if self.rect.y < 740:
                self.rect.y += vel
    
    #draw health bar
    def health(self):
        transition_width = 0
        transition_color = (0,255,0)

        #if player gained health -> green rectangle
        '''if self.current_health < self.target_health:
            self.current_health += self.health_transition_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (0,255,0)'''

        #if player took damage -> yellow/orange rectangle
        if self.current_health > self.target_health:
            self.current_health -= self.health_transition_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (255,200,0)

        #creates rectangles
        health_bar_rect = pygame.Rect(10,45,self.current_health/self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,45,transition_width/self.health_ratio,25)
        transition_bar_rect.normalize() #flip -ive rectangle
        #draws main heath bar, transitional health bar & surrounding white grid
        pygame.draw.rect(screen, (255,0,0), health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen,(255,255,255), (10,45, self.health_bar_length,25),4)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, angle, reverse,clock,startx, starty,delay=False):
        super().__init__() #inherits sprite
        self.angle = angle
        self.startx = startx
        self.starty = starty
        self.rotate_clock = 0
        self.delay_val = clock
        self.delay = delay
        
        self.image = pygame.Surface((20,20))
        self.image.fill((240,0,240))
        self.rect = self.image.get_rect(center = (self.startx,self.starty))

        self.angle_change = 1

        self.projectile_xspeed = int(3 * reverse)
        self.projectile_yspeed = angle
        
    def update(self):
       self.change_position()
      # self.collision(400)
       self.rotate_clock += 1
       
       run = True
       if self.delay:
           if self.rotate_clock < self.delay_val:
               run = False
           
       if (self.rotate_clock % 40 == 0) and run :
           if self.projectile_yspeed == 0:
                 self.angle_change = -1
           if self.projectile_yspeed == -15:
                 self.angle_change  = 1
           #print(self.projectile_yspeed)
           self.projectile_yspeed += self.angle_change 
                
    def collision(self,radius):
        distance = ((self.startx -self.rect.x)**2+(self.starty -self.rect.y)**2)**(1/2)
        if distance >= radius:
            self.reset_position()
    
    def reset_position(self):
        self.rect.x = self.startx
        self.rect.y = self.starty

    def change_position(self):
        if  (self.rect.x >= 800) or (self.rect.y >= 800) or (self.rect.x <= 0) or (self.rect.y <= 0):
             self.reset_position()
        else:
            if self.projectile_xspeed > 0:
                if  self.rect.x <= 800:
                    self.rect.x += self.projectile_xspeed
                if  self.rect.y <= 800:
                   self.rect.y += self.projectile_yspeed
            else:
                if  self.rect.x > 0:
                    self.rect.x += self.projectile_xspeed
                if  self.rect.y > 0:
                    self.rect.y += self.projectile_yspeed
                
            
            

##    def change_position(self):
##        if self.projectile_xspeed > 0:
##            if  self.rect.x <= 800:
##                self.rect.x += self.projectile_xspeed
##            else:
##                self.reset_position()
##            if  self.rect.y <= 800:
##                self.rect.y += self.projectile_yspeed
##            else:
##                 self.reset_position()
##        else:
##            if  self.rect.x > 0:
##                self.rect.x += self.projectile_xspeed
##            else:
##                self.reset_position()
##                
##            if  self.rect.y > 0:
##                self.rect.y += self.projectile_yspeed
##            else:
##                 self.reset_position()
            
            
        
#setup
pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle(Player(400,400))

enemy1x = 20
enemy1y = 780

enemy1 =  pygame.sprite.GroupSingle(Enemy(enemy1x,enemy1y))
projectiles = [Projectile(0,1,0,0,0) for i in range(15)]

for i in range(5):
    projectiles[i] = pygame.sprite.Group(Projectile(-i,1,0,enemy1x,enemy1y))
for i in range(4,10):
    projectiles[i] = pygame.sprite.Group(Projectile(-i,1,40,enemy1x,enemy1y, True))
for i in range(9,15):
    projectiles[i] = pygame.sprite.Group(Projectile(-i,1,80,enemy1x,enemy1y, True))

enemy2x = 780
enemy2y = 780
enemy2 =  pygame.sprite.GroupSingle(Enemy(enemy2x,enemy2y))
projectiles2 = [Projectile(0,1,0,0,0) for i in range(15)]
for i in range(5):
    projectiles2[i] = pygame.sprite.Group(Projectile(-i,-1,0,enemy2x,enemy2y))
for i in range(4,10):
    projectiles2[i] = pygame.sprite.Group(Projectile(-i,-1,40,enemy2x,enemy2y,True))
for i in range(9,15):
    projectiles2[i] = pygame.sprite.Group(Projectile(-i,-1,80,enemy2x,enemy2y,True))


enemies = [enemy1,enemy2]
#text stuff 
font = pygame.font.SysFont(None, 48)
font1 = pygame.font.SysFont(None, 48)
text_color = (200,100,50)
text = ''
lst = spell1[0].split
spell_text = spell1[0]


#main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        #add/sub health on up/down arrow
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(text) > 0:
                    text = text[:-1]
            elif pygame.key.name(event.key).isalnum() :
                text += event.unicode
                           

    #text drawing stuff
    screen.fill((30,30,30))
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (50, 100))
    spell = font1.render(spell_text, True, text_color)
    screen.blit(spell, (50,700))
    
    player.draw(screen)
    player.update()
    
    for enemy in enemies:
        enemy.draw(screen)
    enemies[0].update(enemy1x, enemy1y)
    enemies[1].update(enemy2x-100, enemy2y)
    for projectile in projectiles:
        projectile.draw(screen)
        projectile.update()
        if pygame.sprite.groupcollide(player, projectile, False, True):
            player.sprite.take_damage(100)
    for projectile in projectiles2:
       projectile.draw(screen)
       projectile.update()
       if pygame.sprite.groupcollide(player, projectile, False, True):
            player.sprite.take_damage(100)
     
    pygame.display.update()
    clock.tick(30)
    

