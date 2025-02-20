# Dvm-Task1
## Installation

### Development
1. Start a virtual env and activate it:
```
python -m venv .venv
```
2. Install required modules:
```
pip install requirements.txt
```
3. Create .env file of the following format:
```
SECRET_KEY = 
GOOGLE_CLIENT_SECRET = 
GOOGLE_CLIENT_ID = 
DB_USERNAME = 
DB_PASSWORD = 
PORT_NUMBER = 
EMAIL_HOST_PASSWORD =
DEBUG = True
DJANGO_LOGLEVEL = "info"
DB_NAME = 
DB_HOST = 
DJANGO_ALLOWED_HOSTS =   
DB_ENGINE = "postgresql_psycopg2"
```
Get CLIEND_ID and CLIENT_SECRET from google oauth api
EMAIL_ID and APP_PWD from google security settings

4. Run the following in root directory:

```
docker-compose up -d --build
```

5. Test the app at http://localhost:8000

6. Create superadmin:
```
python manage.py createsuperuser
```

### Production(not completed yet)

1. First stop the development containers:
```
docker-compose down
```

2. Start the production containers:

```
docker-compose -f docker-compose.prod.yml up -d --build
```

3. Perform migrations (if any) by repeating the same process as in development.

4. Test the server at http://localhost

## Walkthrough
https://youtu.be/YzNGsqDOGKg
