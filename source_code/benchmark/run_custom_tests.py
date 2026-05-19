import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.board import Board
from game.logic import GameLogic
from game.evaluator import Evaluator
from ai.minimax import MinimaxAgent

def setup_board_scenario(board, moves):
    for r, c, player in moves:
        board.make_move(r, c, player)

def run_test(name, moves, depth, use_pruning, logic, evaluator):
    board = Board()
    setup_board_scenario(board, moves)
    agent = MinimaxAgent(depth=depth, evaluator=evaluator, use_pruning=use_pruning)
    
    start_time = time.time()
    best_move, best_score = agent.get_move(board, logic)
    elapsed = time.time() - start_time
    nodes = agent.node_count
    
    return best_move, nodes, elapsed

def load_test_cases(filename):
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
                if not line.startswith('# ('):
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
    txt_path = os.path.join(os.path.dirname(__file__), 'testcases.txt')
    test_cases = load_test_cases(txt_path)
    
    # Filter test cases 1, 2, 4, 5, 8, 9
    target_ids = ['1', '2', '4', '5', '8', '9']
    filtered_cases = []
    for name, moves in test_cases:
        test_id = name.split('.')[0].strip()
        if test_id in target_ids:
            filtered_cases.append((name, moves))
            
    output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_results.txt'))
    
    logic = GameLogic()
    evaluator = Evaluator()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for name, moves in filtered_cases:
            f.write(f"\n{'='*60}\n")
            f.write(f"👉 KỊCH BẢN: {name}\n")
            f.write(f"{'='*60}\n")
            
            for depth in [2, 3]:
                f.write(f"\n--- ĐỘ SÂU: {depth} ---\n")
                
                # Minimax
                best_move1, nodes1, elapsed1 = run_test(name, moves, depth, False, logic, evaluator)
                f.write("[ Minimax Thuần ]\n")
                f.write(f"   - Nước đi chọn : {best_move1}\n")
                f.write(f"   - Số trạng thái: {nodes1:,} nodes\n")
                f.write(f"   - Thời gian    : {elapsed1:.4f} giây\n\n")
                
                # Alpha Beta
                best_move2, nodes2, elapsed2 = run_test(name, moves, depth, True, logic, evaluator)
                f.write("[ Alpha-Beta Pruning ]\n")
                f.write(f"   - Nước đi chọn : {best_move2}\n")
                f.write(f"   - Số trạng thái: {nodes2:,} nodes\n")
                f.write(f"   - Thời gian    : {elapsed2:.4f} giây\n\n")
                
                if elapsed2 > 0 and elapsed1 > 0:
                    speedup = elapsed1 / elapsed2
                    node_reduction = (nodes1 - nodes2) / nodes1 * 100 if nodes1 > 0 else 0
                    f.write(f"💡 KẾT LUẬN TẠI ĐỘ SÂU {depth}:\n")
                    f.write(f"   -> Alpha-Beta giảm được {node_reduction:.1f}% số node phải xét.\n")
                    f.write(f"   -> Alpha-Beta chạy nhanh gấp {speedup:.1f} lần Minimax thuần.\n")
                f.write("-" * 40 + "\n")
                
    print(f"Hoàn thành! Đã lưu kết quả vào file: {output_file}")

if __name__ == '__main__':
    main()
