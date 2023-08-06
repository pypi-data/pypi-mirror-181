=====
Login
=====

Login is a Django app to create, authenticate and login users.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "login_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        "login_app.apps.LoginAppConfig",
    ]

2. Go to the bottom of your project setting.py and add::

    AUTH_USER_MODEL = "login_app.User"

3. Include the login_app URLconf in your project urls.py like this::

    path('auth/', include('login_app.urls')),

4. Run ``python manage.py migrate`` to create the User model.

5. Add your login/signup template to views.py login_view

6. Start the development server and visit http://127.0.0.1:8000/auth/login to see you login page

