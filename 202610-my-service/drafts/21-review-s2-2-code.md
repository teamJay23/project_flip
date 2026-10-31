# 코드 검토: S2-2 카드 검사 함수 (커밋 전)

- 작성: 2026-10-24 / 검토자: 기술 검토 담당 (reviewer)
- 기준:
  - `drafts/16-s2-plan-s2-2.md` v1.1 (admin 승인) 3-1·3-2·3-3번
  - PRD v1.5 기능 4·5·7 (4-a, 5-a, 5-b, 7-a, 7-b)
  - `CLAUDE.md` 규칙, `drafts/15-review-s2-0-s2-1-code.md`와 같은 점검
- 본 것: `git diff -- 202610-my-service/my-feature.html`, `git status`
- 이렇게 확인했다 (브라우저 없이):
  - `<script>`만 뽑아 `node --check` → **문법 오류 없음**
  - dev와 **따로** 시험 코드를 써서(임시 폴더, 저장소에 남기지 않음) 실제 파일의 `checkCards`·`FAKE_S2_2`를 불러 **21경우**를 돌렸다 (아래 3번)
  - `AIza`를 `.html`·`.js`·`.gs` 전체에서 검색 → **0개**
- **실제 휴대폰 확인은 아직 아무도 안 했다.** 16번 4번 체크리스트는 admin 몫이다.

---

## 요약

| 꼭 고칠 것 | 고치면 좋은 것 | 괜찮은 점 |
|---|---|---|
| **0** | 2 | 10 |

- 커밋을 막을 문제는 없다. 코드가 16번 v1.1 계획과 맞고, 계획과 다른 점 1개(`hasOwnProperty`)도 타당하다.
- 키 0개, 문구 3종은 PRD와 글자 그대로이고 이번 diff에서 바뀌지 않았다. 기존 기능도 그대로다.

---

## 1. 계획과 맞는지 (줄은 지금 `my-feature.html` 기준)

| 계획 (16 v1.1) | 코드 | 결과 |
|---|---|---|
| 3-1 `MAX_CARDS`·`MAX_SENTENCES`를 길이 상수 아래 | 191~193줄, `MAX_WORDS` 바로 아래 | **통과** |
| 1-3 `countSentences` = `sheet-test.html` 113줄과 같은 정규식 | 255~258줄 `/[.?!。]+/`, 한계 주석 포함 | **통과** |
| 2-2 `isGoodFace`: `typeof` 먼저, `isEmpty` 다시 쓰기 | 260~264줄 | **통과** |
| 1-1 순서: 배열 → 0장 → 20장 자르기 → 형식 전부 → 문장 수 전부 | `checkCards` 270~300줄. 반복문 두 개, 추천 (a) 그대로 | **통과** |
| 2-2 개발자 기록: 이유 코드·카드 번호만 | `NOT_ARRAY`, `BAD_CARD n`. 카드 내용·원문 없음. 원문 문제는 기록 안 함 | **통과** |
| 3-1 `handleResult` 맨 앞 한 줄, `checked`로 처리 | 358~370줄. 임시 표시도 `checked.cards`를 쓴다(22장이 아니라 20장이 보임) | **통과** |
| 3-1 임시 표시 "장수 · 처음 · 끝", `textContent` | 364~365줄 | **통과** |
| 3-1 `.loading-text`에 `text-align:center`·`overflow-wrap:anywhere` | 98~99줄, 한·영 주석 | **통과** |
| 3-2 `[FAKE-S2-2]` 덩어리를 `requestCards` 바로 위에 | 372~394줄, 시작·끝 표시 있음 | **통과** |
| 3-2 `[FAKE-S2-1]` 안 연결 한 줄 | 408줄 | **통과** |
| 3-2 가짜 9종, 2번째 카드를 망가뜨림, 4문장 = `첫째. 둘째. 셋째. 넷째.` | 383~393줄, `FOUR_SENTENCES` 상수 | **통과** |
| `requestCards`는 검사하지 않음 | 검사는 `handleResult`에서만 | **통과** |

