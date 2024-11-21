import pygame

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước màn hình
screen = pygame.display.set_mode((800, 600))

# Tạo đối tượng Clock
clock = pygame.time.Clock()

# Thiết lập FPS mục tiêu
fps = 60

# Vòng lặp chính
running = True
while running:
    pygame.display.set_caption("Thiết lập FPS trong Pygame")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tô màu nền (màu đen)
    screen.fill((0, 0, 0))

    # Cập nhật màn hình
    pygame.display.flip()

    # Giới hạn FPS
    clock.tick(fps)

# Thoát khỏi Pygame
pygame.quit()
