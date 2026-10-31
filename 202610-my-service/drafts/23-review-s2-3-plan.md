# 계획 검토: S2-3 Apps Script에서 Gemini 호출 (22번 초안 v1)

- 작성: 2026-10-27 / 검토자: 기술 검토 담당 (reviewer)
- 본 것: `drafts/22-s2-plan-s2-3.md` v1, `card-api.gs`(지금 NOT_READY), `drafts/02-ai-card-generation-plan.md` 4·5·5-1·7번, `drafts/13-s2-plan-s2-0-s2-1.md` 1-6·0-3, `drafts/08-session-db-plan.md` 3-6, `my-feature.html` 길이 검사(207~253줄), PRD v1.5 기준 `CLAUDE.md`
- 이렇게 확인했다:
  - 공식 문서를 dev와 **따로** 다시 읽었다(2026-10-27). 페이지를 내려받아 글자 그대로 찾아봤다 (2번 표, 출처 URL 포함).
  - 22번 2-1 코드 블록을 그대로 뽑아 **가짜 Apps Script 서비스**(UrlFetchApp·PropertiesService·ContentService 흉내)로 node에서 **24경우**를 돌렸다. 임시 폴더에서만 했고 저장소에는 파일을 만들지 않았다 (3번).
  - 코드 안 `T03_TEXT`가 `docs/test-inputs/03-article.md` 안에 **한 글자도 다르지 않게** 들어 있는지 비교했다 → 같음.
- **실제 Gemini 호출은 아무도 안 했다.** 실제 상태 코드는 22번 4번 순서대로 admin이 확인한다.

---

## 요약

| 꼭 고칠 것 | 고치면 좋은 것 | 괜찮은 점 |
|---|---|---|
| **2** | 6 | 11 |

- 보안: **키·원문이 실행 기록·응답·주소에 남는 길을 찾지 못했다.** 가짜 오류 응답에 "leaked", "not valid" 같은 오류 문장을 넣어 돌려도 기록에 나오지 않았다.
- 코드: 24경우 중 23경우가 계획 표대로 나왔다. 나머지 1경우(오류 `details`가 목록이 아닐 때)는 실제로는 거의 없는 모양이라 [고치면 좋은 것]으로 뒀다.
- [꼭 고칠 것] 2개는 둘 다 **문서 고치기**다. 코드 수정은 아니다.

---

## [꼭 고칠 것]

### K-1. 시험 2가 실패했을 때 "멈추라"는 조건이 404 하나뿐이다 (4번 ④-1)

- 지금 글: `"reason":"OTHER"`, `"status":404`가 보이면 멈추고 dev에게 알린다.
- 문제: 2.5 접근이 막혔을 때 어떤 코드가 오는지는 **공식 문서에 없다.** 404라는 것도 22번 2-2 표에서 dev가 **추측**이라고 적었다. 문제 해결 페이지에는 프로젝트가 막히면 **`403 PERMISSION_DENIED`**("Your project has been denied access", "Free tier unavailable")가 온다고 적혀 있다. 403이나 400이 오면 admin은 무엇을 해야 할지 모른다.
- 고칠 것: ④-1을 "**`reason`이 `OK`가 아니면 무엇이든** 멈추고 기록 줄의 `status`·`errStatus`·`errReason` 세 값만 dev에게 알린다"로 바꾼다. `KEY` 안내 줄은 그대로 둔다. 5번 표 B의 "모델 접근 막힘" 행은 `status` 칸을 비워 둔다(404라고 미리 적지 않는다).

### K-2. 공식 문서 확인 결과 두 칸을 고친다 (1번 ②·⑥, 8번 D-1 표)

dev가 "확인 못 함·추측"으로 적은 것 중 두 가지를 공식 문서에서 찾았다. 둘 다 D-1 결정에 쓰이는 정보라 admin이 보기 전에 고친다.

