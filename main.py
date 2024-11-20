import pygame
from game.game_manager import Game_Manager
from game.game_offline import Game_offline  
from game.game_bot import Game_bot

def main():
    pygame.init()

    # Hiển thị phần Menu game
    game = game_menu()
    while game:
        op = game.start()  # Bắt đầu game với chế độ đã chọn
        if op == 0:
            game = Game_bot()
        elif op == 1:
            game = Game_offline()
        elif op == 2:   
            game = game_menu()
        else:
            break
    
    pygame.quit()

def game_menu():
    settings = Game_Manager()
    game_mode = settings.display()
    if game_mode == 0:
        return Game_bot()
    elif game_mode == 1:
        return Game_offline()
    return False

if __name__ == "__main__":
    main()
