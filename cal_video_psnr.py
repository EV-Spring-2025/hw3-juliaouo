import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def calculate_psnr(img1, img2):
    if img1.dtype != np.uint8:
        img1 = (img1 * 255).clip(0, 255).astype(np.uint8)
    if img2.dtype != np.uint8:
        img2 = (img2 * 255).clip(0, 255).astype(np.uint8)
    mse = np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)
    if mse == 0:
        return float('inf')
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr

def main(video_path1, video_path2, output_file):
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    psnr_list = []
    frame_idx = 0

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not ret1 or not ret2:
            break
        if frame1.shape != frame2.shape:
            continue
        psnr = calculate_psnr(frame1, frame2)
        psnr_list.append(psnr)
        print(f"Frame {frame_idx}: PSNR = {psnr:.2f} dB")
        frame_idx += 1

    cap1.release()
    cap2.release()

    if len(psnr_list) == 0:
        print("No frames to compare.")
        return
    
    finite_psnr_list = [v for v in psnr_list if np.isfinite(v)]
    if len(finite_psnr_list) == 0:
        print("No valid PSNR values to plot.")
        return
    
    # 畫圖
    plt.figure()
    plt.plot(range(len(psnr_list)), psnr_list, marker='o')
    plt.xlabel("Frame")
    plt.ylabel("PSNR (dB)")
    plt.title("PSNR per Frame")
    plt.grid(True)
    avg_psnr = np.mean(psnr_list)

    plt.axhline(avg_psnr, color='r', linestyle='--', label=f'Average PSNR = {avg_psnr:.2f} dB')
    plt.legend()

    if np.isfinite(avg_psnr):
        plt.text(len(psnr_list)*0.6, avg_psnr+0.5, f'Avg: {avg_psnr:.2f} dB', color='r')
    output_dir = os.path.dirname(output_file)
    if output_dir != '':
        os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_file)
    plt.close()
    print(f"Average PSNR: {avg_psnr:.2f} dB")
    print(f"PSNR curve saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("python video_psnr_plot.py <video1> <video2> <output_file>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])