| 위치 | 지금 | 고칠 내용 | 출처 |
|---|---|---|---|
| 1번 ② 헤더 | generateContent에 헤더가 먹는지는 "**추측**" | **확인함.** "Interactions로 옮기기" 페이지의 generateContent curl 예시가 `models/gemini-2.5-flash-lite:generateContent` 주소에 `-H "x-goog-api-key: $GEMINI_API_KEY"`를 쓴다. (참조 페이지 curl은 아직 `?key=`) | https://ai.google.dev/gemini-api/docs/migrate-to-interactions |
| 1번 ⑥, D-1 (가) 단점 | 3.5 Flash-Lite 기본 thinking "**확인 못 함**" | thinking 안내 표: **`gemini-3.5-flash-lite` 기본 "On (minimal)"**(고를 수 있는 값 minimal·low·medium·high), `gemini-3.8-flash` 기본 "On (medium)". 즉 3.5 Flash-Lite는 생각을 **아주 조금** 한다 → `thinkTokens`가 0이 아닐 수 있다. 끌 수 있는지("minimal"이 완전히 끄는지)는 문서에 없다 | https://ai.google.dev/gemini-api/docs/thinking |

- 덧붙여 1번 ④에 한 줄: 참조 페이지 `totalTokenCount` 설명이 "prompt + tool-use prompt + **thoughts** + response candidates"다. 그래서 `candidatesTokenCount`에는 생각 토큰이 **들어 있지 않고** `thoughtsTokenCount`에 따로 나온다. 5번 표 C에서 "출력 + 생각"을 더해 비용을 계산하면 된다.

---

## [고치면 좋은 것]

### G-1. `MAX_TEXT_CHARS = 20000`이 앱 검사를 통과한 정상 원문을 막을 수 있다 (드문 경우)

- PRD 길이 규칙은 **띄어쓰기·줄바꿈을 빼고** 센다(한글 5,000자). 그런데 서버 상한은 띄어쓰기를 **포함한** 글자 수다.
  - 한글 5,000자 + 보통 띄어쓰기 ≈ 6,000~6,500자 → 괜찮다.
  - 영어 2,000단어 ≈ 단어당 평균 6~7자(띄어쓰기 포함) ≈ 12,000~14,000자 → 괜찮다. 다만 주소(URL)·긴 전문 용어가 많거나, PDF에서 복사해 빈 줄·들여쓰기가 많은 글은 20,000자를 넘을 수 있다.
- 넘으면 사용자는 정상 원문인데 "잠시 후 다시 시도해주세요"를 본다. 다시 눌러도 계속 같다.
- 제안 (둘 중 하나, 추천 ①):
  - ① 상한만 **50,000**으로 올린다. 숫자 하나만 바뀐다. "화면을 거치지 않은 이상한 요청 막기"라는 목적(08 3-6 ④)은 그대로 지킨다.
  - ② 서버도 띄어쓰기를 빼고 센다 (`text.replace(/\s/g, '').length > MAX_TEXT_CHARS`). 한 줄이지만 PRD 규칙을 반쯤 다시 쓰는 셈이라 DRY에 조금 어긋난다.
- 참고 (S2-3 범위 밖, 팀장에게): `my-feature.html`의 `measure()`는 한글도 알파벳도 없는 글(일본어·중국어처럼 띄어쓰기가 없는 글)을 "단어 수"로 센다. 그래서 띄어쓰기 없는 아주 긴 글도 5단어만 넘으면 화면 검사를 통과한다. 이런 글은 서버 상한에 걸려 서비스 문제가 된다. PRD가 한글·영어 규칙만 정했으므로 PRD 질문으로 남길 일이다.

### G-2. `readMeta_`가 예상 밖 오류 모양에서 멈춘다

- `(body.error.details || []).filter(...)`는 `details`가 목록이 아닌 값(예: 객체)이면 예외를 던진다. 시험에서 `doPost`가 끝까지 못 가고 멈췄다. 그러면 HTML은 JSON 대신 Apps Script 오류 페이지를 받는다(S2-4에서 `BAD_JSON`으로 서비스 문제가 되니 사용자 화면은 같다). 기록 줄도 남지 않는다.
- Google 오류 응답은 보통 `details`가 목록이라 **실제로는 거의 없다.** 고친다면 한 줄이면 된다: `const list = Array.isArray(body.error.details) ? body.error.details : [];`

### G-3. 차단된 요청의 이유를 기록에 남기기 (`promptFeedback.blockReason`)

