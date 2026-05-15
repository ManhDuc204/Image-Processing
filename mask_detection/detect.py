from ultralytics import YOLO
import cv2
import pygame
import time
import os
import pandas as pd

# Tự động tạo thư mục lưu ảnh vi phạm nếu chưa có
if not os.path.exists("violations"):
    os.makedirs("violations")

# Load model AI
model = YOLO("best.pt")

# Khởi tạo âm thanh
sound_ready = False
try:
    pygame.mixer.init()
    alert_sound = pygame.mixer.Sound("sounds/Beep.mp3")
    sound_ready = True
    print("-> Hệ thống âm thanh: SẴN SÀNG")
except:
    print("-> Chế độ im lặng: KHÔNG TÌM THẤY SOUNDS/BEEP.MP3")

# Biến quản lý dữ liệu và thời gian
log_data = []          # Danh sách lưu nhật ký vi phạm
last_beep_time = 0     # Tránh hú còi liên tục
last_save_time = 0     # Tránh lưu ảnh quá dày đặc (giới hạn 5s/tấm)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("-> Hệ thống đang ghi nhật ký... Nhấn 'Q' để kết thúc và xuất báo cáo.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Chạy AI nhận diện (Sử dụng stream=True để tăng tốc độ)
    results = model.predict(frame, conf=0.6, iou=0.45, stream=True, verbose=False)

    mask_count = 0
    nomask_count = 0
    violation_detected = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Lấy tọa độ và nhãn
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            label = model.names[cls].lower()

            # Phân loại vi phạm
            if 'no' in label:
                color = (0, 0, 255)  # Đỏ cho No-Mask
                nomask_count += 1
                violation_detected = True
            else:
                color = (0, 255, 0)  # Xanh cho Mask
                mask_count += 1

            # Vẽ khung nhận diện
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # --- XỬ LÝ VI PHẠM (ÂM THANH & LƯU TRỮ) ---
    current_time = time.time()
    if violation_detected:
        # 1. Phát còi hú (Cứ 2 giây hú 1 lần nếu vẫn vi phạm)
        if sound_ready and (current_time - last_beep_time > 2):
            alert_sound.play()
            last_beep_time = current_time
        
        # 2. Chụp ảnh & Ghi log (Cứ 5 giây chụp 1 tấm để làm bằng chứng)
        if current_time - last_save_time > 5:
            timestamp = time.strftime("%H%M%S-%d%m%Y")
            file_path = f"violations/vi-pham_{timestamp}.jpg"
            cv2.imwrite(file_path, frame)
            
            # Lưu vào danh sách để xuất Excel sau này
            log_data.append({
                "Thoi_Gian": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Loai_Vi_Pham": "Khong deo khau trang",
                "Anh_Bang_Chung": file_path
            })
            last_save_time = current_time

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (220, 100), (40, 40, 40), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    cv2.putText(frame, f"Mask: {mask_count}", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"No Mask: {nomask_count}", (15, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("He thong Kiem soat Khau trang AI", frame)

    # Thoát khi nhấn phím 'Q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if log_data:
    # Sử dụng Pandas để tạo file báo cáo chuyên nghiệp
    df = pd.DataFrame(log_data)
    df.to_csv("bao_cao_vi_pham.csv", index=False, encoding='utf-8-sig')
    print(f"--- HOÀN THÀNH ---")
    print(f"-> Đã lưu {len(log_data)} bằng chứng vào thư mục 'violations'")
    print(f"-> Đã xuất báo cáo: 'bao_cao_vi_pham.csv'")
else:
    print("-> Không có vi phạm nào được ghi nhận.")

if sound_ready:
    pygame.mixer.quit()