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
	
	def __init__(self, image_name, speed = 1):
	
		super().__init__()
		self.image = pygame.image.load(image_name)
		self.rect = self.image.get_rect()
		self.speed = speed
		
	def update(self):
		self.rect.y += self.speed


class Background(GameSprite):
	"""游戏背景精灵"""
	
	def __init__(self, is_alt = False):
		super().__init__("./images/background.png")
		if is_alt:
			self.rect.y = -self.rect.height
			
	def update(self):
		super().update()
		if self.rect.y >= SCREEN_RECT.height:
			self.rect.y = -self.rect.height
		
	
class Enemy(GameSprite):
    """敌机精灵"""
    
    def __init__(self):
    
        # 1.创建敌机精灵
        super().__init__("./images/enemy1.png")
        
        # 2.指定敌机初始随机速度
        self.speed = random.randint(1, 3)
        
        # 3.指定敌机初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        
    def update(self):
        
        # 1.敌机垂直飞行
        super().update()
        
        # 2.飞出屏幕处理
        if self.rect.y >= SCREEN_RECT.height:
            print("飞出屏幕 更新精灵列表")
            self.kill()
            
    def __del__(self):
        print("销毁敌机 %s" % self.rect)
        

class Hero(GameSprite):
    """英雄精灵"""
    
    def __init__(self):
    
        # 1.设置英雄image和speed
        super().__init__("./images/me1.png", 0)
        
        # 2.设置英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 100
        
        # 3. 创建子弹精灵组
        self.bullets = pygame.sprite.Group()
        
    def update(self):
        
        # 1.英雄水平移动
        self.rect.x += self.speed
        
        # 2.限制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
            
    def fire(self):
        
        # print("发射子弹。。。")
        for i in (0, 1, 2):
            # 1.创建子弹精灵
            bullet = Bullet()
            
            # 2.设置精灵位置
            bullet.rect.bottom = self.rect.y - 20 * i
            bullet.rect.centerx = self.rect.centerx
            
            # 3.将精灵添加到精灵组
            self.bullets.add(bullet)
        
        
class Bullet(GameSprite):
    """子弹精灵"""
    
    def __init__(self):
    
        # 1.设置子弹image和speed
        super().__init__("./images/bullet1.png", -2)
    
    def update(self):
    
        # 1.子弹垂直飞行
        super().update()
        
        # 2.飞出屏幕处理
        if self.rect.bottom < 0:
            self.kill()
    
    def __del__(self):
        
        print("子弹被销毁。。。")