- 원문이 안전 검사에 걸리면 `candidates`가 아예 없고 `promptFeedback.blockReason`(예: `SAFETY`, `PROHIBITED_CONTENT`)만 온다(참조 페이지). 지금 기록에는 `finish: ''`만 남아서 `BAD_RESPONSE`의 원인이 "차단"인지 "JSON 깨짐"인지 나눌 수 없다.
- `readMeta_`에 `if (body.promptFeedback) info.block = body.promptFeedback.blockReason || '';`, `finish_`에 `block: info.block || ''` 두 줄이면 된다. 정해진 영어 단어라 원문·키가 섞이지 않는다.

### G-4. 4번 ⑥-5 `curl` 예시를 Windows에서 그대로 쓰면 안 된다

- PowerShell 5.1에서 `curl`은 진짜 curl이 아니라 `Invoke-WebRequest`의 다른 이름이라 `-L`·`-d`가 먹지 않는다. `curl.exe` 또는 Git Bash에서 쓰라고 적는다.
- `-X POST`를 붙이지 않는 것이 맞다(지금 예시도 안 붙임). Apps Script는 302로 다른 주소로 보내는데, `-d`만 쓰면 curl이 그 주소를 GET으로 따라가서 결과를 받는다. `-X POST`를 붙이면 따라간 주소에도 POST를 보내 실패한다. 이 이유를 한 줄 적어 두면 나중에 실수하지 않는다.
- Windows 명령줄에서 한글이 깨질 수 있다. 영어 예문(예: `"Ebbinghaus published the forgetting curve in 1885. It shows memory loss over time."`)을 쓰거나 JSON을 파일로 만들어 `--data-binary @파일`로 보낸다.

### G-5. 시험 2·3 통과 조건에 "한글이 깨지지 않음"을 더한다 (5번 A-2·A-3)

- `UrlFetchApp`에 글자 payload를 보낼 때 한글 인코딩이 맞는지는 실제로 돌려 봐야 안다. A-2에 "`[TEST]` 카드에 '에빙하우스' 같은 한글이 제대로 읽힌다(□나 ?로 깨지지 않음)"를 더한다. 깨지면 `contentType`을 `'application/json; charset=utf-8'`로 바꿔 본다.

### G-6. 5번 표 B에 403 행을 미리 둔다

- 문제 해결 페이지: 유출·차단된 키는 **`403 PERMISSION_DENIED`**("Your API key was reported as leaked")다. 지금 `reasonFor_`로는 `OTHER`가 된다. 사용자 문구는 어차피 같고 기록에 `status: 403`이 남으니 지금 고칠 필요는 없다.
- 다만 7-d "키 오류는 개발자가 알 수 있게"의 뜻을 생각하면, 표 B에 "403 (나오면)" 행을 두고 실제로 보면 그때 KEY로 넣을지 정한다고 적어 둔다. "본 적 없는 조건은 넣지 않는다"는 22번 원칙은 그대로 맞다.

---

## [괜찮은 점]

