# setup project
* python3 -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py runserver

# endpoints
data_upload/ - GET - upload data
statistics/ - GET - get statistics
weather/ - GET - get weather data
stats/ - GET - get statistics parameters (station, year)    example: stats/?station=1&year=2019
```
