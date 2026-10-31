# 코드 검토: S2-0 · S2-1 (커밋 전)

- 작성: 2026-10-24 / 검토자: 기술 검토 담당 (reviewer)
- 기준:
  - `drafts/13-s2-plan-s2-0-s2-1.md` v1.2
  - PRD v1.5 기능 6·7 (6-b, 7-a, 7-b)
  - `CLAUDE.md` 규칙
- 본 것:
  - `git status`, `git diff 202610-my-service/my-feature.html`
  - 새 파일 4개: `D:\2027_1\.gitignore`, `202610-my-service\.gitignore`, `config.js`, `card-api.gs`
- 이렇게 확인했다 (브라우저 없이):
  - `my-feature.html`의 `<script>`만 뽑아 `node --check` → **문법 오류 없음**
  - `git check-ignore -v`로 무시 규칙이 실제로 걸리는지 확인
  - 옛 저장 시험 주소와 `AIza`를 작업 폴더 전체에서 검색
  - 코드를 한 줄씩 읽으며 성공·실패·두 번 누름·길이 막힘 경로를 따라갔다 (아래 3번)
- **실제 휴대폰 확인은 아직 아무도 안 했다.** 13 2-3번 체크리스트는 admin이 휴대폰에서 해야 한다.

---

## 요약

| 꼭 고칠 것 | 고치면 좋은 것 | 괜찮은 점 |
|---|---|---|
| **0** | 6 | 9 |

- 커밋을 막을 문제는 없다.
- 키 문자열 0개, 옛 저장 시험 주소 0개, `config.js`는 `CARD_API_URL` 한 줄이다.
- 문구 3종은 PRD와 글자까지 같고, `resetStart`도 들어 있다.
- 검토자 실수 1개를 바로잡는다:
  - 14번 메모 K-1에서 "주소 `/macros/s/` 뒤 앞 6글자로 grep"을 제안했다. 그런데 dev가 짚은 대로 **Apps Script 배포 주소는 모두 `AKfycb`로 시작한다.** 6글자로는 옛 주소와 새 주소를 구분할 수 없다.
  - dev가 10글자로 점검한 것이 맞다.
  - 13의 해당 줄도 "10글자 이상"으로 고쳐 두면 좋다.

---

## 1. S2-0 파일 점검

| 점검 | 결과 | 근거 |
|---|---|---|
| `config.js`에 `CARD_API_URL` 한 줄만 | **통과** | 주석 3줄 + `window.APP_CONFIG = { CARD_API_URL: "…/exec" }` 한 줄. `WEB_APP_URL`은 없음 |
| 옛 저장 시험 주소가 없음 | **통과** | 옛 주소의 `/s/` 뒤 10글자로 `D:\2027_1` 전체(`.git` 제외)를 검색 → 0개. 새 주소와 옛 주소는 `AKfycb` 뒤부터 다르다 |
| 옛 주소가 Git 기록에 없음 | **통과** | `git log --all -- 202610-my-service/config.js` → 0줄 (14 재확인 때와 같음) |
| 키 문자열 `AIza` 0개 | **통과** | 코드 파일 0개. PRD 2곳(360·396줄)에 나오는 것은 "`AIza`를 검색하라"는 **설명 글**이라 문제없다 |
| 루트 `.gitignore`: `.env` | **통과** | 첫 규칙 |
| 루트 `.gitignore`: 개인 폴더 | **통과** | `.obsidian/`, `Audiophile/`, `Career/`, `Chinese/`, `Clippings/`, `Memos/`, `Z-warrior/`, `NRF_2026_2.md`. `git check-ignore`로 실제로 걸리는 것을 확인했다 |
| 꼭 필요한 파일이 빠지지 않았나 | **통과** | `docs/`(테스트 원문 `docs/test-inputs/`)는 무시 목록에 없다 → 맞다. `202610-my-service/` 아래 파일도 하나도 막히지 않는다 |
| `202610-my-service\.gitignore` | **통과** | `config.js` 줄이 빠지고 주석 2줄만 남았다. 주석이 "키·저장 시험 주소는 이 폴더에 넣지 않는다"로 바뀌어 의도가 분명하다 |
| `card-api.gs` 사본 | **통과 (확인 1개 남음)** | 키를 읽지 않고, 외부 호출도 없다. `doGet`·`doPost` 모두 `NOT_READY`다. "S2-3에서 `doGet`을 지운다"는 주석도 있다(14 G-7 반영). dev 말대로 **배포된 코드와 같은지는 아직 확인 안 됨** → G-1 |

