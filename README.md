# PDF rendering service

### Build it

Run `docker-compose build` to build an image for api and workers containers.


### Run it

Run `docker-compose up` to run all containers.


### Migrate it

Run `docker-compose exec api python migrate.py`


## Upload file

Run `curl -F file=@filename.pdf -X POST http://127.0.0.1:8000/documents/`
