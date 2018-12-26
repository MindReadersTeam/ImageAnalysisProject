const canvas = document.getElementById('canvas');
const video = document.getElementById('video');


handleCamera();

document.getElementById('snap').addEventListener('click', () => {
    takeScreenshot();
});

document.body.addEventListener('keypress', (e) => {
    if (e.keyCode === 32) {
        takeScreenshot();
    }
});

function handleCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const params = {
            video: {
                width: { ideal: 1920 },
                height: { ideal: 1080 },
                aspectRatio: 1.7777777778
            },
            audio: false
        };

        navigator.mediaDevices.getUserMedia(params)
            .then((stream) => {
                window.stream = stream;
                video.srcObject = stream;
                video.play();
            })
            .catch((err) => {
                console.error(err);
            });
    }
}

function takeScreenshot() {
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    let left = canvas.offsetLeft - video.offsetLeft + canvas.clientLeft;
    let top = canvas.offsetTop - video.offsetTop + canvas.clientTop;

    const context = canvas.getContext('2d');

    context.drawImage(video, left, top, canvas.width, canvas.height,
        0, 0, canvas.width, canvas.height);

    setTimeout(() => {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }, 1000);
}