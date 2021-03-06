import pygame, sys , random 
from pygame.math import Vector2

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
framerate = 60
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf',25)
trap = pygame.image.load('Graphics/trap.png').convert_alpha()

class SNAKE():
    def __init__(self):
        self.time = 0
        self.time_2 = -10
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False
        

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
    
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            # 1. We still need a rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x :
                    screen.blit(self.body_vertical,block_rect)
                if previous_block.y == next_block.y :
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)


    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down
  
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def up(self):
        if self.direction.y != 1:
            self.direction = Vector2(0,-1)

    def down(self):
        if self.direction.y != -1:
            self.direction = Vector2(0,1)

    def left(self):
        if self.direction.x != 1:
            self.direction = Vector2(-1,0)

    def right(self):
        if self.direction.x != -1:
            self.direction = Vector2(1,0)


    def move(self):
        num = random.randint(0,3)
        if num == 0:
            self.left()
        elif num == 1:
            self.up()
        elif num == 2:
            self.down()
        else:
            self.right()
            
    
    def time_move(self):
        self.time_2 -=1
        if self.time >= self.time_2:
            self.time_2+=100
            self.move()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
    

    
    
    


class FRUIT():
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        #pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

class TRAP():
    def __init__(self):
        self.randomize()
    
    def draw_trap(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(trap,fruit_rect)
        #pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

class MENU():
    def __init__(self):
        self.condition = True
        self.menu_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf',80)
        self.menu_font_two = pygame.font.Font('Font/PoetsenOne-Regular.ttf',60)
    def draw_menu(self):
        menu_surface = self.menu_font.render("Snake",True,(56,74,12))
        start_surface = self.menu_font_two.render("Press Start ",True,(56,74,12))
        screen.blit(menu_surface,((cell_number*(cell_size/2))-(menu_surface.get_size()[0]/2),cell_number*(cell_size/2)))
        screen.blit(start_surface,((cell_number*(cell_size/2))-(start_surface.get_size()[0]/2),cell_number*((cell_size/2)+5)))
    def strart(self):
        if self.condition :
            self.condition = False
        else:
            self.condition = True

class MAIN():
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.menu = MENU()
        self.traps = []
        self.traps_sound = pygame.mixer.Sound('Sound/trap.mp3')

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):

        if self.menu.condition:
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.menu.draw_menu()
            self.snake.time_move()

        else:
            self.draw_grass()
            if len(self.traps)> 0:
                for i in self.traps:
                    i.draw_trap()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()
            


    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            if (len(self.snake.body)-2)%5 == 0 and len(self.snake.body)!= 3:
                trap = TRAP()
                for block in self.snake.body[1:]:
                    if block == trap.pos:
                        trap.randomize()
                if len(self.traps) != 0:
                    for tra in self.traps:
                        if tra.pos == trap.pos: 
                            trap.randomize()  
                self.traps.append(trap)
            
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            if len(self.traps) != 0:
                    for tra in self.traps:
                        if tra.pos == self.fruit.pos: 
                            self.fruit.randomize()
            
        
        

    def check_fail(self):
        if self.menu.condition:
            if not 6 <= self.snake.body[0].x < cell_number-6 or not 6 <= self.snake.body[0].y < cell_number-6:
                self.snake.move()
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        if len(self.traps) != 0:
            for tra in self.traps:
                if tra.pos == self.snake.body[0]:
                    self.traps_sound.play()
                    self.game_over()
                    

    def game_over(self):
        self.snake.reset()
        self.traps = []

    def draw_grass(self):
        grass_color= (167,209,61)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_tex = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_tex,True,(56,74,12))
        score_x = int(cell_size*cell_number-60)
        score_y = int(cell_size*cell_number-40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright= (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)




main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

def event_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == SCREEN_UPDATE:
            main_game.update()            
        if event.type == pygame.KEYDOWN:
            if main_game.menu.condition:
                if event.key == pygame.K_RETURN:
                   main_game.menu.strart()
                   main_game.snake.reset()
            else:
                if event.key == pygame.K_UP:
                    main_game.snake.up()
                
                if event.key == pygame.K_DOWN:
                    main_game.snake.down()
                
                if event.key == pygame.K_LEFT:
                    main_game.snake.left()

                if event.key == pygame.K_RIGHT:
                    main_game.snake.right()
                    

                

while True:
    event_game()
    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(framerate)
    

