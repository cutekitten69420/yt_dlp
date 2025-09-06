# reel_downloader3.py
import yt_dlp

def download_instagram(url, audio_only=False):
    if audio_only:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestaudio/best',   # will download as .m4a
        }
    else:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'mp4/bestvideo+bestaudio/best',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("✅ Download complete!")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    # 🔽 Paste your Instagram Reel link here
    insta_url = "https://www.instagram.com/reel/DJVRj8jMr_n"
    
    # change to True if you want just audio (.m4a)
    audio_only = True  

    print(f"Downloading: {insta_url}")
    download_instagram(insta_url, audio_only)