**계획과 다른 점: 가짜 표 값이 "목록"이 아니라 "목록을 만드는 함수"다** (`() => fakeCards(3)` 등)
- 좋은 선택이다. 부를 때마다 **새 목록**이 나오므로(시험으로 확인: 두 번 부르면 다른 목록), 한 가짜가 다른 가짜를 망가뜨릴 일이 없다. 계획의 뜻("이름 → 가짜 결과")은 그대로다.

**계획과 다른 점: `FAKE_S2_2.hasOwnProperty(fake)`** (dev가 알린 것)
- 타당하다. `?fake=constructor`가 이제 서비스 문제가 아니라 다른 오타처럼 **기본 가짜 성공 3장**으로 간다(시험: `hasOwnProperty('constructor')` → false). 16번 3-2 "철자가 틀리면 가짜 성공 3장" 규칙과 같아져서 오히려 일관된다.
- `Object.hasOwn`을 피한 이유(iOS 15.4 미만)도 맞다. 어차피 S2-4에서 지우는 줄이다.

## 2. 15번과 같은 점검

| 점검 | 결과 | 근거 |
|---|---|---|
| 키 문자열 `AIza` 0개 | **통과** | `.html`·`.js`·`.gs` 검색 0줄 |
| 고정 문구 3종이 글자 그대로 | **통과** | `MSG_FAIL`(200~204줄)을 시험에서 꺼내 PRD 기능 7 표(179~181줄)와 비교: 3개 모두 같다. diff에서 바뀌지 않았다 |
| 실패 → `showFail` → `resetStart` | **통과** | `checkCards` 실패도 `showFail(checked.kind)`로 같은 길을 간다. 7-a 원문 유지, 다시 누르기 그대로 |
| 7-b 같은 종류 = 같은 문구 | **통과** | `checkCards`는 `'source'`/`'service'`만 돌려주고 문구를 만들지 않는다 |
| 두 번 누름 막기 | **깨지지 않음** | 클릭 처리기는 diff에서 바뀌지 않았다. `isStarted = true`가 `await`보다 앞 |
| 1단계 길이 검사 | **깨지지 않음** | `isEmpty`·`isKoreanMain`·`measure`·`checkLength`는 바뀌지 않았다. `isEmpty`는 읽기만 한다 |
| `:root` 변수·`100dvh`·safe-area | **통과** | 새 색 없음. `.screen`·`.fail-layer` 규칙은 바뀌지 않았다 |
| 한·영 주석 | **통과** | 새 주석이 모두 "한국어 / English" |
| 바뀐 파일 | **통과** | `202610-my-service` 안에서 dev가 바꾼 것은 `my-feature.html` 하나. (`git status`의 PRD·`CLAUDE.md` 수정은 팀장 몫이라 이 커밋에 넣지 않는다) |
| PRD "만들지 않는 것" | **걸리는 것 없음** | 잘랐다는 안내·진행도·라운드 표시 없음 |

## 3. 검토자가 따로 돌린 시험 (실제 파일의 함수를 불러서)

| 경우 | 기대 (16번) | 결과 |
|---|---|---|
| `cards-0` | source | source ✔ |
| `cards-22` | ok 20장, 처음 1·끝 20 | ok 20, 처음 가짜 질문 1·끝 가짜 질문 20 ✔ |
| `cards-22-bad-tail` | ok 20장 | ok 20 ✔ |
| `sentences-3` | ok 3장 | ok 3 ✔ |
| `sentences-4` | source | source ✔ |
| `empty-front` / `blank-back` / `number-front` | service | service, `BAD_CARD 2` ✔ (셋 다) |
| `not-array` | service | service, `NOT_ARRAY` ✔ |
| node ① 4문장 + 빈 앞면 | service | service, `BAD_CARD 3` ✔ (추천 (a)) |
| node ② `null` 카드 | service | service, `BAD_CARD 2` ✔ |
| node ③ (가) 뒷면 숫자 / (나) 앞면 4문장 | service / source | service / source ✔ |
| (추가) 정확히 20장 | ok 20 | ok 20 ✔ |
| (추가) 21번째만 `null` 앞면 | ok 20 (잘려 나감) | ok 20 ✔ |
| (추가) **20번째** 뒷면 빈칸 (22장 중) | service (경계 안쪽) | service, `BAD_CARD 20` ✔ |
| (추가) `cards`가 `undefined` | service | service, `NOT_ARRAY` ✔ |
| (추가) 카드가 글자 `'abc'` | service, 멈추지 않음 | service, `BAD_CARD 1` ✔ |
| (추가) 원래 목록을 바꾸지 않음 | 22장 그대로 | 22 ✔ |

