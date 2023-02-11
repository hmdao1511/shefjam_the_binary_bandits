import pygame,sys
#health bar & text things
#nb - pygame rectangles (wheretodraw,color, (x,y,length,width)) :p

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__() #inherits sprite
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center = (400,400))
        
        #health variables:
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health/self.health_bar_length #for converting health -> bar length
        self.current_health = 200
        self.target_health = 500
        self.health_transition_speed = 5 

    #updates game status every 60ms
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

#setup
pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle(Player())

#text stuff 
font = pygame.font.SysFont(None, 48)
text_color = (200,100,50)
text = ''

goodwords = []

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
               # print(text)
            

    #text drawing stuff
    screen.fill((30,30,30))
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (50, 100))

    player.draw(screen)
    
    player.update()
    pygame.display.update()
    clock.tick(30)
    

