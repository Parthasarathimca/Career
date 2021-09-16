<!-- Please read this file before setting up the project -->
## steps for building the app

- Install Python version = 3.8.10.
- Create virtual environment using "virtualenv env_cos" command.
- Install the dependencies "pip install -r requirements.txt" command.
- Setup the MySQL database 
- copy COS/sample-env to COS/.env
- provide the database credentials in COS/.env file.
- Run "python manage.py makemigrations"
- Run "python manage.py migrate"
- Run "python manage.py runserver" command to run the server.
