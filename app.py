from flask import Flask, render_template, request, redirect, session, flash, jsonify
import sqlite3
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Carregar configurações de porta
try:
    with open('webServerApiSettings.json') as f:
        config = json.load(f)
    WEB_SERVER_PORT = config.get('webServerPort', 8080)
except (FileNotFoundError, json.JSONDecodeError):
    WEB_SERVER_PORT = 8080  # Porta padrão se o arquivo não existir

# Configuração do banco de dados
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
        # Adicionar usuário de teste se não existir
        try:
            hashed_password = generate_password_hash('senha123')
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                        ('teste@exemplo.com', hashed_password))
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
            cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                return redirect('/')
            else:
                flash('Credenciais inválidas!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/api/config', methods=['GET'])
def get_config():
    try:
        with open('webServerApiSettings.json') as f:
            return jsonify(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({
            "webServerPort": 8080,
            "webSocketPort": 3000,
            "FilesDirectory": "DesignTool",
            "useTerminaloutputCapture": True,
            "useTerminaloutputansistrip": False,
            "useTerminaloutputToHtml": True
        }), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=WEB_SERVER_PORT, debug=True)