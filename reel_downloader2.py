# reel_downloader2.py
import yt_dlp

def download_reel(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Save with reel title as filename
        'format': 'mp4/bestvideo+bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("✅ Download complete!")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # 🔽 Paste your Instagram Reel URL here
    reel_url = "https://www.instagram.com/reel/DIYGiE9TC7C"

    print(f"Downloading: {reel_url}")
    download_reel(reel_url)
