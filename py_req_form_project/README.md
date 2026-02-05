# Python Requirements Intake → Spreadsheet (Student Starter)

This is a **ready-to-run** Flask project that:
- Collects requirement data via an HTML/CSS form
- POSTs data to Python
- Stores records in SQLite (persistent storage)
- Displays records in a spreadsheet-style table

## Fields Collected
- ID (auto-generated)
- Requirements ID
- Date
- Requirement Description
- Spearhead
- Stakeholder

## Quick Start
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
python app.py
```

Then open: http://127.0.0.1:5000/

Database file (`requirements.db`) will be created automatically.

Created: 2026-01-27



## Flask 3.x Note
Flask 3.x removed lifecycle hooks like `before_first_request` and `before_serving`.
This starter initializes the SQLite database **explicitly at startup** (see `if __name__ == "__main__":` in `app.py`).
