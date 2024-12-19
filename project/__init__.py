from flask import Flask, render_template, url_for, request, redirect
import mysql.connector

app = Flask(__name__)
app.secret_key = '13493129d0e6e4eb1604d4ee7e4137e80f47504a96e05ecdbee0eca0f7e37b8b' # $AppDevVendigo2024

def connectDB():
    DB = mysql.connector.connect(
        host="localhost",
        user="root",
        database="vendigodb"
    )

    return DB

# General User
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/submit_order')
def submit_order():
    return render_template('order.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/purchase')
def purchase():
    return render_template('purchase.html')

@app.route('/receipt')
def receipt():
    return render_template('receipt.html')

# Administrator
@app.route('/dashboard')
def dashboard():
    return render_template('admin-dashboard.html')

@app.route('/fetch_table_data')
def fetch_table_data():
    table_name = request.args.get('table_name')
    columns = []
    rows = []
    if table_name:
        connect = connectDB()
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM "+table_name)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        for row in result:
            rows.append(list(row))
        connect.close()

    return {'columns': columns, 'rows': rows}

@app.route('/submit_data', methods=['POST'])
def submit_data():
    table_name = request.form.get('table_name')
    data = {key: value for key, value in request.form.items() if key != 'table_name'}
    if table_name and data:
        connect = connectDB()
        cursor = connect.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
        connect.commit()
        connect.close()
    return redirect(url_for('dashboard'))

@app.route('/modify_data', methods=['POST'])
def modify_data():
    table_name = request.form.get('table_name')
    data = {key: value for key, value in request.form.items() if key not in ['table_name', 'id']}
    record_id = request.form.get('id')
    if table_name and data and record_id:
        connect = connectDB()
        cursor = connect.cursor()
        set_clause = ', '.join([f"{key}=%s" for key in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE id=%s"
        cursor.execute(sql, list(data.values()) + [record_id])
        connect.commit()
        connect.close()
    return redirect(url_for('dashboard'))

@app.route('/remove_data', methods=['POST'])
def remove_data():
    table_name = request.form.get('table_name')
    record_id = request.form.get('id')
    if table_name and record_id:
        connect = connectDB()
        cursor = connect.cursor()
        sql = f"DELETE FROM {table_name} WHERE id=%s"
        cursor.execute(sql, (record_id,))
        connect.commit()
        connect.close()
    return redirect(url_for('dashboard'))
