import pygame
from random import randint, choice

class Mygame:
    def __init__(self):
        pygame.init()
        self.display=pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Coin Collection")

        self.making_monster2=False
        self.use_player2=False
        self.monster2_spawn_time=0
        self.monster2_delay=4000 

        self.clock=pygame.time.Clock()
        self.load_images()
        self.load_sounds()

        self.to_left=False
        self.to_right=False
        self.to_up=False
        self.to_down=False

        self.to_left2=False
        self.to_right2=False
        self.to_up2=False
        self.to_down2=False
        
        self.lives=5
        self.show_rules()
        self.init_positions()
        self.main_loop()

    def load_images(self):
        self.coin=pygame.image.load("src/coin.png")
        self.monster=pygame.image.load("src/monster.png")
        self.monster2=pygame.image.load("src/monster.png")
        self.robot=pygame.image.load("src/robot.png")
        self.robot2=pygame.image.load("src/robot2.png")
        self.robot2=pygame.transform.scale(self.robot2,(self.robot.get_width()+20,self.robot.get_height()+20))
        self.bomb=pygame.image.load("src/bomb.png")
        self.bomb=pygame.transform.scale(self.bomb,(70,70))
        self.heart=pygame.image.load("src/heart.png")
        self.heart=pygame.transform.scale(self.heart,(70,70))
        self.heart2=pygame.image.load("src/heart2.png")
        self.heart2=pygame.transform.scale(self.heart2,(70,70))
        self.bomb2=pygame.image.load("src/bomb2.png")
        self.bomb2=pygame.transform.scale(self.bomb2,(365,365))
        self.background = pygame.image.load("src/background.jpg")
        self.background = pygame.transform.scale(self.background, (640, 480))
        self.gameover_background = pygame.image.load("src/gameover_background.jpg")
        self.gameover_background = pygame.transform.scale(self.gameover_background, (640, 480))
        self.gameover_background2 = pygame.image.load("src/gameover2_background.jpg")
        self.gameover_background2 = pygame.transform.scale(self.gameover_background2, (640, 480))
        self.start_background = pygame.image.load("src/start_background.jpg")
        self.start_background = pygame.transform.scale(self.start_background, (640, 480))

    def load_sounds(self):
        pygame.mixer.init()
        self.coinS=pygame.mixer.Sound("src/coinS.wav")
        self.coin2S=pygame.mixer.Sound("src/coin2S.wav")
        self.bombS=pygame.mixer.Sound("src/bombS.wav")
        self.gameoverS=pygame.mixer.Sound("src/gameoverS.wav")
        self.heartS=pygame.mixer.Sound("src/heartS.wav")
        self.heart2S=pygame.mixer.Sound("src/heart2S.wav")
        self.startS=pygame.mixer.Sound("src/startS.wav")
        self.heart2_channel=pygame.mixer.Channel(5)

        pygame.mixer.music.load("src/backgroundS.mp3")   
        pygame.mixer.music.set_volume(1.0)           
        pygame.mixer.music.play(-1)

    def init_positions(self):
        self.robot_x=400
        self.robot_y=380
        self.round=1

        if self.use_player2==True:
            self.robot2_x=200
            self.robot2_y=380

        self.monster_x=0
        self.monster_y=0
        self.monster_velocity_x=3+self.round/10
        self.monster_velocity_y=3+self.round/10

        self.monster2_x=0
        self.monster2_y=0
        self.monster2_velocity_x=4
        self.monster2_velocity_y=4

        self.points=0
        self.make_coins()
        self.bombs=[]
        self.hearts=[]
        self.bomb2s=[]
        self.heart2s=[]

    def make_coins(self):
        self.coins=[]
        for i in range(self.round):
            if self.round<=10:
                x=randint(0, 640-self.coin.get_width())
                y=randint(-280, -self.coin.get_height())
                self.coins.append([x, y])
            elif self.round<=25:
                x=randint(0, 640-self.coin.get_width())
                y=randint(-460, -self.coin.get_height())
                self.coins.append([x, y])
            elif self.round>25:
                x=randint(0, 640-self.coin.get_width())
                y=randint(-600, -self.coin.get_height())
                self.coins.append([x, y])

    def main_loop(self):
        while True:
            self.check_events()
            self.move_robot()
            self.move_robot2()
            self.move_coins()
            self.move_monster()
            self.move_monster2()
            self.move_bomb()
            self.move_bomb2()
            self.move_heart() 
            self.move_heart2()
            self.gain_heart()  
            self.gain_heart2() 
            self.killed_bomb()
            self.killed_bomb2()
            self.collect_coins()
            self.check_next_round()
            self.draw()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.to_left=True
                if event.key==pygame.K_RIGHT:
                    self.to_right=True
                if event.key==pygame.K_UP:
                    self.to_up=True
                if event.key==pygame.K_DOWN:
                    self.to_down=True

            if self.use_player2==True:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_a:
                        self.to_left2=True
                    if event.key==pygame.K_d:
                        self.to_right2=True
                    if event.key==pygame.K_w:
                        self.to_up2=True
                    if event.key==pygame.K_s:
                        self.to_down2=True

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    self.to_left=False
                if event.key==pygame.K_RIGHT:
                    self.to_right=False
                if event.key==pygame.K_UP:
                    self.to_up=False
                if event.key==pygame.K_DOWN:
                    self.to_down=False

            if self.use_player2==True:
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_a:
                        self.to_left2=False
                    if event.key==pygame.K_d:
                        self.to_right2=False
                    if event.key==pygame.K_w:
                        self.to_up2=False
                    if event.key==pygame.K_s:
                        self.to_down2=False

    def make_bomb(self):
        if choice([1,2,3])==1:
            x=randint(0, 640-self.bomb.get_width())
            y=randint(-900, -200-self.bomb.get_height())
            self.bombs.append([x, y])
            self.bombS.play()
            if choice([1,2,3]) in [2,3]:
                x=randint(0, 640-self.bomb.get_width())
                y=randint(-1300, -200-self.bomb.get_height())
                self.bombs.append([x, y])
                if choice([1,2,3]) in [3,2]:
                    x=randint(0, 640-self.bomb.get_width())
                    y=randint(-1500, -500-self.bomb.get_height())
                    self.bombs.append([x, y])
                    if choice([3,4,5]) in [4,5]:
                        x=randint(0, 640-self.bomb.get_width())
                        y=randint(-1700, -700-self.bomb.get_height())
                        self.bombs.append([x, y])
                        self.bombS.play()
                        if choice([1,2,3]) in [3,1]:
                            x=randint(0, 640-self.bomb.get_width())
                            y=randint(-1900, -1000-self.bomb.get_height())
                            self.bombs.append([x, y])
                            if choice([1,2,3]) in [2,3]:
                                x=randint(0, 640-self.bomb.get_width())
                                y=randint(-2200, -1200-self.bomb.get_height())
                                self.bombs.append([x, y])
                                if choice([1,2,3]) in [3,1]:
                                    x=randint(0, 640-self.bomb.get_width())
                                    y=randint(-2400, -1800-self.bomb.get_height())
                                    self.bombs.append([x, y])
                                    
        else:
            if choice([1,2,3])==1:
                x=randint(0, 640-self.bomb2.get_width())
                y=randint(-1000, -400-self.bomb2.get_height())
                self.bomb2s.append([x, y])
                self.bombS.play()
                self.bombS.play()
                if choice([1,2,3,4])==2:
                    x=randint(0, 640-self.bomb2.get_width())
                    y=randint(-2000, -1500-self.bomb2.get_height())
                    self.bomb2s.append([x, y])
                    self.bombS.play()
                    self.bombS.play()
                    self.bombS.play()
                                         
    def make_heart(self):
        if self.lives==1:
            x=randint(0, 640-self.heart.get_width())
            y=randint(-2000, -1000-self.heart.get_height())
            self.hearts.append([x, y])
            self.heartS.play()

            x=randint(0, 640-self.heart2.get_width())
            y=randint(-2000, -1000-self.heart2.get_height())
            self.heart2s.append([x, y])
            self.heartS.play()
            x=randint(0, 640-self.heart2.get_width())
            y=randint(-2000, -1000-self.heart2.get_height())
            self.heart2s.append([x, y])
            self.heartS.play()
            x=randint(0, 640-self.heart2.get_width())
            y=randint(-2000, -1000-self.heart2.get_height())
            self.heart2s.append([x, y])
            x=randint(0, 640-self.heart2.get_width())
            y=randint(-2000, -1000-self.heart2.get_height())
            self.heart2s.append([x, y])


        elif choice([1,2,3,4,5])==1:
            x=randint(0, 640-self.heart.get_width())
            y=randint(-2000, -1000-self.heart.get_height())
            self.hearts.append([x, y])
            self.heartS.play()

            x=randint(0, 640-self.heart2.get_width())
            y=randint(-2000, -1000-self.heart2.get_height())
            self.heart2s.append([x, y])
            self.heartS.play()
            x=randint(0, 640-self.heart2.get_width())
            y=randint(-2000, -1000-self.heart2.get_height())
            self.heart2s.append([x, y])
            self.heartS.play()
            x=randint(0, 640-self.heart2.get_width())
            y=randint(-2000, -1000-self.heart2.get_height())
            self.heart2s.append([x, y])
            x=randint(0, 640-self.heart2.get_width())
            y=randint(-2000, -1000-self.heart2.get_height())
            self.heart2s.append([x, y])

    def move_bomb(self):
        for bomb in self.bombs:
            bomb[1]+=4.5+self.round/26
            if bomb[1]>=480:
                self.bombs.remove(bomb)
    
    def move_bomb2(self):
        for bomb in self.bomb2s:
            bomb[1]+=5+self.round/18
            if bomb[1]>=480:
                self.bomb2s.remove(bomb)
    
    def move_heart(self):
        for heart in self.hearts:
            heart[1]+=11+self.round/25
            if heart[1]>=480:
                self.hearts.remove(heart)
        
    def move_heart2(self):
        for heart in self.heart2s:
            heart[1]+=11+self.round/25
            if heart[1]>=480:
                self.heart2s.remove(heart)

    def killed_bomb(self):
        for bomb in self.bombs[:]:
            if abs(self.robot_x-bomb[0])<30 and abs(self.robot_y-bomb[1])<40:
                self.bombs.remove(bomb)
                self.gameover()
            elif self.use_player2==True:
                if abs(self.robot2_x-bomb[0])<30 and abs(self.robot2_y-bomb[1])<40:
                    self.bombs.remove(bomb)
                    self.gameover()

            for coin in self.coins[:]:
                if abs(coin[0]-bomb[0])<30 and abs(coin[1]-bomb[1])<40:
                    self.coins.remove(coin)
                    self.coin2S.play()
    
    def killed_bomb2(self):
        for bomb in self.bomb2s[:]:
            bomb2_centerX=bomb[0]+155
            bomb2_centerY=bomb[1]+210
            if abs(self.robot_x-bomb2_centerX)<150 and abs(self.robot_y-bomb2_centerY)<155:
                self.bomb2s.remove(bomb)
                self.gameover()
            elif self.use_player2==True:
                if abs(self.robot2_x-bomb2_centerX)<150 and abs(self.robot2_y-bomb2_centerY)<155:
                    self.bomb2s.remove(bomb)
                    self.gameover()
                
            for coin in self.coins[:]:
                if abs(coin[0]-bomb2_centerX)<150 and abs(coin[1]-bomb2_centerY)<155:
                    self.coins.remove(coin)
                    self.coin2S.play()

    def gain_heart(self):
        for heart in self.hearts[:]:
            if abs(self.robot_x-heart[0])<40 and abs(self.robot_y-heart[1])<55:
                self.hearts.remove(heart)
                if self.lives<5:
                    self.lives+=1
                self.heartS.play()
            elif self.use_player2==True:
                if abs(self.robot2_x-heart[0])<40 and abs(self.robot2_y-heart[1])<55:
                    self.hearts.remove(heart)
                    if self.lives<5:
                        self.lives+=1
                    self.heartS.play()

    def gain_heart2(self):
        for heart in self.heart2s[:]:
            if abs(self.robot_x-heart[0])<40 and abs(self.robot_y-heart[1])<55:
                self.heart2s.remove(heart)
                if self.making_monster2:
                    self.heart2_channel.stop()
                    self.making_monster2=False
                    self.heartS.play()
                else:
                    self.making_monster2=True
                    self.monster2_x=0
                    self.monster2_y=0
                    self.heart2_channel.play(self.heart2S)
                    self.monster2_spawn_time=pygame.time.get_ticks()
            
            elif self.use_player2==True:
                if abs(self.robot2_x-heart[0])<40 and abs(self.robot2_y-heart[1])<55:
                    self.heart2s.remove(heart)
                    if self.making_monster2:
                        self.heart2_channel.stop()
                        self.making_monster2=False
                        self.heartS.play()
                    else:
                        self.making_monster2=True
                        self.monster2_x=0
                        self.monster2_y=0
                        self.heart2_channel.play(self.heart2S)
                        self.monster2_spawn_time=pygame.time.get_ticks()


    def move_robot(self):
        if self.to_left and self.robot_x>0:
            self.robot_x-=8+self.round/8
        if self.to_right and self.robot_x+self.robot.get_width()<640:
            self.robot_x+=8+self.round/8
        if self.to_up and self.robot_y>0:
            self.robot_y-=8+self.round/8
        if self.to_down and self.robot_y+self.robot.get_height()<480:
            self.robot_y+=8+self.round/8
        
    def move_robot2(self):
        if self.use_player2==True:
            if self.to_left2 and self.robot2_x>0:
                self.robot2_x-=8+self.round/8
            if self.to_right2 and self.robot2_x+self.robot2.get_width()<640:
                self.robot2_x+=8+self.round/8
            if self.to_up2 and self.robot2_y>0:
                self.robot2_y-=8+self.round/8
            if self.to_down2 and self.robot2_y+self.robot2.get_height()<480:
                self.robot2_y+=8+self.round/8

    def move_coins(self):
        for coin in self.coins:
            coin[1]+=1.43
            if coin[1]>480:
                self.gameover()
                
    def collect_coins(self):
        for coin in self.coins[:]:
            robot_centerY=self.robot_y+self.robot.get_height()//2-8
            if (abs(self.robot_x-coin[0])<50 and abs(robot_centerY-coin[1])<70):
                self.coins.remove(coin)
                self.points+=1
                self.coinS.play()
            elif self.use_player2==True:
                robot_center2Y=self.robot2_y+self.robot2.get_height()//2-8
                if (abs(self.robot2_x-coin[0])<50 and abs(robot_center2Y-coin[1])<70):
                    self.coins.remove(coin)
                    self.points+=1
                    self.coinS.play()

    def check_next_round(self):
        if len(self.coins)==0:
            self.round+=1
            self.move_monster()
            self.move_monster2()
            self.make_coins()
            self.make_bomb() 
            self.make_heart() 
            speed_m=3+self.round/10
            self.monster_velocity_x=speed_m
            self.monster_velocity_y=speed_m

    def move_monster(self):
        self.monster_x+=self.monster_velocity_x
        self.monster_y+=self.monster_velocity_y

        if self.monster_x<0:
            self.monster_x=0
            self.monster_velocity_x*=-1
        elif self.monster_x>640-self.monster.get_width():
            self.monster_x=640-self.monster.get_width()
            self.monster_velocity_x*=-1

        if self.monster_y<0:
            self.monster_y=0
            self.monster_velocity_y*=-1   
        elif self.monster_y>480-self.monster.get_height():
            self.monster_y=480-self.monster.get_height()
            self.monster_velocity_y*=-1

        if abs(self.robot_x-self.monster_x)<40 and abs(self.robot_y-self.monster_y)<50:
            self.gameover()
        
        if self.use_player2==True:
            if abs(self.robot2_x-self.monster_x)<40 and abs(self.robot2_y-self.monster_y)<50:
                self.gameover()

        for coin in self.coins:
            if abs(coin[0]-self.monster_x)<40 and abs(coin[1]-self.monster_y)<50:
                self.coins.remove(coin)
                if choice([1,2])==1:
                    self.monster_velocity_x*=-1
                    self.monster_velocity_y*=-1
                self.coin2S.play()

    def move_monster2(self):
        now=pygame.time.get_ticks()
        if now-self.monster2_spawn_time<self.monster2_delay:
            return
        if self.making_monster2:
            self.monster2_x+=self.monster2_velocity_x
            self.monster2_y+=self.monster2_velocity_y
            if self.monster2_x<0:
                self.monster2_x=0
                self.monster2_velocity_x*=-1
                if choice([1,2])==2:
                    self.monster2_velocity_y*=-1
            elif self.monster2_x>640-self.monster2.get_width():
                self.monster2_x=640-self.monster2.get_width()
                self.monster2_velocity_x*=-1
                if choice([1,2])==2:
                    self.monster2_velocity_y*=-1

            if self.monster2_y<0:
                self.monster2_y=0
                self.monster2_velocity_y*=-1  
                if choice([1,2])==2:
                    self.monster2_velocity_x*=-1 
            elif self.monster2_y>480-self.monster2.get_height():
                self.monster2_y=480-self.monster2.get_height()
                self.monster2_velocity_y*=-1
                if choice([1,2])==2:
                    self.monster2_velocity_x*=-1

            if abs(self.robot_x-self.monster2_x)<40 and abs(self.robot_y-self.monster2_y)<50:
                self.making_monster2=False
                self.gameover()
            if self.use_player2==True:
                if abs(self.robot2_x-self.monster2_x)<40 and abs(self.robot2_y-self.monster2_y)<50:
                    self.making_monster2=False
                    self.gameover()
            
            for coin in self.coins:
                if abs(coin[0]-self.monster2_x)<40 and abs(coin[1]-self.monster2_y)<50:
                    self.coins.remove(coin)
                    self.coin2S.play()

    def lives_display(self):
        font=pygame.font.SysFont("Impact", 30)
        text=font.render(f"Lives: {self.lives}", True, (0, 0, 255))
        self.display.blit(text, (465, 50))

    def score_display(self):
        font=pygame.font.SysFont("Impact", 30)
        text=font.render(f"Points: {self.points}", True, (255, 0, 0))
        self.display.blit(text, (465, 10))
    
    def round_display(self):
        font=pygame.font.SysFont("Impact", 30)
        text=font.render(f"Round: {self.round}", True, (255, 100, 255))
        self.display.blit(text, (20, 10))

    def show_rules(self):
        self.display.blit(self.start_background, (0, 0))
        
        new_font="src/PressStart2P-Regular.ttf"
        title_font=pygame.font.Font(new_font, 35)
        title_text=title_font.render("COIN COLLECTION", True, (255, 100, 0))
        self.display.blit(title_text, (50, 50))
        
        rules_font=pygame.font.SysFont("Comic Sans MS", 17)
        rules=[
            "Rules:",
            "- In each round, the number of coins will increase.",
            "- The speed of the robot and monster will increase each round gradually.",
            "- Bombs may fall in each round. (you can hear explosion sound when created)",
            "- You have 5 lives.",
            "- A red heart might fall and you can gain one life if you have less than 5 lives. ",
            "- A black heart might fall too and it add one monster.",
            " (it disappers if you collection black heart again)",
            "- Lose a life if hit by the monster, bombs or miss coins.",
        ]
        
        for i, line in enumerate(rules):
            text=rules_font.render(line, True, (30, 30, 30))
            self.display.blit(text, (20, 100 + i*34))
        
        final_font=pygame.font.SysFont("Impact", 30)
        final_text=final_font.render('Press "2" for 2 players and "space" for 1 player!', True, (200, 100, 80))
        self.display.blit(final_text, (10, 400))
        
        
        pygame.display.flip()
        
        continuing=True
        while continuing:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_2:
                        self.use_player2=True
                        continuing=False
                    if event.key==pygame.K_SPACE:
                        continuing=False
        self.startS.play()
        
    def draw(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.robot, (self.robot_x, self.robot_y))
        if self.use_player2==True:
            self.display.blit(self.robot2, (self.robot2_x, self.robot2_y))

        for coin in self.coins:
            self.display.blit(self.coin, coin)

        for bomb in self.bombs:
            self.display.blit(self.bomb, bomb)

        for bomb in self.bomb2s:
            self.display.blit(self.bomb2, bomb)

        for heart in self.hearts:
            self.display.blit(self.heart, heart)
        
        for heart in self.heart2s:
            self.display.blit(self.heart2, heart)

        self.display.blit(self.monster, (self.monster_x, self.monster_y))
        if self.making_monster2:
            self.display.blit(self.monster2, (self.monster2_x, self.monster2_y))
        self.round_display()
        self.score_display()
        self.lives_display()
        pygame.display.flip()

    def gameover(self):
        self.heart2_channel.stop()
        self.making_monster2=False
        self.bombs.clear()
        self.bomb2s.clear()
        self.hearts.clear()
        self.heart2s.clear()
        self.gameoverS.play()

        if self.lives==1:
            self.display.blit(self.gameover_background, (0, 0))
        else:
            self.display.blit(self.gameover_background2, (0, 0))

        if self.lives==1:
            new_font="src/PressStart2P-Regular.ttf"
            font=pygame.font.Font(new_font, 65)
            text=font.render("GAME OVER", True, (0, 0, 0))
            self.display.blit(text, (20, 130))

        if self.lives==1:
            score_font=pygame.font.SysFont("Impact", 60)
            score_text=score_font.render(f"Final Score: {self.points}", True, (255, 255, 255))
            self.display.blit(score_text, (130, 230))
        else:
            score_font=pygame.font.SysFont("Impact", 65)
            score_text=score_font.render(f"Current Score: {self.points}", True, (255, 255, 255))
            self.display.blit(score_text, (80, 170))

        if self.lives<=1:
            instr_font=pygame.font.SysFont("Times New Roman", 33)
            instr_text=instr_font.render("Press SPACE to restart again from round 1", True, (0, 255, 0))
            self.display.blit(instr_text, (50, 320))
        else:
            instr_font=pygame.font.SysFont("Times New Roman", 33)
            instr_text=instr_font.render("Press SPACE to continue from last round", True, (0, 255, 0))
            self.display.blit(instr_text, (50, 280))

        instr_font=pygame.font.SysFont("Impact", 38)
        lives_text=instr_font.render(f"Lives left: {self.lives-1}", True, (0, 255, 255))
        self.display.blit(lives_text, (180, 370))

        pygame.display.flip()

        continuing=True
        while continuing:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        continuing=False 

        self.to_left=self.to_right=self.to_up=self.to_down=False
        self.to_left2=self.to_right2=self.to_up2=self.to_down2=False

        self.lives-=1
        if self.lives<=0:
            self.lives=5
            self.init_positions()
            return

        self.robot_x=400
        self.robot_y=380
        self.robot2_x=200
        self.robot2_y=380

        self.monster_x=0
        self.monster_y=0
        if self.round>1:
            self.round-=1
        self.make_coins() 
        self.startS.play()

if __name__ == "__main__":
    Mygame()


