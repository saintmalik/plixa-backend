# Contributing to the Plixa Project.

The backend of this project has two different versions in development simultaneously.
on the `dev` branch, A backend that
uses [django](https://www.djangoproject.com/) + [postgres](https://www.postgresql.org/) + [GraphQL](https://graphql.org/)
and on
the `experimental`
branch a backend that uses [FastAPI](https://fastapi.tiangolo.com/) + [mongodb](https://www.mongodb.com/). The reason
for this segregation of technologies is due to the uncertainty of how well `django` works with `mongodb`. The version
in the `dev` branch is currently halted in search of a maintainer with an expertise in `django` + `graphql`

## Setting up the Django version

After cloning this repository, you want to check out to the `dev` branch

```bash
git checkout dev
```

Branch off to your local branch

```bash
git checkout -b my-branch
```

Install project dependencies. (You need to have `python=3.11` and `pipenv` installed globally)

```bash
pipenv install 
```

Switch to the project's virtual environment

```bash
pipenv shell
```

Run the development server

```bash
python manage.py runserver
```

## Setting up the FastAPI version

After cloning this repository, you want to check out to the `experimental` branch

```bash
git checkout experimental
```

Branch off to your local branch

```bash
git checkout -b my-branch
```

Install project dependencies. (You need to have `python=3.11` and `pipenv` installed globally)

```bash
pipenv install 
```

Switch to the project's virtual environment

```bash
pipenv shell
```

Run the development server

```bash
 uvicorn main:app --host 0.0.0.0 --port 8082 --reload
```