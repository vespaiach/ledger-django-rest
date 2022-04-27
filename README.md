# ledger_django

REST API backend server for Ledger App, it's written in Python with only Django framework.

# Endpoints

| EP                         | HTTP Method | Description                 |
| -------------------------- | ----------- | --------------------------- |
| /api/token                 | POST        | Get authentication token    |
| /api/token                 | DELETE      | Delete authentication token |
| /api/reasons               | GET         | Get a list of reasons       |
| /api/transactions          | GET         | Query transactions          |
| /api/transactions/<int:id> | GET         | Get a transaction by its id |
| /api/transactions          | POST        | Create a transaction        |
| /api/transactions          | PUT         | Update a transaction        |
| /api/transactions          | DELETE      | Delete a transaction        |

# DB Schema

-   There are two main tables: Transaction and Reason

![Database schema](https://raw.githubusercontent.com/vespaiach/ledger_django/main/db.jpg)

# Developement

-   Load dummy data

```
python manage.py migrate
python manage.py gen_dummy_data
```

-   Update settings in `ledger_django.settings`
    | Key | Description |
    | -------------------------- | --------------------------- |
    | SECRET_KEY | Application secret key |
    | JWT_ALGORITHM | JWT algorithm |
    | JWT_ISSUER | JWT issuer |
    | JWT_DURATION | JWT lifetime in minutes |

-   Run server

```
python manage.py runserver
```

# Testing

This project is using django Client tool to test APIs

```
python manage.py test
```
