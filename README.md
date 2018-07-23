# Coding challenge for Wanderjaunt
Made with Heroku Django Starter Template, see https://github.com/heroku/heroku-django-template/

Request: https://docs.google.com/document/d/1s2jJQ1HDV6p0IvDtxSm_UOHnI0Y5sH3DkEVU13FTRwU/edit?usp=sharing
Applicant: Maggie Moreno

## Notes
I misread the Google Sheet that you guys gave and thought that you had specified the addresses of warehouses as well as properties, so I made a warehouse model as well. `¯\_(ツ)_/¯`

## How to use

```
$ pipenv install
$ pipenv shell
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
See Django admin UI at localhost:8000/admin for models.

For helper methods
```
$ pipenv shell
$ python manage.py shell
```

Helper methods:
```
furniture_instance.add_to_cart(cart)
furniture_instance.current_warehouse()
furniture_instance.current_property()
furniture_instance.current_cart()
furniture_instance.add_to_warehouse(warehouse)
furniture_instance.is_assigned()
furniture_instance.is_reserved()
furniture_instance.history()

cart_instance.furniture()
cart_instance.check_out()
cart_instance.clear()

property_instance.furniture()

warehouse_instance.furniture()
```
See inventory/models.py for more helper methods docs.
