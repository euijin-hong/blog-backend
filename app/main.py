from fastapi import FastAPI
from app.router import auth, user, blog
from app.db.migrate_db import reset_database
from app.core.redis_config import init_redis

app = FastAPI(
    title="FastAPI NCP for blog web app",
    description="Blog posting and NCM mail function service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(user.router, tags=['User'])
app.include_router(blog.router, tags=['Blog'])


@app.get("/")
async def root():
    return {"Please go to /blog to see the blog project."}

# Initialize the database when the server starts
@app.on_event("startup")
def init_db():
    reset_database()

#Initialize Redis
init_redis(app)