let currentDocumentId = null;
let currentClassification = null;
let currentFileMode = 'document'; // 'document' or 'video'

// File mode switching
function switchFileMode(mode) {
    currentFileMode = mode;
    
    // Update button states
    document.getElementById('documentMode').classList.toggle('active', mode === 'document');
    document.getElementById('videoMode').classList.toggle('active', mode === 'video');
    
    // Show/hide upload areas
    document.getElementById('documentUpload').style.display = mode === 'document' ? 'block' : 'none';
    document.getElementById('videoUpload').style.display = mode === 'video' ? 'block' : 'none';
    
    // Show/hide buttons
    document.getElementById('classifyBtn').style.display = mode === 'document' ? 'inline-block' : 'none';
    document.getElementById('classifyVideoBtn').style.display = mode === 'video' ? 'inline-block' : 'none';
    
    // Update batch processing file types
    updateBatchFileTypes();
    
    // Reset inputs
    resetFileInputs();
}

function updateBatchFileTypes() {
    const batchInput = document.getElementById('batchFileInput');
    const includeDocs = document.getElementById('includeDocs').checked;
    const includeVideos = document.getElementById('includeVideos').checked;
    
    let accept = '';
    if (includeDocs) {
        accept += '.pdf,.png,.jpg,.jpeg,.tiff,.bmp';
    }
    if (includeVideos) {
        if (accept) accept += ',';
        accept += '.mp4,.avi,.mov,.wmv,.flv,.webm,.mkv';
    }
    
    batchInput.accept = accept;
}

function resetFileInputs() {
    const fileInput = document.getElementById('fileInput');
    const videoInput = document.getElementById('videoInput');
    
    fileInput.value = '';
    videoInput.value = '';
    
    // Reset upload prompts
    resetUploadPrompt('document');
    resetUploadPrompt('video');
    
    // Disable buttons
    document.getElementById('classifyBtn').disabled = true;
    document.getElementById('classifyVideoBtn').disabled = true;
    
    // Hide video preview
    document.getElementById('videoPreview').style.display = 'none';
}

function resetUploadPrompt(type) {
    const uploadArea = type === 'document' ? 
        document.getElementById('documentUpload') : 
        document.getElementById('videoUpload');
    
    const prompt = uploadArea.querySelector('.upload-prompt');
    
    if (type === 'document') {
        prompt.innerHTML = `
            <span class="upload-icon">📄</span>
            <p>Click to upload or drag and drop</p>
            <p class="upload-hint">PDF, PNG, JPG, TIFF, BMP (Max 50MB)</p>
        `;
    } else {
        prompt.innerHTML = `
            <span class="upload-icon">🎬</span>
            <p>Click to upload or drag and drop video</p>
            <p class="upload-hint">MP4, AVI, MOV, WMV, FLV, WEBM, MKV (Max 200MB, 30min)</p>
            <div class="video-features">
                <div class="feature-item">
                    <span class="feature-icon">🎤</span>
                    <span>Audio Transcription</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🤖</span>
                    <span>ElevenLabs AI</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📝</span>
                    <span>Text Classification</span>
                </div>
            </div>
        `;
    }
}

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
const documentUpload = document.getElementById('documentUpload');
const videoUpload = document.getElementById('videoUpload');
const fileInput = document.getElementById('fileInput');
const videoInput = document.getElementById('videoInput');
const classifyBtn = document.getElementById('classifyBtn');
const classifyVideoBtn = document.getElementById('classifyVideoBtn');

// Document upload handling
documentUpload.addEventListener('click', () => fileInput.click());
videoUpload.addEventListener('click', () => videoInput.click());

// Drag and drop for documents
documentUpload.addEventListener('dragover', (e) => {
    e.preventDefault();
    documentUpload.style.background = '#f8f9ff';
});

documentUpload.addEventListener('dragleave', () => {
    documentUpload.style.background = '';
});

documentUpload.addEventListener('drop', (e) => {
    e.preventDefault();
    documentUpload.style.background = '';
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect('document');
    }
});

// Drag and drop for videos
videoUpload.addEventListener('dragover', (e) => {
    e.preventDefault();
    videoUpload.style.background = '#f9f5ff';
});

videoUpload.addEventListener('dragleave', () => {
    videoUpload.style.background = '';
});

videoUpload.addEventListener('drop', (e) => {
    e.preventDefault();
    videoUpload.style.background = '';
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        videoInput.files = files;
        handleFileSelect('video');
    }
});

