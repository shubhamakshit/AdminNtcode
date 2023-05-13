from flask import *
profile = Blueprint('profile', __name__, template_folder='templates')
app= profile
from mongo import Mongo
user_collection = Mongo().getUserCollection()
usercode_collection = Mongo().getUserCodeCollection()
@app.route('/logout')
@app.route('/logout/')
def logout():
    session.pop('username', None)

    return redirect('/')

@app.route("/profile", methods=["GET", "POST"])
@app.route("/profile/", methods=["GET", "POST"])
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
@app.route("/delete/<name>/", methods=["GET", "POST"])
def delete(name):
    # Delete the entry with the given id

    result = usercode_collection.delete_one({"name": name})

    # Check if the entry was successfully deleted

    if result.deleted_count == 1:

        # Redirect to the list page
        return render_template('alert.html', title="Done!", text="Successfully Deleted the entry", icon="success",
                               red='list')

    else:

        # Return an error message if the entry was not deleted

        return render_template('alert.html', title="Error!", text="Could not delete the entry", icon="error",
                               red='list')















@app.route('/change/password',methods=['POST','GET'])
@app.route('/change/password/',methods=['POST','GET'])
def chpass():
    """
    This function handles the password change functionality.
    
    It is accessed through the routes '/change/password' and '/change/password/' with both GET and POST methods.
    """
    
    if not "username" in session:
        # If the "username" key is not present in the session, the user is not logged in.
        # An alert page is rendered with an error message indicating that the user is not logged in.
        return render_template('alert.html', title="Fatal!", text="User not logged in!", icon="error", red='')
    
    if request.method == 'POST':
        # If the request method is POST, the form data is used for password change.
        
        oldpass = request.form['old_password']
        
        if oldpass == user_collection.find_one({'username': session["username"]})['password']:
            # The entered old password is compared with the stored password for the user.
            
            if request.form['new_password'] == request.form['confirm_password']:
                # The new password and the confirm password fields are checked to ensure they match.
                
                # If they match, the password for the user is updated with the new password in the database.
                user_collection.update_one({"username": session['username']}, {"$set": {"password": request.form['new_password']}})
                
                # An alert page is rendered with a success message indicating that the password has been changed successfully.
                # The "red" parameter is set to 'profile' to redirect the user to the profile page.
                return render_template('alert.html', title="Done", text="Password Changed Successfully", icon="success", red='profile')
            
            else:
                # If the new password and the confirm password fields do not match,
                # an alert page is rendered with an error message indicating the mismatch.
                # The "red" parameter is set to 'change/password/' to redirect the user back to the password change page.
                return render_template('alert.html', title="Fatal!", text="Passwords do not match", icon="error", red='change/password/')
        
        else:
            # If the entered old password does not match the stored password for the user,
            # an alert page is rendered with an error message indicating the wrong old password.
            # The "red" parameter is set to 'change/password/' to redirect the user back to the password change page.
            return render_template('alert.html', title="Fatal!", text="Old password is wrong", icon="error", red='change/password/')
    
    # If the request method is not POST, the password change form is rendered.
    return render_template('chpass.html')
