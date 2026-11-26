# 세션 지도(MAP.md)를 대화·일지 줄에서 바로 만든다 — AI 안 씀, 토큰 0.
# 사용: python ~/.claude/skills/session-router/scripts/make_map.py
# 대화 줄 형식: "- HH:MM 보낸→받는 | 요약 | 경로"  (받는 쪽 여러 개는 · 로)
import re
from collections import defaultdict
from pathlib import Path

H = Path.home() / ".claude" / "sessions-hub"  # 세션 허브 위치
H.mkdir(parents=True, exist_ok=True)
LINE = re.compile(r'^- (\S+) ([^|→]+?)(?:→([^|]+?))? \| (.+?) \| (.*)$')

def parse(text, day):
    out = []
    for l in text.splitlines():
        m = LINE.match(l.strip())
        if m:
            t, a, b, what, path = m.groups()
            out.append((day, t, a.strip(), [x.strip() for x in (b or '').split('·') if x.strip()], what.strip(), path.strip()))
    return out

rows = []
for f in sorted((H / '대화').glob('*.md')):
    rows += parse(f.read_text(encoding='utf-8'), f.stem)

pair = defaultdict(int)
for _, _, a, bs, _, _ in rows:
    for b in bs:
        pair[(a, b)] += 1

md = ['# 세션 지도 (make_map.py 자동 생성, 직접 고치지 말 것)', '',
      '## 누가 누구에게 몇 번', '| 보낸 | 받는 | 횟수 |', '|---|---|---|']
md += [f'| {a} | {b} | {n} |' for (a, b), n in sorted(pair.items(), key=lambda x: -x[1])]
md += ['', '## 파일·경로가 오간 기록 (최근 30)']
md += [f'- {d} {t} {a}→{"·".join(bs) or "-"}: {w} — `{p}`' for d, t, a, bs, w, p in rows if p and p != '-'][-30:]
md += ['', '## 세션별 최근 일지 (각 5줄)']
for f in sorted((H / '일지').glob('*.md')):
    ls = [l for l in f.read_text(encoding='utf-8').splitlines() if l.startswith('- ')]
    md += [f'### {f.stem}'] + ls[-5:] + ['']
(H / 'MAP.md').write_text('\n'.join(md), encoding='utf-8')
print(f'MAP.md: 대화 {len(rows)}줄, 연결 {len(pair)}개')

if __name__ == '__main__':
    assert parse('- 12:02 디자인→앱출시 | 끝 | a.md', 'd')[0][2:4] == ('디자인', ['앱출시'])
    assert parse('- 11:4x 앱출시→쇼츠·디자인 | 규칙 | -', 'd')[0][3] == ['쇼츠', '디자인']
