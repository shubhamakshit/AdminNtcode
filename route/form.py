from flask import *
import urllib.parse

form = Blueprint('form', __name__, template_folder='templates')
app= form
from mongo import Mongo
user_collection = Mongo().getUserCollection()
usercode_collection = Mongo().getUserCodeCollection()

@app.route('/form', methods=['GET', 'POST'])
@app.route('/form/', methods=['GET', 'POST'])
def form():
    if not "username" in session:
        return render_template('alert.html', title="Fatal!", text="User not logged in!", icon="error", red='login')

    if request.method == 'POST':


        ######################################################################################################
        # Get the user's input
        # Try to extract the first name from the "name" field of the form data submitted with the request
        try:
            name = request.form['name'].split(' ')[0]  # Split the name by spaces and take the first element
            name = urllib.parse.unquote(name.strip()).strip()  # Unquote and strip any whitespace from the name
        except KeyError as e:
            # If the "name" field is not found in the form data, raise a KeyError and print an error message
            print("name not found in POST method to /form")
            return str(e)+"\n KeyError in 'name' "
        except:
            return "Error in 'name' in /form/ POST "
        #######################################################################################################
        try:
            sdes=request.form['single'] #single line description
        except:
            return "Error in sdes in /form/ POST \n"
        ######################################################################################################
        # Try to modify the "description" field of the form data using a module called "md"
        try:
            import md
            print(request.form['description'])
            description =request.form['description'].replace('\\n', '\n')
            print(description)
            #des_raw=request.form['description'] 
            # not needed anymore
        except KeyError as e:
            # If the "description" field is not found in the form data, raise a KeyError and print an error message
            print("description not found in POST method to /form")
            return str(e)+" \n error in description (key error) in /form/ POST "
        except:
            return "Error in description in /form/ POST \n"
        ######################################################################################################
        # Try to extract the "code" field from the form data submitted with the request
        code = "//written on ntcode.ml"
        try:
            code = request.form['javacode']
        except:
            return " Unreachable"
        ######################################################################################################
        
        # Check if the user is logged in

        if 'username' not in session:
            return 'You must be logged in to submit code'

        # Insert the new code into the database

        author = session['username']

        if usercode_collection.find_one({"name": name}):
            return render_template('alert.html', title="Error!", text="Code Exists", icon="error", red="form")

        usercode_collection.insert_one(
            {'name': name, 'description': description,"sdes":sdes, 'code': code.replace('\\n', '\n'), 'author': author})
        
        return render_template('alert.html', title="Done!", text="Successfully Appended the code", icon="success",
                               red='form')

    return render_template('form.html')


@app.route('/form/<name>', methods=['POST', 'GET'])
@app.route('/form/<name>/', methods=['POST', 'GET'])
def editEntry(name):
    if request.method == 'POST':
        data_temp = usercode_collection.find_one({"name": name})

        sdes=request.form['single']

        description = request.form['description']

        code = request.form['javacode']

        usercode_collection.update_one({"name": name}, {"$set": {"code": code}})

        usercode_collection.update_one({"name": name}, {"$set": {"sdes": sdes}})

        usercode_collection.update_one({"name": name}, {"$set": {"description": description}})

        return render_template('alert.html', title="Done!", text="Successfully Edited the code", icon="success",
                               red='form')

    if not "username" in session:
        return render_template('alert.html', title="Fatal!", text="User not logged in!", icon="error", red='login')

    data = usercode_collection.find_one({"name": name})

    if data:

        if data['author'] == session['username']:

            return render_template('form.html', name=name, code=data['code'], des=str(data['description']).replace('`','\`'),sdes = data['sdes'],edit="true")

        else:

            return render_template('alert.html', title="Fatal!", text="U must login with Your account to edit .",
                                   icon="error", red='profile')

    else:

        return render_template('alert.html', title="Fatal!", text="Could not find code", icon="error", red='list')
