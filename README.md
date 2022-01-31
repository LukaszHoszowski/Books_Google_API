# Interface for Google Books API

> I've created simple app to import books from Google API ('https://www.googleapis.com/books/v1/volumes?q=') filtered by given keyword. Retrieved data is normalized. Book, Author, Language are stored in seperated tables in relational database (PostgreSQL).
> App also shows the data, you can control your records by editing and deleting them. You can also add your own books outside google API. Results are paginated to fit on the page.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

![](https://www.logistec.com/wp-content/uploads/2017/12/placeholder.png)

## Requirements  (Prerequisites)

* Docker [Install](https://docs.docker.com/get-docker/)

## Installation

`docker-compose up --build`

For Linux and OS X

`docker-compose up --build`

For Windows

`docker-compose up --build`

## Screenshots

![Screenshots of projects](https://dradisframework.com/images/pro/screenshots/screenshot-62_small.png)

![Screenshots of the project](http://securityroots.com/blog/wp-content/uploads/2013/12/snowcrash-01.png)

## Features

* Used Bootstrap to make it 100% responsive
* Simple, intuitive design
* Human friendly interface for Books Google API
* Modeled data for efficient filtering

## Usage example

```python
import foobar

foobar.pluralize('word')  # returns 'words'
foobar.pluralize('goose')  # returns 'geese'
foobar.singularize('phenomena')  # returns 'phenomenon'
``` 

Mention any other documentation or live example available for reverence.

## Running the tests

Describe and show how to run the tests with code examples.. Explain how to run the automated tests for this system. Also
explain how to test and why to test.

Give code examples as:

1. `test example 1`
2. `test example 2`
3. `npm test`
4. `test till you finish`

## Deployment Notes

You need to have only machine with Docker, batteries included.

```sh
docker-compose up --build
```

## Tech Stack / Built With

1. [Django](https://www.djangoproject.com/) - The most popular MVC framework
2. [Docker](https://www.docker.com/)  - Container manager
3. [Django Rest Framework](https://www.django-rest-framework.org/) - REST API
4. [Bootstrap5](https://getbootstrap.com/) - CSS/JS

## How to Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate. If you'd like to contribute, please fork the repository and make
changes as you'd like. Pull requests are warmly welcome.

Steps to contribute:

1. Fork this repository (link to your repository)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

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