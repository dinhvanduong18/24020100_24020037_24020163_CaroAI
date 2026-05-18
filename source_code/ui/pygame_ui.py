# ============================================================
# ui/pygame_ui.py - Class giao diện đồ họa dùng Pygame
# ============================================================

import pygame
import math
from config import (
    BOARD_SIZE, CELL_SIZE, MARGIN, STATUS_HEIGHT, PANEL_WIDTH,
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    PLAYER_X, PLAYER_O, EMPTY,
    COLOR_BG, COLOR_GRID, COLOR_X, COLOR_O,
    COLOR_STATUS_BG, COLOR_STATUS_TXT,
    COLOR_WIN_LINE, COLOR_HOVER, COLOR_BLACK, COLOR_WHITE,
    COLOR_BTN_BG, COLOR_BTN_HOVER, COLOR_BTN_TEXT, COLOR_PANEL_BG,
    MODE_PVE, MODE_PVP
)
from game.board import Board


class PygameUI:
    """
    Lớp PygameUI chịu trách nhiệm toàn bộ phần hiển thị.
    Tách biệt hoàn toàn với logic game.
    """

    def __init__(self):
        """
        Khởi tạo cửa sổ pygame và font chữ.
        """
        pygame.init()
        # Tạo cửa sổ với kích thước đã tính trong config
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        # Font chữ cho trạng thái game
        self.font_status = pygame.font.SysFont("segoeui", 22, bold=True)
        self.font_symbol = pygame.font.SysFont("segoeui", 32, bold=True)
        self.font_btn = pygame.font.SysFont("segoeui", 20, bold=True)

        # Lưu vị trí chuột hiện tại để vẽ hover effect
        self.hover_cell = None
        self.mouse_pos = (0, 0)

        # Định nghĩa vùng nút bấm
        panel_x = CELL_SIZE * BOARD_SIZE + MARGIN * 2
        btn_w = 220
        btn_h = 50
        btn_x = panel_x + (PANEL_WIDTH - btn_w) // 2
        
        self.rect_btn_mode = pygame.Rect(btn_x, 100, btn_w, btn_h)
        self.rect_btn_first = pygame.Rect(btn_x, 180, btn_w, btn_h)
        self.rect_btn_reset = pygame.Rect(btn_x, 260, btn_w, btn_h)
        self.rect_btn_start = None  # Menu chính

    # ----------------------------------------------------------
    # PHẦN VẼ GIAO DIỆN
    # ----------------------------------------------------------

    def draw_status_bar(self, current_player: int, game_over: bool, winner, is_draw: bool, game_mode: int = MODE_PVP, ai_player: int = None):
        """
        Vẽ thanh trạng thái ở phía trên cùng màn hình.
        Hiển thị lượt chơi hiện tại hoặc kết quả game.
        """
        # Vẽ nền thanh trạng thái
        pygame.draw.rect(self.screen, COLOR_STATUS_BG,
                         (0, 0, WINDOW_WIDTH, STATUS_HEIGHT))

        # Khu vực bảng game (bên trái)
        board_area_width = CELL_SIZE * BOARD_SIZE + MARGIN * 2

        # Xác định nội dung text
        if game_over:
            text = "TRẬN ĐẤU KẾT THÚC"
            surf = self.font_status.render(text, True, COLOR_WHITE)
            x_pos = (board_area_width - surf.get_width()) // 2
            y_pos = (STATUS_HEIGHT - surf.get_height()) // 2
            self.screen.blit(surf, (x_pos, y_pos))
        else:
            symbol = "X" if current_player == PLAYER_X else "O"
            color = COLOR_X if current_player == PLAYER_X else COLOR_O
            
            if game_mode == MODE_PVE:
                if current_player == ai_player:
                    prefix_text = "Lượt của Máy (AI):  "
                else:
                    prefix_text = "Lượt của Bạn:  "
            else:
                prefix_text = "Lượt của người chơi:  "
                
            # Render phần đầu với màu trắng, phần tên người chơi với màu riêng
            surf_pre  = self.font_status.render(prefix_text, True, COLOR_STATUS_TXT)
            surf_name = self.font_status.render(symbol, True, color)
            # Tính vị trí căn giữa trên bảng cờ
            total_w = surf_pre.get_width() + surf_name.get_width()
            x_start = (board_area_width - total_w) // 2
            y_pos   = (STATUS_HEIGHT - surf_pre.get_height()) // 2
            self.screen.blit(surf_pre,  (x_start, y_pos))
            self.screen.blit(surf_name, (x_start + surf_pre.get_width(), y_pos))

    def draw_board(self, board: Board):
        """
        Vẽ nền và lưới của bàn cờ.
        Lưới bắt đầu từ tọa độ (MARGIN, STATUS_HEIGHT + MARGIN).
        """
        # Vẽ nền toàn màn hình (màu bàn cờ)
        self.screen.fill(COLOR_BG)

        # Vẽ vùng bàn cờ sáng hơn
        board_rect = pygame.Rect(
            MARGIN, STATUS_HEIGHT + MARGIN,
            CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE
        )
        pygame.draw.rect(self.screen, COLOR_BG, board_rect)

        # Vẽ hover effect (tô màu ô đang trỏ chuột)
        if self.hover_cell:
            h_row, h_col = self.hover_cell
            hover_rect = pygame.Rect(
                MARGIN + h_col * CELL_SIZE,
                STATUS_HEIGHT + MARGIN + h_row * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(self.screen, COLOR_HOVER, hover_rect)

        # Vẽ highlight nước đi cuối cùng (Hiệu ứng nhấp nháy và góc ngắm)
        if getattr(board, 'last_move', None) is not None:
            last_row, last_col = board.last_move
            
            x = MARGIN + last_col * CELL_SIZE
            y = STATUS_HEIGHT + MARGIN + last_row * CELL_SIZE
            
            last_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            
            # Tô nền nhẹ cho ô vừa đánh
            pygame.draw.rect(self.screen, (255, 245, 200), last_rect)
            
            # Hiệu ứng viền nhấp nháy theo thời gian (pulsing)
            time_ms = pygame.time.get_ticks()
            pulse = (math.sin(time_ms / 150.0) + 1) / 2  # Dao động từ 0.0 đến 1.0
            
            # Màu cam đỏ nhấp nháy
            color_pulse = (255, int(100 + 100 * pulse), 0)
            
            # Vẽ viền nhấp nháy mỏng
            pygame.draw.rect(self.screen, color_pulse, last_rect, max(1, int(2 + 2 * pulse)))
            
            # Vẽ 4 góc ngắm (Targeting corners) bao quanh ô
            c_len = CELL_SIZE // 4  # Chiều dài cạnh góc
            c_thick = 3             # Độ dày
            
            # Top-Left
            pygame.draw.line(self.screen, color_pulse, (x, y), (x + c_len, y), c_thick)
            pygame.draw.line(self.screen, color_pulse, (x, y), (x, y + c_len), c_thick)
            # Top-Right
            pygame.draw.line(self.screen, color_pulse, (x + CELL_SIZE, y), (x + CELL_SIZE - c_len, y), c_thick)
            pygame.draw.line(self.screen, color_pulse, (x + CELL_SIZE, y), (x + CELL_SIZE, y + c_len), c_thick)
            # Bottom-Left
            pygame.draw.line(self.screen, color_pulse, (x, y + CELL_SIZE), (x + c_len, y + CELL_SIZE), c_thick)
            pygame.draw.line(self.screen, color_pulse, (x, y + CELL_SIZE), (x, y + CELL_SIZE - c_len), c_thick)
            # Bottom-Right
            pygame.draw.line(self.screen, color_pulse, (x + CELL_SIZE, y + CELL_SIZE), (x + CELL_SIZE - c_len, y + CELL_SIZE), c_thick)
            pygame.draw.line(self.screen, color_pulse, (x + CELL_SIZE, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE - c_len), c_thick)

        # Vẽ các đường kẻ lưới (ngang và dọc)
        for i in range(BOARD_SIZE + 1):
            # Đường ngang
            pygame.draw.line(
                self.screen, COLOR_GRID,
                (MARGIN, STATUS_HEIGHT + MARGIN + i * CELL_SIZE),
                (MARGIN + BOARD_SIZE * CELL_SIZE, STATUS_HEIGHT + MARGIN + i * CELL_SIZE),
                2 if i in (0, BOARD_SIZE) else 1  # Viền ngoài đậm hơn
            )
            # Đường dọc
            pygame.draw.line(
                self.screen, COLOR_GRID,
                (MARGIN + i * CELL_SIZE, STATUS_HEIGHT + MARGIN),
                (MARGIN + i * CELL_SIZE, STATUS_HEIGHT + MARGIN + BOARD_SIZE * CELL_SIZE),
                2 if i in (0, BOARD_SIZE) else 1
            )

    def draw_pieces(self, board: Board):
        """
        Quét mảng bàn cờ và vẽ ký hiệu X hoặc O lên từng ô.
        X được vẽ bằng 2 đường chéo (màu đỏ).
        O được vẽ bằng hình tròn rỗng (màu xanh).
        """
        grid = board.grid
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_value = grid[row][col]
                if cell_value == EMPTY:
                    continue  # Bỏ qua ô trống

                # Tọa độ tâm của ô
                cx = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
                cy = STATUS_HEIGHT + MARGIN + row * CELL_SIZE + CELL_SIZE // 2
                padding = CELL_SIZE // 4  # Khoảng cách từ tâm ra mép X/O

                if cell_value == PLAYER_X:
                    # Vẽ X: hai đường chéo giao nhau
                    pygame.draw.line(
                        self.screen, COLOR_X,
                        (cx - padding, cy - padding),
                        (cx + padding, cy + padding), 4
                    )
                    pygame.draw.line(
                        self.screen, COLOR_X,
                        (cx + padding, cy - padding),
                        (cx - padding, cy + padding), 4
                    )
                elif cell_value == PLAYER_O:
                    # Vẽ O: hình tròn rỗng
                    pygame.draw.circle(self.screen, COLOR_O,
                                       (cx, cy), padding, 4)

    def draw_winning_line(self, winning_cells: list):
        """
        Vẽ vạch vàng nối các ô thắng để làm nổi bật chuỗi chiến thắng.
        """
        if not winning_cells or len(winning_cells) < 2:
            return

        # Tính tọa độ pixel của ô đầu và ô cuối
        r0, c0 = winning_cells[0]
        r1, c1 = winning_cells[-1]

        start_pos = (
            MARGIN + c0 * CELL_SIZE + CELL_SIZE // 2,
            STATUS_HEIGHT + MARGIN + r0 * CELL_SIZE + CELL_SIZE // 2
        )
        end_pos = (
            MARGIN + c1 * CELL_SIZE + CELL_SIZE // 2,
            STATUS_HEIGHT + MARGIN + r1 * CELL_SIZE + CELL_SIZE // 2
        )
        pygame.draw.line(self.screen, COLOR_WIN_LINE, start_pos, end_pos, 5)

    def draw_game_over(self, winner, is_draw, game_mode, ai_player):
        """
        Vẽ màn hình tối mờ (overlay) và popup kết quả khi trận đấu kết thúc.
        Giao diện đẹp mắt, không dùng ký hiệu đặc biệt gây lỗi font.
        """
        # Tạo lớp overlay đen mờ
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # Đen với alpha 160
        self.screen.blit(overlay, (0, 0))
        
        # Kích thước và vị trí bảng kết quả
        panel_w, panel_h = 420, 220
        panel_x = (WINDOW_WIDTH - panel_w) // 2
        panel_y = (WINDOW_HEIGHT - panel_h) // 2
        
        # Vẽ nền bảng
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, (40, 44, 52), panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (80, 85, 95), panel_rect, 3, border_radius=15)
        
        # Lấy thông tin text
        if is_draw:
            title = "HÒA NHAU!"
            color = COLOR_WHITE
            subtext = "Bàn cờ đã kín ô, không ai chiến thắng."
        else:
            symbol = "X" if winner == PLAYER_X else "O"
            color = COLOR_X if winner == PLAYER_X else COLOR_O
            if game_mode == MODE_PVE:
                if winner == ai_player:
                    title = "MÁY THẮNG!"
                    subtext = f"AI ({symbol}) đã vượt qua bạn."
                else:
                    title = "BẠN THẮNG!"
                    subtext = f"Tuyệt vời! Bạn ({symbol}) đã thắng AI."
            else:
                title = f"NGƯỜI CHƠI {symbol} THẮNG!"
                subtext = "Chúc mừng người chiến thắng!"

        # Khởi tạo font cục bộ cho bảng
        font_large = pygame.font.SysFont("segoeui", 38, bold=True)
        font_small = pygame.font.SysFont("segoeui", 20)
        font_hint = pygame.font.SysFont("segoeui", 16, italic=True)
        
        surf_title = font_large.render(title, True, color)
        surf_sub = font_small.render(subtext, True, COLOR_WHITE)
        surf_hint = font_hint.render("Nhấn [Ván mới] hoặc phím R để chơi lại", True, (180, 180, 180))
        
        # Căn giữa text trong bảng
        self.screen.blit(surf_title, (panel_x + (panel_w - surf_title.get_width()) // 2, panel_y + 35))
        self.screen.blit(surf_sub, (panel_x + (panel_w - surf_sub.get_width()) // 2, panel_y + 100))
        self.screen.blit(surf_hint, (panel_x + (panel_w - surf_hint.get_width()) // 2, panel_y + 165))

    def draw_main_menu(self):
        """Vẽ menu chính khi vừa khởi động game."""
        self.screen.fill((30, 34, 42))  # Nền tối sang trọng
        
        # Tiêu đề game
        font_title = pygame.font.SysFont("segoeui", 70, bold=True)
        title_surf = font_title.render("GAME CARO AI", True, (255, 215, 0))  # Vàng Gold
        title_x = (WINDOW_WIDTH - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, 150))
        
        # Nút Bắt đầu
        btn_w, btn_h = 280, 70
        btn_x = (WINDOW_WIDTH - btn_w) // 2
        btn_y = 300
        
        self.rect_btn_start = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        is_hover = self.rect_btn_start.collidepoint(self.mouse_pos)
        
        color = COLOR_BTN_HOVER if is_hover else COLOR_BTN_BG
        pygame.draw.rect(self.screen, color, self.rect_btn_start, border_radius=15)
        pygame.draw.rect(self.screen, COLOR_GRID, self.rect_btn_start, 3, border_radius=15)
        
        font_btn = pygame.font.SysFont("segoeui", 28, bold=True)
        text_surf = font_btn.render("BẮT ĐẦU CHƠI", True, COLOR_BTN_TEXT)
        self.screen.blit(text_surf, (btn_x + (btn_w - text_surf.get_width()) // 2, btn_y + (btn_h - text_surf.get_height()) // 2))
        
        # Hướng dẫn nhỏ
        font_hint = pygame.font.SysFont("segoeui", 18, italic=True)
        hint_surf = font_hint.render("Có thể tùy chỉnh chế độ chơi và người đi trước sau khi vào game", True, (150, 160, 170))
        self.screen.blit(hint_surf, ((WINDOW_WIDTH - hint_surf.get_width()) // 2, WINDOW_HEIGHT - 80))

    def update_hover(self, mouse_pos):
        """
        Cập nhật ô đang được trỏ chuột (dùng cho hover effect).
        Gọi mỗi lần chuột di chuyển.
        """
        self.mouse_pos = mouse_pos
        row, col = self.get_row_col_from_mouse(mouse_pos)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.hover_cell = (row, col)
        else:
            self.hover_cell = None

    # ----------------------------------------------------------
    # PHẦN CHUYỂN ĐỔI TỌA ĐỘ
    # ----------------------------------------------------------

    def get_row_col_from_mouse(self, pos: tuple) -> tuple:
        """
        Chuyển tọa độ pixel (x, y) của chuột thành chỉ số (row, col) trên bàn cờ.

        Công thức:
            col = (x - MARGIN) // CELL_SIZE
            row = (y - STATUS_HEIGHT - MARGIN) // CELL_SIZE

        Trả về (row, col). Nếu click ngoài bàn cờ, giá trị có thể âm
        hoặc >= BOARD_SIZE, cần kiểm tra ở nơi gọi.
        """
        x, y = pos
        col = (x - MARGIN) // CELL_SIZE
        row = (y - STATUS_HEIGHT - MARGIN) // CELL_SIZE
        return int(row), int(col)

    def render(self):
        """Cập nhật toàn bộ màn hình (gọi cuối mỗi vòng lặp)."""
        pygame.display.update()

    def draw_panel(self, game_mode, player_first):
        """Vẽ bảng điều khiển bên phải."""
        panel_x = CELL_SIZE * BOARD_SIZE + MARGIN * 2
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, (panel_x, 0, PANEL_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(self.screen, COLOR_GRID, (panel_x, 0), (panel_x, WINDOW_HEIGHT), 2)

        def draw_button(rect, text, is_hover, is_disabled=False):
            color = COLOR_BTN_BG
            if is_disabled:
                color = (150, 150, 150) # Gray
            elif is_hover:
                color = COLOR_BTN_HOVER
                
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_GRID, rect, 2, border_radius=8)
            
            surf = self.font_btn.render(text, True, COLOR_BTN_TEXT)
            txt_x = rect.x + (rect.width - surf.get_width()) // 2
            txt_y = rect.y + (rect.height - surf.get_height()) // 2
            self.screen.blit(surf, (txt_x, txt_y))

        # Trạng thái hover
        hover_mode = self.rect_btn_mode.collidepoint(self.mouse_pos)
        hover_first = self.rect_btn_first.collidepoint(self.mouse_pos)
        hover_reset = self.rect_btn_reset.collidepoint(self.mouse_pos)

        # Nút Chế độ
        mode_text = "Đánh với người" if game_mode == MODE_PVE else "Đánh với máy"
        draw_button(self.rect_btn_mode, mode_text, hover_mode)

        # Nút Lượt đi
        first_text = "Người đi trước" if player_first else "Máy đi trước"
        draw_button(self.rect_btn_first, first_text, hover_first, is_disabled=(game_mode != MODE_PVE))

        # Nút Dừng chơi / Reset
        draw_button(self.rect_btn_reset, "Ván mới", hover_reset)
        
    def handle_button_click(self, mouse_pos):
        """Trả về tên nút được bấm ('mode', 'first', 'reset') hoặc None."""
        if self.rect_btn_mode.collidepoint(mouse_pos):
            return 'mode'
        if self.rect_btn_first.collidepoint(mouse_pos):
            return 'first'
        if self.rect_btn_reset.collidepoint(mouse_pos):
            return 'reset'
        return None

    def render(self):
        """Cập nhật toàn bộ màn hình (gọi cuối mỗi vòng lặp)."""
        pygame.display.update()

    def quit(self):
        """Dọn dẹp và thoát pygame."""
        pygame.quit()
