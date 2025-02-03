# Boilerplate Python Project 

## Dependencies
- FastAPI
- TortoiseORM
- asyncpg
- Aerich

### Run dev server
In root project dir run - `fastapi dev app/main.py`

### Database migration
- Initialize aerich config and create migrations folder `aerich init -t app.db.TORTOISE_ORM`
- Generate schema and generate app migration folder - `aerich init-db`
- Extend models list if it's a new models module in the app - `app.db.TORTOISE_ORM`
- Create migration `aerich migrate --name {migration name}`
- Apply migration `aerich upgrade`

# How to debug Tortoise ORM and log the SQL queries it is executing?
Set the logging level for Tortoise ORM to DEBUG. 
```
"loggers": {
    "tortoise": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
        "propagate": False,
    },
}
```

### Separate Concerns:
- Use Tortoise models for database interactions. (models.py)
- Use Pydantic models for request/response validation and serialization. (views.py)

TODO:
- 👷‍♂️ Finilize crud for blog app
- 👷‍♂️ Figure out how to organize logs in FastAPI
- ✅ Enable debug, how to debug fastapi with VS Code?
- Check how to write unit tests for endpoints?
- ✅ Figure out how to work with env variables - https://docs.pydantic.dev/latest/concepts/pydantic_settings/#installation
- ✅ How to debug tortoise in terms of SQL queries which it does - https://tortoise.github.io/logging.html?h=logging