# Interface for Google Books API

> Simple app as an interface for Google Books API ('https://www.googleapis.com/books/v1/volumes?q='). App create API request based on filtered by given criteria, let you choose which books needs to be added to DB. Retrieved data is normalized. Book, Author, Language are stored in seperated tables in relational database (PostgreSQL).
> App also shows the data, you can control your records by editing and deleting them. You can also add your own books outside google API. Results are paginated to fit on the page.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

## Requirements  (Prerequisites)

* Docker [Install](https://docs.docker.com/get-docker/)

## Installation

`docker-compose up`

alternatively: `docker-compose up -d` in detached mode

## Features

* Used Bootstrap to make it 100% responsive
* Simple, intuitive design
* Human friendly interface for Google Books API
* Modeled data for efficient filtering

## Running the tests

`pytest`

## Deployment Notes

You need to have only machine with Docker, batteries included.

```sh
docker-compose up
```

## Tech Stack / Built With

1. [Django](https://www.djangoproject.com/) - The most popular MVC framework
2. [Docker](https://www.docker.com/)  - Container manager
3. [Django Rest Framework](https://www.django-rest-framework.org/) - REST API
4. [Bootstrap5](https://getbootstrap.com/) - CSS/JS

## Authors

Lukasz Hoszowski – lukaszhoszowski@gmail.com

You can find me here at:
[Github](https://github.com/LukaszHoszowski)

## Credits

* [@pszat](https://github.com/pszat)
* [@patpio](https://github.com/patpio)
* [@katrze89](https://github.com/katrze89)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

MIT © Lukasz Hoszowski
