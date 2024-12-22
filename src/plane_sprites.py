import random
import pygame

# 屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60
# 分数
SCORE = 0
# color
color_blue = (30, 144, 255)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
color_purple = (148, 0, 211)
color_gray = (251, 255, 242)
# 敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class CanvasOver():


    def __init__(self, screen):
    
        self.img_again = pygame.image.load("./images/again.png")
        self.img_over = pygame.image.load("./images/gameover.png")
        self.rect_again = self.img_again.get_rect()
        self.rect_over = self.img_over.get_rect()
        self.rect_again.centerx = self.rect_over.centerx = SCREEN_RECT.centerx
        self.rect_again.bottom = SCREEN_RECT.centery
        self.rect_over.y = self.rect_again.bottom + 20
        self.screen = screen

    def event_handler(self, event):
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect_again.left < pos[0] < self.rect_again.right and \
                    self.rect_again.top < pos[1] < self.rect_again.bottom:
                return 1
            elif self.rect_over.left < pos[0] < self.rect_over.right and \
                    self.rect_over.top < pos[1] < self.rect_over.bottom:
                return 0

    def update(self):
    
        self.screen.blit(self.img_again, self.rect_again)
        self.screen.blit(self.img_over, self.rect_over)
        # score_font = pygame.font.Font("./STCAIYUN.ttf", 50)
        score_font = pygame.font.SysFont('cambria', 50)
        image = score_font.render("SCORE:" + str(int(SCORE)), True, color_gray)
        rect = image.get_rect()
        rect.centerx, rect.bottom = SCREEN_RECT.centerx, self.rect_again.top - 20
        self.screen.blit(image, rect)


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
	
	def __init__(self, image_name, is_alt = False):
		super().__init__(image_name)
		if is_alt:
			self.rect.y = -self.rect.height
			
	def update(self):
		super().update()
		if self.rect.y >= SCREEN_RECT.height:
			self.rect.y = -self.rect.height
		
	
class Enemy(GameSprite):
    """敌机精灵"""
    
    def __init__(self, image_name):
    
        # 创建敌机精灵
        super().__init__(image_name)
        
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
            print("update sprites-list ...")
            self.kill()
            
    def __del__(self):
        # print("Delete enemy-plane %s" % self.rect)
        pass
        

class Hero(GameSprite):
    """英雄精灵"""
    
    def __init__(self):
    
        # 设置英雄image和speed
        super().__init__("./images/me1.png", 0)
        self.music_down = pygame.mixer.Sound("./music/me_down.wav")
        self.music_upgrade = pygame.mixer.Sound("./music/upgrade.wav")
        self.music_degrade = pygame.mixer.Sound("./music/supply.wav")
        
        # 设置英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 100
        
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
            bullet = Bullet("./images/bullet1.png", 0, -5)
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
        self.music_shoot = pygame.mixer.Sound("./music/bullet.wav")
        self.music_shoot.set_volume(0.4)

    
    def update(self):
    
        # 子弹垂直飞行
        super().update()
        
        # 飞出屏幕处理
        if self.rect.bottom < 0:
            self.kill()
    
    def __del__(self):
        
        print("Delete bullet ...")
