from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "https://mindreaders.ml"
    header["Access-Control-Allow-Headers"] = "*"
    header["Access-Control-Allow-Methods"] = "*"
    return response

from img_uploading import upload_api
app.register_blueprint(upload_api)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
