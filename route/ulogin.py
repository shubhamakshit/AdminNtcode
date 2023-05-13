from flask import Blueprint,redirect,request,session,url_for,render_template
import mongo
m = mongo.Mongo()
user_collection = m.getUserCollection()
login = Blueprint('login', __name__, template_folder='templates')
app= login
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('form.form'))
    
    if request.method == 'POST':

        # Get the user's input

        username = request.form['username']

        password = request.form['password']

        # Check if the user exists in the database

        user = user_collection.find_one({'username': username, 'password': password})

        if user:

            session['username'] = username

            return redirect('/')

        else:

            return render_template('alert.html', title="Error!", text='Invalid username or password', icon="error",
                                   red="form")

    return render_template('login.html')
