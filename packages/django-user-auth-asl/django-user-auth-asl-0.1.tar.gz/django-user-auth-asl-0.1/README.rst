==========
User Auth
==========

User Auth is a Django app to conduct web-based User Auth. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "User Auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'user',
    ]

2. Include the User Auth URLconf in your project urls.py like this::

    path('api/user/', include('user.urls')),

3. Run ``python manage.py migrate`` to create the User Auth models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a user (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/api/user/ to participate in the user auth.

6. all the url for particular action is given below,
    user registration, url: http://127.0.0.1:8000/api/user/users/ , method: post, body: 
    login, url: http://127.0.0.1:8000/api/user/auth/ , method: post, body: username,password
    update profile , http://127.0.0.1:8000/api/user/update_profile/ , method: post
    get user role, http://127.0.0.1:8000/api/user/user_role/ , method: get
    path('change_password/',change_password),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),