## 2. S2-1 코드 점검 (`my-feature.html`)

| 점검 | 결과 | 근거 (줄은 지금 파일 기준) |
|---|---|---|
| 고정 문구 3종이 글자 그대로 | **통과** | `MSG_FAIL.source/network/service`가 PRD 기능 7 표와 글자 하나까지 같다 |
| `resetStart`로 `isStarted`·버튼 잠금 되돌리기 | **통과** | `showFail()` 안에서 `resetStart()`를 부른다 → `isStarted = false; submitBtn.disabled = false` |
| 7-a 원문 유지 | **통과** | 실패 경로 어디에서도 `sourceInput.value`를 바꾸지 않는다. [확인]은 `failLayer.hidden = true`와 포커스 이동만 한다 |
| 6-b 로딩이 결과 때까지 보임 | **통과** | `showScreen('loading')` 다음 `await requestCards()`. 결과가 오기 전에는 화면을 바꾸지 않는다 |
| 7-b 같은 종류 = 같은 문구 | **통과** | 문구가 상수 하나에서만 나온다. 문구를 조합하지 않는다 |
| 2-3 두 번 누름 막기 | **통과** | `await` **전에** `isStarted = true`와 `disabled = true`를 한다. 그래서 두 번째 탭은 첫 줄 `if (isStarted) return`에서 막힌다 |
| 1단계 길이 검사 | **깨지지 않음** | `isEmpty`·`isKoreanMain`·`measure`·`checkLength`와 입력 시 안내 숨기기는 diff에서 바뀌지 않았다. 길이에 걸리면 `isStarted`를 켜기 전에 `return`하는 순서도 그대로다 |
| `:root` 변수만 사용 | **통과** | 새 색 `--dim`을 `:root`에 더했다. 새 CSS 규칙은 모두 `var(--…)`를 쓴다 |
| `100dvh`·safe-area | **통과** | `.screen` 규칙은 바뀌지 않았다. `.fail-layer`에 `env(safe-area-inset-top/bottom)` 여백이 있다 |
| 한·영 주석 | **통과** | 새 주석이 모두 "한국어 / English" 형식이다 |
| `[hidden]`과 `display` 충돌 | **통과** | `.fail-layer[hidden]{ display:none; }`이 있다. `.screen[hidden]`과 같은 방식이다 |
| FAKE 장치가 한곳에 | **통과** | `requestCards()` 안 `[FAKE-S2-1] 시작`~`끝` 한 덩어리뿐이다. `FAKE` 검색 결과는 2줄(시작·끝 표시)이다. S2-4에서 이 함수 몸통만 바꾸면 된다 |
| 고지 문구 위치·내용 | **통과** | `#emptyHint` 아래, `#submitBtn` 바로 위. 문구는 13·02 후보 A(Google 검토자 / Google의 AI)와 같다. 13px, 투명도 .85로 13 2-1 기준(0.85 이상)에 맞다. "PRD 반영 전 임시" 주석도 있다 |
| 실패 안내 접근성 | **통과** | `role="alertdialog"`, `aria-labelledby="failText"`. 열릴 때 `failOkBtn.focus()`, 닫을 때 `submitBtn.focus()` (키보드가 올라오지 않음). 14 G-6 반영 |

## 3. 브라우저 없이 경로 따라가기

