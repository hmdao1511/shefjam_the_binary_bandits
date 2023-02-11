import pygame,sys,math
#health bar & text things
#nb - pygame rectangles (wheretodraw,color, (x,y,length,width)) :p

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__() #inherits sprite
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center = (400,400))
        
        #health variables
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health/self.health_bar_length #for converting health -> bar length
        self.current_health = 200
        self.target_health = 500
        self.health_transition_speed = 5

    def update(self): 
        self.health()

    #subtract from player health
    def take_damage(self,damage):
        if self.target_health > 0:
            self.target_health -= damage
        if self.target_health <= 0:
            self.target_health = 0
            
    #add to player health
    def get_health(self,health):
        if self.target_health < self.maximum_health:
            self.target_health += health
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    #draw health bar
    def health(self):
        transition_width = 0
        transition_color = (0,255,0)

        #if player gained health -> green rectangle
        if self.current_health < self.target_health:
            self.current_health += self.health_transition_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (0,255,0)

        #if player took damage -> yellowy/orange rectangle
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
    def __init__(self, angle, reverse,clock,nox=True):
        super().__init__() #inherits sprite
        self.angle = angle
        self.startx = 400
        self.starty = 400
        self.rotate_clock = clock
        
        self.image = pygame.Surface((8,8))
        self.image.fill((240,0,240))
        self.rect = self.image.get_rect(center = (self.startx,self.starty))

        self.angle_change = 1

        self.projectile_xspeed = int(5 * reverse) *nox
        self.projectile_yspeed = angle
        
    def update(self):
       self.change_position()
       self.collision(200)
       self.rotate_clock += 1
       if (self.rotate_clock % 40) == 0 :
           if self.projectile_yspeed == 10:
                 self.angle_change = -1
           if self.projectile_yspeed == -10:
                 self.angle_change  = 1  
           self.projectile_yspeed += self.angle_change 
                
    def collision(self,radius):
        distance = ((self.startx -self.rect.x)**2+(self.starty -self.rect.y)**2)**(1/2)
        if distance >= radius:
            self.reset_position()
    
    def reset_position(self):
        self.rect.x = self.startx
        self.rect.y = self.starty
        
    def change_position(self):
        if self.projectile_xspeed > 0:
            if  self.rect.x <= 800:
                self.rect.x += self.projectile_xspeed
            else:
                self.reset_position()
            if  self.rect.y <= 800:
                self.rect.y += self.projectile_yspeed
            else:
                 self.reset_position()
        else:
            if  self.rect.x >= 0:
                self.rect.x += self.projectile_xspeed
            else:
                self.reset_position()
            if  self.rect.y >= 0:
                self.rect.y += self.projectile_yspeed
            else:
                 self.reset_position()
            
            
        
#setup
pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle(Player())


projectiles = [Projectile(0,1,0) for i in range(20)]
for i in range(5):
    projectiles[i] = pygame.sprite.Group(Projectile(i,1,0))
    if pygame.sprite.groupcollide(player, projectiles[i], False, True):
        print("group 1 collided")
        player.sprite.take_damage(10)
for i in range(5):
    projectiles[i+5] = pygame.sprite.Group(Projectile(i,-1,0))
    if pygame.sprite.groupcollide(player, projectiles[i+5], False, True):
        print("group 2 collided")
        player.sprite.take_damage(10)
for i in range(5):
    projectiles[i+10] = pygame.sprite.Group(Projectile(i,1, 41))
    if pygame.sprite.groupcollide(player, projectiles[i+10], False, True):
        print("group 3 collided")
        player.sprite.take_damage(10)
for i in range(5):
    projectiles[i+15] = pygame.sprite.Group(Projectile(i,-1,41))
    if pygame.sprite.groupcollide(player, projectiles[i+15], False, True):
        print("group 4 collided")
        player.sprite.take_damage(10)
projectiles.append(pygame.sprite.Group(Projectile(i,-1,41,False)))
#text stuff 
font = pygame.font.SysFont(None, 48)
text_color = (200,100,50)
text = ''


#main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        #add/sub health on up/down arrow
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.sprite.get_health(100)
            elif event.key == pygame.K_DOWN:
                player.sprite.take_damage(100)
            #text stuff 
            elif event.key == pygame.K_BACKSPACE:
                if len(text) > 0:
                    text = text[:-1]
            elif pygame.key.name(event.key).isalnum() :
                text += event.unicode
                           

    #text drawing stuff
    screen.fill((30,30,30))
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (50, 100))
    
    player.draw(screen)
    player.update()
    for projectile in projectiles:
        projectile.draw(screen)
        projectile.update()
            
    pygame.display.update()
    clock.tick(30)
    

