const questions = [
    'Tell me about yourself and what brought you to AI or your chosen career path.',
    'Describe a project or experience where you solved a real problem or created value.',
    'What motivates you most about the role you are preparing for?',
    'How do you learn new skills and stay updated in fast-moving fields?',
    'Tell me about a time you worked in a team and handled a challenge together.',
    'How do you make decisions when requirements are unclear or changing?',
    'What strengths do you bring to our team, and how do you contribute under pressure?',
    'Describe a challenge you overcame and what you learned from it.',
    'How do you prioritize tasks when you have multiple deadlines?',
    'What does success look like for you in this role?',
    'How do you explain a complex idea to someone without a technical background?',
    'Why should we hire you for this opportunity?'
];

const questionText = document.getElementById('question-text');
const questionNumber = document.getElementById('question-number');
const interviewStatus = document.getElementById('interview-status');
const startInterviewBtn = document.getElementById('start-interview');
const startRecordingBtn = document.getElementById('start-recording');
const stopRecordingBtn = document.getElementById('stop-recording');
const nextQuestionBtn = document.getElementById('next-question');
const replayQuestionBtn = document.getElementById('replay-question');
const transcriptArea = document.getElementById('transcript');
const responsesList = document.getElementById('responses-list');
const summaryPanel = document.getElementById('summary-panel');
const overallScoreEl = document.getElementById('overall-score');
const confidenceScoreEl = document.getElementById('confidence-score');
const communicationScoreEl = document.getElementById('communication-score');
const suggestionText = document.getElementById('suggestion-text');
const micWarning = document.getElementById('mic-warning');
const audioPlayback = document.getElementById('audio-playback');
const videoPlayback = document.getElementById('video-playback');
const cameraPreview = document.getElementById('camera-preview');

let currentIndex = 0;
let mediaRecorder = null;
let mediaStream = null;
let audioChunks = [];
let answerResponses = [];
let recognition = null;
let listening = false;
let recording = false;
let volumeSamples = [];
let audioContext = null;
let analyser = null;
let volumeInterval = null;

function supportsSpeechRecognition() {
    return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
}

function createSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return null;
    const recog = new SpeechRecognition();
    recog.continuous = true;
    recog.interimResults = true;
    recog.lang = 'en-US';
    recog.onresult = (event) => {
        const transcript = Array.from(event.results)
            .map((result) => result[0].transcript)
            .join(' ');
        transcriptArea.value = transcript;
    };
    recog.onerror = () => {
        transcriptArea.placeholder = 'Speech recognition is not available. Please use the microphone and type if needed.';
    };
    return recog;
}

function speakQuestion(text) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.voice = window.speechSynthesis.getVoices().find((voice) => voice.lang.startsWith('en')) || null;
    window.speechSynthesis.speak(utterance);
}

function updateQuestion() {
    questionText.textContent = questions[currentIndex];
    questionNumber.textContent = `${currentIndex + 1} / ${questions.length}`;
    interviewStatus.textContent = 'Ready to record your response.';
    transcriptArea.value = '';
    audioPlayback.src = '';
    startRecordingBtn.disabled = false;
    stopRecordingBtn.disabled = true;
    nextQuestionBtn.disabled = true;
    replayQuestionBtn.disabled = false;
    summaryPanel.classList.add('hidden');
}

async function startInterview() {
    currentIndex = 0;
    answerResponses = [];
    responsesList.innerHTML = '';
    summaryPanel.classList.add('hidden');
    startInterviewBtn.disabled = true;
    startInterviewBtn.textContent = 'Interview Started';
    updateQuestion();
    speakQuestion(questions[currentIndex]);
    interviewStatus.textContent = 'Question spoken aloud. Start recording when ready.';
    if (supportsSpeechRecognition()) {
        recognition = createSpeechRecognition();
    }
}

