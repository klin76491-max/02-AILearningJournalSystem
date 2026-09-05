/**
 * 子彈筆記速記與互動腳本 (Rapid Logging & Bullet Operations)
 */

document.addEventListener('DOMContentLoaded', () => {
  const rapidInput = document.getElementById('rapid-log-input');
  if (rapidInput) {
    rapidInput.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        submitRapidLog();
      }
    });
  }
});

function submitRapidLog() {
  const input = document.getElementById('rapid-log-input');
  if (!input) return;

  const rawText = input.value.trim();
  if (!rawText) {
    alert('請輸入速記文字內容。');
    return;
  }

  const skeleton = document.getElementById('bullet-skeleton');
  const btn = document.getElementById('btn-ai-parse');
  const csrftoken = getCSRFToken();

  if (skeleton) skeleton.classList.remove('d-none');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> AI 結構化整理中...';
  }

  fetch('/journal/api/parse-bullets/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      raw_text: rawText
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      input.value = '';
      location.reload();
    } else {
      alert(data.error || '解析失敗');
    }
  })
  .catch(err => {
    console.error(err);
    alert('連線失敗，請稍後再試。');
  })
  .finally(() => {
    if (skeleton) skeleton.classList.add('d-none');
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '<i class="bi bi-stars me-1"></i>✨ AI 智慧整理與結構化';
    }
  });
}

function toggleBullet(bulletId) {
  const csrftoken = getCSRFToken();

  fetch(`/journal/api/bullets/${bulletId}/toggle/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const symbolSpan = document.getElementById(`symbol-${bulletId}`);
      const textSpan = document.getElementById(`bullet-text-${bulletId}`);
      const headerRate = document.getElementById('header-completion-rate');

      if (symbolSpan) symbolSpan.innerText = data.symbol;
      if (textSpan) {
        if (data.is_completed) {
          textSpan.classList.add('completed');
        } else {
          textSpan.classList.remove('completed');
        }
      }
      if (headerRate && data.completion_rate !== undefined) {
        headerRate.innerText = data.completion_rate;
      }
    } else {
      alert(data.error || '切換失敗');
    }
  })
  .catch(err => console.error(err));
}

function migrateBullet(bulletId, target) {
  const csrftoken = getCSRFToken();

  fetch(`/journal/api/bullets/${bulletId}/migrate/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      target: target
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const symbolSpan = document.getElementById(`symbol-${bulletId}`);
      if (symbolSpan) symbolSpan.innerText = data.symbol;
      
      let msg = '遷移完成！';
      if (target === 'tomorrow') msg = '已成功遷移 (>) 至明日日誌！';
      else if (target === 'monthly') msg = '已成功遷移至當月月誌！';
      else if (target === 'future') msg = '已成功排程 (<) 至未來誌！';
      else if (target === 'cancel') msg = '已劃掉 (—) 取消此項目！';

      alert(msg);
      location.reload();
    } else {
      alert(data.error || '遷移失敗');
    }
  })
  .catch(err => console.error(err));
}

function deleteBullet(bulletId) {
  if (!confirm('確定要刪除此子彈項目嗎？')) return;
  const csrftoken = getCSRFToken();

  fetch(`/journal/api/bullets/${bulletId}/delete/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const row = document.getElementById(`bullet-row-${bulletId}`);
      if (row) row.remove();
    } else {
      alert(data.error || '刪除失敗');
    }
  })
  .catch(err => console.error(err));
}

function createSingleBullet() {
  const typeSelect = document.getElementById('modal-item-type');
  const contentInput = document.getElementById('modal-bullet-content');
  if (!contentInput || !contentInput.value.trim()) {
    alert('請輸入內容。');
    return;
  }

  const csrftoken = getCSRFToken();

  fetch('/journal/api/parse-bullets/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      raw_text: `${typeSelect.value === 'task' ? '•' : typeSelect.value === 'note' ? '-' : typeSelect.value === 'event' ? '○' : typeSelect.value === 'reflection' ? '★' : '!'} ${contentInput.value.trim()}`
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      location.reload();
    }
  })
  .catch(err => console.error(err));
}
