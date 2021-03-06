from flask import Flask,request,jsonify
from flask_cors import CORS
import json
app = Flask(__name__ ,  static_url_path='/static')
CORS(app)
OTP_RESPONSE = {
    "message":"",
    "status" : True
}

LEADING_API_KW = ""

USERNAME  = ['admin']
OTP_EXPIRY_TIME = 60*60 #seconds

OTP = {}

class NotAuthorised(Exception):
    pass

@app.errorhandler(404)
def page_not_found(e):
    print("Page not found")
    return app.send_static_file('index.html')

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    if  request.method == "OPTIONS":

        return "",200
    else:
        print(error)
        response = "Something went wront"
        print(response , error)
        return app.send_static_file("index.html")
        # return "Something went wrong" , 200

@app.errorhandler(NotAuthorised)
def handle_invalid_usage(error):
    print(error)
    response = "Not authorised"
    print(response)
    return "Dont try to act smart" , 403

@app.before_request
def before_request():
    try:
        print(request.endpoint)

        if  (request.endpoint=="_static" or request.endpoint == "static"):
            print("static")
            return

        if  (request.endpoint=="generateOtp") or (request.endpoint=="mobileLoginWithEncryption" or (request.endpoint=="mobileLoginWithPlain")):
            print("mobieOTP")
            return


        Headers = request.headers
        if not Headers["Authorization"]:
            raise NotAuthorised()

        Auth = str(Headers["Authorization"] )
        import base64
        Auth = (base64.b64decode( Auth).decode('utf-8') )

        Auth = Auth.split(":")
        print(Auth)
        if not len(Auth) == 3:
            raise NotAuthorised()

        _user = Auth[1]
        _password= Auth[2]



        if Auth[0] == "otp":

            if OTP[_user]["otp"] == _password:
                return
            else:
                raise NotAuthorised()
        elif Auth[0] == "login":
            if  _user in USERNAME and _password == "India@123":
                return
            else:
                raise NotAuthorised()
            pass
        else:
            raise NotAuthorised()
    except:
        raise NotAuthorised()





def generateOTP():
    import random
    from random import randint
    rand_int = randint(0, 9999)  # randint is inclusive at both ends
    OTP = str(rand_int).zfill(4)
    return OTP





@app.route(LEADING_API_KW+ '/validateOTP')
def validateOTP():
    username = request.args.get('username')
    otp = request.args.get('otp')

    if not username in USERNAME:
        raise Exception(username+" no found!")

    import time

    if username in OTP.keys():
        _time = OTP[username]["time"]
        _now  = time.time()

        print(_now, _time)

        if (_now >= _time):
            del OTP[username]
            OTP_RESPONSE["status"]  = False
            OTP_RESPONSE["message"]  = "OTP Expired"

        else:
            if otp == OTP[username]["otp"]:
                OTP_RESPONSE["status"] = True
                OTP_RESPONSE["message"] = "Correct OTP"
                del OTP[username]
            else:
                OTP_RESPONSE["status"] = False
                OTP_RESPONSE["message"] = "Incorrect OTP"

    else:
        OTP_RESPONSE["status"] = False
        OTP_RESPONSE["message"] = "Please generate an OTP first"

    return str(OTP_RESPONSE)

@app.route(LEADING_API_KW+'/generateOtp')
def generateOtp():
    username = request.args.get('username')
    if not username in USERNAME:
        raise Exception(username+" no found!")
    import time
    OTP[username]= {
        "otp":generateOTP(),
        "time": (time.time() + OTP_EXPIRY_TIME)

                       }

    print(OTP[username])

    return jsonify({"message":"4 digit OTP has been generated, you can use it login via it for next 60 minutes"})

@app.route(LEADING_API_KW+'/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    return 'Hello World!'+username

@app.route('/')
def _static():
    return app.send_static_file('index.html')
    # username = request.args.get('username')
    # return 'Hello World!'+str(username)

Templates = {"list":
                 [


{"template":"15.Life is 10% what happens to me and 90% of how I react to it."},
{"template":"The most common way people give up their power is by thinking they don’t have any."},
{"template":"The mind is everything. What you think you become."},
{"template":"The best time to plant a tree was 20 years ago. The second best time is now."},
{"template":"An unexamined life is not worth living."},
{"template":"Eighty percent of success is showing up."},
{"template":"Your time is limited"},
{"template":"Winning isn’t everything"},
{"template":"I am not a product of my circumstances. I am a product of my decisions."},
{"template":"Every child is an artist.  The problem is how to remain an artist once he grows up."},
{"template":"You can never cross the ocean until you have the courage to lose sight of the shore."},
{"template":"I’ve learned that people will forget what you said"},
{"template":"Either you run the day"},
{"template":"Whether you think you can or you think you can’t"},
{"template":"The two most important days in your life are the day you are born and the day you find out why."},
{"template":"Whatever you can do"},
{"template":"The best revenge is massive success."},

                 ]
             }

Entities = {"list":
                 [{"name":"Kevin Kruse"},
{"name":"Napoleon Hill"},
{"name":"Albert Einstein"},
{"name":"Robert Frost"},
{"name":"Florence Nightingale"},
{"name":"Wayne Gretzky"},
{"name":"Michael Jordan"},
{"name":"Amelia Earhart"}]
             }

app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route(LEADING_API_KW+'/createEntity', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    print("myfile")
    file = request.files['myfile']


    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        # filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup

        import os
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return {}


@app.route(LEADING_API_KW+'/Entity')
def xss():
    query = request.args.get('query')

    message = "Sorry, coudn't find " + str(query)


    return   str(message )



@app.route(LEADING_API_KW+'/listTemplates')
def getTemplates():
    return jsonify(Templates)

@app.route(LEADING_API_KW+'/api/ping')
def checkPing():
    return jsonify({})

@app.route(LEADING_API_KW+'/listEntities')
def getEntities():
    return jsonify(Entities)
@app.route(LEADING_API_KW +'/createTemplate',methods=["POST"])
def createTemplate():
    content = request.get_json(silent=True)
    if content[ "template"]:
        Templates["list"].insert( 0 ,content )
    else:
        raise Exception("opz")
    return jsonify(content)


MOBILE_PASSWORD = "SecurityBreakDown"
MOBILE_PASSWORD_ENCRYPTED = "7ECEBD6CEB6473DD66EB0F298176A680CF8DBEAAB41A685D000972816891934B"
# MOBILE_PASSWORD_ENCRYPTED = "7ECEBD6CEB6473DD66EB0F298176A680CF8DBEAAB41A685D000972816891934B"



@app.route('/mobileLoginWithEncryption',methods=["POST"])
def mobileLoginWithEncryption():
    try:
        email = request.form['email']
        password = request.form['password']
        print(email)
        print(password)
        print(MOBILE_PASSWORD_ENCRYPTED)

        if password == MOBILE_PASSWORD_ENCRYPTED:

            return jsonify( {"status":True , "message":"Valid Credentials"} )
        else:
            raise Exception()
    except:
        return jsonify( {"status":False , "message":"Invalid Credentials"} )

@app.route('/mobileLoginWithPlain',methods=["POST"])
def mobileLoginWithPlain():
    try:
        email = request.form['email']
        password = request.form['password']
        print(email)
        print(password)


        if password == MOBILE_PASSWORD:

            return jsonify( {"status":True , "message":"Valid Credentials"} )
        else:
            raise Exception()
    except:
        return jsonify( {"status":False , "message":"Invalid Credentials"} )





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
