# ledger_django_rest

REST API backend server for Ledger Application written in Python with Django framework.

# Endpoints

| EP                         | HTTP Method | Description                 |
| -------------------------- | ----------- | --------------------------- |
| /api/token                 | POST        | Get authentication token    |
| /api/token                 | DELETE      | Delete authentication token |
| /api/reasons               | GET         | Get a list of reasons       |
| /api/transactions          | GET         | Query transactions          |
| /api/transactions          | POST        | Create a transaction        |
| /api/transactions/<int:id> | GET         | Get a transaction by its id |
| /api/transactions/<int:id> | PUT         | Update a transaction        |
| /api/transactions/<int:id> | DELETE      | Delete a transaction        |

# DB Schema

- There are two main tables: Transaction and Reason

![Database schema](https://raw.githubusercontent.com/vespaiach/ledger_django/main/db.jpg)

# Developement

SQLite is using by default. To use other databases, set `DATABASE_URL` environment variable. This project is using `dj-database-url` library for reading database settings, please refer to [dj-database-url](https://github.com/jazzband/dj-database-url) for more database url settings.

- Create a virtual env and activate it

```
python -m venv ./ledger
source ./ledger/bin/activate
```

- Install packages

```
pip install -r requirement.txt
```

- Migrate and generate dummy data (optional)

```
python manage.py migrate
python manage.py gen_dummy_data
```

It will create a user with `username=tester/ password=123` and add 100 dummy transactions for that user. This command can be executed multiple times to generate more data.

- Run server

```
python manage.py runserver
```

# Testing

This project is using django Client tool to test APIs

```
python manage.py test
```

# Deployment

Before deploying, update settings in `ledger_django.settings`

| Key           | Description                                                             |
| ------------- | ----------------------------------------------------------------------- |
| DEBUG         | Set to False when deploying to production                               |
| SECRET_KEY    | Application secret key                                                  |
| DATABASE_URL  | Refer to [dj-database-url](https://github.com/jazzband/dj-database-url) |
| JWT_ALGORITHM | JWT algorithm                                                           |
| JWT_ISSUER    | JWT issuer                                                              |
| JWT_DURATION  | JWT lifetime in minutes                                                 |

# Swagger UI

After running server, interactive API documentation and exploration web user interfaces can be accessed at: http://localhost:8000/

# Frameworks/ libraries

- Django (4.x)
- PyJWT
- PyYAML
- PyTZ
- Faker
- Django-cors-headers
