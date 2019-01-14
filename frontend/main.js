const canvas = document.getElementById('canvas');
const video = document.getElementById('video');

const URL = 'http://192.168.0.220:5000';
const endpoint = 'uploadImg';


handleCamera();
document.getElementById('snap').addEventListener('click', () => {
    takeScreenShot();
});

const handleSpaceBar = debounce(function(e) {
  if (e.code === "Space") {
    takeScreenShot();
  }
}, 500, true);
document.body.addEventListener('keydown', handleSpaceBar);

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

  const left = canvas.offsetLeft - video.offsetLeft + canvas.clientLeft;
  const top = canvas.offsetTop - video.offsetTop + canvas.clientTop;

  const context = canvas.getContext('2d');
  context.drawImage(video, left, top, canvas.width, canvas.height, 0, 0, canvas.width, canvas.height);

  const body = getRequestBody();

  sendImage(body)
    .then(json => {
        const image = new Image();
        image.onload = () => canvas.getContext('2d').drawImage(image, 0, 0);
        image.src = `data:image/jpg;base64,${JSON.parse(json).file}`;

        // Maybe add key board event on the image and also save the filepath from JSON
        clearCanvas(2500);
    });
}

const sendImage = (body) => {
  return fetch(`${URL}/${endpoint}`, {
    method: "post",
    headers: {
      "Content-Type": "application/json"
    },
    body
  })
    .then(response => response.text())
    .catch(err => console.error(err));
};

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

function debounce(func, wait, immediate) {
  let timeout;
  return function() {
    const context = this, args = arguments;
    const later = () => {
      timeout = null;
      if (!immediate) {
        func.apply(context, args);
      }
    };

    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) {
      func.apply(context, args);
    }
  };
}
