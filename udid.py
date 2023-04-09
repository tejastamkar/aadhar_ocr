import re
import os
import pytesseract
from PIL import Image
import ftfy


def udidRecog(img_data):

    imgPath = img_data

    text = pytesseract.image_to_string(Image.open(imgPath), lang="eng")
    # print(text)
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    data = udid_read_data(text)
    # # Delete File
    os.remove(imgPath)
    return data


state_codes = ['AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CT', 'DN', 'DD', 'DL', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA',
               'KL', 'LD', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OR', 'PY', 'PB', 'RJ', 'SK', 'TN', 'TG', 'TR', 'UP', 'UT', 'WB']

disabilityTypeOptions = [
    "Acid Attack Victim",
    "Blindness",
    "Cerebral Palsy",
    "Chronic Neurological Conditions",
    "Hearing Impairment",
    "Hemophilia",
    "Intellectual Disability",
    "Leprosy cured",
    "Locomotor Disability",
    "Low Vision",
    "Mental Illness",
    "Mental Retardation",
    "Multiple Disabilities including Deaf Blindness",
    "Multiple Disabilities including Deaf Dumb",
    "Multiple Disability",
    "Multiple Sclerosis",
    "Muscular Dystrophy",
    "Ortho",
    "Parkinson's Disease",
    "Physical Impairment",
    "Short Stature/Dwarfism",
    "Sickle Cell Disease",
    "Specific Learning Disabilities",
    "Speech and Language Disability",
    "Thalassemia",
    "Visual Impairment",
]


def udid_read_data(text):
    res = text.split()
    print(res)
    udid_number = None
    disability_type = None
    disability_percent = None
    udid_issues = None
    text0 = []
    text1 = []
    lines = text.split("\n")
    for lin in lines:
        s = lin.strip()
        s = lin.replace("\n", "")
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    text1 = list(filter(None, text1))
    text0 = text1[:]
    print("\n")
    print(text0)
    # temp = ""
    try:
        for item in res:
            if (len(item) >= 18 and udid_number == None):

                udid_number = getUDIDNumber(item)
        for item in res:
            if (item.count("%") == 1):
                disability_percent = item
            if (item.count("/") == 2):
                if udid_issues == None:
                    udid_issues = item
            if (item in disabilityTypeOptions):
                disability_type = item
        for item in text0:
            if (len(item) >= 18 and udid_number == None):
                udid_number = getUDIDNumber(item)
            for types in disabilityTypeOptions: 
                if(match_percentage(item, types) > 90 ):
                    disability_type = item

        for item in res:
            if (len(item) == 3 and item.count("%") == 1):
                disability_percent = item
            if (item.count("/") == 2):
                if udid_issues == None:
                    udid_issues = item
            if (item in disabilityTypeOptions):
                disability_type = item
           
                
        # Example usage
        s1 = 'The quick brown fox jumped over the lazy dog'
        s2 = 'The brown fox jumped over the lazy dog'

                # Cleaning first names
                # name = text0[0]
                # print(name)
                # name = name.rstrip()
                # name = name.lstrip()
                # name = name.replace("8", "B")
                # name = name.replace("0", "D")
                # name = name.replace("6", "G")
                # name = name.replace("1", "I")
                # name = re.sub("[^a-zA-Z] +", " ", name)

                # Cleaning DOB
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
                # aadhar_number = ""
                # for word in res:
                #     if len(word) == 4 and word.isdigit():
                #         aadhar_number = aadhar_number + word + " "
                # if len(aadhar_number) >= 14:
                #     print("Aadhar number is :" + aadhar_number)
                #     adh = aadhar_number
                # else:
                #     print("Aadhar number not read")
                #     adh = "Aadhar number is not found "

    except:
        pass

    data = {}
    data["udid"] = udid_number
    data["percent"] = disability_percent
    data["doi"] = udid_issues
    data["type"] = disability_type
    # data["gender"] = sex

    return data


# aadhar = Blueprint("aadhar", __name__, url_prefix="/aadhar")

# tempPath = os.path.join(os.path.dirname(
#     os.path.realpath(__file__)), "..", "tmp")
# if not os.path.exists(tempPath):
#     os.mkdir(tempPath)

def getUDIDNumber(text):
    if len(text) >= 2:
        state = ''.join(text[:2])
        if state in state_codes:
            number = ''.join(text[2:16])
            udidnumber = state+number
            return udidnumber
    return None


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

def get_word_list(s):
    # Split the string into words, convert them to lowercase, and return a list
    return s.lower().split()


def match_percentage(s1, s2):
    # Get the word lists for each string
    words1 = get_word_list(s1)
    words2 = get_word_list(s2)

    # Count the number of matching words
    match_count = sum(1 for word in words1 if word in words2)

    # Calculate the percentage of matching words
    percent = match_count / len(words1) * 100

    # Return the percentage as a string with two decimal places
    return percent



