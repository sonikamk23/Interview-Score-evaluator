const form = document.getElementById('assessment-form');
const submitButton = document.getElementById('submit-button');
const reportSection = document.getElementById('report');
const overallScore = document.getElementById('overall-score');
const dreamScore = document.getElementById('dream-score');
const successScore = document.getElementById('success-score');
const daysReady = document.getElementById('days-ready');
const recommendationList = document.getElementById('recommendation-list');
const badgeList = document.getElementById('badge-list');
const resumeProgress = document.getElementById('resume-progress');
const technicalProgress = document.getElementById('technical-progress');
const communicationProgress = document.getElementById('communication-progress');
const portfolioProgress = document.getElementById('portfolio-progress');
const reportTitle = document.getElementById('report-title');
const reportBadge = document.getElementById('report-badge');
const heroScore = document.getElementById('hero-score');
const cameraVideo = document.getElementById('camera-video');
const cameraStart = document.getElementById('camera-start');
const cameraConfidence = document.getElementById('camera-confidence');
const mockQuestionElement = document.getElementById('mock-question');
const mockAnswer = document.getElementById('mock-answer');
const mockStart = document.getElementById('mock-start');
const mockNext = document.getElementById('mock-next');
const mockScorePanel = document.getElementById('mock-score-panel');
const mockScoreValue = document.getElementById('mock-score');
const mockComment = document.getElementById('mock-comment');
const downloadReport = document.getElementById('download-report');
const showQrButton = document.getElementById('show-qr');
const qrBlock = document.getElementById('qr-block');
const qrImage = document.getElementById('qr-image');

const hasDashboardPage = !!form && !!submitButton;
const hasCamera = !!cameraStart && !!cameraVideo;
const hasMockInterview = !!mockStart && !!mockNext;
const hasDownload = !!downloadReport && !!showQrButton;

let cameraStream = null;
let cameraActive = false;
let currentQuestionIndex = 0;
let mockScores = [];
let analysisResult = null;

const mockQuestions = [
    'Tell me about a time you solved a technical problem under pressure.',
    'Describe one project where you used your strongest technical skill.',
    'How would you introduce yourself in a recruiter screening call?',
    'What steps do you take when learning a new framework or tool?'
];

if (hasCamera) {
    cameraStart.addEventListener('click', async () => {
        if (cameraActive) {
            stopCamera();
            cameraStart.textContent = 'Start Camera';
            cameraConfidence.textContent = '--';
            return;
        }

        try {
            cameraStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            cameraVideo.srcObject = cameraStream;
            cameraVideo.play();
            cameraActive = true;
            cameraStart.textContent = 'Stop Camera';
            cameraConfidence.textContent = 'Analyzing...';
            setTimeout(() => {
                const score = 72 + Math.floor(Math.random() * 18);
                cameraConfidence.textContent = `${score}%`;
                if (!analysisResult && heroScore) heroScore.textContent = `${score}%`;
            }, 1200);
        } catch (error) {
            alert('Unable to access camera. Please allow webcam access or try a different device.');
        }
    });
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach((track) => track.stop());
        cameraStream = null;
    }
    cameraActive = false;
}

if (hasMockInterview) {
    mockStart.addEventListener('click', () => {
        currentQuestionIndex = 0;
        mockScores = [];
        mockScorePanel.classList.remove('visible');
        showMockQuestion();
    });

    mockNext.addEventListener('click', () => {
        if (!mockQuestionElement.textContent || mockQuestionElement.textContent.includes('Press Start')) {
            alert('Please start the interview first.');
            return;
        }
        const answer = mockAnswer.value.trim();
        if (!answer) {
            alert('Type your response before going to the next question.');
            return;
        }
        mockScores.push(evaluateMockAnswer(answer));
        mockAnswer.value = '';
        currentQuestionIndex += 1;
        if (currentQuestionIndex >= mockQuestions.length) {
            finishMockInterview();
        } else {
            showMockQuestion();
        }
    });
}

function showMockQuestion() {
    mockQuestionElement.textContent = mockQuestions[currentQuestionIndex];
}

function evaluateMockAnswer(answer) {
    const wordCount = answer.split(/\s+/).filter(Boolean).length;
    const clarity = Math.min(100, Math.round(wordCount * 4 + 20));
    const structure = answer.includes('because') || answer.includes('therefore') ? 10 : 5;
    return Math.min(100, clarity + structure);
}

function finishMockInterview() {
    const total = mockScores.reduce((sum, value) => sum + value, 0);
    const average = mockScores.length ? Math.round(total / mockScores.length) : 0;
    mockScoreValue.textContent = average;
    mockComment.textContent = average >= 80 ? 'Excellent response flow and clarity.' : average >= 60 ? 'Good structure — refine your storytelling.' : 'Focus on concise, confident answers and avoid filler words.';
    mockScorePanel.classList.add('visible');
    mockQuestionElement.textContent = 'Interview practice complete. Review your responses to improve further.';
}

if (hasDashboardPage) {
    submitButton.addEventListener('click', async () => {
        submitButton.disabled = true;
        submitButton.textContent = 'Analyzing...';
        const formData = new FormData(form);

        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            alert('There was an error processing your assessment. Please try again.');
            submitButton.disabled = false;
            submitButton.textContent = 'Analyze My Readiness';
            return;
        }

        analysisResult = await response.json();
        renderReport(analysisResult);
        submitButton.disabled = false;
        submitButton.textContent = 'Analyze My Readiness';
    });

    if (hasDownload) {
        downloadReport.addEventListener('click', async () => {
            const formData = new FormData(form);
            const response = await fetch('/api/report', {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                alert('Unable to download the report. Please try again.');
                return;
            }
            const blob = await response.blob();
            const filename = 'CareerForge_AI_Pro_Report.pdf';
            downloadBlob(blob, filename);
        });

        showQrButton.addEventListener('click', async () => {
            const formData = new FormData(form);
            if (analysisResult && analysisResult.overall_score !== undefined) {
                formData.append('overall_score', analysisResult.overall_score);
            }
            const response = await fetch('/api/qr', {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                alert('Unable to generate QR code. Please try again.');
                return;
            }
            const data = await response.json();
            qrImage.src = data.qr;
            qrBlock.classList.add('visible');
        });
    }
}

function renderReport(data) {
    reportSection.classList.add('visible');
    overallScore.textContent = `${data.overall_score}`;
    dreamScore.textContent = `${data.dream_company_readiness}`;
    successScore.textContent = `${data.success_probability}%`;
    daysReady.textContent = `${data.days_to_ready} days`;
    heroScore.textContent = `${data.overall_score}%`;

    resumeProgress.style.width = `${data.category_scores.resume}%`;
    technicalProgress.style.width = `${data.category_scores.technical}%`;
    communicationProgress.style.width = `${data.category_scores.communication}%`;
    portfolioProgress.style.width = `${Math.round((data.category_scores.portfolio + data.category_scores.github + data.category_scores.linkedin) / 3)}%`;

    recommendationList.innerHTML = '';
    data.recommendations.forEach((item) => {
        const li = document.createElement('li');
        li.textContent = item;
        recommendationList.appendChild(li);
    });

    badgeList.innerHTML = '';
    data.skill_badges.forEach((badge) => {
        const span = document.createElement('span');
        span.className = 'badge';
        span.textContent = badge;
        badgeList.appendChild(span);
    });

    reportTitle.textContent = 'Your AI Career Report';
    reportBadge.textContent = data.summary.level;
}

function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
}
