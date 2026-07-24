import cv2
import yt_dlp
import os

def extract_frames(video_url, output_folder, target_frame_count=800):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Klasör oluşturuldu: {output_folder}")

    video_filename = "temp_video.mp4"

    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': video_filename,
        'quiet': False
    }

    print(f"Video indiriliyor: {video_url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print("Kareler ayıklanıyor...")
    cap = cv2.VideoCapture(video_filename)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    step = max(1, total_frames // target_frame_count)
    
    count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if count % step == 0 and saved_count < target_frame_count:
            frame_path = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1
            
        count += 1
        
    cap.release()
    
    if os.path.exists(video_filename):
        os.remove(video_filename)
        
    print(f"İşlem tamamlandı! '{output_folder}' klasörüne {saved_count} kare kaydedildi.")

if __name__ == "__main__":
    url = input("YouTube video linkini yapıştır: ")
    output = "extracted_frames"
    try:
        extract_frames(url, output)
    except Exception as e:
        print(f"Bir hata oluştu: {e}")