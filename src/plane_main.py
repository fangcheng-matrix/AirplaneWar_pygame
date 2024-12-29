import pygame
from plane_sprites import *

pygame.init()
class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):

        print("Game initial ...")
        pygame.display.set_caption("飞机大战")
        # 创建游戏的窗口
        self.win_main = pygame.display.set_mode(SCREEN_RECT.size)
        # 游戏状态
        self.is_game_pause = False
        self.is_game_over = False
        # 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 设置定时器事件 - 创建敌机　1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
	

    def __create_sprites(self):
    
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        
        # 创建英雄精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
		
    def start_game(self):
    
        print("Game begin ...")
		
        while True:
        
            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handle()
            # 碰撞检测
            self.__check_collide()
            # 更新精灵组
            self.__update_sprites()
            # 更新显示
            pygame.display.update()
	
    def __event_handle(self):
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                PlaneGame.__game_over()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.is_game_pause = not self.is_game_pause
            elif event.type == CREATE_ENEMY_EVENT:
                # print("Create enemy-plane ...")
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
        
        # 使用键盘提供的方法获取键盘动作 ---> 按键元组
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.hero_move(2, 0)
        elif key_pressed[pygame.K_LEFT]:
            self.hero_move(-2, 0)
        elif key_pressed[pygame.K_UP]:
            self.hero_move(0, -2)
        elif key_pressed[pygame.K_DOWN]:
            self.hero_move(0, 2) 
        else:
            self.hero.speedx = 0
            self.hero.speedy = 0
		
    def hero_move(self, x = 0, y = 0):
        self.hero.speedx = x
        self.hero.speedy = y

    def __check_collide(self):
		# 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        
        # 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        
        # 判断列表是否有内容
        if len(enemies) > 0:
            # 英雄牺牲
            self.hero.kill()
            
            # 结束游戏
            PlaneGame.__game_over()
            
    def __update_sprites(self):
    
        if self.is_game_pause:
            pass

        else:
            self.back_group.update()
            self.back_group.draw(self.win_main)
        
            self.enemy_group.update()
            self.enemy_group.draw(self.win_main)
        
            self.hero_group.update()
            self.hero_group.draw(self.win_main)
        
            self.hero.bullets.update()
            self.hero.bullets.draw(self.win_main)
		
    @staticmethod
    def __game_over():
    
        print("Game over")
        pygame.quit()
        exit()
	
	
if __name__ == '__main__':

    # 创建游戏对象
	game = PlaneGame()
	# 启动游戏
	game.start_game()
	