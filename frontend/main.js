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
                width: {
                    min: 640,
                    ideal: 1280
                },
                height: {
                    min: 480,
                    ideal: 720
                },
                aspectRatio: {
                    ideal: 1.7777777778
                }
            }
        };

        navigator.mediaDevices.getUserMedia(params)
            .then((stream) => {
                //video.src = window.URL.createObjectURL(stream);
                video.srcObject = stream;
                video.play();
            })
            .catch(function(err) {
                console.err(err);
            });
    }
}

function takeScreenshot() {
    let beginWidth = (video.clientWidth - canvas.clientWidth) / 2;
    let beginHeight = (video.clientHeight - canvas.clientHeight) / 2;

    const context = canvas.getContext('2d');

    context.drawImage(video, beginWidth, beginHeight, canvas.clientWidth, canvas.clientHeight,
        0, 0, canvas.clientWidth, canvas.clientHeight);

    setTimeout(() => {
        context.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
    }, 1000);
}