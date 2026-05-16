// ========== STATE MANAGEMENT ==========
const state = {
    resumeData: null,
    jobs: [],
    matchedJobs: [],
    currentStep: 1
};

// ========== STEP NAVIGATION ==========
function showStep(stepNumber) {
    // Hide all sections
    document.querySelectorAll('.step-section').forEach(section => {
        section.classList.remove('active');
    });
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });

    // Show current section
    document.getElementById(`step-${stepNumber}`).classList.add('active');
    document.getElementById(`step-${stepNumber}-indicator`).classList.add('active');

    state.currentStep = stepNumber;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ========== UPLOAD RESUME ==========
const uploadArea = document.getElementById('uploadArea');
const resumeFile = document.getElementById('resumeFile');
const resumeInfo = document.getElementById('resumeInfo');
const uploadError = document.getElementById('uploadError');
const uploadLoading = document.getElementById('uploadLoading');
const nextBtn1 = document.getElementById('nextBtn1');

// Drag and drop
uploadArea.addEventListener('click', () => resumeFile.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#f0f2ff';
    uploadArea.style.borderColor = '#764ba2';
});
uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.background = '#f8f9ff';
    uploadArea.style.borderColor = '#667eea';
});
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#f8f9ff';
    uploadArea.style.borderColor = '#667eea';
    
    if (e.dataTransfer.files.length > 0) {
        resumeFile.files = e.dataTransfer.files;
        uploadResume();
    }
});

// File selection
resumeFile.addEventListener('change', uploadResume);

async function uploadResume() {
    if (!resumeFile.files.length) return;

    const file = resumeFile.files[0];
    
    // Validation
    if (file.type !== 'application/pdf') {
        showError(uploadError, 'Please upload a PDF file');
        return;
    }
    if (file.size > 10 * 1024 * 1024) {
        showError(uploadError, 'File size must be less than 10MB');
        return;
    }

    // Show loading
    uploadLoading.classList.remove('hidden');
    uploadError.classList.add('hidden');
    resumeInfo.classList.add('hidden');

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload-resume', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Upload failed');
        }

        const data = await response.json();
        state.resumeData = data.resume_data;

        // Display resume info
        document.getElementById('extractedRole').textContent = state.resumeData.role || '-';
        document.getElementById('extractedLocation').textContent = state.resumeData.location || '-';
        document.getElementById('extractedSkills').textContent = 
            state.resumeData.skills.slice(0, 5).join(', ') || '-';

        resumeInfo.classList.remove('hidden');
        uploadLoading.classList.add('hidden');
        nextBtn1.disabled = false;
        uploadArea.style.opacity = '0.5';

    } catch (error) {
        console.error('Error:', error);
        showError(uploadError, error.message);
        uploadLoading.classList.add('hidden');
    }
}

// ========== FETCH JOBS ==========
const fetchJobsBtn = document.getElementById('fetchJobsBtn');
const jobStats = document.getElementById('jobStats');
const fetchError = document.getElementById('fetchError');
const fetchLoading = document.getElementById('fetchLoading');
const nextBtn2 = document.getElementById('nextBtn2');

fetchJobsBtn.addEventListener('click', async () => {
    fetchLoading.classList.remove('hidden');
    fetchError.classList.add('hidden');
    jobStats.classList.add('hidden');
    fetchJobsBtn.disabled = true;

    try {
        const response = await fetch('/api/fetch-jobs', {
            method: 'POST'
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to fetch jobs');
        }

        const data = await response.json();
        state.jobs = data.jobs;

        // Display stats
        document.getElementById('totalJobs').textContent = data.total_jobs;
        const sources = Object.entries(data.source_counts)
            .map(([src, count]) => `${src}: ${count}`)
            .join(', ');
        document.getElementById('sourceBreakdown').textContent = sources;

        jobStats.classList.remove('hidden');
        fetchLoading.classList.add('hidden');
        nextBtn2.disabled = false;
        fetchJobsBtn.disabled = false;

    } catch (error) {
        console.error('Error:', error);
        showError(fetchError, error.message);
        fetchLoading.classList.add('hidden');
        fetchJobsBtn.disabled = false;
    }
});

// ========== MATCH JOBS ==========
const matchJobsBtn = document.getElementById('matchJobsBtn');
const matchStats = document.getElementById('matchStats');
const matchError = document.getElementById('matchError');
const matchLoading = document.getElementById('matchLoading');
const nextBtn3 = document.getElementById('nextBtn3');

matchJobsBtn.addEventListener('click', async () => {
    matchLoading.classList.remove('hidden');
    matchError.classList.add('hidden');
    matchStats.classList.add('hidden');
    matchJobsBtn.disabled = true;

    try {
        const response = await fetch('/api/match-jobs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume_data: state.resumeData,
                jobs: state.jobs
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to match jobs');
        }

        const data = await response.json();
        state.matchedJobs = data.matched_jobs;

        // Display stats
        document.getElementById('matchedCount').textContent = data.match_count;

        matchStats.classList.remove('hidden');
        matchLoading.classList.add('hidden');
        nextBtn3.disabled = false;
        matchJobsBtn.disabled = false;

    } catch (error) {
        console.error('Error:', error);
        showError(matchError, error.message);
        matchLoading.classList.add('hidden');
        matchJobsBtn.disabled = false;
    }
});

// ========== EXPORT JOBS ==========
const exportBtn = document.getElementById('exportBtn');
const jobsPreview = document.getElementById('jobsPreview');
const jobsList = document.getElementById('jobsList');
const exportError = document.getElementById('exportError');
const exportLoading = document.getElementById('exportLoading');

// Show preview when entering step 4
document.getElementById('nextBtn3').addEventListener('click', () => {
    displayJobsPreview();
    showStep(4);
});

function displayJobsPreview() {
    jobsList.innerHTML = '';
    
    state.matchedJobs.slice(0, 10).forEach(job => {
        const jobDiv = document.createElement('div');
        jobDiv.className = 'job-item';
        jobDiv.innerHTML = `
            <div class="job-score">${(job.match_score * 100).toFixed(0)}%</div>
            <div class="job-title">${job.title}</div>
            <div class="job-company">${job.company}</div>
        `;
        jobsList.appendChild(jobDiv);
    });

    jobsPreview.classList.remove('hidden');
}

exportBtn.addEventListener('click', async () => {
    exportLoading.classList.remove('hidden');
    exportError.classList.add('hidden');
    exportBtn.disabled = true;

    try {
        const response = await fetch('/api/export-excel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ matched_jobs: state.matchedJobs })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to export');
        }

        // Download file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'matched_jobs.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        exportLoading.classList.add('hidden');
        exportBtn.disabled = false;

    } catch (error) {
        console.error('Error:', error);
        showError(exportError, error.message);
        exportLoading.classList.add('hidden');
        exportBtn.disabled = false;
    }
});

// ========== BACK BUTTONS ==========
document.getElementById('backBtn2').addEventListener('click', () => showStep(1));
document.getElementById('backBtn3').addEventListener('click', () => showStep(2));
document.getElementById('backBtn4').addEventListener('click', () => showStep(3));

// ========== NEXT BUTTONS ==========
document.getElementById('nextBtn1').addEventListener('click', () => showStep(2));
document.getElementById('nextBtn2').addEventListener('click', () => showStep(3));

// ========== UTILITY FUNCTIONS ==========
function showError(element, message) {
    element.textContent = `❌ ${message}`;
    element.classList.remove('hidden');
}

function showSuccess(element, message) {
    element.textContent = `✅ ${message}`;
    element.classList.remove('hidden');
}

// ========== INITIALIZATION ==========
showStep(1);