async function startRecording() {
    if (recording) return;
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        micWarning.textContent = 'Browser cannot access microphone or camera. Use Chrome or Edge and allow permissions.';
        return;
    }

    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: { width: 640, height: 480 } });
    } catch (error) {
        micWarning.textContent = 'Microphone or camera access denied. Please allow permissions and retry.';
        return;
    }

    if (cameraPreview) {
        cameraPreview.srcObject = mediaStream;
        cameraPreview.classList.add('active');
    }

    const audioStream = new MediaStream(mediaStream.getAudioTracks());
    if (!audioStream.getAudioTracks().length) {
        micWarning.textContent = 'No microphone track was found. Please check your device settings.';
        return;
    }

    audioChunks = [];
    micWarning.textContent = '';
    recording = true;
    startRecordingBtn.disabled = true;
    stopRecordingBtn.disabled = false;
    nextQuestionBtn.disabled = true;
    interviewStatus.textContent = 'Recording... speak clearly and confidently.';

    try {
        mediaRecorder = new MediaRecorder(mediaStream);
    } catch (error) {
        micWarning.textContent = 'Your browser cannot record audio/video with the current settings.';
        recording = false;
        return;
    }

    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };
    mediaRecorder.onerror = () => {
        micWarning.textContent = 'Recording failed. Please try again or use a supported browser.';
    };
    mediaRecorder.onstop = handleRecordingStop;
    mediaRecorder.start(100);

    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;
    const source = audioContext.createMediaStreamSource(audioStream);
    source.connect(analyser);
    volumeSamples = [];
    volumeInterval = setInterval(sampleVolume, 200);

    if (recognition && !listening) {
        recognition.start();
        listening = true;
    }
}

function sampleVolume() {
    if (!analyser) return;
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteTimeDomainData(dataArray);
    let sum = 0;
    for (let i = 0; i < dataArray.length; i += 1) {
        const value = dataArray[i] - 128;
        sum += value * value;
    }
    const rms = Math.sqrt(sum / dataArray.length);
    volumeSamples.push(rms);
}

function stopRecording() {
    if (!recording) return;
    recording = false;
    stopRecordingBtn.disabled = true;
    startRecordingBtn.disabled = false;
    interviewStatus.textContent = 'Processing your response...';

    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    if (mediaStream) {
        mediaStream.getTracks().forEach((track) => track.stop());
    }
    if (cameraPreview) {
        cameraPreview.srcObject = null;
    }
    if (volumeInterval) {
        clearInterval(volumeInterval);
        volumeInterval = null;
    }
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }
    if (recognition && listening) {
        recognition.stop();
        listening = false;
    }
}

function handleRecordingStop() {
    const audioBlob = new Blob(audioChunks, { type: 'video/webm' });
    const audioUrl = URL.createObjectURL(audioBlob);
    if (videoPlayback) {
        videoPlayback.hidden = false;
        videoPlayback.src = audioUrl;
        videoPlayback.controls = true;
        videoPlayback.play().catch(() => {});
    }
    if (audioPlayback) {
        audioPlayback.hidden = true;
    }

    const transcript = transcriptArea.value.trim();
    const words = transcript.split(/\s+/).filter(Boolean).length;
    const averageVolume = volumeSamples.length ? volumeSamples.reduce((sum, value) => sum + value, 0) / volumeSamples.length : 0;
    const volumeScore = Math.min(100, Math.round(averageVolume * 4.5 + 20));
    const contentScore = Math.min(100, Math.round(Math.min(1, words / 35) * 60 + (transcript.length > 0 ? 30 : 0)));
    const cameraActiveScore = mediaStream && mediaStream.getVideoTracks().length ? 90 : 40;
    const confidenceScore = Math.min(100, Math.round((volumeScore * 0.45) + (contentScore * 0.35) + (cameraActiveScore * 0.2)));
    const responseScore = Math.min(100, Math.round((contentScore * 0.55) + (confidenceScore * 0.45)));

    const responseData = {
        question: questions[currentIndex],
        transcript: transcript || 'No transcription available. Use the recording playback to review your answer.',
        words,
        audioUrl,
        volumeScore,
        contentScore,
        cameraActiveScore,
        confidenceScore,
        responseScore,
    };

    answerResponses[currentIndex] = responseData;
    renderResponseItem(responseData);
    interviewStatus.textContent = 'Answer saved. Click Next to continue.';
    nextQuestionBtn.disabled = false;
}

