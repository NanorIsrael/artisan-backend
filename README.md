

* SETUP
- All dependancies can be found in the requirement file, 
	pip install -r requirements.txt

- Create a postgres database with name artisanbay
- Run server with the following envs
```
	-- HOST
	-- USER
	-- PASSWORD
```
- Run makemigrations
- Run migrations

HOST=localhost USER=airflow PASSWORD=airflow python3 manage.py runserver