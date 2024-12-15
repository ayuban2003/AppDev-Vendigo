from flask import Flask, render_template, url_for, request

app = Flask(__name__)

# General User
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/order')
def home():
    return render_template('order.html')

@app.route('/payment')
def home():
    return render_template('payment.html')

@app.route('/purchase')
def home():
    return render_template('purchase.html')

@app.route('/receipt')
def home():
    return render_template('receipt.html')

# Administrator
@app.route('/dashboard')
def home():
    return render_template('admin-dashboard.html')