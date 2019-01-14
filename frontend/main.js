const canvas = document.getElementById('canvas');
const video = document.getElementById('video');

const URL = 'http://192.168.0.220:5000';
const uploadEndpoint = 'uploadImg';
const removeEndpoint = 'removeImg';
let capturingFlag = true;


(function handleCamera() {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    const params = {
      video: {
        width: {ideal: 1920},
        height: {ideal: 1080},
        aspectRatio: 1.7777777778
      },
      audio: false
    };

    navigator.mediaDevices.getUserMedia(params)
      .then(stream => {
        window.stream = stream;
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.error(err);
      });
  }
})();

document.getElementById('snap').addEventListener('click', () => takeScreenShot());

const takeScreenShot = () => {
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;

  const left = canvas.offsetLeft - video.offsetLeft + canvas.clientLeft;
  const top = canvas.offsetTop - video.offsetTop + canvas.clientTop;

  const context = canvas.getContext('2d');
  context.drawImage(video, left, top, canvas.width, canvas.height, 0, 0, canvas.width, canvas.height);

  sendImage(getRequestBody())
    .then(json => {
      const image = new Image();
      image.onload = () => canvas.getContext('2d').drawImage(image, 0, 0);
      image.src = `data:image/jpg;base64,${json.file}`;
      document.body.onkeydown = (e) => {
        if (e.code === 'KeyD') {
          removeImage(json.filepath).then(response => {
            restoreHandlingSpaceBar();
          });
        } else {
          restoreHandlingSpaceBar();
        }
      }
    });
};

const restoreHandlingSpaceBar = () => {
  clearCanvas(0);
  capturingFlag = !capturingFlag;
  document.body.onkeydown = handleSpaceBar;
};

const handleSpaceBar = debounce(function (e) {
  if (capturingFlag && e.code === "Space") {
    capturingFlag = !capturingFlag;
    takeScreenShot();
  }
}, 500, true);
document.body.onkeydown = handleSpaceBar;


const sendImage = (body) => {
  return fetch(`${URL}/${uploadEndpoint}`, {
    method: "post",
    headers: {
      "Content-Type": "application/json"
    },
    body
  }).then(response => response.json());
};

const removeImage = (filepath) => {
  return fetch(`${URL}/${removeEndpoint}`, {
    method: "post",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({filepath: filepath})
  }).then(response => response.text());
};

const getRequestBody = () => JSON.stringify({
  file: getBase64Image(),
  type: document.body.querySelector('select').value
});

function getBase64Image() {
  const dataURL = canvas.toDataURL("image/jpeg", .8);
  return dataURL.replace(/^data:image\/(png|jpeg);base64,/, "");
}

const clearCanvas = (timeout) => setTimeout(() => {
  canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
}, timeout);

function debounce(func, wait, immediate) {
  let timeout;
  return function () {
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
