from flask import Flask,request,url_for,redirect,jsonify
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from prediction import predict
# from prediction import pred
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.debug=True
import uuid

app.config['UPLOAD_FOLDER'] = "./audios"
@app.route('/')
def testing():
  return "Speech API endpoint"


@app.route('/predict',methods=["POST"])
@cross_origin()
def tensor():
  if request.method == "POST":
    filelist = []
    for file in request.form["array"].split(","):
      filelist.append(file)
    accent = predict(filelist)
    return jsonify({"status":200,"accent":accent})


@app.route('/save',methods=["POST"])
@cross_origin()
def saved():
  if request.method == "POST":
    f = request.files['data']
    filename = str(uuid.uuid4())
    name = filename+".wav"
    f.save(secure_filename(name))
    return jsonify({"status":200 , "filename":filename})
	
if __name__ == "__main__":
	app.run()
