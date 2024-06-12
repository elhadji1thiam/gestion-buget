# app.py
from werkzeug.exceptions import abort
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('budget.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
@app.route('/index')
def index():
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entries').fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        type_ = request.form['type']

        conn = get_db_connection()
        conn.execute('INSERT INTO entries (date, category, amount, type) VALUES (?, ?, ?, ?)',
                     (date, category, amount, type_))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_entry.html')

if __name__ == '__main__':
    app.run(debug=True)
