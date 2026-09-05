/**
 * 思想盤點 (Mental Inventory) 互動腳本
 */

function siftItem(itemId, testStatus, category = 'none') {
  const csrftoken = getCSRFToken();

  fetch(`/inventory/api/${itemId}/sift/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      test_status: testStatus,
      category: category
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const row = document.getElementById(`item-row-${itemId}`);
      const text = document.getElementById(`item-text-${itemId}`);
      const badge = document.getElementById(`item-status-badge-${itemId}`);

      if (testStatus === 'discarded') {
        if (row) row.classList.add('bg-light', 'opacity-50');
        if (text) text.classList.add('text-decoration-line-through', 'text-muted');
        if (badge) {
          badge.className = 'badge bg-danger';
          badge.innerText = '劃掉丟棄';
        }
      } else {
        if (row) row.classList.remove('bg-light', 'opacity-50');
        if (text) text.classList.remove('text-decoration-line-through', 'text-muted');
        if (badge) {
          badge.className = 'badge bg-success';
          badge.innerText = '保留';
        }
      }
    } else {
      alert(data.error || '操作失敗');
    }
  })
  .catch(err => console.error(err));
}

function toggleFocus(itemId) {
  const csrftoken = getCSRFToken();

  fetch(`/inventory/api/${itemId}/toggle-focus/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      location.reload();
    } else {
      alert(data.error || '切換焦點失敗');
    }
  })
  .catch(err => console.error(err));
}

function deleteItem(itemId) {
  if (!confirm('確定要永久刪除此盤點項目嗎？')) return;
  const csrftoken = getCSRFToken();

  fetch(`/inventory/api/${itemId}/delete/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const row = document.getElementById(`item-row-${itemId}`);
      if (row) row.remove();
    } else {
      alert(data.error || '刪除失敗');
    }
  })
  .catch(err => console.error(err));
}
