😷 AI Mask Detection System
Hệ thống giám sát và phát hiện khẩu trang theo thời gian thực sử dụng YOLOv8 + Flask, tích hợp cảnh báo âm thanh, lưu ảnh vi phạm và dashboard quản lý trực quan.

📸 Tính năng chính

🎥 Nhận diện thời gian thực qua webcam với mô hình YOLOv8 tùy chỉnh (best.pt)
🔴 Cảnh báo âm thanh tự động khi phát hiện người không đeo khẩu trang (cách 2 giây/lần)
📷 Chụp ảnh bằng chứng tự động và lưu vào thư mục static/violations/ (cách 5 giây/lần)
📊 Dashboard web hiển thị thống kê, biểu đồ pie và bảng nhật ký vi phạm
🔐 Xác thực đăng nhập quản trị viên
📥 Xuất báo cáo CSV chứa toàn bộ nhật ký vi phạm


🗂️ Cấu trúc dự án
mask-detection/
│
├── app.py                  # Flask web server (luồng camera + dashboard)
├── detect.py               # Script chạy độc lập (không cần web)
├── best.pt                 # Model YOLOv8 đã huấn luyện
├── requirements.txt        # Các thư viện cần cài
│
├── sounds/
│   └── Beep.mp3            # Âm thanh cảnh báo
│
├── static/
│   ├── styles.css          # Giao diện CSS
│   └── violations/         # Ảnh vi phạm được lưu tự động
│
└── templates/
    ├── login.html          # Trang đăng nhập
    ├── dashboard.html      # Trang dashboard chính
    └── index.html          # Trang chủ (tuỳ chọn)

⚙️ Cài đặt
1. Clone repository
bashgit clone https://github.com/your-username/mask-detection.git
cd mask-detection
2. Tạo môi trường ảo (khuyến nghị)
bashpython -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
3. Cài đặt thư viện
bashpip install -r requirements.txt
4. Chuẩn bị file

Đặt file model best.pt vào thư mục gốc của dự án
Đặt file âm thanh Beep.mp3 vào thư mục sounds/

mask-detection/
├── best.pt         ✅
├── sounds/
│   └── Beep.mp3    ✅

🚀 Chạy ứng dụng
Chế độ Web Dashboard (Flask)
bashpython app.py
Sau đó mở trình duyệt và truy cập: http://127.0.0.1:5000
Thông tinGiá trịUsernameadminPassword123456
Chế độ Standalone (chạy trực tiếp, không cần web)
bashpython detect.py
Nhấn Q để thoát và xuất báo cáo bao_cao_vi_pham.csv.

📊 Hướng dẫn sử dụng Dashboard

Truy cập http://127.0.0.1:5000 → Đăng nhập với tài khoản admin
Camera stream hiển thị trực tiếp với khung nhận diện màu xanh (đeo khẩu trang) / đỏ (không đeo)
Thẻ thống kê cập nhật tổng số lượt Mask / No Mask từ khi khởi động
Biểu đồ Pie trực quan hóa tỉ lệ tuân thủ
Bảng Violation Logs ghi nhận thời gian, trạng thái và ảnh bằng chứng từng vi phạm
Nhấn DOWNLOAD REPORT để tải file CSV


🛠️ Công nghệ sử dụng
Thành phầnCông nghệAI ModelYOLOv8 (Ultralytics)Web FrameworkFlaskComputer VisionOpenCVXử lý dữ liệuPandasÂm thanhPygameFrontend ChartChart.js

⚠️ Lưu ý

Ứng dụng sử dụng webcam mặc định (device index 0). Nếu có nhiều camera, chỉnh cv2.VideoCapture(0) thành index tương ứng.
Biến total_mask và total_nomask trong app.py được đếm tích lũy theo frame, không phải theo người riêng lẻ.
Chạy trong môi trường có đủ ánh sáng để đạt độ chính xác tốt nhất.
Nếu không tìm thấy file âm thanh, hệ thống vẫn hoạt động bình thường ở chế độ im lặng.


📄 License
Dự án này được phát hành theo giấy phép MIT License.

🙌 Đóng góp
Pull request và issues luôn được chào đón! Nếu bạn muốn cải thiện độ chính xác của model hoặc thêm tính năng mới, hãy tạo issue để thảo luận trước.
