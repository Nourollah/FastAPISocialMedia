from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas, database
from .routers import post, user, auth, vote


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   expose_headers=["Content-Disposition"])

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
async def hello_app():
    return {'message': 'Hello to FastAPI Social Media App'}







