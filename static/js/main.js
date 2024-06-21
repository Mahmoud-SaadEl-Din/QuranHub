function selectOption(option) {
  document.getElementById('second-row').style.display = 'block';
  localStorage.setItem('firstOption', option);
}

function selectSubOption(subOption) {
  const firstOption = localStorage.getItem('firstOption');
  const thirdRow = document.getElementById('third-row');
  thirdRow.innerHTML = ''; // Clear previous content

  if (firstOption === 'view') {
    thirdRow.innerHTML = `
      <form method="post" action="/view">
        <div class="form-group">
          <label for="view-input">Enter your input:</label>
          <input type="text" class="form-control" id="view-input" name="view_input" required>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    `;
  } else if (firstOption === 'add') {
    if (subOption === 'subject') {
      window.location.href = '/add/subject';
    } else if (subOption === 'symbol') {
      window.location.href = '/add/symbol';
    }
  }

  document.getElementById('third-row').style.display = 'block';
}

function handleTypeChange(value) {
  document.getElementById('new-subject').style.display = value === 'new' ? 'block' : 'none';
  document.getElementById('existing-subject').style.display = value === 'existing' ? 'block' : 'none';
}

function handleSymbolTypeChange(value) {
  document.getElementById('new-symbol').style.display = value === 'new' ? 'block' : 'none';
  document.getElementById('existing-symbol').style.display = value === 'existing' ? 'block' : 'none';
  document.getElementById('search-symbol').style.display = value === 'search' ? 'block' : 'none';
}

function searchSymbol(query) {
  fetch('/api/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: query })
  })
  .then(response => response.json())
  .then(data => {
    const resultsDiv = document.getElementById('search-results');
    resultsDiv.innerHTML = '';
    data.forEach(item => {
      const div = document.createElement('div');
      div.textContent = item;
      resultsDiv.appendChild(div);
    });
  });
}
