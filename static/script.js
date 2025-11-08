let currentDocumentId = null;
let currentClassification = null;

// Tab switching
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'statistics') {
        loadStatistics();
    }
}

// Interactive Mode
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const classifyBtn = document.getElementById('classifyBtn');

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#f8f9ff';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.background = '';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.background = '';
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
});

fileInput.addEventListener('change', handleFileSelect);

function handleFileSelect() {
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        uploadArea.querySelector('.upload-prompt').innerHTML = `
            <span class="upload-icon">✓</span>
            <p><strong>${fileName}</strong></p>
            <p class="upload-hint">Ready to classify</p>
        `;
        classifyBtn.disabled = false;
    }
}

classifyBtn.addEventListener('click', async () => {
    if (fileInput.files.length === 0) return;
    
    classifyBtn.disabled = true;
    classifyBtn.textContent = 'Classifying...';
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        const response = await fetch('/api/classify', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        classifyBtn.disabled = false;
        classifyBtn.textContent = 'Classify Document';
    }
});

function displayResults(result) {
    currentDocumentId = result.document_id;
    currentClassification = result.classification;
    
    const resultsSection = document.getElementById('results');
    resultsSection.style.display = 'block';
    
    // Category
    const category = result.classification.category;
    const categoryDisplay = category.replace('_', ' ').toUpperCase();
    document.getElementById('resultCategory').textContent = categoryDisplay;
    document.getElementById('resultCategory').className = `category-${category}`;
    
    // Confidence
    const confidence = (result.classification.confidence * 100).toFixed(1);
    const confidenceBadge = document.getElementById('resultConfidence');
    confidenceBadge.textContent = `${confidence}% Confidence`;
    confidenceBadge.className = 'confidence-badge ' + 
        (confidence >= 80 ? 'badge-high' : confidence >= 60 ? 'badge-medium' : 'badge-low');
    
    // Metadata
    document.getElementById('resultPages').textContent = result.classification.page_count;
    document.getElementById('resultImages').textContent = result.classification.image_count;
    document.getElementById('resultSafety').textContent = 
        result.classification.safety_check ? '✓ Safe' : '⚠️ Unsafe';
    
    // Reasoning
    document.getElementById('resultReasoning').textContent = 
        result.classification.reasoning || 'No reasoning provided';
    
    // Evidence
    const evidenceList = document.getElementById('evidenceList');
    evidenceList.innerHTML = '';
    
    if (result.classification.evidence && result.classification.evidence.length > 0) {
        result.classification.evidence.forEach(evidence => {
            const evidenceItem = document.createElement('div');
            evidenceItem.className = 'evidence-item';
            evidenceItem.innerHTML = `
                <strong>${evidence.type || 'Evidence'}:</strong><br>
                ${JSON.stringify(evidence.details || evidence, null, 2)}
            `;
            evidenceList.appendChild(evidenceItem);
        });
    } else {
        evidenceList.innerHTML = '<p>No specific evidence citations available.</p>';
    }
    
    // Review alert
    const reviewAlert = document.getElementById('reviewAlert');
    if (result.needs_review) {
        reviewAlert.style.display = 'block';
        document.getElementById('reviewReason').textContent = result.review_reason;
    } else {
        reviewAlert.style.display = 'none';
    }
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Feedback submission
document.getElementById('submitFeedbackBtn').addEventListener('click', async () => {
    const correctedCategory = document.getElementById('feedbackCategory').value;
    const notes = document.getElementById('feedbackNotes').value;
    
    if (!correctedCategory) {
        alert('Please select a corrected category');
        return;
    }
    
    const feedbackData = {
        document_id: currentDocumentId,
        classification_result: currentClassification,
        human_feedback: {
            corrected_category: correctedCategory,
            notes: notes
        }
    };
    
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(feedbackData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('Feedback submitted successfully!');
            document.getElementById('feedbackCategory').value = '';
            document.getElementById('feedbackNotes').value = '';
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Batch Processing
const batchFileInput = document.getElementById('batchFileInput');
const batchProcessBtn = document.getElementById('batchProcessBtn');

batchProcessBtn.addEventListener('click', async () => {
    if (batchFileInput.files.length === 0) {
        alert('Please select files to process');
        return;
    }
    
    const formData = new FormData();
    for (let file of batchFileInput.files) {
        formData.append('files', file);
    }
    
    batchProcessBtn.disabled = true;
    batchProcessBtn.textContent = 'Starting...';
    
    try {
        const response = await fetch('/api/batch', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            monitorBatchJob(result.job_id);
        } else {
            alert('Error: ' + result.error);
            batchProcessBtn.disabled = false;
            batchProcessBtn.textContent = 'Process Batch';
        }
    } catch (error) {
        alert('Error: ' + error.message);
        batchProcessBtn.disabled = false;
        batchProcessBtn.textContent = 'Process Batch';
    }
});

async function monitorBatchJob(jobId) {
    const batchStatus = document.getElementById('batchStatus');
    batchStatus.style.display = 'block';
    
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`/api/batch/${jobId}/status`);
            const status = await response.json();
            
            // Update progress
            const progressFill = document.getElementById('progressFill');
            progressFill.style.width = status.progress_percent + '%';
            
            const progressText = document.getElementById('progressText');
            progressText.textContent = 
                `Processing: ${status.processed_files + status.failed_files}/${status.total_files} files`;
            
            if (status.status === 'completed') {
                clearInterval(interval);
                loadBatchResults(jobId);
                batchProcessBtn.disabled = false;
                batchProcessBtn.textContent = 'Process Batch';
            }
        } catch (error) {
            console.error('Error monitoring batch:', error);
        }
    }, 1000);
}

async function loadBatchResults(jobId) {
    try {
        const response = await fetch(`/api/batch/${jobId}/results`);
        const data = await response.json();
        
        const batchResults = document.getElementById('batchResults');
        batchResults.innerHTML = '<h3>Results</h3>';
        
        data.results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.className = 'batch-result-item';
            
            if (result.status === 'success') {
                const category = result.classification.category;
                resultItem.innerHTML = `
                    <strong>${result.file.split('/').pop()}</strong><br>
                    Category: <span class="category-${category}">${category.toUpperCase()}</span><br>
                    Confidence: ${(result.classification.confidence * 100).toFixed(1)}%
                    ${result.needs_review ? '<br>⚠️ Requires Review' : ''}
                `;
            } else {
                resultItem.innerHTML = `
                    <strong>${result.file.split('/').pop()}</strong><br>
                    <span style="color: red;">Failed: ${result.error}</span>
                `;
            }
            
            batchResults.appendChild(resultItem);
        });
    } catch (error) {
        console.error('Error loading results:', error);
    }
}

// Statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const stats = await response.json();
        
        document.getElementById('totalFeedback').textContent = stats.total_feedback || 0;
        document.getElementById('agreementRate').textContent = 
            ((stats.agreement_rate || 0) * 100).toFixed(1) + '%';
        document.getElementById('disagreementRate').textContent = 
            ((stats.disagreement_rate || 0) * 100).toFixed(1) + '%';
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}
