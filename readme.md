# Photo Gallery - Studio Essence

A full-stack photography studio platform connecting professional photographers with clients.

## Technology Stack

- **Backend**: Flask, Flask-MySQLdb
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.7
- **Database**: MySQL
- **Forms**: Flask-WTF, WTForms

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure MySQL Database

Create the database by importing the SQL file:

```bash
mysql -u root -p < gallery_database.sql
```

### 3. Configure Database Credentials

Edit `photogallery/__init__.py` and update the database configuration:

```python
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password_here'  # Change this!
app.config['MYSQL_DB'] = 'gallery_database'
app.config['MYSQL_HOST'] = 'localhost'
```

**Important**: Do not commit your actual password to Git!

### 4. Run the Application

```bash
python run.py
```

The app will be available at `http://localhost:9999`

## Default Login Credentials

After importing the database, you can log in with these test accounts:

- **Admin**: Check the SQL file for admin credentials
- **Client**: Register a new client account
- **Photographer**: Register a new photographer account

## Project Structure

```
PhotoGallery/
├── photogallery/
│   ├── __init__.py          # App factory & MySQL config
│   ├── views.py             # Route handlers
│   ├── db.py                # Database query functions
│   ├── forms.py             # WTForms definitions
│   ├── models.py            # Data classes
│   ├── wrappers.py          # Decorators
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, images
├── gallery_database.sql     # Database schema
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

## Features

- **Client Portal**: Browse photographers, book sessions, make payments
- **Photographer Dashboard**: Manage portfolio, upload images, view bookings
- **Admin Panel**: Manage photographers and orders
- **Booking System**: Availability checking to prevent double-booking
- **Image Management**: Upload and control image visibility

## Database Schema

7 tables: Admins, Clients, Photographers, Categories, Images, Bookings, Payments

See `gallery_database.sql` for full schema details.

## License

Educational project - IFN582 Assessment
