import json
import sys
from mongo import Mongo
#working with routes######################################################
sys.path.append('./route/')
import home , ulogin , error , register , form , uprofile ,others
##########################################################################
from flask import *
from pymongo import *
user_collection = Mongo().getUserCollection()
usercode_collection = Mongo().getUserCodeCollection()
app = Flask(__name__)
app.register_blueprint(ulogin.app)
app.register_blueprint(home.app)
app.register_blueprint(error.app)
app.register_blueprint(register.app)
app.register_blueprint(form.app)
app.register_blueprint(uprofile.app)
app.register_blueprint(others.app)
app.secret_key = 'bossBigBoss'
app.run(port=8000, debug=True)
