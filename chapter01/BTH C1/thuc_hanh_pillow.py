import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

def hien_thi_anh_vung_title(img, title):
    """ Hàm hỗ trợ hiển thị ảnh Pillow trong một cửa sổ có tiêu đề và tự động tạm dừng """
    root = tk.Tk()
    root.title(title)
    
    # Để tránh ảnh quá lớn che hết màn hình
    w, h = img.size
    max_w, max_h = 1000, 800
    display_img = img.copy()
    if w > max_w or h > max_h:
        display_img.thumbnail((max_w, max_h))
        
    # Tkinter cần ảnh hệ màu RGB, L hoặc 1 để hiển thị tốt nhất
    if display_img.mode not in ('RGB', 'L', '1'):
        display_img = display_img.convert('RGB')
        
    tk_img = ImageTk.PhotoImage(display_img)
    label = tk.Label(root, image=tk_img)
    label.pack()
    
    # Cho phép bấm phím bất kỳ (kể cả phím chữ, số, Enter, Space...) để đóng cửa sổ
    root.bind('<Key>', lambda e: root.destroy())
    # Cho phép click chuột vào ảnh để đóng cửa sổ
    label.bind('<Button-1>', lambda e: root.destroy())
    
    # Cho cửa sổ nổi lên để dễ nhìn
    root.attributes('-topmost', 1)
    # Tắt topmost sau 0.5s để người dùng có thể thao tác lại với window khác
    root.after(500, lambda: root.attributes('-topmost', 0))
    
    print(f"-> Đang hiển thị: {title} (Bấm phím bất kỳ hoặc click chuột vào ảnh để tiếp tục...)")
    root.mainloop()

def main():
    image_path = 'input.jpg'
    
    # Kiểm tra nếu chưa có ảnh input.jpg
    if not os.path.exists(image_path):
        print(f"Không tìm thấy '{image_path}'. Vui lòng chạy file 'thuc_hanh_opencv.py' trước để tạo ảnh mẫu, hoặc copy một ảnh bất kỳ vào thư mục này đổi tên thành 'input.jpg'.")
        return

    try:
        # ----------------------------------------------------
        # 2. Đọc và hiển thị ảnh
        print("2. Đọc và hiển thị ảnh...")
        img = Image.open(image_path)
        hien_thi_anh_vung_title(img, "2. Anh Goc")
        
        # Lưu hình ảnh đã xử lý lại với định dạng khác (Đã copy/chuyển định dạng RGB)
        save_path = 'output_pillow.png'
        # Convert qua RGB trước khi lưu để phòng trường hợp định dạng gốc không hỗ trợ PNG
        if img.mode != 'RGB':
            img.convert('RGB').save(save_path)
        else:
            img.save(save_path)
        print(f"=> Đã lưu hình ảnh sang định dạng khác: {save_path}")
        
        # ----------------------------------------------------
        # 3. Chuyển đổi không gian màu
        print("\n3. Chuyển đổi không gian màu...")
        
        gray_img = img.convert('L')
        hien_thi_anh_vung_title(gray_img, '3. RGB sang Grayscale')
        
        hsv_img = img.convert('HSV')
        hien_thi_anh_vung_title(hsv_img, '3. RGB sang HSV')
        
        lab_img = img.convert('LAB')
        hien_thi_anh_vung_title(lab_img, '3. RGB sang LAB')
        
        # ----------------------------------------------------
        # 4. Cắt xén (crop) và thay đổi kích thước (resize)
        print("\n4. Cắt xén và đổi kích thước ảnh...")
        
        w, h = img.size
        crop_img = img.crop((w*0.25, h*0.25, w*0.75, h*0.75))
        hien_thi_anh_vung_title(crop_img, '4. Cat xen (Crop) anh')
        
        resize_fixed = img.resize((300, 300))
        hien_thi_anh_vung_title(resize_fixed, '4. Thay doi kich thuoc (Resize) - Kich thuoc co dinh')
        
        resize_ratio = img.resize((int(w * 0.5), int(h * 0.5)))
        hien_thi_anh_vung_title(resize_ratio, '4. Thay doi kich thuoc (Resize) - Theo ty le')
        
        # ----------------------------------------------------

        # 5. Vẽ hình cơ bản và thêm văn bản
        print("\n5. Vẽ hình và thêm chữ lên ảnh...")
        img_draw = img.copy()
        draw = ImageDraw.Draw(img_draw)
        
        draw.line((50, 50, 250, 50), fill="red", width=3)
        draw.ellipse((100, 100, 200, 200), fill="green")
        draw.rectangle((50, 200, 450, 300), outline="blue", width=2)
        draw.text((60, 250), "Pillow Viet Nam", fill="white")
        
        hien_thi_anh_vung_title(img_draw, '5. Ve hinh co ban va Them van ban len anh')
        
        print("\nHoàn thành bài thực hành với Pillow!")
        
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()
