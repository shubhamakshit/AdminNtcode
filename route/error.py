from flask import *
errors = Blueprint('errors', __name__, template_folder='templates')
app= errors

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
