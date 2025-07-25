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

@app.route('/sell')
def sell():
    return render_template('sell.html',)

# dannii pushes
@app.route('/home')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM drinks_inventory")
    data = cursor.fetchall()
    cursor.execute("SELECT * FROM beverages")
    item = cursor.fetchall()
    cursor.execute("SELECT * FROM utensills_inventory")
    uten = cursor.fetchall()
    cursor.close()

    return render_template('index.html', drinks=data, beverages=item, utensills=uten)

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

#samuel pushes

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    cursor = mysql.connection.cursor()

    if request.method == "POST":
        name = request.form['name_of_drink']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor.execute("""
            UPDATE drinks_inventory
            SET name_of_drink = %s, price = %s, quantity = %s, expiry_date = %s, batch_number = %s, subtype = %s
            WHERE ID = %s
        """, (name, price, quantity, expiry_date, batch_number, subtype, id))

        mysql.connection.commit()
        cursor.close()
        flash(f"{name} updated successfully!", "success")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM drinks_inventory WHERE ID = %s", (id,))
    drink = cursor.fetchone()
    cursor.close()
    return render_template("update_drinks.html", drink=drink)

# mary let's push
@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM drinks_inventory WHERE ID = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Drink deleted successfully!", "success")
        return redirect(url_for('index'))

# Beverages inventory
    
@app.route('/insert_beverage', methods=['POST'])
def insert_beverage():
     if request.method == 'POST':
        name = request.form['name_of_item']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form["expiry_date"]
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM beverages WHERE name_of_item = %s",
                       (name,))
        existing = cursor.fetchone()

        if existing:
            flash(f"{name} already exists!", "warning")
            cursor.close()
            return redirect(url_for('index'))
        
        cursor.execute("INSERT INTO beverages (name_of_item, price, quantity, expiry_date, batch_number, subtype) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, price,quantity, expiry_date, batch_number, subtype))
        mysql.connection.commit()
        cursor.close()
        flash(f"{name} added successfully!", "success")
        return redirect(url_for('index'))
        
@app.route("/delete_beverages/<int:id>", methods=["GET"])
def delete_beverages(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM beverages WHERE ID = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Drink deleted successfully!", "success")
        return redirect(url_for('index'))

#samuel pushes

@app.route('/edit_beverages/<int:id>', methods=['GET', 'POST'])
def edit_beverages(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name_of_item']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor.execute(""" UPDATE beverages
                        SET name_of_item = %s, price = %s, quantity =%s, expiry_date = %s, batch_number = %s, subtype = %s
                         WHERE ID = %s
                     """, (name, price, quantity, expiry_date, batch_number, subtype, id))
        mysql.connection.commit()
        cursor.close()
        flash(f"{name} updated successfully!", "success")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM beverages WHERE ID = %s", (id,))
    item = cursor.fetchone()
    cursor.close()
    return render_template("update_beverages.html", beverage=item)


    # Utensils management
@app.route('/insert_utensills', methods=['POST'])
def insert_utensills():
     if request.method == 'POST':
        name = request.form['name_of_item']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor = mysql.connection.cursor()

        cursor.execute(""" INSERT into utensills_inventory(name_of_item, price, quantity, expiry_date, batch_number, subtype)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                       (name, price, quantity, expiry_date, batch_number, subtype))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))
     

@app.route('/edit_utensills/<int:id>', methods= ['GET', 'POST'])
def edit_utensills(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name_of_item']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor.execute(""" UPDATE utensills_inventory
                       SET name_of_item = %s, price = %s, quantity =%s, expiry_date = %s, batch_number = %s, subtype = %s
                        WHERE ID = %s
                    """, (name, price, quantity, expiry_date, batch_number, subtype, id))
        mysql.connection.commit()
        cursor.close()
        flash(f"{name} updated successfully!", "success")
        return redirect(url_for('index'))
     
    cursor.execute("SELECT * FROM utensills_inventory WHERE ID = %s", (id,))
    item = cursor.fetchone()
    cursor.close()
    return render_template("update_utensills.html", utensill=item)

#mary let's push
@app.route("/delete_utensills/<int:id>", methods=["GET"])
def delete_utensills(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM utensills_inventory WHERE ID = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Drink deleted successfully!", "success")
        return redirect(url_for('index'))

if __name__ == '__main__': 
    app.run(debug=True) 