import pygame
from plane_sprites import *

class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("Game initial ...")
        pygame.init()
        # 1.创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 4.设置定时器事件 - 创建敌机　1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
	
    def __create_sprites(self):
    
        # 1.创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        
        # 2.创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        
        # 3.创建英雄精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
		
    def start_game(self):
    
        print("Game begin ...")
		
        while True:
        
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handle()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()
	
    def __event_handle(self):
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("Create enemy-plane ...")
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            # elif event.type == pygame.KEYDOWN and event.type == pygame.K_RIGHT:
            #     print("Move right ...")
        
        # 使用键盘提供的方法获取键盘动作 ---> 按键元组
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif key_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0
		
    def __check_collide(self):
		# 1.子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        
        # 2.敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        
        # 3.判断列表是否有内容
        if len(enemies) > 0:
            # 英雄牺牲
            self.hero.kill()
            
            # 结束游戏
            PlaneGame.__game_over()
            
    def __update_sprites(self):
    
        self.back_group.update()
        self.back_group.draw(self.screen)
        
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
		
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
	