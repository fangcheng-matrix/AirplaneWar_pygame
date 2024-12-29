import random
import pygame

# 屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60
# 敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵类"""

    def __init__(self, image_name, speedx = 0, speedy = 1):

        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speedx = speedx
        self.speedy = speedy

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Background(GameSprite):
	"""游戏背景精灵"""
	
	def __init__(self, is_alt = False):
		super().__init__("../images/background.png")
		if is_alt:
			self.rect.y = -self.rect.height
			
	def update(self):
		super().update()
		if self.rect.y >= SCREEN_RECT.height:
			self.rect.y = -self.rect.height
		
	
class Enemy(GameSprite):
    """敌机精灵"""
    
    def __init__(self):
    
        # 创建敌机精灵
        super().__init__("../images/enemy1.png")
        
        # 指定敌机初始随机速度
        self.speed = random.randint(1, 3)
        
        # 指定敌机初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        
    def update(self):
        
        # 敌机垂直飞行
        super().update()
        
        # 飞出屏幕处理
        if self.rect.y >= SCREEN_RECT.height:
            # print("update sprites-list ...")
            self.kill()
            
    def __del__(self):
        # print("Delete enemy-plane %s" % self.rect)
        pass
        

class Hero(GameSprite):
    """英雄精灵"""
    
    def __init__(self):
    
        # 设置英雄image和speed
        super().__init__("../images/me1.png")
        # self.music_down = pygame.mixer.Sound("../music/me_down.wav")
        # self.music_upgrade = pygame.mixer.Sound("../music/upgrade.wav")
        # self.music_degrade = pygame.mixer.Sound("../music/supply.wav")
        
        # 设置英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom
        
        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()
        
    def update(self):
        
        # 英雄水平移动
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # 限制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom
            
    def fire(self):
        
        # print("Fire ...")
        for i in (0, 1, 2):
            # 创建子弹精灵
            bullet = Bullet("../images/bullet1.png", 0, -5)
            # bullet.music_shoot.play()
            
            # 设置精灵位置
            bullet.rect.bottom = self.rect.y - 20 * i
            bullet.rect.centerx = self.rect.centerx
            
            # 将精灵添加到精灵组
            self.bullets.add(bullet)

        
class Bullet(GameSprite):
    """子弹精灵"""
    
    def __init__(self, image_name, speedx = 0, speedy = -2):
    
        # 设置子弹image和speed
        super().__init__(image_name, speedx, speedy)
        # self.music_shoot = pygame.mixer.Sound("../music/bullet.wav")
        # self.music_shoot.set_volume(0.4)

    
    def update(self):
    
        # 子弹垂直飞行
        super().update()
        
        # 飞出屏幕处理
        if self.rect.bottom < 0:
            self.kill()
    
    def __del__(self):
        
        print("Delete bullet ...")
