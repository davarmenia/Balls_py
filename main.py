import pygame
import random
import sys, os
pygame.init()

WIN_W = 660
WIN_H = 520
file_path = os.path.dirname(os.path.realpath(__file__))
BG_dir = (file_path + "\\Images\\bg.jpg")
BG = pygame.image.load(BG_dir)
FPS = 60
# colors in game
colors = {
    "BLACK"     : (0,0,0),
    "RED"       : (255,0,0),
    "GREEN"     : (0,255,0),
    "BLUE"      : (0,0,255),
    "YELLOW"    : (255,255,0),
    "ORANGE"    : (255,128,0),
    "GRAY"      : (255,255,180),
    "DEEPPINK"  : (255,20,147)
}

id_to_colors = {
    1 : "YELLOW",
    2 : "BLUE",
    3 : "GREEN",
    4 : "RED",
    5 : "ORANGE"
}

screen = pygame.display.set_mode([WIN_W, WIN_H])
pygame.display.set_caption('Bottles bolls')

class INFOTEXT():
    def draw_score(self, moves):
        font = pygame.font.Font(file_path + '\\Fonts\\Lightdot-13x9.ttf', 14)
        text_for_show = "Score: %d" % (moves)
        text = font.render(text_for_show, True, colors["DEEPPINK"])
        textRect = text.get_rect()
        textRect.left = (10)
        textRect.top = (WIN_H - 18)
        screen.blit(text, textRect)

    def draw_win(self):
        font = pygame.font.Font(file_path + '\\Fonts\\Super Festival Personal Use.ttf', 72)
        text_for_show = "!!! YOU WIN !!!"
        text = font.render(text_for_show, True, colors["DEEPPINK"])
        textRect = text.get_rect()
        textRect.left = (WIN_W /2 - (len(text_for_show) * 28) / 2)
        textRect.top = (10)
        screen.blit(text, textRect)

class BALL():
    def __init__(self):
        self.ball_radius = 24

    #   Draw ball with color in position
    def draw(self, color, pos_x, pos_y):
        pos_x = pos_x * 90 + 20
        pygame.draw.circle(screen, colors["BLACK"], [self.ball_radius + pos_x + 14, 465 - pos_y * self.ball_radius * 2 - pos_y], self.ball_radius, 3)
        pygame.draw.circle(screen, colors[id_to_colors[color]], [self.ball_radius + pos_x + 14, 465 - pos_y * self.ball_radius * 2 - pos_y], self.ball_radius - 2, 0)

class TUBE():
    def __init__(self):
        #   Creating array for tubes image and set the paths
        self.image_list = ["tube.png", "tube_yellow.png", "tube_blue.png", "tube_green.png", "tube_red.png", "tube_orange.png"]
        self.image = pygame.image.load(file_path + "\\Images\\" + self.image_list[0])

    def draw(self, color, pos):
        #   If in tube will be only one color balls, tube will load image with that color
        self.image = self.image = pygame.image.load(file_path + "\\Images\\" + self.image_list[color])
        #   This line will print tube in screen
        screen.blit(self.image, (20 + pos * 90,90))

    def clicked_tube(self, pos_x, pos_y = 90):
        #   calculating tmp_pos_x for size of tube image
        tmp_pos_x = 20 + pos_x * 90
        #   checking position of tube image to check collision
        if self.get_position(tmp_pos_x, pos_y).collidepoint(event.pos):
            return pos_x
        return -1

    #   Get position of tube image
    def get_position(self, x, y):
        self.rect = self.image.get_rect(topleft = (x, y))
        return self.rect
    

