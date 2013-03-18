MovieMongo
==========

MovieMongo is a small web application to manage movies which are integrated from
different datasources (like DBPedia, freebase or IMDB). Users can register and
add movies to their personal movies list. The backend acts as a caching layer
for search requests and builds same-as links based on given information.

Movies are integrated refering to a canonical schema. Additional information is
also stored. User can add own information by using simple key-value data fields.

The project was developed during a practical course at the University of Leipzig
in 2012/13.

Config
------

Use `db_setup.py` and `movies/settings.py` for configuration.

Install
-------

Use `install.sh` to install all python dependencies.

Run
---

`python main.py`
