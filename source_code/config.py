# ============================================================
# config.py - File cấu hình chứa các hằng số của game
# ============================================================

# --- Hằng số logic bàn cờ ---
BOARD_SIZE = 9          # Kích thước bàn cờ 9x9
EMPTY     = 0           # Ô trống
PLAYER_X  = 1           # Người chơi X
PLAYER_O  = 2           # Người chơi O
WIN_COUNT = 4           # Số quân liên tiếp để thắng

# --- Hằng số giao diện Pygame ---
CELL_SIZE     = 60                              # Kích thước mỗi ô (pixel)
MARGIN        = 40                              # Khoảng cách lề xung quanh bàn cờ
STATUS_HEIGHT = 60                              # Chiều cao thanh trạng thái phía trên
PANEL_WIDTH   = 280                             # Chiều rộng bảng điều khiển bên phải

WINDOW_WIDTH  = CELL_SIZE * BOARD_SIZE + MARGIN * 2 + PANEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE * BOARD_SIZE + MARGIN * 2 + STATUS_HEIGHT

FPS = 30  # Số khung hình mỗi giây

# --- Màu sắc (RGB) ---
COLOR_BG         = (245, 222, 179)   # Màu nền bàn cờ (vàng gỗ)
COLOR_GRID       = (100,  70,  30)   # Màu lưới bàn cờ (nâu đậm)
COLOR_X          = (210,  50,  50)   # Màu X (đỏ)
COLOR_O          = ( 30, 100, 200)   # Màu O (xanh dương)
COLOR_WHITE      = (255, 255, 255)   # Trắng
COLOR_BLACK      = (  0,   0,   0)   # Đen
COLOR_STATUS_BG  = ( 40,  40,  60)   # Màu nền thanh trạng thái (tím đậm)
COLOR_STATUS_TXT = (255, 255, 200)   # Màu chữ trạng thái (vàng nhạt)
COLOR_WIN_LINE   = (255, 215,   0)   # Màu vạch thắng (vàng)
COLOR_HOVER      = (180, 220, 140)   # Màu highlight ô đang trỏ chuột

# --- Màu Nút Bấm ---
COLOR_BTN_BG     = (70, 130, 180)    # Màu nền nút
COLOR_BTN_HOVER  = (100, 149, 237)   # Màu nền nút khi hover
COLOR_BTN_TEXT   = (255, 255, 255)   # Màu chữ nút
COLOR_PANEL_BG   = (230, 210, 170)   # Màu nền panel

# --- Màu mới cho Menu & Game Over ---
COLOR_BTN_MENU_BG = (139, 69, 19)    # Nâu (SaddleBrown)
COLOR_BTN_MENU_HOVER = (160, 82, 45) # Nâu sáng (Sienna)
COLOR_TEXT_DARK = (60, 30, 10)       # Nâu cực đậm

# --- Chế độ chơi ---
MODE_PVE = 0
MODE_PVP = 1

# --- Tên cửa sổ ---
WINDOW_TITLE = "Game Caro 9x9"
