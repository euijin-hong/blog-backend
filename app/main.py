from fastapi import FastAPI
from app.router import auth, user, blog


app = FastAPI()

app.include_router(auth.router, tags=['Authentication'])
app.include_router(user.router, tags=['User'])
app.include_router(blog.router, tags=['Blog'])


@app.get("/")
async def root():
    return {"Hello": "World"}