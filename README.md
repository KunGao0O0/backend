<!-- This ReadMe need to be updated in the future. Probably.  -->
# Quick steps to run the server locally
```
python --version
Python 3.10.10
```
You can choose to run this in a virtual environment or not. If you do, you can create a virtual environment with the following command:
```
python -m pip install virtualenv

verntualenv .venv
```

Then activate the virtual environment Microsoft:
```
.venv\Scripts\activate
```

macOS and Linux:
```
source .venv/bin/activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## database migration
```
python manage.py makemigrations
python manage.py migrate
```

If something doesn't work, you can try following commands:
```
python manage.py makemigrations <appname>
```
For example
```
python manage.py makemigrations base
```
Then
```
python manage.py migrate --run-syncdb
```

## Create superuser
You might want to create a superuser to access the admin page, and for testing, thus
```
python manage.py createsuperuser
```
The instruction should be clear enough to follow.

## Run the server
This is the Step where you actually run the server
```
python manage.py runserver
```

## Access the server
You are supposed to be able to access the server at http://localhost:8000/ now. If you want to access the admin page, go to http://localhost:8000/admin/ and login with the superuser you just created.

## APIs
You can access the list of APIs at http://localhost:8000/api/ now. 

# Errors?
I spent like 5 minutes writing this README, so it is very likely that I missed something. 

If you encounter any errors in this page or the project overall, or you are running into troubles initializing the project, please contact me at u7294212@anu.edu.au. 

For Penwell memebers, you can directly contact me in MS Teams. 

Thank you!

Team Penwell
