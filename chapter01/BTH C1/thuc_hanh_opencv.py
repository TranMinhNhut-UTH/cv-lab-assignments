import cv2
import numpy as np
import os

def cho_phim_hoac_chuot(window_name):
    """ Hàm chờ người dùng bấm phím bất kỳ HOẶC click chuột vào ảnh """
    # Biến cờ kiểm tra xem đã click chuột chưa
    clicked = [False]
    
    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked[0] = True
            
    cv2.setMouseCallback(window_name, on_mouse)
    
    # Vòng lặp chờ: thoát ra nếu có phím được bấm (k > -1) hoặc chuột được click
    while True:
        k = cv2.waitKey(50) # Chờ 50ms kiểm tra phím mỗi vòng lặp
        if k != -1 or clicked[0]:
            break

    # Gỡ callback chuột đi (nếu sử dụng lại cửa sổ cũ)
    cv2.setMouseCallback(window_name, lambda *args: None)

def main():
    image_path = 'input.jpg'
    
    # Tạo một bức ảnh mẫu (ảnh nhiễu màu) nếu chưa có input.jpg để code có thể chạy ngay
    if not os.path.exists(image_path):
        print(f"Không tìm thấy '{image_path}', đang tạo một ảnh mẫu...")
        sample_img = np.zeros((500, 500, 3), dtype=np.uint8)
        sample_img[:] = (200, 150, 100) # Màu nền
        cv2.circle(sample_img, (250, 250), 100, (0, 0, 255), -1)
        cv2.imwrite(image_path, sample_img)

    # ----------------------------------------------------
    # 2. Đọc và hiển thị ảnh
    print("2. Đọc, hiển thị và lưu ảnh...")
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Không thể đọc ảnh từ {image_path}.")
        return
        
    window_goc = '2. Anh Goc (Nhan phim bat ky de tiep tuc)'
    cv2.imshow(window_goc, img)
    cho_phim_hoac_chuot(window_goc)
    
    # Lưu hình ảnh với định dạng khác (.png) ngay khi vừa đọc
    save_path = 'output_image.png'
    cv2.imwrite(save_path, img)
    print(f"=> Đã lưu hình ảnh sang định dạng khác: {save_path}")
    
    # ----------------------------------------------------
    # 3. Chuyển đổi không gian màu
    print("3. Chuyển đổi không gian màu...")
    
    # RGB sang Grayscale (Lưu ý: OpenCV đọc ảnh theo định dạng BGR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    window_gray = '3. RGB sang Grayscale'
    cv2.imshow(window_gray, gray_img)
    cho_phim_hoac_chuot(window_gray)
    
    # Sang các không gian màu khác (HSV, LAB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    window_hsv = '3. RGB sang HSV'
    cv2.imshow(window_hsv, hsv_img)
    cho_phim_hoac_chuot(window_hsv)
    
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    window_lab = '3. RGB sang LAB'
    cv2.imshow(window_lab, lab_img)
    cho_phim_hoac_chuot(window_lab)
    
    # ----------------------------------------------------
    # 4. Cắt xén (crop) và thay đổi kích thước (resize)
    print("4. Cắt xén và đổi kích thước ảnh...")
    
    # Cắt một vùng hình ảnh: Numpy array slicing img[y1:y2, x1:x2]
    h, w = img.shape[:2]
    crop_img = img[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
    window_crop = '4. Cat xen (Crop) anh'
    cv2.imshow(window_crop, crop_img)
    cho_phim_hoac_chuot(window_crop)
    
    # Thay đổi kích thước (Resize theo kích thước cố định)
    resize_fixed = cv2.resize(img, (300, 300))
    window_resize_fixed = '4. Thay doi kich thuoc (Resize) - Kich thuoc co dinh'
    cv2.imshow(window_resize_fixed, resize_fixed)
    cho_phim_hoac_chuot(window_resize_fixed)
    
    # Thay đổi kích thước (Resize theo tỷ lệ 50%)
    resize_ratio = cv2.resize(img, None, fx=0.5, fy=0.5) 
    window_resize_ratio = '4. Thay doi kich thuoc (Resize) - Theo ty le'
    cv2.imshow(window_resize_ratio, resize_ratio)
    cho_phim_hoac_chuot(window_resize_ratio)
    
    # ----------------------------------------------------
    # 5. Vẽ hình cơ bản và thêm văn bản
    print("5. Vẽ hình và thêm chữ lên ảnh...")
    img_draw = img.copy()
    
    # Vẽ đường thẳng (Hỉnh, Tọa độ bắt đầu, Tọa độ kết thúc, Màu (B,G,R), Độ dày)
    cv2.line(img_draw, (50, 50), (250, 50), (0, 0, 255), 3) # Đường màu đỏ
    
    # Vẽ hình tròn (Trọng tâm, Bán kính, Màu, Độ dày: -1 là tô kín)
    cv2.circle(img_draw, (150, 150), 50, (0, 255, 0), -1) # Hình tròn xanh lá
    
    # Vẽ hình chữ nhật (Góc trên-trái, Góc dưới-phải, Màu, Độ dày)
    cv2.rectangle(img_draw, (50, 200), (450, 300), (255, 0, 0), 2) # Hình bao xanh dương
    
    # Thêm văn bản
    # (Ảnh, Nội dung, Tọa độ góc dưới bên trái, Font, Tỷ lệ, Màu, Độ dày)
    cv2.putText(img_draw, 'OpenCV Viet Nam', (60, 260), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    
    window_draw = '5. Ve hinh co ban va Them van ban len anh'
    cv2.imshow(window_draw, img_draw)
    cho_phim_hoac_chuot(window_draw)
    
    # Đóng tất cả cửa sổ báo cáo
    cv2.destroyAllWindows()
    print("Hoàn thành bài thực hành với OpenCV!")

if __name__ == "__main__":
    main()
