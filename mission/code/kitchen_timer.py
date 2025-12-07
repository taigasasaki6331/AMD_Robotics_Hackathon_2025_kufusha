import pygame
import sys

# 初期化
pygame.init()

# 画面設定
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# フォント設定
font_large = pygame.font.Font(None, 120)
font_medium = pygame.font.Font(None, 60)

# タイマー設定
TIMER_DURATION = 180  # 3分 = 180秒
timer_running = False
timer_elapsed = 0.0
timer_finished = False

# 時計
clock = pygame.time.Clock()
FPS = 60

# メインループ
running = True

while running:
    dt = clock.tick(FPS) / 1000.0  # 秒単位

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # ESCキーで即座に終了
            if event.key == pygame.K_ESCAPE:
                running = False
            elif not timer_running and not timer_finished:
                # タイマー開始
                timer_running = True
                timer_elapsed = 0.0
            elif timer_running:
                # カウントダウン中にキー入力 -> 緑画面へ
                timer_running = False
                timer_finished = True

    # タイマー更新
    if timer_running:
        timer_elapsed += dt
        if timer_elapsed >= TIMER_DURATION:
            # 規定時間経過 -> 緑画面へ
            timer_running = False
            timer_finished = True
            timer_elapsed = TIMER_DURATION

    # 描画
    if timer_finished:
        # 緑一色の画面
        screen.fill(GREEN)
    elif timer_running:
        # 赤い背景でカウントダウン表示
        screen.fill(RED)

        # 残り時間計算
        remaining = TIMER_DURATION - timer_elapsed
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)

        # タイマー表示
        timer_text = font_large.render(f"{minutes:02d}:{seconds:02d}", True, WHITE)
        timer_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(timer_text, timer_rect)
    else:
        # 待機画面（白背景）
        screen.fill(WHITE)

        # 指示メッセージ
        message = font_medium.render("Press any key to start", True, BLACK)
        message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(message, message_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
