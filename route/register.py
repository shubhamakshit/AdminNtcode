from flask import *
from mongo import Mongo
user_collection = Mongo().getUserCollection()
register = Blueprint('register', __name__, template_folder='templates')
app= register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(url_for('form'))

    if request.method == 'POST':

        # Get the user's input

        name = request.form['name']

        username = request.form['username']

        bio = request.form['bio']

        password = request.form['password']

        password2 = request.form['password2']

        # Check if the passwords match

        if password != password2:
            return render_template('alert.html', title="Error!", text='Passwords do not match', icon="error",
                                   red="login")

        # Check if the user already exists

        existing_user = user_collection.find_one({'username': username})

        if existing_user:
            return render_template('alert.html', title="Error!", text='Username already exists', icon="error",
                                   red="login")

        # Insert the new user into the database

        user_collection.insert_one({'name': name, 'username': username, 'bio': bio, 'password': password})

        # Log the user in

        session['username'] = username

        return redirect('/')

    return render_template('register.html')