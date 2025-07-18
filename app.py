from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

from blockchain import Blockchain
from encryption import encrypt_message, decrypt_message

app = Flask(__name__)
app.secret_key = 'supersecretkey'

blockchain = Blockchain()
USERS_FILE = 'users.json'

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)


def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        users = load_users()
        if user_id in users:
            return "User ID already exists!"
        users[user_id] = password
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        users = load_users()
        if users.get(user_id) == password:
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        return "Invalid credentials!"
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user_id=session['user_id'])


@app.route('/chat/<receiver>', methods=['GET', 'POST'])
def chat(receiver):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    sender = session['user_id']
    if request.method == 'POST':
        msg = request.form['message']
        encrypted = encrypt_message(msg)
        blockchain.add_block(sender, receiver, encrypted)
        return redirect(url_for('chat', receiver=receiver))

    messages = []
    for block in blockchain.chain:
        if (block['sender'] == sender and block['receiver'] == receiver) or \
                (block['sender'] == receiver and block['receiver'] == sender):
            try:
                text = decrypt_message(block['message'])
            except:
                text = "[Error decrypting]"
            messages.append({'sender': block['sender'], 'text': text})

    return render_template('chat.html', receiver_id=receiver, messages=messages)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
