import pygame
from config import *

import pygame

class Game_Manager:
    # Constructor khởi tạo 
    def __init__(self):
        
        # Cài đặt màn hình và thông tin cơ bản
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Manager")
        # Tải ảnh nền và thay đổi kích thước
        self.background_image = pygame.image.load(IMAGE_PATH + "b_ground.png").convert_alpha()      # tối ưu hóa hiển thị hình ảnh
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))      # Chuẩn hóa hình ảnh về 800x800

        # Cài đặt font chữ
        self.font = pygame.font.Font(None, 36)

        # Cài đặt âm thanh
        self.select_opption = pygame.mixer.Sound("sounds/capture.wav")

        # Tùy chọn menu
        self.options = ["Single Player Mode", "Two Players Mode", "Quit Game"]
        self.selected_option = 0  # Tùy chọn được chọn
    
    # Xử lý sự kiện (phím, chuột) và cập nhật tùy chọn được chọn.
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None  # Thoát chương trình
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    self.select_opption.play()
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    self.select_opption.play()
                elif event.key == pygame.K_RETURN:
                    self.select_opption.play()
                    return False, self.selected_option  
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_hover(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return self.handle_mouse_click(pygame.mouse.get_pos())
        return True, None
    
    # Cập nhật tùy chọn được chọn khi di chuyển chuột.
    def handle_mouse_hover(self, mouse_pos):
        for i in range(len(self.options)):
            button_rect = pygame.Rect(WIDTH // 2 + 100, 250 + i * 90, 250, 70)
            if button_rect.collidepoint(mouse_pos):
                self.selected_option = i
    
    # Xử lý sự kiện nhấp chuột và trả về tùy chọn nếu chọn thành công.
    def handle_mouse_click(self, mouse_pos):
        for i in range(len(self.options)):
            button_rect = pygame.Rect(WIDTH // 2 + 100, 250 + i * 90, 250, 70)
            if button_rect.collidepoint(mouse_pos):
                self.select_opption.play()
                return False, i  # Trả về tùy chọn được chọn
        return True, None

    # Hiển thị giao diện và các tùy chọn trên màn hình.
    def render(self):
        self.screen.blit(self.background_image, (0, 0))  # Vẽ nền

        for i, option in enumerate(self.options):
            # Chọn màu cho nút (được chọn hoặc không)
            button_color = HIGHLIGHT_BUTTON_COLOR if i == self.selected_option else BUTTON_COLOR
            button_rect = pygame.Rect(WIDTH // 2 + 100, 250 + i * 90, 250, 70)
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, TEXT_COLOR, button_rect, width=3, border_radius=10)  # Viền nút

            # Vẽ văn bản lên nút
            text = self.font.render(option, True, TEXT_COLOR)
            self.screen.blit(text, text.get_rect(center=button_rect.center))

        pygame.display.flip()  # Cập nhật màn hình

    # Vòng lặp chính của giao diện
    def display(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running, selected_option = self.handle_events()
            if selected_option is not None:
                return selected_option  # Trả về tùy chọn được chọn
            self.render()
            clock.tick(FPS)


