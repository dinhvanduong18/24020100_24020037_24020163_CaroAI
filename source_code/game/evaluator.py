from config import WIN_COUNT

class Evaluator:
    # Hằng số quy định trạng thái ô cờ
    EMPTY = 0
    PLAYER = 1   # MIN (Người chơi đánh X)
    MACHINE = 2  # MAX (Máy đánh O)

    def __init__(self):
        pass

    def evaluate_window(self, window):
        """
        Đánh giá điểm số của duy nhất MỘT cửa sổ.
        Trả về điểm số dương cho MACHINE (MAX) và âm cho PLAYER (MIN).
        """
        player_count = window.count(self.PLAYER)
        machine_count = window.count(self.MACHINE)
        
        # 1. Cửa sổ bị chặn hoặc chứa quân của cả hai bên -> Vô hại
        if player_count > 0 and machine_count > 0:
            return 0
            
        # 2. Cửa sổ chỉ chứa quân của MACHINE (MAX) - Tấn công
        if machine_count > 0:
            if machine_count == WIN_COUNT:
                return 100000000
            elif machine_count == WIN_COUNT - 1:
                return 200000
            elif machine_count == WIN_COUNT - 2:
                return 20000
            elif machine_count == WIN_COUNT - 3:
                return 100
                
        # 3. Cửa sổ chỉ chứa quân của PLAYER (MIN) - Phòng thủ (Điểm trừ cực nặng)
        if player_count > 0:
            if player_count == WIN_COUNT:
                return -100000000
            elif player_count == WIN_COUNT - 1:
                # Đặt điểm số phòng thủ cực lớn (-5,000,000) để đảm bảo không một tổ hợp tấn công nào
                # của Máy (trừ nước thắng trực tiếp) có thể che mờ hoặc lấn át nước đi chặn này.
                return -5000000
            elif player_count == WIN_COUNT - 2:
                return -300000
            elif player_count == WIN_COUNT - 3:
                return -1000
                
        return 0

    def evaluate_board_global(self, board_grid):
        """
        Quét toàn bộ bàn cờ theo hệ thống cửa sổ trượt không trùng lặp.
        Bao quát 100% bàn cờ và giải quyết hoàn toàn vấn đề sót/trùng điểm.
        """
        total_score = 0
        size = len(board_grid)
        win_count = WIN_COUNT  # Kích thước cửa sổ bằng WIN_COUNT động từ config
        
        # --- 1. Quét theo hàng NGANG ---
        for r in range(size):
            for c in range(size - win_count + 1):
                window = [board_grid[r][c + i] for i in range(win_count)]
                total_score += self.evaluate_window(window)
                
        # --- 2. Quét theo hàng DỌC ---
        for c in range(size):
            for r in range(size - win_count + 1):
                window = [board_grid[r + i][c] for i in range(win_count)]
                total_score += self.evaluate_window(window)
                
        # --- 3. Quét đường CHÉO CHÍNH (Từ trên-trái xuống dưới-phải) ---
        for r in range(size - win_count + 1):
            for c in range(size - win_count + 1):
                window = [board_grid[r + i][c + i] for i in range(win_count)]
                total_score += self.evaluate_window(window)
                
        # --- 4. Quét đường CHÉO PHỤ (Từ trên-phải xuống dưới-trái) ---
        for r in range(size - win_count + 1):
            for c in range(win_count - 1, size):
                window = [board_grid[r + i][c - i] for i in range(win_count)]
                total_score += self.evaluate_window(window)
                
        return total_score
