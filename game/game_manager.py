import pygame
from config import *

import pygame

class Game_Manager:
    def __init__(self):
        pygame.init()

        # Kích thước màn hình
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Settings")

        # Load ảnh nền  
        self.background_image = pygame.image.load(IMAGE_PATH + "b_ground.png").convert_alpha()
        self.background_image = pygame.transform.scale(
            self.background_image, (WIDTH, HEIGHT)
        )

        # Cài đặt font và màu sắc cho các tùy chọn
        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)
        self.highlight_color = (0, 200, 0)  # Màu xanh lá cho tùy chọn được chọn
        self.button_color = (50, 50, 50)    # Màu nút thông thường

        # Vị trí và nội dung cho các tùy chọn
        self.options = ["Play vs Computer", "Two Players (Offline)", "Quit Game"]
        self.selected_option = 0  # Dùng để xác định lựa chọn hiện tại
        self.select_opption = pygame.mixer.Sound("sounds/capture.wav")

    def display(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))  # Vẽ nền mỗi vòng lặp

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
                    for i, option in enumerate(self.options):
                        button_rect = pygame.Rect(WIDTH // 2 + 100, 250 + i * 90, 250 , 70)
                        if button_rect.collidepoint(mouse_pos):
                            self.selected_option = i
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Chọn tùy chọn khi nhấp chuột
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.options):
                        button_rect = pygame.Rect(WIDTH // 2 + 100, 250 + i * 90, 250 , 70)
                        if button_rect.collidepoint(mouse_pos):
                            self.selected_option = i
                            self.select_opption.play()
                            return self.selected_option

            # Hiển thị từng nút tùy chọn
            for i, option in enumerate(self.options):
                # Chọn màu cho nút
                button_color = self.highlight_color if i == self.selected_option else self.button_color
                # Tạo hình chữ nhật đại diện cho nút
                button_rect = pygame.Rect(WIDTH // 2 + 100, 250 + i * 90, 250 , 70)
                pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
                # Vẽ viền nút
                pygame.draw.rect(self.screen, self.text_color, button_rect, width=3, border_radius=10)

                # Vẽ văn bản lên nút
                text = self.font.render(option, True, self.text_color)
                text_rect = text.get_rect(center=button_rect.center)
                self.screen.blit(text, text_rect)

            pygame.display.flip()  # Cập nhật màn hình

        pygame.quit()
# Ví dụ sử dụng
# if __name__ == "__main__":
#     gameopption = GameOpption()
#     choice = gameopption.display()
#     print("Option selected:", choice)
