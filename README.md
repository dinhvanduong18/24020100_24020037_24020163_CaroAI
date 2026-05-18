# 🎮 CaroAI - Trò chơi Caro 9x9 với AI

Trò chơi Caro cổ điển trên bàn cờ 9x9 với khả năng chơi đối kháng AI sử dụng thuật toán Minimax.

## 📋 Giới thiệu

CaroAI là một dự án game Caro được phát triển bằng Python và Pygame. Game cho phép người chơi:
- Chơi với AI (người vs máy)
- Chơi 2 người (người vs người)
- Sử dụng AI thông minh với thuật toán Minimax

## ✨ Tính năng

- **2 chế độ chơi**:
  - **PVE (Player vs Environment)**: Đấu với AI
  - **PVP (Player vs Player)**: Đấu 2 người
  
- **AI thông minh**: Sử dụng thuật toán Minimax với độ sâu tìm kiếm là 3

- **Tùy chọn lượt đi**: Có thể chọn người đi trước hoặc máy đi trước

- **Giao diện đẹp mắt**: 
  - Bàn cờ 9x9 với màu sắc gỗ
  - Highlight ô khi di chuột
  - Hiển thị đường thắng khi có người chiến thắng
  - Thanh trạng thái thông tin lượt chơi

- **Điều khiển dễ dàng**: Chỉ cần chuột để chơi

## 🎯 Luật chơi

- Bàn cờ kích thước: **9x9**
- Người chơi: **X** (đỏ) và **O** (xanh dương)
- Điều kiện thắng: **4 quân liên tiếp** theo chiều ngang, dọc hoặc chéo
- Nếu bàn cờ đầy mà không ai thắng → Hòa

## 🛠️ Cài đặt

### Yêu cầu

- Python 3.7+
- Pygame

### Cài đặt Pygame

```bash
pip install pygame
```

## 🚀 Chạy game

```bash
cd source_code
python main.py
```

## 🎮 Cách chơi

### Điều khiển

- **Chuột trái**: Đặt quân cờ
- **Phím R**: Reset ván chơi mới
- **Nút trên màn hình**:
  - **Chế độ**: Chuyển đổi giữa PVE và PVP
  - **Đi trước**: Chọn người đi trước (chỉ trong chế độ PVE)
  - **Reset**: Bắt đầu ván mới

### Giao diện

- **Bàn cờ chính**: Khu vực chơi ở giữa màn hình
- **Thanh trạng thái**: Hiển thị lượt chơi và kết quả ở trên cùng
- **Bảng điều khiển**: Các nút chức năng ở bên phải

## 📁 Cấu trúc dự án

```
24020100_24020037_24020163_CaroAI/
├── source_code/
│   ├── main.py              # Entry point của game
│   ├── config.py            # Cấu hình hằng số
│   ├── game/
│   │   ├── board.py         # Quản lý bàn cờ
│   │   ├── logic.py         # Xử lý luật chơi
│   │   └── evaluator.py     # Đánh giá điểm số cho AI
│   ├── ai/
│   │   └── minimax.py       # Thuật toán Minimax
│   └── ui/
│       └── pygame_ui.py     # Giao diện Pygame
└── README.md
```

## 🔬 Kỹ thuật

- **Ngôn ngữ**: Python
- **Thư viện đồ họa**: Pygame
- **Thuật toán AI**: Minimax với Alpha-Beta Pruning
- **Đánh giá vị trí**: Heuristic evaluation function

## 👨‍💻 Nhóm phát triển

- **24020100 - Đinh Văn Dương**
- **24020037 - Phạm Xuân Bắc**
- **24020163 - Nguyễn Minh Huy**

## 📝 Ghi chú

- AI có độ sâu tìm kiếm là 3 để cân bằng giữa tốc độ và độ thông minh
- Game chạy ở 30 FPS
- Màu sắc được thiết kế để dễ nhìn và thân thiện

---

Chúc bạn chơi vui vẻ! 🎉