fileInput.addEventListener('change', () => handleFileSelect('document'));
videoInput.addEventListener('change', () => handleFileSelect('video'));

function handleFileSelect(type = currentFileMode) {
    const input = type === 'document' ? fileInput : videoInput;
    const button = type === 'document' ? classifyBtn : classifyVideoBtn;
    
    if (input.files.length > 0) {
        const file = input.files[0];
        const fileName = file.name;
        
        if (type === 'document') {
            updateDocumentPrompt(fileName);
            button.disabled = false;
        } else {
            updateVideoPrompt(file);
            button.disabled = false;
        }
    }
}

function updateDocumentPrompt(fileName) {
    const prompt = documentUpload.querySelector('.upload-prompt');
    prompt.innerHTML = `
        <span class="upload-icon">✓</span>
        <p><strong>${fileName}</strong></p>
        <p class="upload-hint">Ready to classify</p>
    `;
}

function updateVideoPrompt(file) {
    const fileName = file.name;
    const fileSize = (file.size / (1024 * 1024)).toFixed(1);
    const prompt = videoUpload.querySelector('.upload-prompt');
    
    prompt.innerHTML = `
        <span class="upload-icon">✓</span>
        <p><strong>${fileName}</strong></p>
        <p class="upload-hint">Size: ${fileSize}MB - Ready to process</p>
    `;
    
    // Show video preview
    const videoPreview = document.getElementById('videoPreview');
    const previewVideo = document.getElementById('previewVideo');
    
    const url = URL.createObjectURL(file);
    previewVideo.src = url;
    videoPreview.style.display = 'block';
    
    previewVideo.addEventListener('loadedmetadata', () => {
        const duration = Math.round(previewVideo.duration);
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        const format = fileName.split('.').pop().toUpperCase();
        
        document.getElementById('videoDuration').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        document.getElementById('videoSize').textContent = `${fileSize}MB`;
        document.getElementById('videoFormat').textContent = format;
    });
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
            displayResults(result, 'document');
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

classifyVideoBtn.addEventListener('click', async () => {
    if (videoInput.files.length === 0) return;
    
    classifyVideoBtn.disabled = true;
    classifyVideoBtn.innerHTML = '<span class="processing-spinner"></span> Processing Video...';
    
    const formData = new FormData();
    formData.append('file', videoInput.files[0]);
    
    try {
        const response = await fetch('/api/classify/video', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            if (result.warning) {
                // Handle case where transcription failed but we got video metadata
                displayVideoWarning(result);
            } else {
                displayResults(result, 'video');
            }
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        classifyVideoBtn.disabled = false;
        classifyVideoBtn.innerHTML = '<span class="btn-icon">🎬</span> Transcribe & Classify Video';
    }
});

function displayVideoWarning(result) {
    const resultsSection = document.getElementById('results');
    resultsSection.style.display = 'block';
    
    // Show warning instead of classification
    const categoryEl = document.getElementById('resultCategory');
    categoryEl.textContent = 'VIDEO PROCESSING ISSUE';
    categoryEl.className = 'category-warning';
    
    const confidenceEl = document.getElementById('resultConfidence');
    confidenceEl.textContent = 'Transcription Failed';
    confidenceEl.className = 'confidence-badge badge-low';
    
    // Show video metadata
    const videoMetadata = document.getElementById('videoMetadata');
    videoMetadata.style.display = 'block';
    
    const duration = result.video_metadata.duration;
    const minutes = Math.floor(duration / 60);
    const seconds = Math.round(duration % 60);
    
    document.getElementById('resultDuration').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    document.getElementById('resultTranscription').textContent = 'Failed';
    document.getElementById('resultMethod').textContent = result.video_metadata.processing_method || 'none';
    
    // Hide document metadata
    document.getElementById('resultPages').parentElement.style.display = 'none';
    document.getElementById('resultImages').parentElement.style.display = 'none';
    document.getElementById('resultSafety').parentElement.style.display = 'none';
    
    // Show reasoning
    document.getElementById('resultReasoning').textContent = result.details || 'Could not extract audio transcript from video for classification.';
    
    // Hide evidence
    document.getElementById('evidenceList').innerHTML = '<p>No classification performed due to transcription failure.</p>';
    
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayResults(result, type = 'document') {
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
    
    // Show/hide appropriate metadata
    if (type === 'video') {
        // Show video metadata
        document.getElementById('videoMetadata').style.display = 'block';
        
        const duration = result.video_metadata.duration;
        const minutes = Math.floor(duration / 60);
        const seconds = Math.round(duration % 60);
        
        document.getElementById('resultDuration').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        document.getElementById('resultTranscription').textContent = 
            result.video_processing.transcript_extracted ? 'Success' : 'Failed';
        document.getElementById('resultMethod').textContent = 
            result.video_processing.processing_method || 'none';
        
        // Hide document metadata
        document.getElementById('resultPages').parentElement.style.display = 'none';
        document.getElementById('resultImages').parentElement.style.display = 'none';
        
        // Show transcript section if available
        if (result.video_processing.transcript_extracted) {
            displayTranscript(result);
        }
    } else {
        // Show document metadata
        document.getElementById('resultPages').textContent = result.classification.page_count;
        document.getElementById('resultImages').textContent = result.classification.image_count;
        
        // Hide video metadata
        document.getElementById('videoMetadata').style.display = 'none';
        document.getElementById('transcriptSection').style.display = 'none';
        
        // Show document metadata elements
        document.getElementById('resultPages').parentElement.style.display = 'flex';
        document.getElementById('resultImages').parentElement.style.display = 'flex';
    }
    
    // Safety check (common to both)
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

function displayTranscript(result) {
    const transcriptSection = document.getElementById('transcriptSection');
    const transcriptText = document.getElementById('transcriptText');
    const transcriptStats = document.getElementById('transcriptStats');
    
    // Get transcript from classification content (this would need to be passed through)
    const transcript = result.classification.reasoning; // Placeholder - actual transcript would come from the content
    const segmentsCount = result.video_processing.audio_segments_count || 0;
    const wordsCount = transcript ? transcript.split(' ').length : 0;
    
    // Show transcript section
    transcriptSection.style.display = 'block';
    
    // Set transcript preview (first 200 characters)
    const preview = transcript ? transcript.substring(0, 200) + (transcript.length > 200 ? '...' : '') : 'No transcript available';
    transcriptText.textContent = preview;
    
    // Set stats
    transcriptStats.textContent = `${wordsCount} words, ${segmentsCount} segments`;
    
    // Handle full transcript toggle
    const showFullButton = document.getElementById('showFullTranscript');
    showFullButton.onclick = () => toggleFullTranscript(transcript, result.video_processing.audio_segments);
}

function toggleFullTranscript(fullText, segments = []) {
    const transcriptFull = document.getElementById('transcriptFull');
    const button = document.getElementById('showFullTranscript');
    
    if (transcriptFull.style.display === 'none' || !transcriptFull.style.display) {
        // Show full transcript
        transcriptFull.style.display = 'block';
        button.textContent = 'Hide Full Transcript';
        
        // Populate segments
        const segmentsDiv = document.getElementById('transcriptSegments');
        segmentsDiv.innerHTML = '';
        
        if (segments && segments.length > 0) {
            segments.forEach(segment => {
                const segmentDiv = document.createElement('div');
                segmentDiv.className = 'transcript-segment';
                
                const start = Math.floor(segment.start);
                const startMin = Math.floor(start / 60);
                const startSec = start % 60;
                
                segmentDiv.innerHTML = `
                    <span class="segment-timestamp">${startMin}:${startSec.toString().padStart(2, '0')}</span>
                    <span class="segment-text">${segment.text}</span>
                `;
                
                segmentsDiv.appendChild(segmentDiv);
            });
        } else {
            // Show full text as one segment
            const segmentDiv = document.createElement('div');
            segmentDiv.className = 'transcript-segment';
            segmentDiv.innerHTML = `<span class="segment-text">${fullText}</span>`;
            segmentsDiv.appendChild(segmentDiv);
        }
    } else {
        // Hide full transcript
        transcriptFull.style.display = 'none';
        button.textContent = 'Show Full Transcript';
    }
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

// Update batch file types when checkboxes change
document.getElementById('includeDocs').addEventListener('change', updateBatchFileTypes);
document.getElementById('includeVideos').addEventListener('change', updateBatchFileTypes);

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

// Batch processing checkbox handlers
document.getElementById('includeDocs').addEventListener('change', updateBatchFileTypes);
document.getElementById('includeVideos').addEventListener('change', updateBatchFileTypes);

// Initialize batch file types on page load
document.addEventListener('DOMContentLoaded', function() {
    updateBatchFileTypes();
});
