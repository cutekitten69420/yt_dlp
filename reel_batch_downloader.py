import yt_dlp

def download_reels(file_path, cookies_file):
    try:
        with open(file_path, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return

    if not urls:
        print("⚠️ No URLs found in file.")
        return

    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'mp4/bestvideo+bestaudio/best',
        'cookiefile': cookies_file,   # <-- use the cookies.txt
        'ignoreerrors': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"⬇️ Downloading: {url}")
            try:
                ydl.download([url])
            except Exception as e:
                print(f"❌ Error downloading {url}: {e}")

if __name__ == "__main__":
    file_with_links = "reels.txt"
    cookies_file = "cookies.txt"
    download_reels(file_with_links, cookies_file)
