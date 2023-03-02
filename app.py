from flask import Flask, request
from mycode import aadharRecog
from PIL import Image

from udid import udidRecog
# from werkzeug.utils import secure_filenam
app = Flask(__name__)


@app.route("/", methods=['POST'])
def getfile():
    if request.method == 'POST':
        imageFile = request.files['file']
        imageFile.save("temp.png")
        # imageFile = Image.open(request.files['file'])
        data = aadharRecog("temp.png")
        # print(data["aadhar_number"])
        if (data["aadhar_number"] == "Aadhar number is not found"):
            return "data invaild"
        return data

@app.route("/udid", methods=['POST'])
def getudidFile():
    if request.method == 'POST':
        imageFile = request.files['file']
        imageFile.save("temp.png")
        # imageFile = Image.open(request.files['file'])
        data = udidRecog("temp.png")
        # print(data["aadhar_number"])
        # if (data["aadhar_number"] == "UDID number is not found"):
            # return "data invaild"
        return data


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
