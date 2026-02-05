from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timezone 
import os

app = Flask(__name__)
DB_PATH = 'requirements.db' 

# INITIALIZE DATABASE
def init_db():
    # Create the SQLite table if it does not already exist.
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requirements_id TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                spearhead TEXT NOT NULL,
                stakeholder TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        ''')

@app.route('/')
def form():
    return render_template('form.html')

# ADD INFORMATION TO DATABASE
@app.route('/submit', methods=['POST'])
def submit():
    data = {k: (request.form.get(k) or '').strip() for k in ['requirements_id', 'date', 'description', 'spearhead', 'stakeholder']}
    if not all(data.values()):
        return 'All fields are required.', 400

    created_at = datetime.now(timezone.utc).isoformat()
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO requirements (requirements_id, date, description, spearhead, stakeholder, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (*data.values(), created_at))
    return redirect(url_for('sheet'))

# VIEW SHEET
@app.route('/sheet')
def sheet():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute('''
            SELECT id, requirements_id, date, description, spearhead, stakeholder 
                FROM requirements 
                ORDER BY id DESC
        ''').fetchall()
    return render_template('sheet.html', rows=rows)

# SORT BY DATE ADDED
@app.route('/sort_by_date', methods=['POST'])
def sort_by_date():
    order = request.form.get('order', 'DESC').upper()

    # safety check
    if order not in ('ASC', 'DESC'):
        order = 'DESC'

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(f'''
            SELECT id, requirements_id, date, description, spearhead, stakeholder
            FROM requirements
            ORDER BY datetime(date) {order}
        ''').fetchall()

    return render_template('sheet.html', rows=rows, order=order)

# SORT BY REQ NUMBER 
@app.route('/sort_by_req', methods=['POST'])
def sort_by_req():
    order = request.form.get('order', 'DESC').upper()

    # safety check
    if order not in ('ASC', 'DESC'):
        order = 'DESC'

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(f'''
            SELECT id, requirements_id, date, description, spearhead, stakeholder
            FROM requirements
            ORDER BY CAST(REPLACE(requirements_id, 'REQ-', '') AS INTEGER
    ) {order}

        ''').fetchall()

    return render_template('sheet.html', rows=rows, order=order)



# RUNNING PROGRAM
if __name__ == '__main__':
    # Flask 3.x compatibility: initialize explicitly (no lifecycle decorators)
    init_db()
    app.run(debug=True)
