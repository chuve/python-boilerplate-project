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

### Separate Concerns:
- Use Tortoise models for database interactions. (models.py)
- Use Pydantic models for request/response validation and serialization. (views.py)

TODO:
- 👷‍♂️ Finilize crud for blog app
- 👷‍♂️ Figure out how to organize logs in FastAPI
- ✅ Enable debug, how to debug fastapi with VS Code?
- Check how to write unit tests for endpoints?