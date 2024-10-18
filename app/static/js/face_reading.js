document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const cameraBtn = document.getElementById('cameraBtn');
    const videoFeed = document.getElementById('videoFeed');
    const capturedImage = document.getElementById('capturedImage');
    const captureBtn = document.getElementById('captureBtn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const reportElement = document.getElementById('report');
    const analyzedImage = document.getElementById('analyzedImage');
    const placeholderText = document.getElementById('placeholderText');
    const faceDetectionStatus = document.getElementById('faceDetectionStatus');

    let stream;
    let isCameraOn = false;
    let recognitionInterval;

    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                capturedImage.src = e.target.result;
                capturedImage.classList.remove('hidden');
                videoFeed.classList.add('hidden');
                placeholderText.classList.add('hidden');
            };
            reader.readAsDataURL(file);
        }
    });

    cameraBtn.addEventListener('click', async () => {
        if (!isCameraOn) {
            try {
                const response = await fetch('/start-camera', { method: 'POST' });
                const result = await response.json();
                if (result.error) {
                    console.error(result.error);
                    return;
                }
                stream = await navigator.mediaDevices.getUserMedia({ video: true });
                videoFeed.srcObject = stream;
                videoFeed.classList.remove('hidden');
                captureBtn.classList.remove('hidden');
                capturedImage.classList.add('hidden');
                placeholderText.classList.add('hidden');
                videoFeed.play();
                isCameraOn = true;
                cameraBtn.innerHTML = '(⭐️AI 실시간 분석⭐️)<br>카메라 닫기';
                cameraBtn.classList.remove('bg-green-500', 'hover:bg-green-700');
                cameraBtn.classList.add('bg-red-500', 'hover:bg-red-700');
                
                startFaceRecognition();
            } catch (err) {
                console.error("Error accessing camera:", err);
            }
        } else {
            stopCamera();
        }
    });

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        videoFeed.classList.add('hidden');
        captureBtn.classList.add('hidden');
        placeholderText.classList.remove('hidden');
        isCameraOn = false;
        cameraBtn.innerHTML = '(⭐️AI 실시간 분석⭐️)<br>카메라 열기';
        cameraBtn.classList.remove('bg-red-500', 'hover:bg-red-700');
        cameraBtn.classList.add('bg-green-500', 'hover:bg-green-700');
        fetch('/stop-camera', { method: 'POST' });
        
        stopFaceRecognition();
    }

    function startFaceRecognition() {
        recognitionInterval = setInterval(async () => {
            const canvas = document.createElement('canvas');
            canvas.width = videoFeed.videoWidth;
            canvas.height = videoFeed.videoHeight;
            canvas.getContext('2d').drawImage(videoFeed, 0, 0);
            const imageDataUrl = canvas.toDataURL('image/jpeg');

            try {
                const response = await fetch('/recognize-face', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ image: imageDataUrl }),
                });

                const result = await response.json();
                faceDetectionStatus.textContent = result.faces_detected ? '얼굴이 감지되었습니다🐵' : '얼굴이 감지되지 않았습니다.🙈';
            } catch (error) {
                console.error('Error:', error);
            }
        }, 1000);
    }

    function stopFaceRecognition() {
        clearInterval(recognitionInterval);
        faceDetectionStatus.textContent = '';
    }

    captureBtn.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        canvas.width = videoFeed.videoWidth;
        canvas.height = videoFeed.videoHeight;
        canvas.getContext('2d').drawImage(videoFeed, 0, 0);
        capturedImage.src = canvas.toDataURL('image/jpeg');
        capturedImage.classList.remove('hidden');
        videoFeed.classList.add('hidden');
        stopCamera();
    });

    analyzeBtn.addEventListener('click', async function() {
        if (capturedImage.src) {
            reportElement.innerHTML = '외모 분석 중...';
            
            const response = await fetch(capturedImage.src);
            const blob = await response.blob();
            
            const formData = new FormData();
            formData.append('file', blob, 'image.jpg');

            try {
                const response = await fetch('/analyze-face', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.error) {
                    reportElement.innerHTML = result.error;
                } else {
                    reportElement.innerHTML = result.analysis;
                    analyzedImage.src = `data:image/jpeg;base64,${result.image}`;
                    analyzedImage.classList.remove('hidden');
                }
            } catch (error) {
                console.error('Error:', error);
                reportElement.innerHTML = '분석 중 오류가 발생했습니다.';
            }
        } else {
            reportElement.innerHTML = '분석할 이미지가 없습니다. 사진을 업로드하거나 캡처해주세요.';
        }
    });
});
