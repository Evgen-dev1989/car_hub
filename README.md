# Car Hub — Django Car Dealership Platform

Car Hub is a Django-based web application for car sales. It features a car catalog, user registration, shopping cart, order placement, online payments (Stripe), reviews, and a powerful REST API. The project supports multilingual interfaces, full-text search with Solr and Haystack, and is ready for integration with mobile apps or external services.

---

## Features

- **Car Catalog**: Browse, search, and filter cars by category, brand, model, and more.
- **User Registration & Authentication**: Register, login, and manage user profiles.
- **Shopping Cart**: Add, remove, and update cars in the cart (session-based and persistent for authenticated users).
- **Order Placement**: Place orders for cars, with email notifications.
- **Online Payments**: Stripe integration for secure online payments.
- **Order History & Payments**: Track orders and payment status.
- **Reviews**: Leave and view reviews for cars.
- **Admin Panel**: Manage cars, categories, clients, payments, and reviews.
- **REST API**: Full CRUD API for cars, categories, reviews, payments, clients, and cart.
- **Internationalization**: Multilingual support (English, Russian, etc.) with language switcher.
- **Full-text Search**: Integrated with Haystack and Solr for fast and flexible search.
- **RSS Feed & Sitemap**: For SEO and content syndication.

---

## Technologies

- Python 3.x
- Django
- Django REST Framework
- Celery, Redis (for background tasks)
- Stripe (for payments)
- Bootstrap (UI)
- PostgreSQL or SQLite (default)
- **django-haystack** and **Solr** (for search)
- **django-modeltranslation** (for multilingual support)

---

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/car_hub.git
cd car_hub

2. Install dependencies
pip install -r [requirements.txt]

3. Configure environment
Copy .env.example to .env and set your environment variables (DB, Stripe keys, etc.)
Or set variables in car_hub/settings.py for quick start.

4. Apply migrations
python manage.py migrate

5. Create a superuser
python manage.py createsuperuser

6. Run Solr for Haystack search
Download and extract Apache Solr.
Start Solr:
bin/solr start --host 0.0.0.0 --port 8983 --user-managed
bin/solr stop -p 8983
bin/solr restart

Create a core for your project
bin/solr create -c carhub
Make sure your settings.py Haystack config points to the correct Solr URL and core.

To reset and rebuild indexes, use the commands
python manage.py clear_index --noinput
python manage.py rebuild_index

7. Run the development server
python manage.py runserver

8. Start Celery worker
celery -A car_hub worker -l info

Usage
Language Switcher:
The site supports multiple languages. Use the language switcher in the UI to change the interface language.
Search:
Use the search bar to find cars by keywords, powered by Haystack and Solr.
API:
Access the REST API at /api/ (see endpoints below).

to add new translations use the command
 django-admin makemessages -l ru
 django-admin compilemessages

API Endpoints
/api/cars/
/api/categories/
/api/reviews/
/api/payments/
/api/clients/
/api/carts/
API authentication: /api-auth/login/

Payments
Stripe integration is enabled. Set your STR<vscode_annotation details='%5B%7B%22title%22%3A%22hardcoded-credentials%22%2C%22description%22%3A%22Embedding%20credentials%20in%20source%20code%20risks%20unauthorized%20access%22%7D%5D'>IPE</vscode_annotation>_SECRET_KEY and STRIPE_PUBLISHABLE_KEY in settings.
Test payments using Stripe test keys.

Requirements
Main dependencies (see requirements.txt for full list):

Django
djangorestframework
django-haystack
pysolr
celery
stripe
django-modeltranslation
social-auth-app-django

Author
Evgen-dev1989

**This README includes:**  
- Requirements from requirements.txt
- Instructions for Solr/Haystack search
- Info about language switching (multilingual support)
- All main features and setup steps

You can further customize it for your project and deployment specifics!