1. **키를 헤더로 보낸다.** 가짜 시험에서 요청 주소에 키가 없고 헤더에만 있음을 확인했다. 시간 초과 예외 메시지에 주소가 들어가도 키는 없다. 그 메시지도 기록하지 않는다.
2. **기록 줄이 숫자·짧은 코드뿐이다.** 원문 자리에 표시 글자를 넣고 17가지 Gemini 응답을 흉내 냈는데, 기록 줄에 키·원문·오류 문장이 한 번도 나오지 않았다. `errReason`은 Google의 `ErrorInfo.reason`(정해진 영어 단어)만 꺼낸다.
3. **`testWrongKey`가 속성을 건드리지 않는다.** 보낸 키가 진짜 키와 다르고, 바뀐 키도 기록에 없음을 확인했다. admin이 키를 지우고 다시 넣다 채팅에 붙여넣는 위험이 없다. 속성에 키가 없으면 `'x'` 한 글자로 부르게 되는데, 이것도 틀린 키 시험으로 쓸 수 있어 문제없다.
4. **`doPost` 입력 확인이 안전하다.** `e`가 없음, `postData` 없음, 빈 본문, `"null"`, `text`가 숫자, 20,001자 → 모두 `BAD_REQUEST`로 끝나고 Gemini를 부르지 않았다. 20,000자는 통과.
5. **카드 꺼내기 경로가 맞다.** `candidates[0].content.parts[].text`. 정상 → `ok`, `cards: []` → `ok`(0장은 HTML이 원문 문제로 처리), `cards: null`·`null`·문자열·목록·잘린 JSON(`MAX_TOKENS`)·차단(후보 없음)·후보에 `content` 없음·HTML 응답 → 모두 `BAD_RESPONSE`.
6. **상태 코드 나누기.** 400+`API_KEY_INVALID` → `KEY`, 429 → `QUOTA`, 403·404·502 → `OTHER`+`status`, 예외 → `OTHER`+`status: 0`. 계획 2-0 표와 같다.
7. **KEY 규칙을 "임시"로 두고 시험으로 확정한다.** 공식 문서끼리 실제로 엇갈린다(아래 2번 ⑤). 02 5-1 "추측으로 적지 않는다"를 지켰다.
8. **`doGet` 삭제가 다른 확인과 부딪히지 않는다.** 13번 0-3(주소창에 `NOT_READY`)은 S2-0에서 끝난 확인이다. S2-4 휴대폰 확인은 HTML이 POST로 부른다. S2-4 전에 GET이 필요한 확인은 없다. A-6에 "오류가 정상"이라고 미리 적은 것도 좋다.
9. **범위가 깨끗하다.** HTML 연결, 60초, 인터넷 구분, 가짜 장치 삭제가 모두 "하지 않는 것"(S2-4)에 있다. 하루 상한·스키마·Interactions도 미뤘다(YAGNI). `my-feature.html`·`config.js`는 바꾸지 않는다.
10. **admin 순서를 따라 하기 쉽다.** 키 붙여넣기 금지 주의가 맨 위에 있고, "새 배포 누르지 않기", 주소 끝 6글자만 비교하기, 권한 화면 순서가 있다. 시험 횟수를 정해 두어 한도를 일부러 쓰지 않는다.
11. **`split/join`, `T03_TEXT` 원문 일치, UTC 안내, 시험 함수 이름 규칙(`_` 없음)** 모두 맞다. `parts`에서 `thought`를 빼는 줄은 지금은 필요 없다(`includeThoughts` 기본값이 꺼짐이라 생각 조각이 안 옴) — 한 줄이고 모델을 바꿔도 안전해서 남겨도 된다.

---

## 2. 공식 문서 독립 확인 (2026-10-27)

