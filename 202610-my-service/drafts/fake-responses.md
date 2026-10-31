# 가짜 결과 장치 보관 (S2-1·S2-2, 2026-10-27 S2-4에서 my-feature.html에서 지움)

> 다시 가짜 시험이 필요하면 이 코드를 requestCards 안에 잠시 넣고, 시험 뒤 지운다.
> 사용법: 주소 끝 ?fake=ok|slow|fail-source|fail-network|fail-service|cards-0|cards-22|cards-22-bad-tail|sentences-3|sentences-4|empty-front|blank-back|number-front|not-array

```js
  // [FAKE-S2-2] 시작: 검사 함수 시험용 가짜 AI 결과 (S2-4에서 지움) / Fake AI cards for checkCards (remove in S2-4)
  // 가짜 카드 n장 만들기 / Make n fake cards
  function fakeCards(n){
    const cards = [];
    for (let i = 1; i <= n; i++) {
      cards.push({ front: `가짜 질문 ${i}`, back: `가짜 답 ${i}` });
    }
    return cards;
  }
  const FOUR_SENTENCES = '첫째. 둘째. 셋째. 넷째.';
  // 2번째 카드를 망가뜨려 "첫 카드만 보는" 실수를 잡는다 / Break card 2 to catch first-card-only bugs
  const FAKE_S2_2 = {
    'cards-0': () => [],
    'cards-22': () => fakeCards(22),
    'cards-22-bad-tail': () => { const c = fakeCards(22); c[20].back = FOUR_SENTENCES; c[21].front = ''; return c; },
    'sentences-3': () => { const c = fakeCards(3); c[1].back = '첫째. 둘째. 셋째.'; return c; },
    'sentences-4': () => { const c = fakeCards(3); c[1].back = FOUR_SENTENCES; return c; },
    'empty-front': () => { const c = fakeCards(3); c[1].front = ''; return c; },
    'blank-back': () => { const c = fakeCards(3); c[1].back = '   \n  '; return c; },
    'number-front': () => { const c = fakeCards(3); c[1].front = 123; return c; },
    'not-array': () => 'cards'
  };
  // [FAKE-S2-2] 끝 / End

    // [FAKE-S2-1] 시작: 가짜 결과 (S2-4에서 진짜 요청으로 바꾸며 지움) / Fake results (remove in S2-4)
    // 주소 끝 ?fake=ok|slow|fail-source|fail-network|fail-service / Pick result by URL parameter
    // S2-2 이름(cards-0 등)은 위 FAKE_S2_2 참고 / See FAKE_S2_2 above for S2-2 names
    const fake = new URLSearchParams(location.search).get('fake') || 'ok';
    const wait = fake === 'slow' ? 8000 : 2000;
    await new Promise((resolve) => setTimeout(resolve, wait));
    if (fake === 'fail-source') return { kind: 'source' };
    if (fake === 'fail-network') return { kind: 'network' };
    if (fake === 'fail-service') return { kind: 'service' };
    // S2-2 가짜는 AI 성공처럼 넘기고 검사는 checkCards가 한다 / S2-2 fakes go through checkCards as success
    if (FAKE_S2_2.hasOwnProperty(fake)) return { kind: 'ok', cards: FAKE_S2_2[fake]() };
    return { kind: 'ok', cards: [
      { front: '가짜 질문 1', back: '가짜 답 1' },
      { front: '가짜 질문 2', back: '가짜 답 2' },
      { front: '가짜 질문 3', back: '가짜 답 3' }
    ] };
    // [FAKE-S2-1] 끝 / End
```
