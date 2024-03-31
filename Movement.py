import pygame,math,sys

pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = screen_width/2
map_size = 8
tile_size = int(screen_width/2/map_size)
max_depth = int(map_size*tile_size)
l = 50

screen = pygame.display.set_mode ((screen_width, screen_height))
pygame.display.set_caption('Raycasting')

player = pygame.Rect((screen_width/4-7.5), (screen_height/2-7.5), 15,15)

speed = 2
player_speedx = 0
player_speed = 0
rot_speed = 0
rot_speed_value = 0.05

player_angle = (0)
fov = math.pi/3
no_rays = 80
h = fov/no_rays
#MAPPPPP
MAP = ('########'
       '# B B  #'
       '#      #'
       '#      #'
       '#   # ##'
       '#   #  #'
       '#   #  #'
       '########')
now = 0

white = (211,81,0)
bg_color = (248,161,69)
black = (0, 0, 0)  
lblack = (15, 15, 15)
mid = (240, 121, 0)
ghost_line = (0,0,0)
red = (255,0,0)
blue = (135,206,235)


def draw_map(MAP):
    for row in range(8):
        for col in range(8):
            square = row *map_size + col

            #drawingstuff
            
            if MAP[square] =="#":
                pygame.draw.rect(screen,(200,200,200), (col*(tile_size),row*tile_size, tile_size-2,tile_size-2) )
            elif MAP[square]=="B":
                pygame.draw.rect(screen,(0,0,200), (col*(tile_size),row*tile_size, tile_size-2,tile_size-2) )
        
            else: 
                pygame.draw.rect(screen,(100,100,100), (col*(tile_size),row*tile_size, tile_size-2,tile_size-2) )





while True:
    eyes=[]
    color =[]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:#and player.y <=screen_height:
                player_speed = -speed 
            if event.key == pygame.K_w:#and player.y <=screen_height:
                player_speed = speed
            if event.key == pygame.K_d:#and player.y <=screen_height:
                rot_speed = -rot_speed_value
            if event.key == pygame.K_a:#and player.y <=screen_height:
                rot_speed = +rot_speed_value
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:#and player.y <=screen_height:
                player_speed = 0 
            if event.key == pygame.K_w:#and player.y <=screen_height:
                player_speed = 0
            if event.key == pygame.K_d:#and player.y <=screen_height:
                rot_speed = 0
            if event.key == pygame.K_a:#and player.y <=screen_height:
                rot_speed = 0
    player.centerx += player_speed*math.cos(player_angle)
    player.centery -= player_speed*math.sin(player_angle)
    player_angle += rot_speed

    screen.fill(black)
    
    update_list = list(MAP)
    B_pos = update_list.index("B")
    
    if B_pos//8<=5 and pygame.time.get_ticks()-now  >= 2000:
        update_list = list(MAP)
        now = pygame.time.get_ticks()
        B_pos = update_list.index("B")
        update_list[B_pos] = " "
        update_list[B_pos+8] = "B"
        MAP = ""
        for i in update_list:
            MAP += i 
        
    
    draw_map(MAP)

    pygame.draw.ellipse(screen, red, player)
    pygame.draw.aaline(screen,(0,255,0),player.center, (player.centerx + l*math.cos(player_angle), player.centery - l*math.sin(player_angle)) )
    
    coneL = player_angle+fov/2
    y_snip = player.centery%tile_size

    for i in range(no_rays):
        current_angle = coneL-h*i
        if i in range(no_rays//2-1,no_rays//2+1 ):
        
            pygame.draw.aaline(screen,(0,255,0),player.center, (player.centerx + l*math.cos(current_angle), player.centery - l*math.sin(coneL-h*i)) )
        else:
            pygame.draw.aaline(screen,bg_color,player.center, (player.centerx + l*math.cos(coneL-h*i), player.centery - l*math.sin(coneL-h*i)) )

        #RAYMEASURING
        
        for depth in range(max_depth):
            ray_y = (player.centery- depth*math.sin(current_angle))
            ray_x = (player.centerx + depth*math.cos(current_angle))
            #pygame.draw.circle(screen,(255,0,0), (ray_x,ray_y), 5)
            row = int(ray_y/tile_size)
            col = int(ray_x/tile_size)
            square = row *map_size + col
            if MAP[square] == "#":
                #pygame.draw.aaline(screen, (255,0,0), player.center, (ray_x, ray_y))
                eyes.append(math.sqrt((player.centery-ray_y)**2 +  (player.centerx-ray_x)**2))
                color.append("1")
                break
            elif MAP[square] == "B":
                #pygame.draw.aaline(screen, (0,0,255), player.center, (ray_x, ray_y))
                eyes.append(math.sqrt((player.centery-ray_y)**2 +  (player.centerx-ray_x)**2))
                color.append("2")
                break
            
        #print(eyes) 
        
        #horzontal Lines CHECK TRIG SUX IN THESE KIND OF SITUATIONS QUADRANT ISSUES WHICH I DONT KNOW HOW TO FIX
        '''x_snip'' = y_snip/ math.tan(current_angle+0.001)
        x_inc = tile_size/(math.tan(current_angle)+0.001)
        y_inc = tile_size
        ray_x = player.centerx + x_snip
        ray_y = player.centery - y_snip'''

        #while ray_y >=0:
            #pygame.draw.aaline(screen,(255,0,0),(player.center),(ray_x, ray_y))
            #ray_x += x_inc
            #ray_y -= y_inc
    #RENDER 3D
    x_rend = screen_width/2    
    #sky
    skybox = pygame.Rect(x_rend, 0, x_rend,445)
    pygame.draw.rect(screen, blue,skybox)

    
    strip = screen_width/2 / no_rays
    for i in range(no_rays):
        if color[i] == "1":
            height = 12000/(eyes[i]+0.01)
            k = 8000/(eyes[i]+0.01)
            if k >=255:
                k=255
            if k <= 10:
                k = 10
            rendstrip = pygame.Rect((x_rend+strip*i), (450-height), strip, height)
            #dosomethng rendstrip.centery
            pygame.draw.rect(screen, (k,k,k), rendstrip)
        elif color[i] == "2":
            height = 12000/(eyes[i]+0.01)
            k = 8000/(eyes[i]+0.01)
            if k >=255:
                k=255
            if k <= 10:
                k = 10
            rendstrip = pygame.Rect((x_rend+strip*i), (450-height), strip, height)
            #dosomethng rendstrip.centery
            pygame.draw.rect(screen, (0,0,k), rendstrip)

    floor = pygame.Rect(x_rend,450-4 , screen_width/2, (screen_height-450)+4)
    pygame.draw.rect(screen, (5,20,5),floor)


         
        

   

    pygame.display.flip()
    
    clock.tick(60)