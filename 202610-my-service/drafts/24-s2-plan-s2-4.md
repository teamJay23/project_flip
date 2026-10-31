# S2-4 계획 — HTML ↔ Apps Script 연결 (v1, 2026-10-27)

> 기준: PRD v1.5, 02 계획 6-1번 표 0~5 · 7번 S2-4 · 8번 체크리스트, 13 1-7, 16 9번, 22 7번
> 상태: **admin 승인 전 초안**

## 0. 먼저 알아둘 것 (3가지)

1. **`my-feature.html`이 지금 `config.js`를 불러오지 않는다.** 주소(`CARD_API_URL`)를 쓰려면 `<script src="config.js"></script>`를 먼저 넣어야 한다.
2. 가짜 장치(`?fake=…`)를 **모두 지운다.** 지우기 전에 `drafts/fake-responses.md`로 옮겨 둔다. 지운 뒤에는 5-a·5-b(4문장, 22장)를 휴대폰에서 다시 시험할 수 없다 → S2-2에서 이미 통과했으므로 받아들인다.
3. 다른 앱에 갔다 오기(`visibilitychange`, 6-a)는 **S2-7**이다. 이번에는 화면이 켜져 있을 때의 60초만 만든다.

## 1. 바꿀 곳 (`my-feature.html` 한 파일)

| # | 무엇 | 왜 |
|---|---|---|
| 1 | `<script src="config.js"></script>` 추가 (앱 스크립트 바로 위) | 웹 앱 주소를 읽기 위해 |
| 2 | 상수 `LOAD_TIMEOUT_MS = 60000` | 60초 제한 (Apps Script 50초 < 화면 60초 유지) |
| 3 | `[FAKE-S2-1]`, `[FAKE-S2-2]` 덩어리 삭제 | 진짜 요청으로 바꿈 |
| 4 | `requestCards`를 진짜 `fetch`로 다시 씀 (아래 2번) | 6-1 표 0~5 |
| 5 | 클릭 처리기에 마지막 안전망 `try/catch` → `showFail('service')` | 13 1-7: 예외가 나도 로딩에 갇히지 않게 |
| 6 | 임시 성공 표시 주석의 "S2-4에서 정리" → "3단계에서 정리" | 학습 화면은 3단계 |

지우지 않는 것: `checkCards`·`countSentences`·`isGoodFace`·상수·임시 성공 표시.
`card-api.gs`는 **고치지 않는다** (시험 때만 잠깐 한 줄 넣었다 뺀다, 4번 6-c).

## 2. `requestCards` 초안

```js
  // 카드 요청: { kind: 'ok', cards } 또는 { kind: 'source' / 'network' / 'service' }
  // Request cards: returns { kind: 'ok', cards } or a failure kind
  async function requestCards(text){
    // 0. 보내기 전에 인터넷이 꺼져 있으면 보내지 않음 / Offline: don't send
    if (!navigator.onLine) return { kind: 'network' };

    const url = window.APP_CONFIG && window.APP_CONFIG.CARD_API_URL;
    if (!url) {
      console.warn('[Flip] NO_URL'); // config.js를 못 읽음 / config.js missing
      return { kind: 'service' };
    }

    // 1. 60초가 지나면 요청을 끊음 / Abort after 60s
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), LOAD_TIMEOUT_MS);
    let res = null;
    try {
      // text/plain: 브라우저 사전 요청(CORS preflight)을 피함 (22 7번) / Avoids CORS preflight
      res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({ text }),
        signal: controller.signal
      });
      const data = await res.json();
      // 4. Apps Script가 실패라고 알려 줌 → 서비스 문제 / Server said not ok
      if (!data || data.ok !== true) {
        console.warn('[Flip]', data && data.reason, data && data.status);
        return { kind: 'service' };
      }
      // 5·6~9. 목록인지·장수·형식·문장 수는 checkCards가 본다 / checkCards does the rest
      return { kind: 'ok', cards: data.cards };
    } catch (err) {
      // 1. 60초 초과 / Timed out
      if (controller.signal.aborted) {
        console.warn('[Flip] TIMEOUT');
        return { kind: 'service' };
      }
      // 2. 응답을 못 받음: 인터넷이 꺼졌을 때만 인터넷 문구 / No response: network only if offline
      if (!res) {
        console.warn('[Flip] FETCH_FAILED');
        return { kind: navigator.onLine ? 'service' : 'network' };
      }
      // 3. 응답이 JSON이 아님 (예: Apps Script 오류 페이지) / Response not JSON
      console.warn('[Flip] BAD_JSON', res.status);
      return { kind: 'service' };
    } finally {
      clearTimeout(timer); // 먼저 끝나면 타이머 끄기 / Stop timer once done
    }
  }
```

