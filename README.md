# Projectfetch
## Overview
This is my assignment project. Overview of this project is to fetch price's of ETH in USD from [UniswapV3 Pool](https://www.geckoterminal.com/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640) & [Coingecko](https://www.coingecko.com/en/coins/weth), 1 price point each day. Then save it into database and return an array of the following data structure - with 30 entries one for each of the last 30 days. 
```
{
"priceUniswapV3" : "3333.121",
"priceCoingecko" : "3334.10",
"timestamp": "<Timestamp>,"
"blockNo" : "<BlockNumber>"
}
```
### Tech stack to use
- Django
- Postgres or Sqllite
- Host it on Render/Railway/Heroku

## Project Structure
```
.
└── projectfetch/
    ├── appfetch/
    │   ├── admin.py           => allows developers to customize the Django admin interface
    │   ├── apps.py            => app configuration file 
    │   ├── db_operations.py   => custom module, handles database-related operations
    │   ├── models.py          => to define the database of our app
    │   ├── serializers.py     => has serializers for models created
    │   ├── tests.py           => unit tests file
    │   ├── urls.py            => for routing, specific for application
    │   ├── utils.py           => custom utility/helper module
    │   └── views.py           => where handles http requests are handled
    ├── projectfetch/
    │   ├── settings.py        => contains all the configuration settings for a project
    │   └── urls.py            => for project level routing
    ├── .env                   => for storing secret data like api keys
    ├── db.sqlite3             => database
    ├── manage.py              => command-line utility that help to interact with the project
    ├── Procfile               => has commands that Heroku app executes on startup 
    ├── requirements.txt       => contains a list of packages for a project to work
    └── runtime.txt            => contains python version 
```
## How to run this project locally?
1) Create env `python3 venv [env_name]`
2) Activate env `source [env_name]/bin/activate`
3) Clone project `git clone https://github.com/preethampy/projectfetch.git`
4) Install packages from `requirements.txt` using `pip install -r requirements.txt`
5) Run migrations `python3 manage.py makemigrations`
6) Do migrate `python3 manage.py migrate`
7) Create superuser `python3 manage.py createsuperuser` and provide the details asked
8) Create a .env file at root of project (where manage.py exists) and add `api_key = 'your api key'` & `coingecko_key = 'your api key'` to it
9) Run server `python3 manage.py runserver`

## How to deploy this project to heroku ?
I have already made necessary changes needed to deploy this project on heroku. I will mention them below:

1) In `settings.py`
```
import os
...
...

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', (Add under this)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]

...
...

# Static files

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
2) Add `Procfile` at root of the project and add this below.
```
web: gunicorn projectfetch.wsgi --log-file -
```
3) Create a `requirements.txt` file using `pip freeze requirements.txt` at root of the project.
4) Create `runtime.txt` file and add your python version in it. Ex. `python-3.10.12`
5) Push your project code to your github
6) Login to heroku and create a new app and connect your github to the app you created, choose the branch and click Deploy Branch button
7) Thats all. Now try to access `/fetch` endpoint from the deployed project link given to you and you should get the data like below
   
![https://ibb.co/b7qJrxq](https://ibb.co/b7qJrxq "My Screenshot")
