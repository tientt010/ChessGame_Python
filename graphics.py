import pygame
import random
from config import *
from scipy.ndimage import gaussian_filter
from moviepy.editor import VideoFileClip
from threading import Thread

class Graphics:
    # Khởi tạo lớp Graphics với các thuộc tính cơ bản.
    def __init__(self, board, title):
        self.board = board  # Bảng cờ
        self.font = pygame.font.Font(None, 24)  # Font mặc định
        self.window = pygame.display.set_mode((WIDTH + 200, HEIGHT), pygame.DOUBLEBUF | pygame.SRCALPHA)
        pygame.display.set_caption(title)  # Tiêu đề cửa sổ
        self.load_images()  # Tải các hình ảnh quân cờ
        self.clock = pygame.time.Clock()  # Đối tượng clock của pygame
        self.running = True  # Trạng thái game
        self.draw_initial_board()  # Vẽ bàn cờ ban đầu

    # Tải dữ liệu (hình ảnh)
    def load_images(self):
        """
        Tải và điều chỉnh kích thước các hình ảnh quân cờ.
        """
        self.images = {}
        pieces = ['wP', 'bP', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ', 'wK', 'bK']
        for piece in pieces:
            original_image = pygame.image.load(IMAGE_PATH + piece + ".png").convert_alpha()
            self.images[piece] = pygame.transform.smoothscale(
                original_image, (SQUARE_SIZE, SQUARE_SIZE)
            )

    # Vẽ bàn cờ và quân cờ
    def draw_board(self, pos=None):
        # Vẽ bàn cờ với các ô vuông xen kẽ màu.
        colors = [LIGHT_BROWN, DARK_BROWN]
        for row in range(ROWS):
            for col in range(COLS):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if pos is not None:
            row, col = pos
            pygame.draw.rect(self.window, RED, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Vẽ quân cờ trên bàn cờ
    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece((row, col))
                if piece:
                    color = 'w' if piece.get_color() == 'w' else 'b'
                    piece_name = color + piece.__class__.__name__[0]
                    if piece.__class__.__name__ == "Knight":
                        piece_name = color + 'N'
                    self.window.blit(self.images[piece_name], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Vẽ bàn cờ ban đầu và khu vực thời gian
    def draw_initial_board(self):
        self.draw_board()
        self.draw_pieces()
        # Vẽ khu vực đồng hồ
        black_rect = pygame.Rect(WIDTH, 0, 200, HEIGHT // 2)
        white_rect = pygame.Rect(WIDTH, HEIGHT // 2, 200, HEIGHT // 2)
        pygame.draw.rect(self.window, (0, 0, 0), black_rect)
        pygame.draw.rect(self.window, (255, 255, 255), white_rect)
        pygame.display.flip()

    # Cập nhật bàn cờ sau mỗi nước đi
    def draw_update(self, is_capture, current="w", pos=None):
        self.draw_board(pos)
        self.draw_pieces()
        pygame.display.flip()
        if is_capture:
            show_icon_thread = Thread(target=self.show_icon(current), daemon=True)
            show_icon_thread.start()

    # Highlight ô vuông hoặc các nước đi hợp lệ.
    def highlight_square(self, position, highlight_type='piece'):
        if position:
            row, col = position
            if highlight_type == 'piece':
                pygame.draw.rect(self.window, HIGHLIGHT_COLOR,
                                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
            elif highlight_type == 'move':
                pygame.draw.circle(self.window, MOVE_HIGHLIGHT_COLOR,
                                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                SQUARE_SIZE // 4)
            pygame.display.flip()
    
    # Lấy vị trí ô vuông đang được con trỏ chuột trỏ vào.
    def get_square_under_mouse(self, mouse_pos):
        x, y = mouse_pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        if col >= COLS or row >= ROWS:
            return None
        return row, col

    # Hiển thị icon trạng thái dựa vào lượt đi.
    def show_icon(self, current_turn):
        if current_turn == 'b':
            self.show_status(WIDTH + 50, HEIGHT // 2 + 50, 'happy', WIDTH + 50, HEIGHT // 2 - 150, 'sad')
        else:
            self.show_status(WIDTH + 50, HEIGHT // 2 + 50, 'sad', WIDTH + 50, HEIGHT // 2 - 150, 'happy')
    
    # Hiển thị icon trạng thái (happy hoặc bad)
    def show_status(self, x1, y1, status1, x2, y2, status2):
        gif_index1 = random.randrange(1, 5 if status1 == 'happy' else 9)  # Chọn ngẫu nhiên một trong các file GIF đầu tiên
        gif_index2 = random.randrange(1, 5 if status2 == 'happy' else 9)  # Chọn ngẫu nhiên một trong các file GIF thứ hai
        gif_path1 = f'images/{status1}{gif_index1}.gif'
        gif_path2 = f'images/{status2}{gif_index2}.gif'

        # Tải GIF động với moviepy và chỉnh kích thước về 100x100
        clip1 = VideoFileClip(gif_path1).resize((100, 100))
        clip2 = VideoFileClip(gif_path2).resize((100, 100))

        running = True
        start_ticks = pygame.time.get_ticks()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
            frame1 = clip1.get_frame(elapsed_time % clip1.duration)
            frame_surface1 = pygame.surfarray.make_surface(frame1.swapaxes(0, 1))

            frame2 = clip2.get_frame(elapsed_time % clip2.duration)
            frame_surface2 = pygame.surfarray.make_surface(frame2.swapaxes(0, 1))

            # Vẽ GIF lên màn hình tại vị trí xác định (x, y) trên nền màu đã tạo
            self.window.blit(frame_surface1, (x1, y1))
            self.window.blit(frame_surface2, (x2, y2))

            # Cập nhật màn hình
            pygame.display.update(x1, y1, 100, 100)
            pygame.display.update(x2, y2, 100, 100)

            # Kết thúc sau 3 giây
            if pygame.time.get_ticks() - start_ticks >= 1500:
                running = False

        # Đóng các clip sau khi hiển thị
        clip1.close()
        clip2.close()

    # Hiển thị kết quả sau khi kết thúc trò chơi
    def show_result(self, result, message, color=(0, 0, 255)):
        pygame.time.wait(3000)
        gif_path = 'images/' + result + ".gif"
        background = self.window.copy()
        blurred_background = self.apply_gaussian_blur(background, 10)
        self.window.blit(blurred_background, (0, 0))

        # Tải video và chuyển đổi thành danh sách frame
        clip = VideoFileClip(gif_path)
        frames = [pygame.surfarray.make_surface(frame.swapaxes(0, 1)) for frame in clip.iter_frames()]

        font = pygame.font.SysFont(None, 50)

        # Vẽ text
        def draw_text(surface, text, font, pos, text_color, shadow_color):
            text_surface = font.render(text, True, shadow_color)
            text_rect = text_surface.get_rect(center=(pos[0] + 2, pos[1] + 2))
            surface.blit(text_surface, text_rect)
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=pos)
            surface.blit(text_surface, text_rect)

        # Vẽ nút
        def draw_button(surface, text, rect, color, hover_color):
            mouse_pos = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, hover_color, rect)  # Hover
            else:
                pygame.draw.rect(surface, color, rect)  # Bình thường
            draw_text(surface, text, font, rect.center, (255, 255, 255), (0, 0, 0))

        # Xử lý sự kiện nút
        def handle_button_click():
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_pos):
                return 1  # Chuyển trạng thái
            elif exit_button.collidepoint(mouse_pos):
                return 2  # Chuyển trạng thái
            return False

        running = True
        start_ticks = pygame.time.get_ticks()

        # Định nghĩa các nút
        button_width, button_height = 200, 50
        restart_button = pygame.Rect(
            self.window.get_width() // 2 - button_width - 10,
            self.window.get_height() - button_height - 20,
            button_width, button_height
        )
        exit_button = pygame.Rect(
            self.window.get_width() // 2 + 10,
            self.window.get_height() - button_height - 20,
            button_width, button_height
        )

        # Vòng lặp hiển thị
        clock = pygame.time.Clock()
        check = 2
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    check = handle_button_click()
                    if check:
                        running = False

            # Tính toán frame hiện tại
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
            frame_index = int(elapsed_time * clip.fps) % len(frames)

            # Hiển thị background và frame video
            self.window.blit(blurred_background, (0, 0))
            frame_surface = frames[frame_index]
            screen_width, screen_height = self.window.get_size()
            x_pos = (screen_width - frame_surface.get_width()) // 2
            y_pos = (screen_height - frame_surface.get_height()) // 2
            self.window.blit(frame_surface, (x_pos, y_pos))

            # Hiển thị thông điệp
            draw_text(self.window, message, font, (screen_width // 2, y_pos - 50), color, (0, 0, 0))

            # Vẽ các nút
            draw_button(self.window, "Play Again", restart_button, (0, 128, 0), (0, 255, 0))
            draw_button(self.window, "Exit", exit_button, (128, 0, 0), (255, 0, 0))

            pygame.display.update()
            clock.tick(30)  # Giới hạn 30 FPS

        clip.close()
        return check
    
    # Vẽ khung hiển thị của đồng hồ của 2 bên
    def draw_timer_box(self, height = HEIGHT//2):
        white_timer_rect = pygame.Rect(WIDTH, HEIGHT-height, 200, height)    
        pygame.draw.rect(self.window, (255, 255, 255), white_timer_rect)  # Nền màu trắng

        black_timer_rect = pygame.Rect(WIDTH, 0, 200, height)
        pygame.draw.rect(self.window, (0, 0, 0), black_timer_rect)  # Nền màu đen

    # Vẽ thời gian cho hai người chơi
    def draw_timers(self, time_white, time_black):
        # Vẽ lại các hộp đồng hồ trước khi vẽ thời gian
        self.draw_timer_box(150)

        # Phông chữ nhỏ hơn cho đồng hồ
        small_font = pygame.font.SysFont(None, 50)  # Đặt kích thước phông chữ nhỏ hơn cho phù hợp với ô đồng hồ

        # Tạo text thời gian cho quân trắng và đen
        white_time_text = small_font.render(f"{time_white // 60}:{time_white % 60:02}", True, (0, 0, 0))
        black_time_text = small_font.render(f"{time_black // 60}:{time_black % 60:02}", True, (255, 255, 255))

        # Đặt vị trí text thời gian để căn giữa trong các ô đồng hồ
        white_text_rect = white_time_text.get_rect(center=(WIDTH + 100, HEIGHT - 100))  
        black_text_rect = black_time_text.get_rect(center=(WIDTH + 100, 100))            

        # Vẽ text lên cửa sổ
        self.window.blit(white_time_text, white_text_rect)
        self.window.blit(black_time_text, black_text_rect)

        # Cập nhật phần hiển thị của các ô đồng hồ
        pygame.display.update(WIDTH, 0, 200, HEIGHT)
    
    # Áp dụng Gaussian Blur lên bề mặt
    def apply_gaussian_blur(self, surface, sigma=5):
        # Chuyển bề mặt thành mảng numpy
        array = pygame.surfarray.pixels3d(surface).copy()

        # Áp dụng Gaussian Blur
        blurred_array = gaussian_filter(array, sigma=(sigma, sigma, 0))

        # Tạo lại bề mặt từ mảng đã làm mờ
        blurred_surface = pygame.surfarray.make_surface(blurred_array)
        return blurred_surface
