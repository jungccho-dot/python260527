import pygame
import sys
import random

# Pygame 초기화
pygame.init()

# 게임 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# 스크린 생성
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블럭깨기 게임")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Paddle(pygame.sprite.Sprite):
    """플레이어 패들 클래스"""
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 15
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 7

    def update(self):
        """마우스 위치로 패들 이동"""
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.centerx = mouse_x
        
        # 화면 범위 내 유지
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    """공 클래스"""
    def __init__(self, paddle):
        super().__init__()
        self.radius = 7
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.paddle = paddle
        self.reset()

    def reset(self):
        """공을 패들 위에 리셋"""
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top - 5
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = -5

    def update(self):
        """공의 위치 업데이트"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 좌우 벽 충돌
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x

        # 위 벽 충돌
        if self.rect.top < 0:
            self.speed_y = -self.speed_y

        # 화면 하단 (게임 오버)
        if self.rect.top > SCREEN_HEIGHT:
            return False
        return True

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Block(pygame.sprite.Sprite):
    """블럭 클래스"""
    def __init__(self, x, y, color):
        super().__init__()
        self.width = 70
        self.height = 25
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        # 테두리 추가
        pygame.draw.rect(self.image, WHITE, (0, 0, self.width, self.height), 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Game:
    """게임 메인 클래스"""
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.blocks = pygame.sprite.Group()
        self.create_blocks()
        self.score = 0
        self.running = True
        self.game_over = False
        self.game_won = False

    def create_blocks(self):
        """블럭 생성"""
        self.blocks.empty()
        colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
        block_rows = 4
        block_cols = 8
        block_width = 70
        block_height = 25
        padding = 8  # 블록 사이 간격
        
        # 전체 블록들의 너비 계산
        total_width = block_cols * block_width + (block_cols - 1) * padding
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = 30

        for row in range(block_rows):
            for col in range(block_cols):
                x = start_x + col * (block_width + padding)
                y = start_y + row * (block_height + padding)
                color = colors[row % len(colors)]
                block = Block(x, y, color)
                self.blocks.add(block)

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over or self.game_won:
                        self.__init__()
                    else:
                        # 게임 시작
                        if self.ball.speed_y == 0:
                            self.ball.speed_y = -5

    def check_collisions(self):
        """충돌 감지"""
        # 패들과 공 충돌
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y = -self.ball.speed_y
            # 패들의 위치에 따라 각도 조정
            collision_x = self.ball.rect.centerx - self.paddle.rect.centerx
            self.ball.speed_x = (collision_x / self.paddle.width) * 8

        # 블럭과 공 충돌
        hit_blocks = pygame.sprite.spritecollide(self.ball, self.blocks, True)
        for block in hit_blocks:
            self.ball.speed_y = -self.ball.speed_y
            self.score += 10

        # 게임 승리 조건
        if len(self.blocks) == 0:
            self.game_won = True

    def update(self):
        """게임 상태 업데이트"""
        if not self.game_over and not self.game_won:
            self.paddle.update()
            
            if not self.ball.update():
                self.game_over = True
            
            self.check_collisions()

    def draw(self):
        """화면에 그리기"""
        screen.fill(BLACK)
        
        # 모든 객체 그리기
        self.paddle.draw(screen)
        self.ball.draw(screen)
        for block in self.blocks:
            block.draw(screen)
        
        # 점수 표시
        score_text = font.render(f"점수: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # 블럭 남은 개수
        blocks_text = font.render(f"블록: {len(self.blocks)}", True, WHITE)
        screen.blit(blocks_text, (SCREEN_WIDTH - 200, 10))
        
        # 게임 오버 메시지
        if self.game_over:
            game_over_text = font.render("게임 오버! (SPACE: 재시작)", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        # 게임 승리 메시지
        if self.game_won:
            won_text = font.render("축하합니다! 승리! (SPACE: 재시작)", True, GREEN)
            text_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(won_text, text_rect)
        
        # 게임 시작 안내
        if not self.game_over and not self.game_won and self.ball.speed_y == 0:
            start_text = font.render("SPACE: 게임 시작", True, YELLOW)
            text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(start_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        """게임 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
