import cv2
import numpy as np
import os

# 1. Cấu hình đường dẫn
# Folder chứa ảnh gốc để đọc
SOURCE_DIR = 'BTCB/data/test' 
# Folder để lưu các biến thể
DEST_DIR   = 'BTCB/data/positive'

# Tên file gốc bạn muốn xử lý (Ví dụ: test1.jpg hoặc test2.jpg)
input_filename = 'test2.jpg' 

# Tạo thư mục đích nếu chưa có
os.makedirs(DEST_DIR, exist_ok=True)

# --- XỬ LÝ PREFIX THÔNG MINH ---
# Lấy tên file bỏ đuôi (Ví dụ: 'test1.jpg' -> 'test1')
# Điều này cực kỳ quan trọng để hàm split('_')[0] ở file Hashing chạy đúng
prefix = os.path.splitext(input_filename)[0]

# 2. Đọc ảnh gốc từ thư mục test
img_input_path = os.path.join(SOURCE_DIR, input_filename)
img = cv2.imread(img_input_path)

if img is not None:
    print(f"--- Đang xử lý ảnh gốc: {img_input_path} ---")

    # --- TẠO CÁC BIẾN THỂ ---
    # 1. Chỉnh độ sáng
    bright_img = cv2.convertScaleAbs(img, beta=50)

    # 2. Làm mờ (Gaussian Blur)
    blur_img = cv2.GaussianBlur(img, (7, 7), 0)

    # 3. Thêm nhiễu (Noise)
    noise = np.random.randint(0, 50, img.shape, dtype='uint8')
    noisy_img = cv2.add(img, noise)

    # 4. Xoay ảnh (Rotate 90 độ)
    rotate_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # 5. Tổng hợp (Sáng + Mờ + Nhiễu)
    tmp = cv2.convertScaleAbs(img, beta=50)
    tmp = cv2.GaussianBlur(tmp, (7, 7), 0)
    noise_mask = np.random.randint(0, 50, img.shape, dtype='uint8')
    combined_img = cv2.add(tmp, noise_mask)

    # Danh sách các file cần lưu với cấu trúc Tên_BiếnThể.jpg
    variations = [
        (f"{prefix}_img_original.jpg", img),
        (f"{prefix}_img_bright.jpg",   bright_img),
        (f"{prefix}_img_blur.jpg",     blur_img),
        (f"{prefix}_img_noise.jpg",    noisy_img),
        (f"{prefix}_img_rotate.jpg",   rotate_img),
        (f"{prefix}_img_combined.jpg", combined_img),
    ]

    # 3. Lưu các file vào thư mục DEST_DIR (positive)
    for filename, image_data in variations:
        save_path = os.path.join(DEST_DIR, filename)
        cv2.imwrite(save_path, image_data)
        print(f"   -> Đã lưu: {save_path}")

    print(f"\n[Xong] Tất cả ảnh biến thể của '{prefix}' đã nằm trong: {DEST_DIR}")
else:
    print(f"LỖI: Không tìm thấy file gốc tại '{img_input_path}'")