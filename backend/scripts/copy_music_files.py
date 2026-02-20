import os
import shutil

V1_MUSIC_PATH = r"c:\BM_Program\shElter-v1\00_shElter\03_Echoom\music"
V3_MUSIC_PATH = r"c:\BM_Program\shElter-v3\backend\static\music"

def copy_music_files():
    print(f"Copying music from {V1_MUSIC_PATH} to {V3_MUSIC_PATH}...")
    
    if not os.path.exists(V1_MUSIC_PATH):
        print("Source directory not found.")
        return
        
    if not os.path.exists(V3_MUSIC_PATH):
        os.makedirs(V3_MUSIC_PATH)
        
    audio_extensions = ['.mp3', '.wav', '.ogg']
    count = 0
    
    for filename in os.listdir(V1_MUSIC_PATH):
        ext = os.path.splitext(filename)[1].lower()
        if ext in audio_extensions:
            src = os.path.join(V1_MUSIC_PATH, filename)
            dst = os.path.join(V3_MUSIC_PATH, filename)
            
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                print(f"Copied: {filename}")
                count += 1
            else:
                print(f"Skipped (exists): {filename}")
                
    print(f"Copied {count} files.")

if __name__ == "__main__":
    copy_music_files()
