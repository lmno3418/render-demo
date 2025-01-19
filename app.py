from flask import Flask, request, render_template, redirect, url_for, flash, session
from database import register_user, login_user, get_user_details

app = Flask(__name__)
app.secret_key = "pokedex"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['userid']
        password = request.form['password']
        full_name = request.form['name']
        email = request.form['email']

        if register_user(user_id, password, full_name, email):
            flash("Registration successful! You can now log in.", "success")
        else:
            flash("Error during registration. Please try again.", "danger")
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']

        login_result = login_user(user_id, password)

        if login_result == "Login successful!":
            session['user_id'] = user_id  # Store user ID in session
            flash(login_result, "success")
            return redirect(url_for('dashboard'))
        else:
            flash(login_result, "danger")  # Pass the error message to the template
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        flash("Please log in to access the dashboard.", "danger")
        return redirect(url_for('home'))
    
    user_details = get_user_details(user_id)  # Fetch user details from the database
    if user_details:
        return render_template(
            'dashboard.html', 
            user_id=user_details['user_id'], 
            full_name=user_details['full_name'], 
            email=user_details['email']
        )
    else:
        flash("Error loading dashboard. Please try again.", "danger")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)