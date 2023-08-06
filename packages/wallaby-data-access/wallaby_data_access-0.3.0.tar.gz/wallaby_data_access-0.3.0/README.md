# WALLABY data access

Python module with tools for accessing internal release data from the WALLABY database

## Configuration

Users will need to define a `.env` file to configure this module. The variables you will need to set (and default where possible) in this configuration are

```
DJANGO_SECRET_KEY
DJANGO_SETTINGS_MODULE
DJANGO_ALLOW_ASYNC_UNSAFE = "True"
DATABASE_HOST
DATABASE_NAME
DATABASE_USER
DATABASE_PASS
```