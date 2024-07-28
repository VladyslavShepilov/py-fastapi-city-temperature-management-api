## Async service to fetch data from weather API

### Instruction

    pip install -r requirements.txt
* get your API key from https://www.weatherapi.com/
* create .env file with settings or simply overwrite default settings values
* setup async database or use defined one from the settings


    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    uvicorn main:app --reload


##  Structure
Application in divided in two separate applications with validators&serializers in schemas.py
models in models.py and global database settings in database.py and settings.py .

Migrations are handled by Alembic:

    alembic revision --autogenerate -m ""
    alembic upgrade head

### City
Application to manage City records with models for city, with name and brief description.


### Temperature
Application responsible for fetching data from external API, main logic is implemented in cruds.py .
Data in processed and inserted into temperatures table and linked with City model by many to one relationship so you can filter and process data by city_id.


## Technical
 * Project is organized by FastAPI best practices
 * DB is passed to every endpoint function with a Dependency injection to simplify the process of managing connections.
 * All requests to database and to external API are async
 * Optimized queries using SQLAlchemy core
 * Optimized requests to API, used Dependency injection with data necessary for requests.
 * Additional validation in performed on cruds.py, which is also best practice.

