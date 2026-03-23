# Hướng dẫn Bài thực hành Chương 1: OpenCV & Pillow

## Đề bài

### Bài thực hành chương 1

1. Cài đặt các thư viện OpenCV và Pillow.

2. Đọc và hiển thị ảnh:
   - Đọc một hình ảnh bất kỳ từ máy tính.
   - Hiển thị hình ảnh đó lên màn hình.
   - Lưu hình ảnh đã xử lý lại với định dạng khác.

3. Chuyển đổi không gian màu:
   - Chuyển đổi ảnh từ RGB sang grayscale.
   - Chuyển đổi ảnh sang các không gian màu khác như HSV, LAB.

4. Cắt xén (crop) và thay đổi kích thước (resize):
   - Cắt một vùng hình ảnh bất kỳ.
   - Thay đổi kích thước hình ảnh theo tỷ lệ hoặc kích thước cố định.

5. Vẽ hình cơ bản:
   - Vẽ các hình cơ bản như đường thẳng, hình tròn, hình chữ nhật lên hình ảnh.
   - Thêm văn bản vào hình ảnh.

Cách cài đặt và chạy mã nguồn cho **Bài thực hành chương 1** của môn Thị giác máy tính & Xử lý ảnh.

## 1. Yêu cầu 1: Cài đặt thư viện
Mở Terminal (hoặc Command Prompt) và chạy lệnh sau để cài đặt các thư viện cần thiết:

```bash
pip install opencv-python pillow numpy
```

## 2. Các file mã nguồn
Trong thư mục này đã tạo sẵn 2 file Python giải quyết toàn bộ các yêu cầu của bài thực hành:

1. **`thuc_hanh_opencv.py`**: Chứa code sử dụng thư viện `cv2` (OpenCV).
   - Đọc, hiển thị, lưu ảnh (`cv2.imread`, `cv2.imshow`, `cv2.imwrite`).
   - Chuyển không gian màu RGB -> Grayscale, HSV, LAB (`cv2.cvtColor`).
   - Cắt ảnh (numpy slicing), Thay đổi kích thước (`cv2.resize`).
   - Vẽ hình (đường thẳng, tròn, chữ nhật) và thêm chữ (`cv2.line`, `cv2.circle`, `cv2.rectangle`, `cv2.putText`).

2. **`thuc_hanh_pillow.py`**: Chứa code sử dụng thư viện `PIL` (Pillow).
   - Đọc, hiển thị, lưu ảnh (`Image.open`, `show`, `save`).
   - Chuyển không gian màu (`convert('L')`, `convert('HSV')`, `convert('LAB')`).
   - Cắt ảnh (`crop`), Thay đổi kích thước (`resize`).
   - Vẽ hình và thêm chữ (`ImageDraw`).

## 3. Cách chạy code
Chuẩn bị một bức ảnh bất kỳ, đổi tên thành `input.jpg` và để cùng thư mục này.
*(Nếu không có ảnh `input.jpg`, file code OpenCV sẽ tự động tạo một bức ảnh mẫu để bạn có thể xem kết quả chạy ngay lập tức!)*

Chạy file bằng các lệnh sau trong Terminal:
```bash
python thuc_hanh_opencv.py
```
*(Bấm một phím bất kỳ trên bàn phím khi cửa sổ ảnh hiện lên để xem hiệu ứng tiếp theo)*

```bash
python thuc_hanh_pillow.py
```
*(Lưu ý: Thư viện Pillow sẽ mở các ảnh bằng phần mềm xem ảnh mặc định của Windows)*
