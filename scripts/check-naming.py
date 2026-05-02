"""
PA45 命名ルール検証スクリプト
pac CLI で Solution 一覧を取得し、release-flow.bat のマッピングと突き合わせる。
不整合があれば具体的な対処を表示してエラー終了。

使い方:
  python scripts/check-naming.py
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RELEASE_BAT = REPO / 'scripts' / 'release-flow.bat'


def parse_release_bat() -> dict[int, str]:
    """release-flow.bat から Vol番号→Solution UniqueName のマッピングを抽出"""
    text = RELEASE_BAT.read_text(encoding='utf-8')
    mapping = {}
    for m in re.finditer(r'if "%VOL%"=="(\d+)" set SOLUTION=(\w+)', text):
        mapping[int(m.group(1))] = m.group(2)
    return mapping


def get_pac_solutions() -> set[str]:
    """pac solution list から UniqueName 一覧を取得"""
    try:
        result = subprocess.run(
            ['pac', 'solution', 'list'],
            capture_output=True, text=True, encoding='utf-8',
            shell=True, timeout=60
        )
    except FileNotFoundError:
        print('✗ pac CLI が見つかりません。インストール: https://aka.ms/PowerPlatformCLI')
        sys.exit(2)
    except subprocess.TimeoutExpired:
        print('✗ pac solution list がタイムアウトしました')
        sys.exit(2)

    if result.returncode != 0:
        print(f'✗ pac solution list 失敗:')
        print(result.stderr)
        sys.exit(2)

    lines = result.stdout.splitlines()
    solutions = set()
    capture = False
    for line in lines:
        if line.startswith('Unique Name'):
            capture = True
            continue
        if capture and line.strip() and not line.startswith('---'):
            cols = line.split()
            if cols:
                solutions.add(cols[0])
    return solutions


def main():
    print('=== PA45 命名ルール検証 ===')

    mapping = parse_release_bat()
    if not mapping:
        print('✗ release-flow.bat から Vol マッピングを抽出できません')
        return 1

    print(f'  release-flow.bat: {len(mapping)} 個の Vol マッピング検出')

    pac_solutions = get_pac_solutions()
    print(f'  pac solution list: {len(pac_solutions)} 個の Solution 検出')

    errors = []
    warnings = []

    for vol, expected_name in sorted(mapping.items()):
        if expected_name in pac_solutions:
            print(f'  ✓ Vol.{vol}: {expected_name}')
        else:
            # 似た名前を探す
            similar = [s for s in pac_solutions if expected_name.lower() in s.lower() or s.lower() in expected_name.lower()]
            errors.append((vol, expected_name, similar))

    # release-flow.bat に未登録のSolution（PA45系）を警告
    pa45_solutions = {s for s in pac_solutions if s.startswith('PA45') and s != 'PA45Handson'}
    registered = set(mapping.values())
    unregistered = pa45_solutions - registered
    for s in sorted(unregistered):
        warnings.append(s)

    if errors:
        print()
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        print('❌ 命名ミス・未作成のSolution検出')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        for vol, expected, similar in errors:
            print(f'  Vol.{vol}: 期待 = "{expected}" だが PA に存在しない')
            if similar:
                print(f'    💡 似た名前: {", ".join(similar)}')
                print(f'    対処A: PA で Solution 名を "{expected}" に直す')
                print(f'    対処B: release-flow.bat の Vol.{vol} の SOLUTION を "{similar[0]}" に直す')
            else:
                print(f'    💡 PA で Solution "{expected}" を新規作成してください')
            print()

    if warnings:
        print()
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        print('⚠ release-flow.bat に未登録のPA45 Solution')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        for s in warnings:
            print(f'  - {s}')
        print('  対処: scripts/add-vol-card.py で登録するか手動でマッピング追加')

    if errors:
        print()
        print('検証 NG。修正してから release-flow.bat を実行してください。')
        return 1

    print()
    print('✓ 命名ルール OK。release-flow.bat 実行可能です。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
