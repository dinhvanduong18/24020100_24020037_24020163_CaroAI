import time

class MinimaxAgent:
    """
    Class AI sử dụng thuật toán Minimax tích lũy điểm dọc theo các nhánh tìm kiếm.
    Cấu trúc có áp dụng cắt tỉa Alpha-Beta để tối ưu.
    """

    def __init__(self, depth, evaluator, use_pruning=True):
        self.max_depth = depth
        self.evaluator = evaluator
        self.PLAYER = 1   # X (MIN)
        self.MACHINE = 2  # O (MAX)
        self.node_count = 0
        self.use_pruning = use_pruning

    def get_move(self, board, game_logic):
        """
        Khởi động quá trình tìm kiếm nước đi tốt nhất cho Máy (MAX) sử dụng cắt tỉa Alpha-Beta.
        """
        start_time = time.time()
        self.node_count = 0
        
        best_score = -float('inf')
        best_move = None
        best_move_score = -float('inf')
        
        alpha = -float('inf')
        beta = float('inf')
        
        # Lấy các ô trống trong bán kính 2 để tập trung đánh xoay quanh các quân cờ
        empty_cells = board.get_empty_cells(radius=2)
        
        for r, c in empty_cells:
            # 1. Tính điểm phòng thủ: Nếu Người (MIN) đánh vào đây thì được bao nhiêu?
            board.make_move(r, c, self.PLAYER)
            defense_score = self.evaluator.evaluate_local(board.grid, r, c)
            board.undo_move(r, c)
            
            # 2. Tính điểm tấn công: Máy (MAX) thực sự đánh vào đây
            board.make_move(r, c, self.MACHINE)
            attack_score = self.evaluator.evaluate_local(board.grid, r, c)
            
            # Đánh giá toàn cục bàn cờ làm tiêu chí phụ (tie-breaker)
            board_score = self._evaluate_board(board)
            
            # Điểm của nước đi = Điểm tấn công của Máy - Điểm phòng thủ (tức là chặn Người chơi)
            # Vì Evaluator trả điểm âm cho Người chơi, nên attack - defense -> Tăng điểm dương cho Máy
            move_score = attack_score - defense_score
            
            # Gọi đệ quy hàm minimax với alpha, beta
            score = self._minimax_rec(board, self.max_depth - 1, False, move_score, r, c, game_logic, alpha, beta)
            
            # Rút lại nước đi để làm sạch trạng thái bàn cờ
            board.undo_move(r, c)
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
                best_move_score = board_score
            elif score == best_score:
                # Nếu có nhiều nước đi dẫn đến cùng một kết quả (ví dụ đều bị thua)
                # thì ưu tiên nước đi có điểm bàn cờ toàn cục (board_score) cao hơn
                if best_move is None or board_score > best_move_score:
                    best_move = (r, c)
                    best_move_score = board_score
                
            # Cập nhật alpha
            if self.use_pruning:
                alpha = max(alpha, best_score)
                
        execution_time = time.time() - start_time
        
        # Báo cáo ra terminal
        print(f"[Alpha-Beta] Độ sâu: {self.max_depth} | Trạng thái đã xét: {self.node_count} "
              f"| Thời gian: {execution_time:.4f}s | Chọn nước: {best_move} | Điểm: {best_score}")
              
        return best_move, best_score

    def _minimax_rec(self, board, depth, is_maximizing, current_score, last_r, last_c, game_logic, alpha, beta):
        """
        Hàm đệ quy duyệt cây Minimax theo cách cộng dồn điểm (current_score) với cắt tỉa Alpha-Beta.
        
        Args:
            board: Bàn cờ hiện tại
            depth: Độ sâu còn lại
            is_maximizing: True (MAX - Máy), False (MIN - Người)
            current_score: Điểm tổng tích lũy từ gốc cây xuống tới node hiện tại
            last_r, last_c: Tọa độ nước đi vừa thực hiện (để kiểm tra kết thúc/thắng)
            game_logic: Đối tượng xử lý luật chơi
            alpha: Giá trị tốt nhất hiện tại cho nhánh MAX
            beta: Giá trị tốt nhất hiện tại cho nhánh MIN
        """
        self.node_count += 1
        
        # Kiểm tra thắng thua thực tế
        winner, _ = game_logic.check_winner(board)
        if winner == self.MACHINE:
            return 100000000 + depth 
        elif winner == self.PLAYER:
            return -100000000 - depth 
            
        if board.is_full() or depth == 0:
            # Chỉ tính toán điểm Heuristic tại nút lá
            return self._evaluate_board(board)
            
        moves = board.get_empty_cells(radius=2)
        
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in moves:
                board.make_move(r, c, self.MACHINE)
                
                eval_score = self._minimax_rec(board, depth - 1, False, current_score, r, c, game_logic, alpha, beta)
                board.undo_move(r, c)
                max_eval = max(max_eval, eval_score)
                
                if self.use_pruning:
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
                
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in moves:
                board.make_move(r, c, self.PLAYER)
                
                eval_score = self._minimax_rec(board, depth - 1, True, current_score, r, c, game_logic, alpha, beta)
                board.undo_move(r, c)
                min_eval = min(min_eval, eval_score)
                
                if self.use_pruning:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
                
            return min_eval

    def _evaluate_board(self, board):
        """
        Đánh giá điểm số của toàn bộ bàn cờ.
        """
        total_score = 0
        # Chỉ quét những ô có quân cờ để tính điểm
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] != 0:
                    # evaluate_local sẽ trả về điểm dương cho MACHINE, âm cho PLAYER
                    total_score += self.evaluator.evaluate_local(board.grid, r, c)
        return total_score
