from flask import request, jsonify, Blueprint
import os
import json
import base64
from img_processing import process_dir

upload_api = Blueprint('upload_api', __name__)

mainImgDir = '../images/'

@upload_api.route('/uploadImg', methods=['POST', 'GET'])
def uploadImg():
	if request.method == 'POST' :	
			requestData = request.get_json()
			
			if 'file' in requestData and 'type' in requestData:
				saveImg(requestData['file'], requestData['type'])
				increaseImgCounter(requestData['type'])
				process_dir(mainImgDir + 'raw/' + requestData['type'], mainImgDir + 'processed/' + requestData['type'], True)

			return jsonify({'filepath' : requestData['type'] + '/' + getImgFileName(requestData['type']), 'file' : getEncodedStringOfProcessedImg(requestData['type'])})
	
	return 'Error'

@upload_api.route('/removeImg', methods=['POST', 'GET'])
def removeImg():
	if request.method == 'POST':
		requestData = request.get_json()

		if 'filepath' in requestData:
			deleteImgs(requestData['filepath'])
			reduceImgCounter(requestData['filepath'].split('/', 1)[0])

		return 'File removed'
	return 'Error'

def deleteImgs(filePath):
		try:
			os.remove(mainImgDir + 'raw/' + filePath)
			os.remove(mainImgDir + 'processed/' + filePath)
		except:
			return 'Cannot remove file'


def getEncodedStringOfProcessedImg(type):
	with open(mainImgDir + 'processed/' + type + '/' + getImgFileName(type), 'rb') as file:
			encodedImg = base64.b64encode(file.read())

	return encodedImg

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
