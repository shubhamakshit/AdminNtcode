from flask import Flask, render_template, request, session, redirect,url_for
from pymongo import *
import urllib.parse
from pygments import highlight
from pygments.lexers import JavaLexer
from pygments.formatters import HtmlFormatter
app = Flask(__name__)
app.secret_key = 'bossBigBoss'

client = MongoClient('mongodb+srv://akshit:akshit@cluster0.dcipu28.mongodb.net/?retryWrites=true&w=majority',tls=True,
                             tlsAllowInvalidCertificates=True)
db = client['userdata']
user_collection = db['userlist']
usercode_collection=db['usercode']
@app.route('/')
def index():
    print(user_collection.find({}))
    if 'username' in session:
        return render_template('index.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
      return redirect(url_for('form'))
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
            return render_template('alert.html',title="Error!",text='Invalid username or password',icon="error",red="form")
    return render_template('login.html')

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
            return render_template('alert.html',title="Error!",text='Passwords do not match',icon="error",red="login")
        
        # Check if the user already exists
        existing_user = user_collection.find_one({'username': username})
        if existing_user:
            return render_template('alert.html',title="Error!",text='Username already exists',icon="error",red="login")
        
        # Insert the new user into the database
        user_collection.insert_one({'name': name, 'username': username, 'bio': bio, 'password': password})
        
        # Log the user in
        session['username'] = username
        return redirect('/')
    return render_template('register.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get the user's input
        name = request.form['name'].split(' ')[0]
        name=urllib.parse.unquote(name.strip()).strip()
        description = request.form['description']
        code = request.form['code']
        
        # Check if the user is logged in
        if 'username' not in session:
            return 'You must be logged in to submit code'
        
        # Insert the new code into the database
        author = session['username']
        if usercode_collection.find_one({"name":name}):
          return render_template('alert.html',title="Error!",text="Code Exists",icon="error",red="form")
        usercode_collection.insert_one({'name': name, 'description': description, 'code': code.replace('\\n','\n'), 'author': author})
        # successfull appended
        return render_template('alert.html',title="Done!",text="Successfully Appended the code",icon="success",red='form')
    return render_template('form.html')


@app.route('/form/<name>',methods=['POST','GET'])
def editEntry(name):
    if request.method == 'POST':
        data_temp=usercode_collection.find_one({"name":name})
        description=request.form['description']
        code=request.form['code']
        usercode_collection.update_one({"name":name},{"$set":{"code":code}})
        usercode_collection.update_one({"name":name},{"$set":{"description":description}})
        return render_template('alert.html',title="Done!",text="Successfully Edited the code",icon="success",red='form')
    if not "username" in session:
        return render_template('alert.html',title="Fatal!",text="User not logged in!",icon="error",red='login')
    data=usercode_collection.find_one({"name":name})
    if data:
        if data['author'] == session['username']:
            return render_template('edit.html',name=name,code=data['code'],des=data['code'])
        else:
            return render_template('alert.html',title="Fatal!",text="U must login with Your account to edit .",icon="error",red='profile')
    else:
        return render_template('alert.html',title="Fatal!",text="Could not find code",icon="error",red='list')



@app.route('/list')
def list():
    return render_template('list.html',entries=usercode_collection.find(),x=1)
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        name = request.form["name"]
        bio = request.form["bio"]
        username = session["username"]
        user_collection.update_one({"username": username}, {"$set": {"name": name, "bio": bio}})
        return redirect("/profile")
    elif "username" in session:
        user = user_collection.find_one({"username": session["username"]})
        return render_template("profile.html", name=user["name"], username=user["username"], bio=user["bio"])
    else:
        return redirect("/login")

@app.route("/delete/<name>", methods=["GET", "POST"])
def delete(name):
    # Delete the entry with the given id
    result = usercode_collection.delete_one({"name": name})

    # Check if the entry was successfully deleted
    if result.deleted_count == 1:
        # Redirect to the list page
        return render_template('alert.html',title="Done!",text="Successfully Deleted the entry",icon="success",red='list')
    else:
        # Return an error message if the entry was not deleted
        return render_template('alert.html',title="Error!",text="Could not delete the entry",icon="error",red='list')

#app.run(port=8000,debug=True)