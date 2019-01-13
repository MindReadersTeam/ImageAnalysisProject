const canvas = document.getElementById('canvas');
const video = document.getElementById('video');

const URL = 'http://192.168.0.220:5000';
const endpoint = 'uploadImg';

handleCamera();

document.getElementById('snap').addEventListener('click', () => {
    takeScreenShot();
});

document.body.addEventListener('keypress', (e) => {
    //TODO: Add appropriate keyboard handling and debouncing
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

  const body = getRequestBody().toString();

  fetch(`${URL}/${endpoint}`, {
    method: "post",
    headers: {
      'Content-Type': 'application/json'
    },
    body
  })
    .then(response => response.text())
    .then(json => {
      const image = new Image();
      image.onload = () => canvas.getContext('2d').drawImage(image, 0, 0);
      image.src = `data:image/jpg;base64,${JSON.parse(json).file}`;

      clearCanvas(2500);
    })
    .catch(err => console.error(err));

  // TODO: check if without get_json(force=true)
  // var oReq = new XMLHttpRequest();
  // oReq.onload = (response) => {
  //   console.log(response.currentTarget.responseText);
  //   const resImg = JSON.parse(response.currentTarget.responseText);
  //
  //   var image = new Image();
  //   image.onload = function() {
  //     canvas.getContext('2d').drawImage(image, 0, 0);
  //   };
  //   image.src = "data:image/png;base64," + resImg.file;
  //
  //   clearCanvas(2500);
  // };
  // oReq.overrideMimeType("application/json");
  // oReq.open("POST", `${URL}/${endpoint}`);
  // oReq.send(getRequestBody());
}

const getRequestBody = () =>
  JSON.stringify({
    file: getBase64Image(),
    type: 'like'
    //TODO: get type from select
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