- **먼저 온 것 하나만 처리**: 60초가 되면 `abort()`로 `fetch`가 끊기고 `catch`로 한 번만 온다. 결과가 먼저 오면 `finally`에서 타이머를 끈다. 그래서 실패 안내가 두 번 뜨지 않는다.
- 콘솔에는 짧은 코드(`TIMEOUT`, `FETCH_FAILED`, `BAD_JSON`, `KEY` 등)와 상태 숫자만 남긴다. 원문·카드는 남기지 않는다.

## 3. 클릭 처리기 안전망

```js
    showScreen('loading');
    try {
      const result = await requestCards(sourceInput.value);
      handleResult(result);
    } catch (err) {
      // 예상 못 한 오류도 로딩에 갇히지 않게 / Never stay stuck on loading
      console.warn('[Flip] UNEXPECTED');
      showFail('service');
    }
```

## 4. 확인 체크리스트 (PRD 완료 조건 번호)

먼저 **PC 브라우저**에서 `my-feature.html`을 열어 T03으로 1번 성공을 본 뒤, 커밋·푸시하고 휴대폰(브랜치 주소)에서 확인한다.

| 조건 | 해 보기 | 통과 |
|---|---|---|
| CORS | PC 개발자 도구(F12) → Network 탭에서 [카드 만들기] | `OPTIONS` 요청이 없고, 카드 요청이 성공 |
| 6-b | T03 원문 → [카드 만들기] | 결과까지 로딩 화면, 그 뒤 "카드 N장 받음 (임시)" |
| 2-3 | [카드 만들기] 빠르게 두 번 | Apps Script "실행" 기록에 1번만 |
| 7-c | 비행기 모드 켜고 [카드 만들기] | "인터넷 연결을 확인한 뒤 다시 시도해주세요" |
| 7-b 구분 | `config.js` 주소 끝 한 글자를 바꿔 시험 (와이파이 켠 채, 시험 후 되돌림) | "인터넷" 문구가 아니라 "잠시 후 다시 시도해주세요" |
| 7-d | 스크립트 속성 키 끝에 `x` 더하고 시험 → 지우기 (22 4번 ⑤) | "잠시 후 다시 시도해주세요" + 콘솔·실행 기록에 `KEY` |
| 6-c | `card-api.gs` `doPost` 첫 줄에 `Utilities.sleep(70000);` → 새 버전 배포 → 시험 → 줄 빼고 다시 배포 | 60초쯤 로딩이 사라지고 "잠시 후 다시 시도해주세요", 콘솔 `TIMEOUT` |
| 7-a | 위 실패 안내마다 [확인] | 원문 그대로, [카드 만들기] 다시 누를 수 있음 |
| 가짜 0줄 | `git grep -i fake -- 202610-my-service/my-feature.html` | 0줄 |

- 7-b 구분·6-c 시험은 **휴대폰에서 하려면 바뀐 파일을 푸시해야** 한다 → PC에서만 확인하고 되돌리는 것을 추천 (주소를 틀린 채로 커밋하지 않게).
- 6-c 시험 중 `Utilities.sleep` 줄이 들어간 채로 두면 모든 요청이 실패한다. 시험 끝나면 꼭 빼고 "새 버전"으로 다시 배포.

## 5. 바뀌는 파일과 커밋

- `202610-my-service/my-feature.html` — 연결, 60초, 안전망, 가짜 삭제
- `drafts/fake-responses.md` — 지운 가짜 장치 보관 (drafts는 아직 커밋 안 함)
- 커밋 제안: `feat: 카드 생성 Apps Script 연결 (60초 제한, 인터넷 끊김 구분, 가짜 장치 삭제)`
- 커밋 전: `git grep -nE "AIza[0-9A-Za-z_-]{20,}|AQ\.[0-9A-Za-z_./+-]{10,}"` 0줄

## 6. 결과 (2026-10-27)

