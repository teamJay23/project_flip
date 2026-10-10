# Flip — 5초 복습 (study card)

모바일용 플래시카드 학습 앱의 프로토타입. 카드를 뒤집어 답을 확인하고,
"알고있음 / 복습 / 다음"으로 분류하며 복습한다.

## 구조
- `trialnerror/index.html` — 앱 전체 (HTML·CSS·JS 단일 파일, 빌드 과정 없음)
  - 카드 데이터: `cardData` 배열에 하드코딩
  - 진행 로직: `queue`(남은 카드 인덱스), `reviewMarked`, `skipHistory`
    - 알고있음 → queue에서 제거
    - 복습/다음 → queue 맨 뒤로 이동
- 외부 의존성: Pretendard 폰트(jsDelivr CDN)만 사용

## 실행 및 확인
- 빌드나 설치 없이 `trialnerror/index.html`을 브라우저에서 직접 열면 된다.
- 모바일 화면(너비 약 375~430px) 기준으로 확인할 것.
- 테스트 코드는 없다. 변경 후에는 브라우저에서 카드 뒤집기, 세 버튼, 완료 화면을 직접 확인할 것.

## 배포
- Vercel에 배포한다. (설정 세부 내용: 확인 필요)

## 규칙
- 프레임워크나 빌드 도구를 도입하지 말 것. 단일 HTML 파일 구조를 유지할 것.
- 색상은 `:root`의 CSS 변수(`--paper`, `--amber`, `--know`, `--review` 등)를 사용할 것.
- iOS 안전 영역(`env(safe-area-inset-*)`)과 `100dvh` 처리를 깨뜨리지 말 것.
