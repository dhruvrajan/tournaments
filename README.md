tournaments
-----------

Framework for storing match data in a PostgreSQL Database for a swiss
style tournament.

To Run:
------

1. Clone this repository.
2. Download postgres (from http://www.postgresql.org/)
3. cd into tournament, and run:
```
$ psql
```
4. In the psql prompt, type:
```
psql > CREATE DATABASE tournament;
psql > \c tournament;
psql > \i tournament.sql
```
Now that you've configured your database, feel free to import tournament.py into
your own projects, or just run tournament_test.py .