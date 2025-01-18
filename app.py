from flask import Flask, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "pokedex"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    # Simulated registration logic
    flash("Registration successful! You can now log in.", "success")
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    # Simulated login logic (replace this with actual logic)
    username = "testuser"  # Simulated username
    password = "testpass"  # Simulated password
    entered_username = "testuser"  # Simulated entered username for demonstration
    entered_password = "wrongpass"  # Simulated entered password for demonstration

    if entered_username != username or entered_password != password:
        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('home'))
    
    flash("Login successful!", "success")
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == '__main__':
    app.run(debug=True)