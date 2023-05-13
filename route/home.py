from flask import *
home = Blueprint('home', __name__, template_folder='templates')
app= home
@app.route('/')
@app.route('/home')
@app.route('/home/')
def index():
    #print(user_collection.find({}))
    """for x in usercode_collection.find({}):
        if x['name'].startswith('klcp[k\'p;c'):
            usercode_collection.delete_one({'name': x['name']})"""
    if 'username' in session:
        return render_template('index.html')

    return render_template('index.html')