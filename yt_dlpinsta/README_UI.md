Local React UI + Flask server for the existing downloader scripts

What I added
- `ui/index.html` - a small React single-file app (loaded via CDN) that collects input: single link, mode (audio/video), bulk file (.txt), cookies file, and output folder.
- `server.py` - a Flask app that serves the UI and exposes two endpoints:
  - POST `/api/download` for single links (form fields: `link`, `mode`, `outdir`)
  - POST `/api/download_bulk` for bulk (multipart form: `file`=links file, `cookies` optional, `outdir`)
- `requirements.txt` - minimal Python deps for the server.

How it works (assumptions)
- Mapping of modes to scripts:
  - audio -> `reel_downloader3.py`
  - video -> `reel_downloader.py`
  - bulk -> `reel_batch_downloader.py`
- The server calls the mapped script using your Python interpreter (sys.executable) and passes positional arguments as: for single -> [script, link, outdir?]; for bulk -> [script, links_file, cookies_file?, outdir?].
- If your existing scripts accept different flags, update `SCRIPT_MAP` or modify `server.py` to match their CLI signature.

Run locally (Windows PowerShell)

1) Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2) Install requirements:

```powershell
python -m pip install -r requirements.txt
```

3) Run the server from the `yt_dlpinsta` folder:

```powershell
python server.py
```

4) Open your browser at http://127.0.0.1:5000

Notes and next steps
- The UI sends the output folder as a text path; browsers cannot choose arbitrary server-side folders, so the server expects a path valid on the machine running the Flask process.
- If you want a production-ready React app, I can scaffold a proper create-react-app / Vite project and implement nicer UX, plus better background job handling and real-time progress.
- If your downloader scripts require specific command-line flags, tell me their exact signatures and I'll adjust `server.py` to call them correctly.
