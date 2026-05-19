# 🎮 CaroAI - Trò chơi Caro 9x9 với AI

Trò chơi Caro cổ điển trên bàn cờ 9x9 với khả năng chơi đối kháng AI sử dụng thuật toán Minimax với Alpha-Beta Pruning.

## 📋 Giới thiệu

CaroAI là một dự án game Caro được phát triển bằng Python và Pygame. Game cho phép người chơi:
- Chơi với AI (người vs máy) với độ thông minh cao
- Chơi 2 người (người vs người) trên cùng một máy
- Sử dụng AI thông minh với thuật toán Minimax và Alpha-Beta Pruning
- Trải nghiệm giao diện đẹp mắt, mượt mà

## 🎯 Tính năng nổi bật

### Chế độ chơi đa dạng
- **PVE (Player vs Environment)**: Đấu với AI thông minh
- **PVP (Player vs Player)**: Đấu 2 người trên cùng máy

### AI thông minh
- Thuật toán Minimax với độ sâu tìm kiếm là 3
- Alpha-Beta Pruning để tối ưu hóa hiệu suất
- Hàm đánh giá heuristic thông minh
- Có thể chọn người đi trước hoặc máy đi trước

### Giao diện hiện đại
- Bàn cờ 9x9 với màu sắc gỗ tự nhiên
- Highlight ô khi di chuột để dễ dàng chọn vị trí
- Hiển thị đường thắng khi có người chiến thắng
- Thanh trạng thái thông tin lượt chơi
- Các nút điều khiển trực quan
- Mượt mà với tốc độ 30 FPS

### Điều khiển dễ dàng
- Chỉ cần chuột để chơi
- Phím tắt nhanh để reset
- Giao diện thân thiện với người dùng


## 🎯 Luật chơi

- Bàn cờ kích thước: **9x9**
- Người chơi: **X** (đỏ) và **O** (xanh dương)
- Điều kiện thắng: **4 quân liên tiếp** theo chiều ngang, dọc hoặc chéo
- Nếu bàn cờ đầy mà không ai thắng → Hòa

## 🛠️ Cài đặt

### Yêu cầu hệ thống

- **Hệ điều hành**: Windows, macOS, hoặc Linux
- **Python**: Phiên bản 3.7 trở lên
- **RAM**: Tối thiểu 2GB
- **Bộ nhớ**: ~50MB cho dự án

### Cài đặt Pygame

#### Cách 1: Sử dụng pip (Khuyên dùng)

```bash
pip install pygame
```

#### Cách 2: Sử dụng pip với phiên bản cụ thể

```bash
pip install pygame==2.5.2
```

### Kiểm tra cài đặt

```bash
python -c "import pygame; print(pygame.version.ver)"
```

Nếu hiển thị phiên bản pygame, cài đặt thành công!


## 🚀 Chạy game

```bash
cd source_code
python main.py
```

### Lưu ý
- Đảm bảo bạn đang ở thư mục gốc của dự án trước khi chạy lệnh `cd source_code`
- Game sẽ mở trong một cửa sổ mới
- Để thoát game, nhấn nút đóng cửa sổ hoặc nhấn ESC

## 🎮 Cách chơi

### Điều khiển

- **Chuột trái**: Đặt quân cờ vào ô được chọn
- **Phím R**: Reset ván chơi mới (khởi động lại game)
- **Phím ESC**: Thoát game
- **Nút trên màn hình**:
  - **Chế độ (Mode)**: Chuyển đổi giữa PVE (chơi với AI) và PVP (chơi 2 người)
  - **Đi trước (First Move)**: Chọn người đi trước hoặc máy đi trước (chỉ trong chế độ PVE)
  - **Reset**: Bắt đầu ván chơi mới

### Giao diện

- **Bàn cờ chính**: Khu vực chơi 9x9 ở giữa màn hình với màu gỗ tự nhiên
- **Thanh trạng thái**: Hiển thị lượt chơi hiện tại và kết quả ở trên cùng
- **Bảng điều khiển**: Các nút chức năng ở bên phải với thiết kế trực quan
- **Highlight**: Ô được chọn sẽ được highlight khi di chuột qua

### Chiến thuật

- **Chế độ PVE**: AI sẽ tính toán nước đi tối ưu, hãy cố gắng tạo chuỗi 4 quân liên tiếp
- **Chế độ PVP**: Cạnh tranh với bạn bè, người nào tạo được 4 quân liên tiếp trước sẽ thắng
- **Phòng thủ**: Chặn đối phương tạo chuỗi 3 quân liên tiếp
- **Tấn công**: Tạo nhiều cơ hội chiến thắng cùng lúc

## 📁 Cấu trúc dự án

```
24020100_24020037_24020163_CaroAI/
├── source_code/
│   ├── main.py              # Entry point của game, khởi tạo và chạy game loop
│   ├── config.py            # Cấu hình hằng số (màu sắc, kích thước, FPS)
│   ├── game/
│   │   ├── board.py         # Quản lý bàn cờ, trạng thái và vị trí quân cờ
│   │   ├── logic.py         # Xử lý luật chơi, kiểm tra điều kiện thắng
│   │   └── evaluator.py     # Đánh giá điểm số cho AI, hàm heuristic
│   ├── ai/
│   │   └── minimax.py       # Thuật toán Minimax với Alpha-Beta Pruning
│   ├── ui/
│   │   └── pygame_ui.py     # Giao diện Pygame, vẽ bàn cờ và xử lý sự kiện
│   └── benchmark/
│       ├── run_benchmark.py # Chạy benchmark test cho AI
│       └── testcases.txt    # Các test case cho benchmark
└── README.md                # Tài liệu dự án
```

### Mô tả chi tiết

- **main.py**: File chính khởi tạo game, kết nối các module và chạy game loop
- **config.py**: Chứa tất cả các hằng số cấu hình như màu sắc, kích thước ô, FPS
- **game/board.py**: Quản lý trạng thái bàn cờ, thêm quân cờ, kiểm tra ô trống
- **game/logic.py**: Xử lý logic game, kiểm tra điều kiện thắng, hòa
- **game/evaluator.py**: Hàm đánh giá vị trí cho AI, tính điểm cho các nước đi
- **ai/minimax.py**: Thuật toán AI chính với Minimax và Alpha-Beta Pruning
- **ui/pygame_ui.py**: Xử lý tất cả các thao tác vẽ và sự kiện người dùng
- **benchmark/run_benchmark.py**: Script chạy benchmark test để đánh giá hiệu suất AI
- **benchmark/testcases.txt**: File chứa các test case dùng cho benchmark

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