- 코드: 커밋 c94b7c8 (`my-feature.html`). reviewer 검토 `drafts/25-review-s2-4-code.md` — 꼭 고칠 것 0개, 통과.
- 확인: A-1·A-2, B-1~B-5, C-1·C-2 모두 통과 (admin, Android Chrome). C-2 뒤 서버 정상 복구도 확인(빈 글 요청 1.7초 BAD_REQUEST).
- **새로 발견: `BAD_RESPONSE`가 가끔 남** (S2-4 연결 문제는 아님, 화면은 계획대로 "잠시 후…")
  - 앱(시크릿 창) 여러 번 중 2번, PC에서 웹 앱 직접 10번 중 1번, 편집기 `testT03` 10번 중 0번, 진단 배포 후 웹 앱 20번 중 0번
  - 웹 앱 실행은 Apps Script "실행" 목록에서 `console.log` 기록이 보이지 않음 (익명 사용자 실행이라 추정)
  - 그래서 `card-api.gs`에 `[DIAG-S2-4]` 진단을 넣고 "새 버전" 배포: 실패 응답에만 `why`(NO_BODY / NO_CANDIDATE / NOT_JSON / NOT_JSON_FENCE / ARRAY / NO_CARDS:칸이름 / TYPE_…)·`len`·`finish`·`block`·`outTokens`를 붙임. 원문·카드는 넣지 않음
  - 앱 콘솔은 `reason`·`status`만 찍으므로 `why`는 **PC에서 웹 앱으로 직접 보낼 때** 보인다

### 다음 할 일 (S2-5 전)
1. S2-5 테스트 원문(T01~T03)을 웹 앱으로 여러 번 보내며 `why`를 모은다
2. 원인에 맞게 고친다: ARRAY·NO_CARDS면 `responseSchema`(답 모양 정해 주기), NOT_JSON·MAX_TOKENS면 답 길이 설정 확인, NO_CANDIDATE면 차단 사유 확인
3. 고칠 때 `[DIAG-S2-4]` 덩어리를 지우고 "새 버전" 배포 → `git grep -n DIAG -- 202610-my-service/card-api.gs` 0줄
4. 끝까지 한 번도 안 잡히면: 고치지 않고 S2-6(시간·실패율 재기)에서 다시 본다

### 1번 결과 (2026-10-28, PC에서 웹 앱 직접)
- T01·T02·T03 각 11번(시험 1 + 본 10) = **33번 모두 성공, `BAD_RESPONSE` 0번**. 진단 배포 뒤 누적 53번 중 0번
- → 4번대로 **고치지 않고 S2-6에서 다시 본다.** `[DIAG-S2-4]`는 그때까지 둔다
- 카드 장수: T01 10장(11번 모두), T02 8장(1번만 5장, 시험 때 9장), T03 9~13장
- 걸린 시간: 대부분 3~12초. 느린 것 T01 31.2초·T02 22.5초(첫 요청), T03 17초대 2번 → 60초 제한 안이지만 S2-6에서 잰다
- F-1 원문(`docs/test-inputs/05-fail-meaningless.md`) 5번: 모두 `{"ok":true,"cards":[]}` → 앱에서 "원문 문제" 안내가 나와야 한다 (휴대폰 확인은 S2-5)

### S2-5 채점 (2026-10-28)
- **주의: 이날 1차 채점과 프롬프트 수정 직후 1회차는 무효.** PC에서 원문을 `python … sys.stdin.read()`로 읽어 Windows 기본(cp949)으로 깨진 한글이 Gemini에 갔다. 그래서 보였던 "T02 0장", "acquire 획득하다", "망각 효과"는 근거가 아니다. 원문은 반드시 `open(…, encoding='utf-8')`로 읽는다 (`docs/test-results/raw/collect.py`). 위 1번 결과(33번)는 UTF-8로 읽어서 유효
- 프롬프트 S2-5판(규칙 1·2·6·7·8 고침) 배포 → UTF-8로 23번: T01 3/3, T02 10/10(9장), T03 5/5, F-1 5/5 모두 0장. 3-5 위반 0개, 함정 0개. 채점표 `docs/test-results/2026-10-28-0[1235]-채점.md`
- **남은 문제: T03 5번 중 1번, 카드 칸 이름이 `"front>"`로 옴** → 앱이 stack 전체를 "잠시 후…"로 처리. 고칠 방법: `responseSchema` (위 2항)
- `responseSchema` 추가·배포 → 25번(T03 16, T01·T02·F-1 각 3): 모두 성공, 칸 이름 문제 0번, 앱 검사에 걸리는 카드 0장. 3.5 Flash-Lite가 설정을 받아들임
- `[DIAG-S2-4]`는 아직 그대로 (S2-6에서 실패율 잰 뒤 지움)
