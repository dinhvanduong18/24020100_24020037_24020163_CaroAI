# ============================================================
# main.py - Entry point của game Caro
# ============================================================

import sys
import pygame

if sys.stdout is not None and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from config import FPS, PLAYER_X, PLAYER_O, BOARD_SIZE, MODE_PVE, MODE_PVP
from game.board import Board
from game.logic import GameLogic
from ui.pygame_ui import PygameUI
from game.evaluator import Evaluator
from ai.minimax import MinimaxAgent

def main():
    # ── 1. KHỞI TẠO ──────────────────────────────────────────
    board      = Board()       # Quản lý dữ liệu bàn cờ
    logic      = GameLogic()   # Xử lý luật chơi
    ui         = PygameUI()    # Giao diện pygame
    evaluator  = Evaluator()   # Bộ đánh giá điểm số

    # Khởi tạo AI với độ sâu bằng 3
    ai_agent   = MinimaxAgent(depth=3, evaluator=evaluator)
    clock      = pygame.time.Clock()

    # Trạng thái game ban đầu
    game_mode      = MODE_PVE
    player_first   = True        # True: Người đi trước, False: Máy đi trước
    
    current_player = PLAYER_X    # Quân hiện tại đang đi
    human_player   = PLAYER_X    # Quân của Người chơi
    ai_player      = PLAYER_O    # Quân của Máy (AI)
    game_over      = False
    winner         = None
    winning_cells  = []
    is_draw        = False

    def reset_game():
        nonlocal current_player, human_player, ai_player, game_over, winner, winning_cells, is_draw
        board.reset()
        if game_mode == MODE_PVE:
            if player_first:
                human_player = PLAYER_X
                ai_player    = PLAYER_O
            else:
                human_player = PLAYER_O
                ai_player    = PLAYER_X
            
            # Đồng bộ vai trò động cho AI Agent và Evaluator
            ai_agent.PLAYER  = human_player
            ai_agent.MACHINE = ai_player
            evaluator.PLAYER  = human_player
            evaluator.MACHINE = ai_player
        else:
            # Chế độ PVP: Người đi trước mặc định là X, người thứ 2 là O
            human_player = PLAYER_X
            ai_player    = PLAYER_O
            
        current_player = PLAYER_X  # PLAYER_X (quân X) luôn đi trước
        game_over = False
        winner = None
        winning_cells = []
        is_draw = False
        print(f"\n--- Ván mới bắt đầu! (Chế độ: {'PVE' if game_mode == MODE_PVE else 'PVP'}, Đi trước: {'Người' if player_first or game_mode == MODE_PVP else 'Máy'}) ---")

    # Gọi reset_game ngay khi bắt đầu để thiết lập trạng thái ban đầu một cách nhất quán
    reset_game()

    STATE_MENU = 0
    STATE_PLAYING = 1
    game_state = STATE_MENU

    # ── 2. GAME LOOP ─────────────────────────────────────────
    running = True
    while running:
        if game_state == STATE_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    ui.update_hover(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if hasattr(ui, 'rect_btn_start') and ui.rect_btn_start and ui.rect_btn_start.collidepoint(event.pos):
                        game_state = STATE_PLAYING
                        reset_game()
            
            if running:
                ui.draw_main_menu()
                ui.render()
                clock.tick(FPS)
            continue
            
        # ── 2a. XỬ LÝ LƯỢT AI (MÁY CHƠI) ──────────────────────────
        is_ai_turn = (not game_over and game_mode == MODE_PVE and current_player == ai_player)
        
        if is_ai_turn:
            print("\n🤖 AI đang suy nghĩ...")
            
            ui.draw_board(board)
            ui.draw_pieces(board)
            ui.draw_status_bar(current_player, game_over, winner, is_draw, game_mode, ai_player)
            ui.draw_panel(game_mode, player_first)
            ui.render()
            
            best_move, _ = ai_agent.get_move(board, logic)
            
            if best_move is not None:
                row, col = best_move
                board.make_move(row, col, ai_player)
                board.last_move = (row, col)  # Lưu nước đi cuối cùng thực tế
                print(f"👉 Máy ({'X' if ai_player == PLAYER_X else 'O'}) đánh tại tọa độ [{row}, {col}]")
                
                winner, winning_cells = logic.check_winner(board)
                if winner is not None:
                    game_over = True
                    print(f"🏆 MÁY ({'X' if ai_player == PLAYER_X else 'O'}) ĐÃ THẮNG!")
                    ui.hover_cell = None
                elif logic.is_draw(board):
                    game_over = True
                    is_draw   = True
                    print("🤝 HÒA! Bàn cờ đã đầy.")
                    ui.hover_cell = None
                else:
                    current_player = human_player

        # ── 2b. XỬ LÝ SỰ KIỆN TỪ BÀN PHÍM/CHUỘT ─────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

            if event.type == pygame.MOUSEMOTION:
                # Update hover even if game_over to highlight buttons
                ui.update_hover(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = ui.handle_button_click(event.pos)
                if action == 'mode':
                    game_mode = MODE_PVP if game_mode == MODE_PVE else MODE_PVE
                    reset_game()
                    continue
                elif action == 'first':
                    if game_mode == MODE_PVE:
                        player_first = not player_first
                        reset_game()
                    continue
                elif action == 'reset':
                    reset_game()
                    continue

                if game_over or is_ai_turn:
                    continue  

                row, col = ui.get_row_col_from_mouse(event.pos)
                if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
                    continue  

                moved = board.make_move(row, col, current_player)
                if not moved:
                    continue  
                board.last_move = (row, col)  # Lưu nước đi cuối cùng thực tế
                    
                print(f"\n👤 Người chơi ({'X' if current_player == PLAYER_X else 'O'}) đánh tại [{row}, {col}]")
                
                winner, winning_cells = logic.check_winner(board)
                if winner is not None:
                    game_over = True
                    print(f"🏆 NGƯỜI CHƠI ({'X' if current_player == PLAYER_X else 'O'}) THẮNG!")
                    ui.hover_cell = None  
                elif logic.is_draw(board):
                    game_over = True
                    is_draw   = True
                    print("🤝 HÒA! Bàn cờ đã đầy.")
                    ui.hover_cell = None
                else:
                    current_player = ai_player if current_player == human_player else human_player

        # ── 2c. VẼ MÀN HÌNH ─────────────────────────────────
        ui.draw_board(board)
        ui.draw_pieces(board)

        if game_over and winning_cells:
            ui.draw_winning_line(winning_cells)

        ui.draw_status_bar(current_player, game_over, winner, is_draw, game_mode, ai_player)
        ui.draw_panel(game_mode, player_first)

        if game_over:
            ui.draw_game_over(winner, is_draw, game_mode, ai_player)

        ui.render()

        # ── 2d. GIỚI HẠN FPS ────────────────────────────────
        clock.tick(FPS)

    # ── 3. KẾT THÚC ─────────────────────────────────────────
    ui.quit()
    sys.exit()

if __name__ == "__main__":
    main()
