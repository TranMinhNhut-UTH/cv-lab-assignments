import pywt
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

# ============================================================
# CẤU HÌNH ĐƯỜNG DẪN & THAM SỐ
# ============================================================
POS_FOLDER = 'BTCB/data/positive'
NEG_FOLDER = 'BTCB/data/negative'
OUTPUT_DIR = 'BTCB/output'

THRESHOLD_DEFAULT = 15.0  # Ngưỡng % dùng để tính Accuracy/Sensitivity/Specificity
WAVELET = 'db4'
LEVEL = 3
IMG_SIZE = (128, 128)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1, 2, 3. XỬ LÝ ẢNH & TẠO MÃ BĂM
# ============================================================

def get_wavelet_hash(image_path: str):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None: return None

    img = cv2.resize(img, IMG_SIZE)
    # Bước 2: Trích xuất wavelet ma trận
    coeffs = pywt.wavedec2(img, WAVELET, level=LEVEL)
    approx = coeffs[0]  # Thành phần LL (xấp xỉ thấp tần)

    # Bước 3: Tạo mã băm dựa trên lượng tử hóa (so với trung bình)
    avg = np.mean(approx)
    hash_code = (approx > avg).flatten().astype(int)
    return hash_code

def hamming_distance(h1, h2):
    # Bước 4: So sánh hàm băm (Tính khoảng cách Hamming)
    return int(np.count_nonzero(h1 != h2))

# ============================================================
# TỰ ĐỘNG GHÉP CẶP (Dựa trên folder và tiền tố tên file)
# ============================================================

def build_pairs(pos_folder, neg_folder):
    pairs = []
    pos_files = [f for f in os.listdir(pos_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    neg_files = [f for f in os.listdir(neg_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Cặp Positive: Cùng folder positive, cùng tiền tố (test1_... vs test1_...)
    for i in range(len(pos_files)):
        for j in range(i + 1, len(pos_files)):
            f1, f2 = pos_files[i], pos_files[j]
            prefix1, prefix2 = f1.split('_')[0], f2.split('_')[0]
            label = 1 if prefix1 == prefix2 else 0
            pairs.append({'fileA': os.path.join(pos_folder, f1), 'fileB': os.path.join(pos_folder, f2), 'label': label})

    # Cặp Negative: Positive vs Negative folder
    for pf in pos_files:
        for nf in neg_files:
            pairs.append({'fileA': os.path.join(pos_folder, pf), 'fileB': os.path.join(neg_folder, nf), 'label': 0})
    
    return pairs

# ============================================================
# 5. ĐÁNH GIÁ & VẼ ĐƯỜNG CONG ROC
# ============================================================

def run_evaluation(pairs):
    raw_results = []
    print("[PROCESSING] Đang tính toán mã băm và khoảng cách cho các cặp ảnh...")
    
    for pair in pairs:
        h1 = get_wavelet_hash(pair['fileA'])
        h2 = get_wavelet_hash(pair['fileB'])
        if h1 is None or h2 is None: continue
        
        dist = hamming_distance(h1, h2)
        dist_pct = (dist / len(h1)) * 100
        raw_results.append({'dist_pct': dist_pct, 'label': pair['label']})

    # --- TÍNH CHỈ SỐ TẠI NGƯỠNG MẶC ĐỊNH ---
    TP = TN = FP = FN = 0
    for res in raw_results:
        pred = 1 if res['dist_pct'] < THRESHOLD_DEFAULT else 0
        if pred == 1 and res['label'] == 1: TP += 1
        elif pred == 0 and res['label'] == 0: TN += 1
        elif pred == 1 and res['label'] == 0: FP += 1
        else: FN += 1

    total = TP + TN + FP + FN
    acc = (TP + TN) / total if total > 0 else 0
    sen = TP / (TP + FN) if (TP + FN) > 0 else 0
    spe = TN / (TN + FP) if (TN + FP) > 0 else 0

    print("\n" + "="*50)
    print(f"KẾT QUẢ TẠI NGƯỠNG {THRESHOLD_DEFAULT}%")
    print("-" * 50)
    print(f"Độ chính xác (Accuracy):   {acc*100:.2f}%")
    print(f"Độ nhạy (Sensitivity):     {sen*100:.2f}%")
    print(f"Độ đặc biệt (Specificity): {spe*100:.2f}%")
    print(f"Confusion Matrix: TP={TP}, TN={TN}, FP={FP}, FN={FN}")
    print("="*50)

    # --- QUÉT CÁC NGƯỠNG ĐỂ VẼ ĐƯỜNG CONG ROC ---
    tpr_list = [0] # True Positive Rate
    fpr_list = [0] # False Positive Rate
    
    # Quét ngưỡng từ 0% đến 100%
    for thr in np.linspace(0, 100, 100):
        tp = fn = tn = fp = 0
        for res in raw_results:
            p = 1 if res['dist_pct'] < thr else 0
            if p == 1 and res['label'] == 1: tp += 1
            elif p == 0 and res['label'] == 1: fn += 1
            elif p == 0 and res['label'] == 0: tn += 1
            elif p == 1 and res['label'] == 0: fp += 1
        
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        tpr_list.append(tpr)
        fpr_list.append(fpr)

    # Thêm điểm cuối (1,1)
    tpr_list.append(1)
    fpr_list.append(1)

    # Vẽ ROC
    plt.figure(figsize=(8, 6))
    plt.plot(fpr_list, tpr_list, color='darkorange', lw=2, label='Wavelet Hashing ROC')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    
    roc_path = os.path.join(OUTPUT_DIR, 'roc_curve.png')
    plt.savefig(roc_path)
    print(f"\n[SUCCESS] Đã lưu biểu đồ ROC tại: {roc_path}")
    plt.show()

# ============================================================
# CHƯƠNG TRÌNH CHÍNH
# ============================================================
if __name__ == '__main__':
    all_pairs = build_pairs(POS_FOLDER, NEG_FOLDER)
    if not all_pairs:
        print("LỖI: Không tìm thấy ảnh hoặc cặp ảnh hợp lệ.")
    else:
        run_evaluation(all_pairs)