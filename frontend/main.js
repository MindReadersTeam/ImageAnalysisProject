const canvas = document.getElementById('canvas');
const video = document.getElementById('video');


handleCamera();

document.getElementById('snap').addEventListener('click', () => {
    takeScreenShot();
});

document.body.addEventListener('keypress', (e) => {
    //TODO: Add appropriate keyboard handling
    if (e.keyCode === 32) {
        takeScreenShot();
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

function takeScreenShot() {
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    let left = canvas.offsetLeft - video.offsetLeft + canvas.clientLeft;
    let top = canvas.offsetTop - video.offsetTop + canvas.clientTop;

    const context = canvas.getContext('2d');

    context.drawImage(video, left, top, canvas.width, canvas.height,
        0, 0, canvas.width, canvas.height);

  console.log(getRequestBody());

  fetch('http://192.168.0.220:5000/uploadImg', {
    method: "POST",
    mode: "no-cors",
    headers: {
      "Content-Type": "application/json"
    },
    body: getRequestBody()
  })
    .then(response => response.json())
    .then(json => {
      console.log(json);
      clearCanvas(500);
    });

  // var oReq = new XMLHttpRequest();
  // oReq.addEventListener("load", (response) => console.log(response.json()));
  // oReq.overrideMimeType("application/json");
  // oReq.open("POST", "http://192.168.0.220:5000/uploadImg");
  // oReq.send(getRequestBody());
}

const getRequestBody = () =>
  JSON.stringify({
    file: getBase64Image(),
    type: 'ok'
});

function getBase64Image() {
    const dataURL = canvas.toDataURL("image/jpeg", .8);
    return dataURL.replace(/^data:image\/(png|jpeg);base64,/, "");
}

function clearCanvas(timeout) {
    setTimeout(() => {
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    }, timeout);
}