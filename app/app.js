// Flip MVP — PRD v1.4
// 1단계: 입력 화면 (기능 1, 2, 3)

const screens = {
  input: document.getElementById('screen-input'),
  loading: document.getElementById('screen-loading'),
};

const form = document.getElementById('inputForm');
const sourceText = document.getElementById('sourceText');
const emptyHint = document.getElementById('emptyHint');
const submitBtn = document.getElementById('submitBtn');

let submitting = false; // 2-3: 두 번째 누름 무시

function showScreen(name) {
  for (const [key, el] of Object.entries(screens)) {
    el.hidden = key !== name;
  }
}

// 기능 3: 띄어쓰기·줄바꿈만 있으면 빈 입력
function isEmpty(text) {
  return text.trim() === '';
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  if (submitting) return;

  const text = sourceText.value;
  if (isEmpty(text)) {
    emptyHint.hidden = false; // 3-a: 입력 화면에 그대로 머묾
    return;
  }

  submitting = true;
  submitBtn.disabled = true;
  showScreen('loading'); // 2-2
  startGeneration(text);
});

sourceText.addEventListener('input', () => {
  emptyHint.hidden = true;
});

// 2단계에서 AI 카드 생성으로 교체
function startGeneration(text) {
  console.log('[flip] 카드 만들기 시작:', text.length, '자');
}
