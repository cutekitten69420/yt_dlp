# reel_downloader.py
import sys
import yt_dlp

def download_reel(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Save with reel title as filename
        'format': 'mp4/bestvideo+bestaudio/best',  # Prefer mp4
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("✅ Download complete!")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reel_downloader.py <Instagram_Reel_URL>")
    else:
        reel_url = sys.argv[1]
        download_reel(reel_url)
