# switch_to_sustainable
Django, SQLite3

API information and endpoints

http://127.0.0.1:8000/products/
returns the Json list of items in the database for use in the select bar

http://127.0.0.1:8000/products/search?item_id=2
returns the Json list of products that match the specified integer item_id (2 in the example above) 

To run:
py manage.py runserver