- 20번째(남김)와 21번째(버림) 경계를 양쪽에서 확인했다. `slice(0, 20)`의 한 칸 어긋남 실수는 없다.

---

## [고치면 좋은 것]

**G-1. `requestCards` 안 주석에 S2-2 이름도 적기**
- 400줄 주석은 아직 `?fake=ok|slow|fail-source|fail-network|fail-service`(S2-1 것)만 적혀 있다.
- 끝에 "· S2-2 이름은 위 `FAKE_S2_2` 참고 / See FAKE_S2_2 for S2-2 names" 정도를 덧붙이면, 이 줄만 보고 "가짜가 5개뿐"이라고 오해하지 않는다. 한 줄이고 S2-4에서 함께 지워진다.

**G-2. 커밋 때 줄바꿈 경고는 무시해도 된다 (참고)**
- `git diff` 때 `LF will be replaced by CRLF` 경고가 나온다. 15번 때와 같은 Windows Git 설정 탓이라 동작과 상관없다.

---

## [괜찮은 점]

- **계획 v1.1을 빠짐없이 따랐다.** 함수 이름·자리·순서·주석이 3-1번 표와 같다.
- **검사 순서가 PRD와 같고 경계도 맞다.** 20/21번째, 3/4문장, 빈칸/공백/숫자/`null`/글자 카드 모두 기대대로다.
- **추천 (a)(형식 먼저 전부)가 반복문 두 개로 분명하게 들어갔다.** 둘째 반복문에서는 면이 모두 문자열이라 `countSentences`가 멈출 일이 없다.
- **`checkCards`가 화면을 건드리지 않는다.** 그래서 DOM 없이 함수만 불러 시험할 수 있었다.
- **가짜 값을 함수로 만들어 매번 새 목록을 준다.** 가짜끼리 서로 영향을 주지 않는다.
- **`hasOwnProperty`로 이상한 이름도 "오타 = 가짜 성공" 규칙에 맞췄다.** 오래된 iOS도 고려했다.
- **개발자 기록에 카드 내용·원문이 없다.** 공개 저장소·무료 등급 상황에 맞다.
- **임시 표시를 `textContent`로 넣고 `overflow-wrap`까지 넣었다.** S2-4 진짜 결과에도 안전하다.
- **기존 코드는 `handleResult` 말고 한 줄도 바뀌지 않았다.** 두 번 누름 막기, `resetStart`, 1단계 길이 검사, 안전 영역이 그대로다.
- **지우기 쉽다.** S2-4에서 지울 것은 `[FAKE-S2-2]` 덩어리(372~394줄)와 `[FAKE-S2-1]` 덩어리뿐이다. `FOUR_SENTENCES`·`fakeCards`도 덩어리 안에 있다.

---

## 커밋 때 참고 (커밋은 하지 않았다)

- `git add 202610-my-service/my-feature.html` 하나만 이름으로 지정한다.
- 커밋 전에 다시 `AIza` 검색을 한다(지금 0줄).
- 16번 5번 제안 메시지 그대로 쓰면 된다: `feat: 카드 검사 함수 추가 (0장·20장 자르기·빈 면·3문장 검사, 가짜 결과로 확인)`
