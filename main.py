    # main.py
from game.game_manager import Game_Manager
from game.game_offline import Game_offline  
from game.game_bot import Game_bot
# from game_online import Game_online
def main():
    # Hiển thị phần Menu game
    settings = Game_Manager()
    game_mode = settings.display()
    # Kiểm tra lựa chọn và bắt đầu game theo chế độ
    if game_mode == 0:
        # Bắt đầu game với AI (cần tích hợp AI vào phần này)
        try:
            game = Game_bot()
            game.start()
        except Exception as e:
            print(f"Error: {e}")
        return
    elif game_mode == 1:
        # Bắt đầu game với chế độ offline
        game = Game_offline()
    elif game_mode == 2:
        # Bắt đầu game với chế độ online (cần tích hợp online vào phần này)
        # game = Game_online()
        return

    game.start()  # Bắt đầu game với chế độ đã chọn


if __name__ == "__main__":
    main()
