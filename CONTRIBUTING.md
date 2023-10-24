# Contributing

:wave: Hiya! We're glad you clicked your way over.

The best way to surface an bug or feature is via GitHub issues. You can even just complain, we'd love to hear it.

You can also submit a PR if you'd like! If viable, your submission should include unit tests (and, um, pass them). All python code should be [black (19.10b0)](https://github.com/psf/black) formatted.

## Developer Setup

Set up a python (3.10) environment however you'd like. Install the developer requires to your python environment:

```sh
$ pip install -r requirements-dev.txt
```

Run the app locally and start breaking things:

```sh
$ flask run
```

Then hit up [localhost:5000](http://127.0.0.1:5000/) to check out what you've ruined. You can run the full lint and test suite locally via `tox`

```sh
$ pip install tox
```

And finally:

```sh
$ tox
```



