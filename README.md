# LibraVault — Library Management System

A full-featured **Library Management System** built with Python, Flask, and MySQL.

## Features

### 👤 Normal User
- **Browse Books** — Search by title, author, ISBN; filter by genre and availability
- **Rent Books** — Choose rental period (1–6 days or 1–6 months)
- **Return Books** — Auto-calculated late fees for overdue returns
- **My Rentals** — Track active and past rentals
- **Profile** — View and edit personal details

### 🔑 Admin
- **Dashboard** — Stats overview (books, rentals, revenue, overdue)
- **Manage Books** — Add, edit, delete books (title, author, genre, price, rent/day, copies)
- **Manage Authors** — CRUD for authors
- **Manage Genres** — CRUD for genres/categories
- **Manage Users** — Approve new users, block/unblock accounts
- **View Rentals** — Filter by active, overdue, returned
- **Settings** — Configure late fee rate & max books per user

### 📧 Email Notifications
- Rental confirmation
- Due date reminders
- Overdue notices
- Account approval notification

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | MySQL + SQLAlchemy ORM |
| Auth | Flask-Login |
| Forms | Flask-WTF |
| Email | Flask-Mail |
| Frontend | Jinja2, Bootstrap 5, Custom CSS |

## Setup

### 1. Prerequisites
- Python 3.8+
- MySQL Server running

### 2. Create MySQL Database
```sql
CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Install Dependencies
```bash
cd "Library Management system"
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Environment
Edit the `.env` file with your MySQL credentials and mail settings:
```
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=library_db
```

### 5. Run the Application
```bash
python run.py
```

The app will be available at **http://localhost:5000**

### 6. Default Admin Login
- **Username:** `admin`
- **Password:** `admin123`

## Rental Pricing

```
Rental Amount = Rent per Day × Number of Days

If returned after due date:
  Late Fee = Overdue Days × Late Fee per Day (default ₹5/day)

Total Charge = Rental Amount + Late Fee
```

## Project Structure

```
Library Management system/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms
│   ├── email_utils.py       # Email functions
│   ├── routes/
│   │   ├── auth.py          # Auth routes
│   │   ├── user.py          # User routes
│   │   └── admin.py         # Admin routes
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, images
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
├── run.py                   # Entry point
└── README.md
```

## License

This project is for educational purposes.
