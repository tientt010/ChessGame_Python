import pygame
from game.config import *

class GameOpption:
    def __init__(self):
        pygame.init()
        
        # Sử dụng kích thước từ config
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Settings")

        # Load ảnh nền  
        self.background_image = pygame.image.load(IMAGE_PATH + "back_ground.png")
        self.background_image = pygame.transform.scale(
            self.background_image, (WIDTH, HEIGHT)
        )
        
        # Cài đặt font và màu cho các tùy chọn
        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)

        # Vị trí và nội dung cho các tùy chọn
        self.options = ["Play vs Computer", "Two Players (Offline)", "Two Players (Online)"]
        self.selected_option = 0  # Dùng để xác định lựa chọn hiện tại
        self.select_opption = pygame.mixer.Sound("sounds/capture.wav")


    def display(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.select_opption.play()
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                        self.select_opption.play()
                    elif event.key == pygame.K_RETURN:
                        self.select_opption.play()
                        return self.selected_option
                elif event.type == pygame.MOUSEMOTION:
                    # Cập nhật selected_option khi di chuyển chuột vào vùng của một tùy chọn
                    mouse_pos = pygame.mouse.get_pos()
                    #self.select_opption.play()
                    for i, option in enumerate(self.options):
                        text_rect = self.font.render(option, True, self.text_color).get_rect(
                            center=(WIDTH // 2, 150 + i * 50)
                        )
                        if text_rect.collidepoint(mouse_pos):
                            self.selected_option = i
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Chọn tùy chọn khi nhấp chuột
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.options):
                        text_rect = self.font.render(option, True, self.text_color).get_rect(
                            center=(WIDTH // 2, 150 + i * 50)
                        )
                        if text_rect.collidepoint(mouse_pos):
                            self.selected_option = i
                            self.select_opption.play()
                            return self.selected_option

            # Vẽ ảnh nền
            self.screen.blit(self.background_image, (0, 0))

            # Hiển thị từng tùy chọn và highlight tùy chọn được chọn
            for i, option in enumerate(self.options):
                color = (255, 255, 0) if i == self.selected_option else self.text_color
                text = self.font.render(option, True, color)
                text_rect = text.get_rect(center=(WIDTH // 2, 150 + i * 50))
                self.screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.quit()
# Ví dụ sử dụng
# if __name__ == "__main__":
#     gameopption = GameOpption()
#     choice = gameopption.display()
#     print("Option selected:", choice)
