from fastapi import FastAPI

from . import models, schemas, database
from .routers import post, user, auth


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get('/', response_model=schemas.Post)
async def hello_app():
    return {'message': 'Hello, world'}