class ENGINE():
    def __init__(self):
        self.moves = 0
        self.selected_tube_id = None
        self.selected_ball_id = None
        self.selected_ball_pos_y = None
        self.selected_ball = False
        self.game_win = False
        self.game_start = False
        self.balls_matrix = [[], # 1 - orange | 2 - blue | 3 - green | 4 - red | 5 - yellow
                             [],
                             [],
                             [],
                             [],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0]]
        #   Game tubes colors
        self.tube_color = [0,0,0,0,0,0,0]
        #   Init game objects
        self.tube = TUBE()
        self.ball = BALL()
        self.text = INFOTEXT()
        #   Shafle balls to start
        self.shafle_game_matrix()
        #   Init mixer for sounds
        pygame.mixer.init()
        #   Init sounds paths
        self.ouch = pygame.mixer.Sound(file_path + "\\Sounds\\click.ogg")
        music = pygame.mixer.music.load(file_path + "\\Sounds\\bg_music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        
    #   Shafle game matrix to start game
    def shafle_game_matrix(self):
        arr = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5]
        random.shuffle(arr)
        for x in range(5):
            for i in range(x*8,x*8 + 8):
                #   Split arr and append to GameEngine board matrix
                self.balls_matrix[x].append(arr[i])


    def draw(self):
        #   Get count of lists in matrix and print tube
        for x, id in list(enumerate(self.tube_color)):
            self.tube.draw(id, x)
        
        #   Get numbers of each element of lists in matrix and print ball
        for x, arr in list(enumerate(self.balls_matrix)):
            for y, sub_arr in list(enumerate(arr)):
                if not sub_arr == 0:
                    self.ball.draw(sub_arr, x, y)
        
        #   Getting out a highest ball in tube, like selecting
        if self.selected_ball_id:
            self.ball.draw(self.selected_ball_id, self.selected_tube_id, 8.2)

        #   Draw score
        self.text.draw_score(self.moves)
        if self.game_win:
            self.text.draw_win()

    def check_for_clicked_tube_id(self):
        #   Play sound for click
        pygame.mixer.Sound.play(self.ouch)
        for x, id in list(enumerate(self.tube_color)):
            tube_id = self.tube.clicked_tube(x)
            #   Check if clicked on tube or not
            if not tube_id == -1:
                if self.selected_tube_id == None and self.balls_matrix[tube_id][0] == 0:
                    return -1
                if self.selected_tube_id == None:
                    self.selected_tube_id = tube_id
                    break
                break
        return tube_id
        
    def game_update(self, tube_id):
        if not self.selected_tube_id == -1 and not self.selected_tube_id == None and not tube_id == -1:
            if not self.selected_ball:
                if self.balls_matrix[self.selected_tube_id][0]:
                    for x, pos in reversed(list(enumerate(self.balls_matrix[self.selected_tube_id]))):
                        if not pos == 0:
                            self.selected_ball_id = pos
                            self.selected_ball = True
                            self.balls_matrix[self.selected_tube_id][x] = 0
                            self.selected_ball_pos_y = x
                            break
            #   Case when allready have a selected id
            else:
                #   Retrun ball to the tube from where we got it
                if self.selected_tube_id == tube_id:
                    self.balls_matrix[self.selected_tube_id][self.selected_ball_pos_y] = self.selected_ball_id
                    self.selected_tube_id = None
                    self.selected_ball_id = None
                    self.selected_ball = False
                #   Put the ball in new tube
                else:
                    prev_ball_id = self.selected_ball_id
                    self.balls_matrix[self.selected_tube_id][self.selected_ball_pos_y] = self.selected_ball_id
                    #   Do the ball move if next color of ball in previous tube is the same
                    for y, prv_pos in reversed(list(enumerate(self.balls_matrix[self.selected_tube_id]))):
                        #   In tube can be less than 8 balls, so we need to continue while there is no ball 
                        if prv_pos == 0:
                            continue
                        #   Check if next ball of temp tube is in same color
                        if prv_pos == prev_ball_id:
                            for x, pos in list(enumerate(self.balls_matrix[tube_id])):
                                if pos == 0:
                                    self.balls_matrix[tube_id][x] = self.selected_ball_id
                                    self.balls_matrix[self.selected_tube_id][y] = 0
                                    break
                        #   Finish moving all ball in same color
                        else:
                            break
                    #   Reset all variables
                    self.selected_tube_id = None
                    self.selected_ball_id = None
                    self.selected_ball_index = None
                    self.selected_ball = False
                #   Increment moves
                self.moves += 1

    #   Update color of balls
    def tube_update(self):
        for x, arr in list(enumerate(self.balls_matrix)):
            #   For check get color of the bottom ball in tube
            color_id = arr[0]
            one_color = True
            #   if the tube no balls or not only one color ball
            if not color_id:
                self.tube_color[x] = 0
                continue
            for sub_arr in arr:
                #   Check is there a ball in tube
                if sub_arr:
                    #   If ball color is same with color of ball in bottom of tube then continue to next ball
                    if sub_arr == color_id:
                        continue
                    #   This case will be true if in tube will be different colors
                    else:
                        one_color = False
                        break
                #   There is no balls in tube
                else:
                    break
            
            #   If one_color so change the color of tube
            if one_color:
                self.tube_color[x] = color_id
            else:
                self.tube_color[x] = 0

    def check_win(self):
        #   Tube can be colord if there is only one ball,
        #   and colored tube can be accept as game win 
        #   so we need to check if the tube is full
        count = 0
        for i, pos in list(enumerate(self.tube_color)):
            if pos and self.balls_matrix[i][7]:
                count += 1
        #   If there is 5 colored tubes, and they are full, it's win
        if count == 5:
            self.game_win = True

    #   Reset game
    def reset(self):
        self.__init__()

GAME_CLOCK = pygame.time.Clock()
game_engine = ENGINE()

#   Start Game Engine
running = True
while running:
    #   Get event in pygame
    event_list = pygame.event.get()
    for event in event_list:
        #   Closing window event
        if event.type == pygame.QUIT:
            running = False
        #   Mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_engine.game_win:
                game_engine.game_update(game_engine.check_for_clicked_tube_id())
                game_engine.tube_update()
                game_engine.check_win()
        #   R key for game reset
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_engine.reset()

    #   Fill screen with BLACK color
    screen.fill(colors["BLACK"])
    #   Put the background image
    screen.blit(BG, (0, 0))
    #   Draw all objects
    game_engine.draw()
    #   Set FPS for game
    GAME_CLOCK.tick(FPS)
    #   Display construced screen
    pygame.display.update()

#   Exit pygame
pygame.quit()
#   Close the window
exit()