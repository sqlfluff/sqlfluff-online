# SQLFluff Online

![Lint and Test](https://github.com/nolanbconaway/sqlfluff-online/workflows/Lint%20and%20Test/badge.svg)

[Fluff](https://github.com/alanmcruickshank/sqlfluff) is a SQL formatter that I like a lot. 
I built this app because I often want to format one-off, adhoc sql that isn't even worth saving to a file.

You can use the application on [Heroku](https://sqlfluff-online.herokuapp.com/).

## Development

Set up a python (3.8) environment:

```sh
$ pip install -r requirements-dev.txt
```

Run the app locally:

```sh
$ flask run
```

Lint and run unit tests:

```sh
$ tox
```

Run the production application:

```sh
$ python -m app.wsgi
```
