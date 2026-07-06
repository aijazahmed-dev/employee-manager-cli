# 👨‍💼 Employee Management CLI (Python + SQLite)

A simple but powerful command-line Employee Management System built using Python and SQLite.

## Project Overview
A simple but powerful **command-line Employee Management System** built using Python and SQLite.  
This project demonstrates core Python concepts including OOP, database handling, CLI development using argparse, and clean code architecture.

### ✨ Features
- Add new employees
- View all employees in a formatted table
- Search employees by name or email
- Update employee details
- Delete employees with confirmation
- Export employee data to CSV
- SQLite database integration (auto-created)
- Clean OOP-based architecture

## ⚙️ Technologies Used

- Python 3.10+
- SQLite3
- argparse (CLI handling)
- tabulate (table formatting)
- CSV module
- Logging module

## Installation

```bash
git clone https://github.com/your-username/employee-manager-cli.git
cd employee-manager-cli
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run

```bash
python app.py
```

## Example Commands

### Add Employee
```bash
python app.py add --name "John Marker" --email "john@test.com" --department "IT" --position "Dev" --salary 50000 --joining-date 2026-01-01
```

### List Employees
```bash
python app.py list
```

### Search Employee
```bash
python app.py search --keyword "John"
```

### Update Employee
```bash
python app.py update --id 1 --name "Updated Name" --email "new@test.com" --department "IT" --position "Senior" --salary 70000 --joining-date 2026-01-01
```

### Delete Employee
```bash
python app.py delete --id 1
```

### Export CSV
```bash
python app.py export --file employees.csv
```

## Python Version
Python 3.10+

## 📁 Project Structure
employee_manager/
│
├── app.py
├── employee.py
├── employee_service.py
├── database.py
├── employees.db
├── requirements.txt
└── README.md

## Notes
- Database is auto-created (employees.db)
- Logs stored in employee_manager.log
- CSV exported in project folder
