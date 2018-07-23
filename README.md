# Coding challenge for Wanderjaunt
Made with Heroku Django Starter Template, see https://github.com/heroku/heroku-django-template/

Request: https://docs.google.com/document/d/1s2jJQ1HDV6p0IvDtxSm_UOHnI0Y5sH3DkEVU13FTRwU/edit?usp=sharing
Applicant: Maggie Moreno

## Goals

* Allow the user to add furniture to their cart (which is attached to a user and a property) and "check out", assigning that furniture to that property.

* Holding furniture in a cart reserves it so that other users can't try to reserve the same furniture.

* Furniture that is already assigned or reserved cannot be added to a cart.

* All history of furniture movement (i.e., all activities except when a user clears an active cart) is kept.


## Notes
I misread the Google Sheet that you guys gave and thought that you had specified the addresses of warehouses as well as properties, so I made a warehouse model as well. `¯\_(ツ)_/¯`

Also, I focused on the UI around adding furniture to properties instead of discovering the furniture that one might like to add. Which is to say, I didn't write a lot of helper methods for filtering on furniture attributes.


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
Furniture.available_pieces()
furniture_instance.add_to_cart(cart)
furniture.add_to_property()
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