| # | 확인할 것 | 결과 | dev와 같은가 | 출처 |
|---|---|---|---|---|
| ① | 2.5 제한, 모델 ID | 모델 페이지 원문: "we are limiting access to the 2.5 models to users who have actively used them in the past", "not deprecated and will continue to be served until further notice", 새 프로젝트는 "3.5 Flash-Lite or 3.8 Flash". ID: `gemini-2.5-flash-lite`, `gemini-2.5-flash`, **`gemini-3.5-flash-lite`(Stable)**, `gemini-3.8-flash`(New Stable), `gemini-3.1-flash-lite`(Stable). 지원 중단 페이지: 2.5 둘 다 종료 날짜 없음, `gemini-3.5-flash-lite` 출시 2026-07-21·종료 날짜 없음, **`gemini-3.1-flash-lite` 종료 2027-05-07, 대체 = 3.5 Flash-Lite** | **같음** | https://ai.google.dev/gemini-api/docs/models , https://ai.google.dev/gemini-api/docs/deprecations |
| ② | `x-goog-api-key` + generateContent | **된다.** 옮기기 안내의 generateContent 예시가 헤더를 쓴다(K-2). API 키 페이지 예시도 헤더. 참조 페이지 curl만 `?key=`. API 키 페이지: "Never check API keys into source control" | dev는 "추측" → **확인함으로 올림** | https://ai.google.dev/gemini-api/docs/migrate-to-interactions , https://ai.google.dev/gemini-api/docs/api-key |
| ②보충 | generateContent 계속 지원 | "While generateContent remains fully supported, we recommend the Interactions API for all new development." | 같음 | 위 옮기기 안내 |
| ③ | 필드 이름 | `responseMimeType`: "application/json: JSON response in the response candidates". `responseSchema`: "**deprecated** … Use responseFormat instead". `usageMetadata`: `promptTokenCount`, `candidatesTokenCount`, `thoughtsTokenCount`, `totalTokenCount`(생각 포함 합계) | 같음 (+ 합계 설명 보충) | https://ai.google.dev/api/generate-content |
| ④ | thinking | 참조: `thinkingLevel` "Recommended for Gemini 3 or later models. **Use with earlier models results in an error.**", 값 MINIMAL/LOW/MEDIUM/HIGH. `thinkingBudget` "The number of thoughts tokens…". `includeThoughts` 기본 꺼짐. thinking 표: 2.5 Flash-Lite **Off**, 2.5 Flash **On**, **3.5 Flash-Lite On (minimal)**, 3.8 Flash On (medium). "2.5 Flash를 budget 0으로 끄기"는 공식 페이지에서 **나도 못 찾음** | dev가 못 찾은 3.5 기본값을 찾음 (K-2) | https://ai.google.dev/gemini-api/docs/thinking , https://ai.google.dev/api/generate-content |
| ⑤ | 잘못된 키·429 | 429 = `RESOURCE_EXHAUSTED`(문제 해결 페이지). 잘못된 키: 문제 해결 페이지 "400, 402, 403 … indicate issues like invalid API keys…", 유출 키 = **403 PERMISSION_DENIED**. API 오류 페이지 "missing, invalid, or expired" = **401**이지만 이 페이지는 "All errors from the **Interactions API**" 기준이고 `error.status`·`details`는 적혀 있지 않다 → generateContent에 그대로 적용된다는 근거가 없다 | 같음 (문서가 엇갈림 → 직접 시험이 맞다) | https://ai.google.dev/gemini-api/docs/troubleshooting , https://ai.google.dev/gemini-api/docs/api-errors |
| 덤 | 가격·무료 | 3.5 Flash-Lite: 무료 등급 "Free of charge", 유료 $0.30 / $2.50(출력은 생각 포함), "Used to improve our products: Yes". 2.5 Flash-Lite 유료 $0.10 / $0.40 | 같음 | https://ai.google.dev/gemini-api/docs/pricing |
| 덤 | `UrlFetchApp` | `timeoutSeconds` "The maximum time in seconds to wait for the request to complete. The default is 360 (6 minutes)." `muteHttpExceptions`·`headers`·`contentType` 이름 맞음 | 같음 | https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app |

- 참고(dev 문서에 없음): 문제 해결 페이지에 "Gemini 4 and Gemini 3.6+ models ignore custom values for `temperature`…"가 있다. 우리 코드는 `temperature`를 넣지 않으므로 영향 없다.

---

## 3. 가짜 서비스로 돌린 결과 (node, 임시 폴더)

| 경우 | 결과 | 기록에 키·원문·오류 문장 |
|---|---|---|
| 200 정상 / `cards: []` | `ok:true` | 없음 |
| 200 `cards:null` / `null` / 문자열 / 목록 / 잘린 JSON / 차단 / `content` 없음 / HTML | `BAD_RESPONSE` | 없음 |
| 400 `API_KEY_INVALID` | `KEY` | 없음 |
| 429 | `QUOTA` | 없음 |
| 403 유출 키 / 404 / 502 HTML | `OTHER` + `status` | 없음 |
| 예외(시간 초과) | `OTHER`, `status: 0` | 없음 |
| `details`가 객체 | **멈춤(예외)** → G-2 | 없음 |
| `doPost` 이상한 요청 6가지 | `BAD_REQUEST` | — |
| 속성에 키 없음 | `KEY` | — |
| `testWrongKey` | 보낸 키 ≠ 진짜 키, 기록에 키 없음 | 없음 |

---

## 4. 결정 필요 D-1~D-3 의견

### D-1. 모델 — **처음부터 `gemini-3.5-flash-lite`로 시험하기를 권한다** (팀 질문 3을 바꾸는 일이라 admin 결정 필요)

