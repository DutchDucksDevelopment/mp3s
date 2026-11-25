from pathlib import Path
import subprocess
import sys

links_file = Path("links.txt")
output_dir = Path("../Mp3s")
output_dir.mkdir(exist_ok=True)

if not links_file.is_file():
    sys.exit("Create links.txt with one URL per line.")

links = [
    line.strip()
    for line in links_file.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]

if not links:
    sys.exit("No links found in links.txt.")

for url in links:
    result = subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "--extract-audio",
        "--audio-format", "vorbis",
        "--audio-quality", "80K",
        "--postprocessor-args", "FFmpegExtractAudio:-ac 2 -ar 44100 -b:a 80k",
        "--output", str(output_dir / "%(title)s.%(ext)s"),
        url,
    ])
    if result.returncode:
        print(f"Failed to process: {url}")

