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

# dannii pushes
@app.route('/home')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM drinks_inventory")
    data = cursor.fetchall()
    cursor.close()

    return render_template('index.html', drinks=data)

#dannii pushes
@app.route("/insert", methods=["POST"])
def insert():
    name = request.form['name of drink']
    price = request.form['price']
    quantity = request.form['quantity']
    expiry_date = request.form['expiry date']
    batch_number = request.form['batch number']
    drink_subtype = request.form['drink subtype']

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM drinks_inventory WHERE name_of_drink = %s", (name,))
    existing = cursor.fetchone()

    if existing:
        flash(F"{name} already exists!","warning")
        cursor.close()
        return redirect(url_for('index'))

    cursor.execute("""INSERT INTO drinks_inventory (name_of_drink, price, quantity, expiry_date, batch_number, drink_subtype)   VALUES (%s, %s, %s, %s, %s, %s)""", (name, price, quantity, expiry_date, batch_number, drink_subtype))

    mysql.connection.commit()
    flash(f'{name} added successfully!') 
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__': 
    app.run(debug=True) 