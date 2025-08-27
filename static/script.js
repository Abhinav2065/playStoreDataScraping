function fetchAppData() {
    const appUrl = document.getElementById('appUrl').value;
    const errorDiv = document.getElementById('error');
    const appInfo = document.getElementById('appInfo');
    const result = document.getElementById('result');
    
    // Hide previous results and errors
    errorDiv.classList.add('hidden');
    result.classList.add('hidden');
    
    if (!appUrl.includes('id=')) {
        showError('Please enter a valid Google Play Store URL containing "id="');
        return;
    }

    // Show loading state
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.disabled = true;

    fetch('/get_app_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `app_url=${encodeURIComponent(appUrl)}`
    })
    .then(response => response.json())
    .then(data => {
        button.textContent = originalText;
        button.disabled = false;
        
        if (data.success) {
            document.getElementById('appName').textContent = data.app_name;
            appInfo.classList.remove('hidden');
        } else {
            showError('Error: ' + data.error);
        }
    })
    .catch(error => {
        button.textContent = originalText;
        button.disabled = false;
        showError('Network error: ' + error);
    });
}

function showInstalls() {
    const result = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    
    resultContent.textContent = 'Loading installs...';
    result.classList.remove('hidden');
    
    fetch('/get_installs')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            resultContent.innerHTML = `📥 <strong>Real Installs:</strong> ${data.installs}`;
        } else {
            resultContent.textContent = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        resultContent.textContent = 'Network error: ' + error;
    });
}

function showReviews() {
    const result = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    
    resultContent.textContent = 'Loading reviews...';
    result.classList.remove('hidden');
    
    fetch('/get_reviews')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            resultContent.innerHTML = `
                ⭐ <strong>Rating:</strong> ${data.review_score}/5<br>
                📊 <strong>Total Reviews:</strong> ${data.review_count}
            `;
        } else {
            resultContent.textContent = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        resultContent.textContent = 'Network error: ' + error;
    });
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}