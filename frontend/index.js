const canvas = document.getElementById('canvas');
const video = document.getElementById('video');

const URL = 'https://mindreaders.ml:8553';
const predictEndpoint = 'predict';
const fetchParams = {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: null
};

let capturingFlag = true;

const LABELS = {
  0: 'c_letter',
  1: 'call_me',
  2: 'dislike',
  3: 'fist',
  4: 'hook',
  5: 'like',
  6: 'number_5',
  7: 'ok',
  8: 'victory',
  9: 'w_letter'
};


video.onloadedmetadata = (e) => {
  canvas.style.top = Math.abs(video.videoHeight - canvas.clientHeight) / 2 + "px";
};

(function handleCamera() {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    const params = {
      video: {
        width: {
 //         min: 640,
          ideal: 1920,
          max: window.innerWidth
        },
        height: {
//          min: 640,
          ideal: 1080,
          max: window.innerHeight
        }
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

document.getElementById('snap').addEventListener('click', () => {
  capturingFlag = false;
  takeScreenShot();
});

const handleSpaceBar = debounce(function (e) {
  if (capturingFlag && e.code === "Space") {
    e.preventDefault();
    capturingFlag = false;
    takeScreenShot();
  }
}, 500, true);
document.body.onkeydown = handleSpaceBar;


const takeScreenShot = callback => {
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;

  const left = canvas.offsetLeft - video.offsetLeft + canvas.clientLeft;
  const top = canvas.offsetTop - video.offsetTop + canvas.clientTop;

  const context = canvas.getContext('2d');
  context.drawImage(video, left, top, canvas.width, canvas.height, 0, 0, canvas.width, canvas.height);

  sendImage(getRequestBody())
    .then(json => {
      putLabels(json);
      restoreHandlingSpaceBar();
    });

  function restoreHandlingSpaceBar() {
    clearCanvas(0);
    capturingFlag = true;
    document.body.onkeydown = handleSpaceBar;
  }

  function putLabels(probabilities) {
    const maxProb = Math.max(...probabilities);

    probabilities.map((probability, index) => {
      putLabelFor(LABELS[index], probability);
      if (probability === maxProb) {
        markRecognized(LABELS[index]);
      }
    });
  }

  function markRecognized(recognized) {
    const previous = document.querySelector('.recognized');
    previous && previous.classList.remove('recognized');
    document.querySelector(`.${recognized}`).classList.add('recognized');
  }

  function putLabelFor(className, value) {
    document.body.querySelector(`.${className} span`).innerText = `${(value * 100).toFixed(2)}%`;
  }
};

const sendImage = (body) => {
  return fetch(`${URL}/${predictEndpoint}`, {...fetchParams, body})
    .then(response => response.json());
};


const getRequestBody = () => JSON.stringify({
  file: getBase64Image()
});

const getBase64Image = () => {
  const dataURL = canvas.toDataURL("image/jpeg", .8);
  return dataURL.replace(/^data:image\/(png|jpeg);base64,/, "");
};

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
