/**
 * AI 每日反思生成非同步腳本
 */

function generateAIReflection(dateStr) {
  const box = document.getElementById('ai-reflection-box');
  const csrftoken = getCSRFToken();

  if (box) {
    box.innerHTML = `
      <div class="d-flex align-items-center text-muted py-3">
        <div class="spinner-border spinner-border-sm text-warning me-2" role="status"></div>
        <span class="small">AI 導師正在梳理今日走過的路與微小進展...</span>
      </div>
    `;
  }

  fetch(`/journal/api/entry/${dateStr}/reflection/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success && box) {
      box.innerHTML = `
        <p class="small text-muted mb-2 fade-in"><strong>📝 今日摘要：</strong>${data.summary}</p>
        <p class="small text-dark mb-0 fade-in"><strong>💡 溫暖洞察：</strong>${data.reflection}</p>
      `;
    } else {
      if (box) box.innerHTML = '<p class="small text-danger mb-0">生成失敗，請稍後重試。</p>';
    }
  })
  .catch(err => {
    console.error(err);
    if (box) box.innerHTML = '<p class="small text-danger mb-0">連線異常。</p>';
  });
}
