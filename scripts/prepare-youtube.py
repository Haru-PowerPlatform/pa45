#!/usr/bin/env python3
"""
PA45 録画 → YouTube投稿準備 ワンコマンドスクリプト

Teams録画ファイルを渡すと、ffmpegでトリミング＋クロップした動画と
サムネイル画像を一発で生成する。アップロード自体は YouTube Studio で手動。

使い方:
    python scripts/prepare-youtube.py --vol 10 --theme "総復習回" \
        --src "C:\\Users\\isamu\\Videos\\pa45-vol10-raw.mp4" \
        --start 00:11:00 --end 01:11:00

主なオプション:
    --vol     回数（必須）
    --theme   テーマ名（必須・サムネイルとファイル名に使用）
    --src     Teams録画ファイルのパス（必須）
    --start   切り出し開始位置 HH:MM:SS（省略時は先頭から）
    --end     切り出し終了位置 HH:MM:SS（省略時は末尾まで）
    --crop    クロップ指定 w:h:x:y（既定 1133:719:125:49 = 1920x1080用）
    --outdir  出力先フォルダ（既定 C:\\Temp）

実行内容:
    1. ffmpeg で録画をトリミング＋クロップ → {outdir}\\P00N-PA45.mp4
    2. make-ogp.py でサムネイル生成 → assets/ogp/pa45-volN-thumb.png
    3. サムネイルを {outdir} にもコピー（手動アップロード用）
    4. 次の手順（YouTube Studio アップロード）を表示
"""

import sys
import io
import shutil
import argparse
import subprocess
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent
DEFAULT_CROP = "1133:719:125:49"   # 1920x1080 の白いスライド領域
DEFAULT_OUTDIR = r"C:\Temp"


def run_ffmpeg(src: Path, out: Path, crop: str, start: str, end: str) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        sys.exit("✗ ffmpeg が見つかりません。PATH を確認してください。")

    cmd = [ffmpeg, "-y"]
    if start:
        cmd += ["-ss", start]
    if end:
        cmd += ["-to", end]
    cmd += ["-i", str(src), "-vf", f"crop={crop}", str(out)]

    print("  実行コマンド:")
    print("    " + " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    if result.returncode != 0:
        print(result.stderr[-2000:])
        sys.exit(f"✗ ffmpeg が失敗しました（exit={result.returncode}）")


def make_thumbnail(vol: int, theme: str) -> Path:
    rel_out = f"assets/ogp/pa45-vol{vol}-thumb.png"
    cmd = [
        sys.executable, str(SCRIPT_DIR / "make-ogp.py"),
        "--title", f"第{vol}回\\n{theme}",
        "--label", f"PA45 第{vol}回",
        "--sub",   "Power Automate ハンズオン",
        "--theme", "orange",
        "--out",   rel_out,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        sys.exit(f"✗ サムネイル生成に失敗しました（exit={result.returncode}）")
    return ROOT / rel_out


def main():
    p = argparse.ArgumentParser(description="PA45 録画 → YouTube投稿準備")
    p.add_argument("--vol", required=True, type=int, help="回数")
    p.add_argument("--theme", required=True, help="テーマ名")
    p.add_argument("--src", required=True, help="Teams録画ファイルのパス")
    p.add_argument("--start", default="", help="切り出し開始 HH:MM:SS")
    p.add_argument("--end", default="", help="切り出し終了 HH:MM:SS")
    p.add_argument("--crop", default=DEFAULT_CROP, help=f"クロップ w:h:x:y（既定 {DEFAULT_CROP}）")
    p.add_argument("--outdir", default=DEFAULT_OUTDIR, help=f"出力先（既定 {DEFAULT_OUTDIR}）")
    args = p.parse_args()

    src = Path(args.src)
    if not src.exists():
        sys.exit(f"✗ 録画ファイルが見つかりません: {src}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    video_out = outdir / f"P{args.vol:03d}-PA45.mp4"
    thumb_copy = outdir / f"pa45-vol{args.vol}-thumb.png"

    print(f"\n=== PA45 Vol.{args.vol} YouTube投稿準備 ===\n")

    # 1. 動画のトリミング＋クロップ
    print("[1/3] ffmpeg で録画を編集中...")
    run_ffmpeg(src, video_out, args.crop, args.start, args.end)
    size_mb = video_out.stat().st_size / 1024 / 1024
    print(f"  ✓ 動画を出力: {video_out}  ({size_mb:.1f} MB)")

    # 2. サムネイル生成
    print("[2/3] サムネイル画像を生成中...")
    thumb = make_thumbnail(args.vol, args.theme)
    print(f"  ✓ サムネイル: {thumb.relative_to(ROOT)}")

    # 3. サムネイルを出力先にもコピー（手動アップロード用）
    print("[3/3] サムネイルをコピー中...")
    shutil.copy(thumb, thumb_copy)
    print(f"  ✓ コピー: {thumb_copy}")

    print(f"\n✅ 準備完了！次の手順:\n")
    print(f"  1. YouTube Studio で動画をアップロード")
    print(f"     動画ファイル: {video_out}")
    print(f"  2. カスタムサムネイルを設定")
    print(f"     画像ファイル: {thumb_copy}")
    print(f"  3. アップロード後、URL を取得して以下を実行:")
    print(f"     python scripts/youtube-release.py {args.vol} <YouTube URL>")


if __name__ == "__main__":
    main()
