# 테스트 원문을 웹 앱에 보내고 응답을 저장 (원문은 UTF-8로 읽음)
# Send test texts to the web app and save responses (read as UTF-8)
# 사용법 / Usage: python collect.py <저장 폴더> 03-article:5 06-max-ko:10 ...
# S2-6: 실패해도 멈추지 않음, 왕복 시간(rt) 저장, 앱 checkCards와 같은 판정(app), 끝에 요약
import json, re, sys, time, urllib.request
URL = re.search(r'https://script\.google\.com[^"]*', open('../../../202610-my-service/config.js', encoding='utf-8').read()).group(0)
OUT = sys.argv[1]

# my-feature.html countSentences와 같은 규칙 / Same rule as countSentences
def sentences(s):
    return len([x for x in re.split(r'[.?!。]+', s) if x.strip()])

def good_face(f):
    return isinstance(f, str) and f.strip() != ''

# my-feature.html checkCards와 같은 판정 / Same verdict as checkCards
def app_kind(d):
    if d.get('ok') is not True:
        return 'service'
    cards = d.get('cards')
    if not isinstance(cards, list):
        return 'service'
    if len(cards) == 0:
        return 'source'
    kept = cards[:20]
    if any(not isinstance(c, dict) or not good_face(c.get('front')) or not good_face(c.get('back')) for c in kept):
        return 'service'
    if any(sentences(c['front']) > 3 or sentences(c['back']) > 3 for c in kept):
        return 'service'                              # 3문장 초과 = 서비스 문제 (2026-10-31) / Over 3 sentences = service
    return 'ok'

rows = []
for spec in sys.argv[2:]:
    name, n = spec.split(':')
    md = open(f'../../test-inputs/{name}.md', encoding='utf-8').read()
    text = md.split('```')[1].lstrip('\n')            # 첫 코드 상자 / first code block
    for i in range(1, int(n) + 1):
        req = urllib.request.Request(URL, data=json.dumps({'text': text}).encode('utf-8'),
                                     headers={'Content-Type': 'text/plain;charset=utf-8'})
        t0 = time.time()
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=90).read().decode('utf-8'))
        except Exception as err:                      # 끊김·시간 초과·JSON 아님 / network, timeout, not JSON
            d = {'ok': False, 'reason': 'CLIENT_' + type(err).__name__}
        d['rt'] = round(time.time() - t0, 1)          # 왕복 초 / round trip seconds
        d['app'] = app_kind(d)
        open(f'{OUT}/{name}-{i}.json', 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
        meta = {k: v for k, v in d.items() if k != 'cards'}
        print(f'{name} #{i} cards={len(d.get("cards") or [])} {meta}', flush=True)
        rows.append((name, d))
        # 한도 2번 연속이면 멈춤 / Stop after 2 QUOTA in a row
        if len(rows) >= 2 and all(r[1].get('reason') == 'QUOTA' for r in rows[-2:]):
            sys.exit('QUOTA 2번 연속 - 측정 중단 / quota twice in a row: stopped')
        time.sleep(5)                                 # 분당 한도 피하기 / avoid per-minute quota

# 원문별 요약 / Summary per text
def avg(xs):
    return round(sum(xs) / len(xs), 1) if xs else '-'

print('\n== 요약 / Summary ==')
for name in dict.fromkeys(r[0] for r in rows):
    ds = [d for n, d in rows if n == name]
    oks = [d for d in ds if d.get('ok') is True and 'ms' in d]
    rts = [d['rt'] for d in ds]
    ms = [d['ms'] / 1000 for d in oks]
    apps = {k: sum(1 for d in ds if d['app'] == k) for k in ('ok', 'source', 'service')}
    fails = sorted({d.get('reason') for d in ds if d.get('ok') is not True})
    print(f'{name}: n={len(ds)} app={apps} fail={fails}')
    print(f'  rt avg {avg(rts)} max {max(rts)} / server avg {avg(ms)} max {max(ms) if ms else "-"}'
          f' / gap avg {avg([d["rt"] - d["ms"] / 1000 for d in oks])}')
    print(f'  tokens in {avg([d["inTokens"] for d in oks])} out {avg([d["outTokens"] for d in oks])}'
          f' think {avg([d["thinkTokens"] for d in oks])} / cards {avg([len(d["cards"]) for d in oks])}')
