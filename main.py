    # main.py
from game.game_manager import Game_Manager
from game.game_offline import Game_offline  
from game.game_bot import Game_bot
# from game_online import Game_online
def main():
    # Hiển thị phần Menu game
    settings = Game_Manager()
    game_mode = settings.display()
    if game_mode == 0:

        game = Game_bot()
    elif game_mode == 1:
        game = Game_offline()
    elif game_mode == 2:
        return
    game.start()  # Bắt đầu game với chế độ đã chọn


if __name__ == "__main__":
    main()