- 근거 (공식 문서로 확인):
  1. 2.5 계열은 "**예전에 활발히 쓴 사용자에게만**" 열려 있다. 우리 키는 2026-10-24에 새로 만들었다. admin 계정이 예전에 2.5를 썼는지는 아무도 모른다. 첫 시험이 통과해도, 그 판단 기준이 공개돼 있지 않아 **나중에 막혀도 이유를 알 수 없다.** MVP 평가(12-12)와 Phase 3 사용자 시험 중에 막히면 가장 곤란하다.
  2. Google이 새 프로젝트에 **직접 권하는 안정판**이고 종료 날짜가 없다. 3.1 Flash-Lite는 2027-05-07에 끝나고 대체 모델이 바로 3.5 Flash-Lite다.
  3. 기본 thinking이 "minimal"이라 토큰·시간 부담이 작다(3.8 Flash는 "medium"이라 60초 규칙에 더 불리할 수 있다).
  4. 무료 등급이라 유료 값 차이(약 3~6배)는 지금 돈이 아니다(02 3-1). 대가는 "Google이 데이터를 개선에 씀"으로 2.5와 같다.
  5. 2.5로 S2-5 품질 맞추기(프롬프트 다듬기)를 해 놓고 나중에 모델을 바꾸면 그 작업을 다시 해야 한다. 처음부터 쓸 모델로 맞추는 게 덜 돈다.
- 바꿀 것: `MODEL` 한 줄, 1번 ⑥ / 2-2 "`thinkingConfig` 없음" 설명("기본 minimal이라 따로 설정하지 않음"), 5번 표 C·D의 모델 칸. `thinkingLevel`을 넣지 않으면 2.5로 돌아가도 오류가 없다.
- 그래도 팀 질문 3 순서(2.5 Flash-Lite 먼저)를 지키겠다면: dev 안대로 "**막히면 3.5 Flash-Lite로 바로 바꿔도 된다**"를 미리 승인받는다. 이때 K-1처럼 "OK가 아니면 멈춤"으로 고쳐 둬야 막힌 걸 알아챌 수 있다. (다) 2.5 Flash는 같은 제한에 걸리므로 대안 목록에서 빼도 된다.
- 3.5 Flash-Lite가 무료 등급에서 막히거나 한도가 너무 작으면(4번 ①에서 확인) 그다음은 3.1 Flash-Lite(2027-05-07 종료 — MVP 평가에는 문제없음)를 권한다.
- 팀장 몫: 02 3번 모델 표·3-1 비용 표, 3-2 "2.5 Flash와 2.5 Flash-Lite 두 개로 T02·T03" 문장, 07 질문 3을 함께 고쳐야 한다.

### D-2. 하루 상한 — **dev 추천 (가)에 동의** (이번엔 길이 제한만, Phase 3 전 재검토)

- 결제를 연결하지 않아 최악이 "무료 한도 소진"이고, 그때 429 → `QUOTA` → 서비스 문제로 이미 안내된다. 하루 상한은 숫자(08 질문 10)도 없고 잠금(`LockService`)까지 넣으면 입문자가 읽기 어렵다.
- 덧붙일 것: "원인 모를 `QUOTA`가 보이면 (나)로 바꾼다"는 조건을 07 질문 5에 같이 적어 두면 좋다. AI Studio 한도 숫자(5번 표 D)가 그 근거가 된다.

### D-3. 실패 기록 = 콘솔 + Apps Script 실행 기록 — **동의, "결정"으로 적어도 된다**

- 3번 시험대로 기록 줄에는 숫자와 정해진 영어 코드만 남고 원문·카드·키·오류 문장이 없다. 02 5번 "원문 전체는 남기지 않는다", PRD 7-d "개발자는 기록으로 알 수 있게"를 둘 다 지킨다.
- 단서 하나: 편집기 시험 함수(`testShort`·`testT03`)는 카드 전체를 찍는다. 우리가 쓴 원문이라 괜찮다는 22번 설명이 맞다. 다만 **실제 사용자 원문으로 시험 함수를 돌리지 않는다**는 한 줄을 4번에 더해 두면 오해가 없다.
