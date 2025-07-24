from flask import Flask, render_template, flash, url_for,request
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'my_secret_key'


# Configuration for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory'

mysql = MySQL(app)
# WELCOME TO DATACOM ... landing page
@app.route('/')
def landing():
    return render_template('landing.html')








if __name__ == '__main__': 
    app.run(debug=True) 