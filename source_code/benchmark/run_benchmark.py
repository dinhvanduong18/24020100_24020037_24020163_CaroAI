import sys
import os
import time

if sys.stdout is not None and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Thêm thư mục gốc vào sys.path để có thể import các module của game
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.board import Board
from game.logic import GameLogic
from game.evaluator import Evaluator
from ai.minimax import MinimaxAgent

def setup_board_scenario(board, moves):
    """
    Thiết lập trạng thái bàn cờ từ danh sách các nước đi.
    moves: list các tuple (row, col, player)
    """
    for r, c, player in moves:
        board.make_move(r, c, player)

def run_test_case(name, moves, depth=3):
    """
    Chạy benchmark so sánh giữa Minimax thuần và Alpha-Beta Pruning.
    """
    print(f"\n{'='*60}")
    print(f"👉 KỊCH BẢN: {name} (Độ sâu: {depth})")
    print(f"{'='*60}")
    
    logic = GameLogic()
    evaluator = Evaluator()
    
    # 1. Minimax Thuần (Không Pruning)
    board1 = Board()
    setup_board_scenario(board1, moves)
    agent_minimax = MinimaxAgent(depth=depth, evaluator=evaluator, use_pruning=False)
    
    print("\n[ 1. Minimax Thuần ]")
    start_time = time.time()
    best_move1, best_score1 = agent_minimax.get_move(board1, logic)
    elapsed1 = time.time() - start_time
    nodes1 = agent_minimax.node_count
    print(f"   - Nước đi chọn : {best_move1}")
    print(f"   - Số trạng thái: {nodes1:,} nodes")
    print(f"   - Thời gian    : {elapsed1:.4f} giây")
    
    # 2. Alpha-Beta Pruning
    board2 = Board()
    setup_board_scenario(board2, moves)
    agent_alphabeta = MinimaxAgent(depth=depth, evaluator=evaluator, use_pruning=True)
    
    print("\n[ 2. Alpha-Beta Pruning ]")
    start_time = time.time()
    best_move2, best_score2 = agent_alphabeta.get_move(board2, logic)
    elapsed2 = time.time() - start_time
    nodes2 = agent_alphabeta.node_count
    print(f"   - Nước đi chọn : {best_move2}")
    print(f"   - Số trạng thái: {nodes2:,} nodes")
    print(f"   - Thời gian    : {elapsed2:.4f} giây")
    
    # So sánh
    if elapsed2 > 0 and elapsed1 > 0:
        speedup = elapsed1 / elapsed2
        node_reduction = (nodes1 - nodes2) / nodes1 * 100 if nodes1 > 0 else 0
        print(f"\n💡 KẾT LUẬN:")
        print(f"   -> Alpha-Beta giảm được {node_reduction:.1f}% số node phải xét.")
        print(f"   -> Alpha-Beta chạy nhanh gấp {speedup:.1f} lần Minimax thuần.")

def load_test_cases(filename):
    """Đọc cấu hình testcase từ file txt"""
    test_cases = []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = content.split('\n\n')
    for block in blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue
            
        name = "Unknown"
        moves = []
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                if not line.startswith('# ('): # Bỏ qua dòng comment giải thích
                    name = line[1:].strip()
            elif line:
                for m_str in line.split('|'):
                    m_str = m_str.strip()
                    if m_str:
                        r, c, p = map(int, m_str.split(','))
                        moves.append((r, c, p))
        
        if name != "Unknown":
            test_cases.append((name, moves))
            
    return test_cases

def main():
    print("BẮT ĐẦU CHẠY BENCHMARK SO SÁNH THUẬT TOÁN...")
    
    txt_path = os.path.join(os.path.dirname(__file__), 'testcases.txt')
    if not os.path.exists(txt_path):
        print(f"❌ Không tìm thấy file {txt_path}")
        return
        
    test_cases = load_test_cases(txt_path)
    
    for name, moves in test_cases:
        run_test_case(name, moves, depth=3)

if __name__ == '__main__':
    main()