| 경로 | 따라간 결과 |
|---|---|
| 빈 입력 / 9자 / 5,001자 | `checkLength`가 문구를 돌려준다 → `emptyHint`가 보이고 `return`. `isStarted`는 false 그대로, 로딩으로 넘어가지 않는다 ✔ |
| `?fake=fail-source` | 로딩(2초) → `{kind:'source'}` → `showFail('source')`. 문구가 바뀌고 → 입력 화면 → 실패 층이 보이고 → 잠금 해제 → [확인] 포커스. [확인]을 누르면 층이 닫히고 원문은 그대로. 다시 누르면 다시 로딩 ✔ |
| `fail-network` / `fail-service` | 위와 같고 문구만 다르다 ✔ |
| `?fake=slow` | 8초 동안 로딩 화면 ✔ (6-b) |
| 파라미터 없음 / `?fake=ok` | 2초 뒤 로딩 화면 글자가 "카드 3장 받음 (임시)"로 바뀐다. `isStarted`는 true로 남는다(성공 뒤 화면은 3단계에서 만듦) ✔ — 다만 G-2 참고 |
| 로딩 중 빠르게 두 번 탭 | 두 번째 탭은 `isStarted`에서 막힌다. 그리고 로딩 화면에는 버튼이 없다 ✔ |
| `?fake=오타` | `'ok'`로 처리된다(가짜 성공). 시험 장치라 괜찮지만, 오타를 낸 줄 모르고 "실패가 안 뜬다"고 착각할 수 있다 → G-3 |

---

## [고치면 좋은 것]

**G-1. `card-api.gs` 사본과 배포된 코드가 같은지 확인하기**
- dev 말대로 이 사본은 다시 쓴 것이다.
- 가장 쉬운 방법: admin이 Apps Script 편집기 내용을 이 사본으로 **통째로 바꿔 붙여 넣고** "배포 관리 → 새 버전"으로 배포한다. 그러면 처음부터 같아진다.
- 확인은 13 0-3 그대로 한다: 휴대폰 주소창에서 `{"ok":false,"reason":"NOT_READY"}`가 보이면 된다.

**G-2. 가짜 성공 뒤에도 원이 계속 돈다**
- `handleResult`의 `ok` 경로는 글자만 "카드 3장 받음 (임시)"로 바꾸고, `.loading-spinner`는 그대로 돈다. 그래서 "아직 만드는 중"처럼 보인다.
- 임시 화면이라 큰 문제는 아니다. 하지만 휴대폰 확인 때 admin이 헷갈릴 수 있다.
- 한 줄로 해결된다: 성공 시 원을 숨긴다(예: `loadingScreen.querySelector('.loading-spinner').hidden = true`, 또는 원에 `id`를 주고 숨김).
- 원을 다시 쓸 일은 3단계에서 생기므로, 이 줄도 `[FAKE-S2-1]` 근처 임시 표시와 함께 S2-4에서 정리한다.

**G-3. 알 수 없는 `?fake=` 값은 성공으로 처리된다**
- `get('fake') || 'ok'` 다음에 오타 검사가 없다.
- 시험 장치라 KISS 기준으로 지금도 괜찮다. 다만 13 2-2 표 아래에 "철자가 틀리면 가짜 성공이 나온다"를 한 줄 적어 두면 휴대폰 확인 때 덜 헷갈린다.

**G-4. (S2-4로 넘길 메모) `requestCards`가 오류를 던지면 로딩에서 멈춘다**
- 지금 클릭 처리기는 `await requestCards()`를 `try/catch` 없이 부른다.
- S2-1의 가짜 코드는 오류를 던지지 않으니 지금은 문제없다.
- 하지만 S2-4에서 진짜 `fetch`·`res.json()`으로 바꿀 때 예외가 나면 다음 일이 생긴다.
  - `handleResult`가 불리지 않는다.
  - 로딩 화면에 영원히 머문다.
  - `isStarted`가 true로 남는다.
- S2-4 계획에 두 가지를 적어 두기를 권한다.
  - "`requestCards` 안에서 모든 예외를 잡아 `{kind:'service'}`(또는 02 6-1번 표대로 `network`)로 돌려준다."
  - "클릭 처리기에도 마지막 안전망 `try/catch` → `showFail('service')`."

