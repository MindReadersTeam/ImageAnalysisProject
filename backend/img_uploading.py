from flask import request, jsonify, Blueprint
import os
import json
import base64
from img_processing import process_and_save_image
from pathlib import Path
import gest_types

upload_api = Blueprint('upload_api', __name__)

mainImgDir = '../imgs/'


def prepareImgDirs():
    for gest_type in gest_types.types:
        (Path(mainImgDir) / "raw" / gest_type).mkdir(parents=True, exist_ok=True)
        (Path(mainImgDir) / "processed" / gest_type).mkdir(parents=True, exist_ok=True)

    try:
        with open(mainImgDir + 'imgNumbers.json', 'r') as file:
            json.load(file)

    except FileNotFoundError:
        with open(mainImgDir + 'imgNumbers.json', 'w') as file:
            json.dump({t: 0 for t in gest_types.types}, file)


prepareImgDirs()

@upload_api.route('/uploadImg', methods=['POST'])
def uploadImg():
    requestData = request.get_json()

    if 'file' in requestData and 'type' in requestData:
        saveImg(requestData['file'], requestData['type'])
        increaseImgCounter(requestData['type'])
        img_fn = getImgFileName(requestData['type'])
        process_and_save_image(mainImgDir + 'raw/' + requestData['type'] + "/" + img_fn,
                               mainImgDir + 'processed/' + requestData['type'] + "/" + img_fn)

    return jsonify({'filepath': requestData['type'] + '/' + img_fn,
                    'file': getEncodedStringOfProcessedImg(requestData['type'])})


@upload_api.route('/removeImg', methods=['POST'])
def removeImg():
    requestData = request.get_json()

    if 'filepath' in requestData:
        deleteImgs(requestData['filepath'])
        reduceImgCounter(requestData['filepath'].split('/', 1)[0])

    return 'File removed'


def deleteImgs(filePath):
    try:
        os.remove(mainImgDir + 'raw/' + filePath)
        os.remove(mainImgDir + 'processed/' + filePath)
    except:
        return 'Cannot remove file'


def getEncodedStringOfProcessedImg(type):
    with open(mainImgDir + 'processed/' + type + '/' + getImgFileName(type), 'rb') as file:
        encodedImg = base64.b64encode(file.read())

    base64_string = encodedImg.decode('utf-8')
    return base64_string


def saveImg(img, type):
    with open(getNewImgPath(type), 'wb') as file:
        file.write(base64.b64decode(img))


def getImgFileName(type):
    with open(mainImgDir + 'imgNumbers.json', 'r') as file:
        imgNumbers = json.load(file)

    return str(imgNumbers[type]) + '.jpg'


def getNewImgPath(type):
    with open(mainImgDir + 'imgNumbers.json', 'r') as file:
        imgNumbers = json.load(file)

    return mainImgDir + 'raw/' + type + '/' + str(imgNumbers[type] + 1) + '.jpg'


def reduceImgCounter(type):
    with open(mainImgDir + 'imgNumbers.json', 'r') as file:
        imgNumbers = json.load(file)

    imgNumbers[type] -= 1

    with open(mainImgDir + 'imgNumbers.json', 'w') as file:
        json.dump(imgNumbers, file)


def increaseImgCounter(type):
    with open(mainImgDir + 'imgNumbers.json', 'r') as file:
        imgNumbers = json.load(file)

    imgNumbers[type] += 1

    with open(mainImgDir + 'imgNumbers.json', 'w') as file:
        json.dump(imgNumbers, file)
