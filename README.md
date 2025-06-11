# My Investment Portfolio API

This APIs is created to manage user investments and view portfolio performance.

## Setup

1. Clone the Repository
    ```bash
    git clone https://github.com/glorypuncuna/investment_tracker.git
    cd myproject
    ```
2.  Create Virtual Env
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Install Django and its simple JWT:
    ```bash
    pip install Django djangorestframework djangorestframework-simplejwt django-filter
    ```
4.  Apply Migration
    ```bash
    python manage.py makemigrations investments
    python manage.py migrate
    ```
6.  Run
    ```bash
    python manage.py runserver
    ```
    The API will be accessible at `http://127.0.0.1:8000/`.
