import re
import os
import pytesseract
from PIL import Image
import ftfy


def aadharRecog(img_data):
    # data = request.get_json()
    # if not "img" in data:
    #     print("img is required")
    #     return jsonify(error="img is required"), 422
    # # Save Image
    # img_data = data["img"]
    imgPath = img_data
    # imgPath = convert_and_save(img_data)
    # Check for Blurry Image
    # img = cv2.imread(imgPath)
    # img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # var = cv2.Laplacian(img, cv2.CV_64F).var()
    # if var < 50:
    #     print("img is too blurry")
    #     return jsonify(error="img is too blurry"), 422
    # Read Text
    text = pytesseract.image_to_string(Image.open(imgPath), lang="eng")
    # print(text)
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    data = adhaar_read_data(text)
    # Delete File
    os.remove(imgPath)
    return data


def adhaar_read_data(text):
    res = text.split()
    print(res)
    name = None
    dob = None
    adh = None
    sex = None
    text0 = []
    text1 = []
    lines = text.split("\n")
    for lin in lines:
        s = lin.strip()
        s = lin.replace("\n", "")
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    if "female" in text.lower():
        sex = "FEMALE"
    else:
        sex = "MALE"

    text1 = list(filter(None, text1))
    text0 = text1[:]
    print(text0)
    try:

        # Cleaning first names
        name = text0[0]
        print(name)
        name = name.rstrip()
        name = name.lstrip()
        name = name.replace("8", "B")
        name = name.replace("0", "D")
        name = name.replace("6", "G")
        name = name.replace("1", "I")
        name = re.sub("[^a-zA-Z] +", " ", name)

        # Cleaning DOB
        for date in res: 
            if(date.count("/") == 2 ): 
                dob = date
                break


        # dob = text0[1][-10:]
        # dob = dob.rstrip()
        # dob = dob.lstrip()
        # dob = dob.replace("l", "/")
        # dob = dob.replace("L", "/")
        # dob = dob.replace("I", "/")
        # dob = dob.replace("i", "/")
        # dob = dob.replace("|", "/")
        # dob = dob.replace('"', "/1")
        # dob = dob.replace(":", "")
        # dob = dob.replace(" ", "")

        # Cleaning Adhaar number details
        aadhar_number = ""
        for word in res:
            if len(word) == 4 and word.isdigit():
                aadhar_number = aadhar_number + word + " "
        if len(aadhar_number) >= 14:
            print("Aadhar number is :" + aadhar_number)
            adh = aadhar_number
        else:
            print("Aadhar number not read")
            adh = "Aadhar number is not found "

    except:
        pass

    data = {}
    data["name"] = name
    data["dob"] = dob
    data["aadhar_number"] = adh.strip()
    data["gender"] = sex
    
    return data


# aadhar = Blueprint("aadhar", __name__, url_prefix="/aadhar")

# tempPath = os.path.join(os.path.dirname(
#     os.path.realpath(__file__)), "..", "tmp")
# if not os.path.exists(tempPath):
#     os.mkdir(tempPath)


def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split()
        if [w for w in xx if re.search(wordstring, w)]:
            lineno = textlist.index(wordline)
            textlist = textlist[lineno + 1:]
            return textlist
    return textlist


# def convert_and_save(data):
#     im = Image.open()
#     fileName = str(uuid.uuid4()) + ".png"
#     filePath = os.path.join(tempPath, fileName)
#     im.save(filePath)
#     return filePath
