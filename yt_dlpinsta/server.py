from flask import Flask, request, jsonify, send_from_directory, abort
import os
import subprocess
import sys
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="ui", static_url_path="")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mapping: mode -> script
SCRIPT_MAP = {
    'audio': 'reel_downloader3.py',
    'video': 'reel_downloader.py',
    'bulk': 'reel_batch_downloader.py'
}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/download', methods=['POST'])
def download_single():
    data = request.form
    link = data.get('link')
    mode = data.get('mode', 'video')
    outdir = data.get('outdir') or ''
    if not link:
        return jsonify({'error': 'missing link'}), 400

    script_name = SCRIPT_MAP.get(mode, 'reel_downloader.py')
    script_path = os.path.join(BASE_DIR, script_name)
    if not os.path.isfile(script_path):
        return jsonify({'error': f'script not found: {script_name}'}), 500

    cmd = [sys.executable, script_path, link]
    if outdir:
        cmd += [outdir]

    try:
        # Force UTF-8 in the child Python process to avoid UnicodeEncodeError on Windows
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900, env=env)
        return jsonify({'returncode': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'process timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_bulk', methods=['POST'])
def download_bulk():
    # Expects: file (txt), cookies (file), outdir
    if 'file' not in request.files:
        return jsonify({'error': 'missing file (txt)'}), 400
    data = request.form
    outdir = data.get('outdir') or ''

    file = request.files['file']
    cookies = request.files.get('cookies')

    temp_dir = tempfile.mkdtemp(prefix='yt_dl_bulk_')
    try:
        file_name = secure_filename(file.filename or 'links.txt')
        file_path = os.path.join(temp_dir, file_name)
        file.save(file_path)

        cookies_path = ''
        if cookies and cookies.filename:
            cookies_name = secure_filename(cookies.filename)
            cookies_path = os.path.join(temp_dir, cookies_name)
            cookies.save(cookies_path)

        script_name = SCRIPT_MAP.get('bulk')
        script_path = os.path.join(BASE_DIR, script_name)
        if not os.path.isfile(script_path):
            return jsonify({'error': f'script not found: {script_name}'}), 500

        cmd = [sys.executable, script_path, file_path]
        if cookies_path:
            cmd += [cookies_path]
        if outdir:
            cmd += [outdir]

        # Force UTF-8 in the child Python process to avoid UnicodeEncodeError on Windows
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, env=env)
        return jsonify({'returncode': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'process timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ui/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Development server
    app.run(host='127.0.0.1', port=5000, debug=True)
