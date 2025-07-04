# app.py
from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATABASE = 'users.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        # Usuário de teste
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                        ('teste@exemplo.com', 'senha123'))
        except sqlite3.IntegrityError:
            pass

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=? AND password=?", 
                          (username, password))
            user = cursor.fetchone()
            
            if user:
                session['user_id'] = user[0]
                return redirect('/')
            else:
                flash('Credenciais inválidas!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)