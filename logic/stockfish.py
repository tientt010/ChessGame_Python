import subprocess

class StockfishEngine:
    def __init__(self, stockfish_path="stockfish.exe"):
        self.stockfish_path = stockfish_path
        self.stockfish_process = None
        self.stockfish_reader = None
        self.stockfish_writer = None

    # Khởi chạy Stockfish
    def start(self):
        try:
            self.stockfish_process = subprocess.Popen(
                [self.stockfish_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True
            )
            self.stockfish_reader = self.stockfish_process.stdout
            self.stockfish_writer = self.stockfish_process.stdin
            return True
        except Exception as e:
            print(f"Lỗi khởi tạo stockfish: {e}")
            return False

    # Gửi lệnh tới Stockfish
    def send_command(self, command):
        try:
            self.stockfish_writer.write(command + '\n')
            self.stockfish_writer.flush()
        except Exception as e:
            print(f"Gửi lệnh thất bại: {e}")

    # Đọc phản hồi từ Stockfish
    def read_output(self):
        try:
            output = []
            while True:
                line = self.stockfish_reader.readline().strip()
                output.append(line)
                if line.startswith("bestmove"):
                    break
            return output
        except Exception as e:
            print(f"Không nhận được phản hồi: {e}")
            return None

    # Xử lý trường hợp gửi hàng loạt các nước đi từ trước tới giờ
    def set_position(self, moves):
        if isinstance(moves, list):
            command = f"position startpos moves {' '.join(moves)}"
        else:
            command = f"position startpos moves {moves}"
        self.send_command(command)

    # Lấy nước đi tốt nhất từ vị trí hiện tại
    def get_best_move(self):
        self.send_command("go movetime 1000")   # Phân tích trong 1 giây
        output = self.read_output()
        for line in output:
            if line.startswith("bestmove"):
                return line.split(" ")[1]
        return None

    # Dừng Stockfish
    def stop(self):
        try:
            self.send_command("quit")
            self.stockfish_process.terminate()
        except Exception as e:
            print(f"Xảy ra lỗi khi dừng stockfish: {e}")

    # Demo chơi với bot dưới dạng dòng lệnh
    def run_cli_game(self):
        try:
            moves = []
            while True:
                user_move = input("Your move: ").strip()
                if user_move == "end":
                    break
                moves.append(user_move)
                self.set_position(moves)
                best_move = self.get_best_move()
                print(f"Stockfish's move: {best_move}")
                moves.append(best_move)
        finally:
            self.stop()