**G-5. `.claude/settings.local.json`을 루트 `.gitignore`에 넣을지 정하기**
- `D:\2027_1\.claude\settings.local.json`이 "추적 안 됨"으로 남아 있다. 이 파일은 이 PC의 Claude Code 권한 설정(허용한 명령 목록 등)이다.
- 공개 저장소에 올릴 이유가 없다. 이름에 `local`이 붙은 것도 "이 컴퓨터 전용"이라는 뜻이다.
- 같은 폴더의 `.claude/skills/flip-card-check`(팀 스킬)는 올릴 수도 있으니, **파일 하나만** 무시하기를 권한다: `.claude/settings.local.json`.
- `My_Real_AI_Service/`, `day20-practice/`, `day22-practice-v1/`도 추적 안 됨이다. 수업 실습이라 올릴지 말지는 admin이 정할 일이다. 지금은 파일 이름을 하나씩 `git add`하므로 실수로 올라갈 위험은 낮다.

**G-6. 실패 층 작은 접근성 보완 (선택)**
- `aria-modal="true"`를 더하면, 화면 읽기 기능이 뒤의 입력 화면을 읽지 않는다.
- 회전 애니메이션은 `@media (prefers-reduced-motion: reduce)`에서 멈추게 할 수 있다. 움직임을 줄여 달라고 설정한 사용자를 위한 배려다.
- 둘 다 1줄짜리다. YAGNI로 미뤄도 된다.

---

## [괜찮은 점]

- **S2-0 보안 점검을 모두 통과했다.**
  - 키 0개, 옛 주소 0개(작업 폴더와 Git 기록 모두), `config.js`는 새 주소 한 줄, `docs/`는 막히지 않음.
  - 14 K-1에서 걱정한 "옛 주소가 커밋에 섞이는 일"이 생길 수 없는 상태다.
- **6글자 grep 문제를 dev가 스스로 찾아 10글자로 고쳐 점검했다.** 검토 제안을 그대로 따르지 않고 실제로 확인한 좋은 사례다.
- **문구 3종이 상수 하나에서만 나온다.** 7-b("같은 종류 = 같은 문구")가 구조적으로 보장된다.
- **`resetStart`가 실패 경로 한 곳(`showFail`)에만 있다.** 앞으로 실패 종류가 늘어도 되돌리기를 빠뜨릴 일이 없다.
- **두 번 누름 막기가 `await`보다 앞에 있다.** 비동기로 바꾸면서 흔히 생기는 "기다리는 사이 두 번째 탭이 들어오는" 버그가 없다.
- **1단계 코드는 한 줄도 바뀌지 않았다.** 길이 검사 함수들과 그 순서가 그대로라 3-a~3-g가 깨질 이유가 없다.
- **FAKE 장치가 함수 하나 안에 시작·끝 표시로 모여 있다.** S2-4에서 함수 몸통만 바꾸고 `FAKE` 0줄을 확인하면 끝난다.
- **스타일 규칙을 지켰다.** `:root` 변수(`--dim` 추가), `100dvh`·safe-area 유지, 실패 층에도 safe-area, `[hidden]` 처리, 한·영 주석, 새 라이브러리 없음.
- **고지 문구가 13·02 결정과 같고, 위치와 "PRD 반영 전 임시" 표시가 정확하다.**

---

## 커밋 때 참고 (커밋은 하지 않았다)

- `git status`에는 팀장이 고친 `CLAUDE.md`와 PRD 수정도 함께 보인다. S2-0·S2-1 커밋에는 **dev가 바꾼 5개 파일만** 이름으로 지정해 넣는다.
- 13 1-2-1 점검 순서를 따른다: `git diff --cached -- 202610-my-service/config.js`, `AIza` 검색, 옛 주소 10글자 검색.
- 줄바꿈 경고(`LF will be replaced by CRLF`)는 Windows Git 설정 때문이고 동작에는 영향이 없다.
- 13의 커밋 메시지 제안(S2-0 `chore:`, S2-1 `feat:`)대로 **두 커밋으로 나누는 것**을 권한다. 문제가 생겼을 때 어느 단계 탓인지 찾기 쉽다.
