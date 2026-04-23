# 🔗 URL Shortener

A Django-based URL shortener with click tracking, QR codes, user authentication, and analytics.

## Features

- ✅ Shorten long URLs to 6-character codes
- ✅ QR code generation for every short link
- ✅ Click tracking with IP, referrer, and device info
- ✅ User registration and login
- ✅ Personal dashboard to manage links
- ✅ Link expiration dates
- ✅ Admin panel for moderation

## Tech Stack

- Django 5.x
- MySQL
- HTML/CSS (no framework)
- QR Code (qrcode library)

## Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install django mysqlclient qrcode pillow`
5. Copy `core/settings_example.py` to `core/settings.py`
6. Update database credentials in `settings.py`
7. Run migrations: `python manage.py migrate`
8. Create superuser: `python manage.py createsuperuser`
9. Run server: `python manage.py runserver`

## Screenshots

*(Add )*

## What I Learned

- Django model relationships (ForeignKey, One-to-Many)
- URL routing patterns and why order matters
- MySQL integration with Django
- Generating unique random strings
- Tracking user data with request.META
- Template inheritance and context passing

## Live Demo

*(Link coming after deployment)*

## Author

Your Name - [https://www.linkedin.com/in/vinay-kumar-gorli-263634266/]

## License

MIT
