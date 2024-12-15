from flask import Flask, render_template, url_for, request, redirect, session
import datetime

app = Flask(__name__)
app.secret_key = '13493129d0e6e4eb1604d4ee7e4137e80f47504a96e05ecdbee0eca0f7e37b8b' # $AppDevVendigo2024

# General User
@app.route('/')
@app.route('/home')
def home():
    if 'has_access' in session:
        if session['has_access']:
            return render_template('index.html', has_access=True)
        else:
            return render_template('index.html', has_access=False)
    else:
        return render_template('index.html', has_access=False)
    
@app.route('/access_dashboard', methods=['POST'])
def access_dashboard():
    correct_combination = session.get('correct_combination')
    if request.form['key'] == correct_combination:
        session['has_access'] = True
        return redirect(url_for('dashboard'))
    else:
        return 'Incorrect combination'
    
@app.before_request
def generate_combination():
    if 'correct_combination' not in session:
        # Generate a new combination based on current date and time
        today = datetime.datetime.now()
        combination = f"{today.day}{today.hour}10"
        session['correct_combination'] = combination

@app.route('/order')
def order():
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
    if 'has_access' in session and session['has_access']:
        return render_template('admin-dashboard.html')
    else:
        return redirect(url_for('home'))