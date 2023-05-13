from flask import *
other = Blueprint('other', __name__, template_folder='templates')
app= other
from mongo import Mongo
user_collection = Mongo().getUserCollection()
usercode_collection = Mongo().getUserCodeCollection()

@app.route('/list')
@app.route('/list/')
def list():
    """
    This function handles the route '/list' and '/list/'.
    
    It renders a template called 'list.html' and retrieves entries from the 'usercode_collection' collection.
    """
    
    # Render the 'list.html' template and pass the entries from the 'usercode_collection' collection to it.
    return render_template('list.html', entries=usercode_collection.find())


@app.route('/download/<username>', methods=['GET'])
@app.route('/download/<username>/', methods=['GET'])
def download_codes(username):
    # get all codes by the user from the database

    user_codes = usercode_collection.find({'author': username})

    # create a list of code dictionaries

    code_list = []

    for code in user_codes:
        code_dict = {

            'title': code['name'],

            'language': code['description'],

            'content': code['code']

        }

        code_list.append(code_dict)

    # convert the list to JSON format

    json_data = json.dumps(code_list, indent=4)

    # create a response with the JSON data and appropriate headers

    response = make_response(json_data)

    response.headers['Content-Disposition'] = 'attachment; filename="{}-codes.json"'.format(username)

    return response

@app.route('/test')
def test():
    import md
    return md.mdfy(usercode_collection.find({"name":"Test"})[0]['description'])


@app.route('/get/code/<name>/')
@app.route('/get/code/<name>')
def getcode(name):
    return "<pre>"+str(usercode_collection.find({"name":name})[0]['code'])+"</pre>"


@app.route('/get/description/<name>')
def getdescription(name):
    import md
    return md.mdfy(usercode_collection.find({"name":name})[0]['description'])


@app.route('/get/sdes/<name>/')
@app.route('/get/sdes/<name>')
def sdes(name):
    return usercode_collection.find({"name":name})[0]['sdes']
@app.route('/download/code/<name>', methods=['GET'])
def download_codes_user(name):
    # get all codes by the user from the database

    user_codes = usercode_collection.find({'name': name})

    # create a list of code dictionaries

    code_list = []

    for code in user_codes:
        code_dict = {

            'title': code['name'],

            'language': code['description'],

            'content': str(code['code'])

        }

        code_list.append(code_dict)

    # convert the list to JSON format

    json_data = json.dumps(code_list, indent=4)

    # create a response with the JSON data and appropriate headers

    response = make_response(json_data)

    response.headers['Content-Disposition'] = 'attachment; filename="{}-codes.json"'.format(name)

    return response