from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.after_request
def after_request(response):
    header = response.headers
    #header["Access-Control-Allow-Origin"] = "https://mindreaders.ml"
    header["Access-Control-Allow-Origin"] = "*"
    header["Access-Control-Allow-Headers"] = "content-type"
    header["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

from img_uploading import upload_api
from img_predicting import predict_api
app.register_blueprint(upload_api)
app.register_blueprint(predict_api)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
