"""
PA45 フローZIP 自動インポートスクリプト
pac CLI でエクスポートしたZIPを取り込んで flows/vol-XX/ に配置・サイト更新する。

使い方:
  python scripts/import-flow-zip.py --src C:/Temp/pa45/flow-zips
    → 最新ZIPを Vol番号判別して flows/vol-NN/ にコピー
    → sessions/index.html の DLボタンURL更新
"""
import argparse
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Solution UniqueName から Vol番号 を取り出す regex
# 実ファイル名パターン:
#   PA45No9SharePointUpdate_managed.zip                (バージョン無)
#   PA45No9SharePointUpdate_1_0_0_0_managed.zip        (バージョン有)
SOLUTION_RE = re.compile(r'PA45No(\d+)([A-Za-z]+?)(?:_\d+_\d+_\d+_\d+)?_managed\.zip$', re.IGNORECASE)

# Vol番号 → 配布ファイル名サフィックス（既存flows/vol-NN/PA45-VolNN-XXX.zipと整合）
VOL_TOPIC = {
    1: 'InitializeVariable',
    2: 'SetVariable',
    3: 'Condition',
    4: 'ApplyToEach',
    5: 'Review',
    6: 'FormsMail',
    7: 'FormsSPTeams',
    8: 'ApprovalFlow',
    9: 'SharePointUpdate',
}


def find_latest_zip(src: Path, vol: int | None = None) -> Path | None:
    """src フォルダから最新の PA45_NoN_*.zip を取得（vol指定時は絞り込み）"""
    candidates = []
    for p in src.glob('PA45No*_managed.zip'):
        m = SOLUTION_RE.match(p.name)
        if not m:
            continue
        n = int(m.group(1))
        if vol is not None and n != vol:
            continue
        candidates.append((p.stat().st_mtime, n, p))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][2]


def import_zip(zip_path: Path) -> tuple[int, Path]:
    """ZIPを flows/vol-NN/ に配置。Vol番号と配置先パスを返す"""
    m = SOLUTION_RE.match(zip_path.name)
    if not m:
        raise ValueError(f'ファイル名がSolution規則に合わない: {zip_path.name}')
    vol = int(m.group(1))
    topic = VOL_TOPIC.get(vol, m.group(2))

    vol_dir = REPO / 'flows' / f'vol-{vol:02d}'
    vol_dir.mkdir(parents=True, exist_ok=True)

    dest_name = f'PA45-Vol{vol:02d}-{topic}.zip'
    dest = vol_dir / dest_name
    shutil.copy2(zip_path, dest)
    print(f'  ✓ {zip_path.name} → {dest.relative_to(REPO)}')
    return vol, dest


def update_sessions_html(vol: int, dest: Path) -> bool:
    """sessions/index.html の該当 Vol カードのZIP DLボタンURLを更新"""
    html_path = REPO / 'sessions' / 'index.html'
    text = html_path.read_text(encoding='utf-8')

    rel_url = f'https://haru-powerplatform.github.io/pa45/{dest.relative_to(REPO).as_posix()}'

    # 既存パターン: flows/vol-NN/PA45-VolNN-OLD.zip → 新URLに置換
    pattern = re.compile(
        rf'https://haru-powerplatform\.github\.io/pa45/flows/vol-{vol:02d}/PA45-Vol{vol:02d}-[\w]+\.zip'
    )
    new_text, n = pattern.subn(rel_url, text)
    if n > 0:
        html_path.write_text(new_text, encoding='utf-8')
        print(f'  ✓ sessions/index.html の {n} 箇所を更新')
        return True
    print(f'  ⚠ sessions/index.html に Vol{vol} のリンクが見つからない（手動追加が必要かも）')
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='C:/Temp/pa45/flow-zips', help='ZIP保存ディレクトリ')
    ap.add_argument('--vol', type=int, help='特定Volのみ処理（省略時：最新ZIP1個）')
    ap.add_argument('--all', action='store_true', help='src内の全PA45ZIPを処理')
    args = ap.parse_args()

    src = Path(args.src)
    if not src.exists():
        print(f'エラー: {src} が存在しません')
        return 1

    print(f'=== PA45 フローZIPインポート ===')
    print(f'  src: {src}')

    if args.all:
        zips = list(src.glob('PA45No*_managed.zip'))
        zips.sort()
        if not zips:
            print('  対象ZIPなし')
            return 0
        seen_vols = set()
        # 各Vol最新だけ採用
        per_vol = {}
        for z in zips:
            m = SOLUTION_RE.match(z.name)
            if not m: continue
            v = int(m.group(1))
            mt = z.stat().st_mtime
            if v not in per_vol or per_vol[v][0] < mt:
                per_vol[v] = (mt, z)
        for v in sorted(per_vol):
            _, z = per_vol[v]
            vol, dest = import_zip(z)
            update_sessions_html(vol, dest)
    else:
        zip_path = find_latest_zip(src, args.vol)
        if not zip_path:
            print('  対象ZIPなし')
            return 0
        vol, dest = import_zip(zip_path)
        update_sessions_html(vol, dest)

    print('完了！次のコマンドでpush:')
    print('  git add -A && git commit -m "feat: フローZIP更新" && git push origin main')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
