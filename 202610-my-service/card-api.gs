// Flip 카드 생성용 Apps Script(flip-card-api) 사본. 지금은 S2-0 임시 코드다.
// Copy of the flip-card-api Apps Script. Currently the S2-0 placeholder.
// 키(GEMINI_API_KEY)는 스크립트 속성에만 있다. 이 파일에 키를 넣지 않는다. / Never put the key here.
// S2-3에서 진짜 카드 생성 코드로 바꾸고, 그때 doGet은 지운다. / Replace in S2-3 and remove doGet then.

// 아직 준비 안 됨 응답 / Not-ready response
function doGet() {
  return reply_({ ok: false, reason: 'NOT_READY' });
}

function doPost() {
  return reply_({ ok: false, reason: 'NOT_READY' });
}

// JSON으로 돌려주기 / Return as JSON
function reply_(value) {
  return ContentService.createTextOutput(JSON.stringify(value))
    .setMimeType(ContentService.MimeType.JSON);
}