function renderResponseItem(data) {
    const existingItem = document.querySelector(`[data-question-index="${currentIndex}"]`);
    if (existingItem) existingItem.remove();
    const item = document.createElement('div');
    item.className = 'response-item glass-panel';
    item.dataset.questionIndex = currentIndex;
    item.innerHTML = `
        <div class="response-header">
            <strong>Question ${currentIndex + 1}</strong>
            <span>Score ${data.responseScore}</span>
        </div>
        <p class="response-question">${data.question}</p>
        <p class="response-transcript">${data.transcript}</p>
        <div class="response-badges">
            <span>Voice: ${data.volumeScore}</span>
            <span>Content: ${data.contentScore}</span>
            <span>Camera: ${data.cameraActiveScore}</span>
            <span>Confidence: ${data.confidenceScore}</span>
        </div>
    `;
    responsesList.appendChild(item);
}

function nextQuestion() {
    if (recording) {
        stopRecording();
    }
    if (!answerResponses[currentIndex]) {
        interviewStatus.textContent = 'Please record your answer before moving to the next question.';
        return;
    }

    if (currentIndex + 1 < questions.length) {
        currentIndex += 1;
        updateQuestion();
        speakQuestion(questions[currentIndex]);
    } else {
        finishInterview();
    }
}

function replayQuestion() {
    speakQuestion(questions[currentIndex]);
    interviewStatus.textContent = 'Question replayed. Start recording when you are ready.';
}

function finishInterview() {
    const totalResponses = answerResponses.filter(Boolean);
    const overall = totalResponses.length
        ? Math.round(totalResponses.reduce((sum, item) => sum + item.responseScore, 0) / totalResponses.length)
        : 0;
    const averageConfidence = totalResponses.length
        ? Math.round(totalResponses.reduce((sum, item) => sum + item.confidenceScore, 0) / totalResponses.length)
        : 0;
    const averageCommunication = totalResponses.length
        ? Math.round(totalResponses.reduce((sum, item) => sum + item.contentScore, 0) / totalResponses.length)
        : 0;

    overallScoreEl.textContent = `${overall}`;
    confidenceScoreEl.textContent = `${averageConfidence}`;
    communicationScoreEl.textContent = `${averageCommunication}`;
    suggestionText.textContent = totalResponses.length === questions.length
        ? 'Great work! Review your responses and practice pacing, clarity, and confidence for the next round.'
        : 'Complete all questions to get a more accurate interview score. Review the responses above and try again.';

    summaryPanel.classList.remove('hidden');
    startInterviewBtn.disabled = false;
    startInterviewBtn.textContent = 'Restart Interview';
    interviewStatus.textContent = 'Interview complete. Review your scores below.';
    startRecordingBtn.disabled = true;
    stopRecordingBtn.disabled = true;
    nextQuestionBtn.disabled = true;
    replayQuestionBtn.disabled = true;
}

if (startInterviewBtn) {
    startInterviewBtn.addEventListener('click', startInterview);
}

if (startRecordingBtn) {
    startRecordingBtn.addEventListener('click', startRecording);
}

if (stopRecordingBtn) {
    stopRecordingBtn.addEventListener('click', stopRecording);
}

if (nextQuestionBtn) {
    nextQuestionBtn.addEventListener('click', nextQuestion);
}

if (replayQuestionBtn) {
    replayQuestionBtn.addEventListener('click', replayQuestion);
}
