# main.py
from game.game_opption import GameOpption
from game.game_offline import Game_offline  
# from game_online import Game_online
# from game_bot import Game_bot
def main():
    # Hiển thị phần Menu game
    settings = GameOpption()
    game_mode = settings.display()
    # Kiểm tra lựa chọn và bắt đầu game theo chế độ
    if game_mode == 0:
        # Bắt đầu game với AI (cần tích hợp AI vào phần này)
        # game = Game_bot()
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